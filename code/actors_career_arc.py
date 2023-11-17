import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def release_by_genre(data, genre='Silent film'):


    genre_films = data[data['genres'].apply(lambda x: np.isin(genre, x))]

    films_by_year = data[data['movie_release_date'].isin(genre_films['movie_release_date'])].groupby(by = 'movie_release_date').apply(lambda x: pd.Series({'total_nb_films': x['movie_wikipedia_id'].count()}))

    genre_films_by_year = genre_films.groupby(by = 'movie_release_date').apply(lambda x: pd.Series({'frequency': x['movie_wikipedia_id'].count()}))

    genre_films_by_year = pd.concat((genre_films_by_year, films_by_year), axis = 1)

    return genre_films, genre_films_by_year


def plot_release_by_genre(genre_films_by_year, genre = 'Silent'):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.plot(genre_films_by_year.index, genre_films_by_year.frequency, color = color)
    ax1.set_xlabel('Release year')
    ax1.set_ylabel('number of movies released', color = color)
    ax1.tick_params(axis='y', labelcolor=color)
    if genre == None:
        ax1.set_title('Genre films released over the years')
    else:
        ax1.set_title('{} films released over the years'.format(genre))

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.plot(genre_films_by_year.index, genre_films_by_year.frequency/genre_films_by_year.total_nb_films, ls = '-.', color = color)
    ax2.set_ylabel('proportion of {} movies released'.format(genre), color = color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yticks(ticks = np.arange(0, 1.2, 0.2), labels = [str(int(p*100))+'%' for p in np.arange(0, 1.2, 0.2)])

    plt.show()


def select_non_genre(genre, total):
    res = []
    for y in total:
        if ~np.isin(y, genre):
             res.append(y)
    return np.asarray(res)



def actors_by_genre(data_character, genre_films, genre = 'Silent'):

    if genre == 'Silent':
        date = 1940
    elif genre == 'Black-and-white':
        date = 10**(12)

    #characters metadata : only movies that are silent and released before 1940
    data_character_filt = data_character[data_character['movie_wikipedia_id'].isin(genre_films['movie_wikipedia_id'])]
    data_character_filt = data_character_filt[data_character_filt['movie_release_date'] < date]

    #only actors that appear in silent movies and before 1940, but appearances are limited to silent movies
    characters_by_actor = data_character_filt.groupby(by = 'actor_name').apply(lambda x: pd.Series({'{}_appearances'.format(genre) : x['movie_release_date'].values,
                                                                                                        #add age info 
                                                                                                        'birth_date' : x['actor_birth_date'].values[0],
                                                                                                        'age_last_genre': x['movie_release_date'].values.max() - x['actor_birth_date'].values[0]}))

    #only movies that feature an actor that has played at least once in a silent movie
    movies_genre_actors = data_character[data_character['actor_name'].isin(characters_by_actor.index)]
    #only actors that appear in silent movies, but appearances are not limited to silent movies
    characters_by_actor_all = movies_genre_actors.groupby(by = 'actor_name').apply(lambda x: pd.Series({'total_appearances' : x['movie_release_date'].values,}))

    characters_by_actor = pd.concat((characters_by_actor, characters_by_actor_all), axis = 1)

    characters_by_actor['non_{}_appearances'.format(genre)] = characters_by_actor.apply(lambda x: select_non_genre(x['{}_appearances'.format(genre)], x['total_appearances']), axis = 1)

    #Add columns indicating the number of appearances
    characters_by_actor['nb_{}_appearances'.format(genre)] = characters_by_actor['{}_appearances'.format(genre)].apply(lambda x: x.shape[0])
    characters_by_actor['nb_total_appearances'] = characters_by_actor['total_appearances'].apply(lambda x: x.shape[0])
    characters_by_actor['nb_non_{}_appearances'.format(genre)] = characters_by_actor['non_{}_appearances'.format(genre)].apply(lambda x: x.shape[0])

    characters_by_actor['ratio'] = characters_by_actor['nb_non_{}_appearances'.format(genre)].values / characters_by_actor['nb_{}_appearances'.format(genre)].values

    cols = ['birth_date', 'age_last_genre', '{}_appearances'.format(genre), 'non_{}_appearances'.format(genre), 'total_appearances', 
            'nb_{}_appearances'.format(genre), 'nb_non_{}_appearances'.format(genre), 'nb_total_appearances', 'ratio']

    characters_by_actor = characters_by_actor[cols]
    
    return characters_by_actor

    
def plot_distrib_actors_by_genre(characters_by_actor, genre = 'Silent'):

    plt.figure()

    plt.hist(characters_by_actor.nb_total_appearances, label = 'All films', bins = 100, range = (0, 100), histtype= 'step')
    plt.hist(characters_by_actor['nb_{}_appearances'.format(genre)], label = '{} films'.format(genre), bins = 100, range = (0, 100), histtype= 'step')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Number of movies released per actor')
    plt.ylabel('Number of actors')
    plt.title('Distribution of number of movies released by an actor that has appeared in at least one {} film'.format(genre))
    plt.legend()
    plt.show()
