import json
import pandas as pd
import numpy as np
import regex as re
import ast  # Evaluate the literal syntax tree of a string
import requests
import matplotlib.pyplot as plt
import nltk
from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from bs4 import BeautifulSoup
import re

def print_versions(modules):
    """
        Prints the names and versions of Python modules. This is useful for 
        understanding which version of a module was used to run a program.
        
        Parameters:
            (Array-like) modules: python modules to print 
    """
    
    for module in modules:
        print(module.__name__ + "==" + module.__version__)
    return

def expand_list_data(df, column, names):
    """
        Takes a pandas DataFrame with list data in a column and expands it 
        into multiple columns with the required names.

        Parameters:
            (DataFrame) df: a frame with a list-valued column
            (string) column: the name of the list-valued column
            (string) names: the new column names
    """
    
    df[names]=pd.DataFrame(df[column].to_list(), index=df.index)
    
    return df.drop(columns=column)

def load_data_with_columns(folder, filename):
    """
        Loads file as pandas DataFrame with relevant column names.
        Does not transform the data other than unpacking array-like data
        into multiple columns.

        Parameters:
            (string) folder: file location ending in / (forward-slash) 
            (string) filename: one of  
                ['character.metadata.tsv', 
                'movie.metadata.tsv',
                'name.clusters.txt',
                'tvtropes.clusters.txt',
                'plot_summaries.txt',
                all_lost_films.csv] 
    """

    # Load table of column names 
    names = pd.read_table(folder + 'column_names.txt', sep=' ', 
                  converters={'columns': lambda x: str.split(x, sep=',')})

    # Converters for initial formatting
    converters = {'data': lambda x: list(json.loads(x).values())} if filename == 'tvtropes.clusters.txt' else None

    # Load data with column names
    if filename != 'all_lost_films.csv':
        data = pd.read_table(folder + filename, names = list(names[names['filename']==filename]['columns'])[0], converters=converters) 
    else:
        data = pd.read_csv(folder + filename)
        
    
    # Preprocess columns from json to list
    if filename == 'movie.metadata.tsv':
        data['genres'] = data['genres'].apply(ast.literal_eval)
        data['languages'] = data['languages'].apply(ast.literal_eval)
        data['countries'] = data['countries'].apply(ast.literal_eval)
        data['genres'] = data['genres'].apply(lambda x: list(x.values()))
        data['languages'] = data['languages'].apply(lambda x: list(x.values()))
        data['countries'] = data['countries'].apply(lambda x: list(x.values()))
        # If freebase_id in json wanted, then expand the data with new colomns instead of replacing them
        #data['genres_list'] = data['genres'].apply(lambda x: list(x.values()))
        #data['languages_list'] = data['languages'].apply(lambda x: list(x.values()))
        #data['countries_list'] = data['countries'].apply(lambda x: list(x.values()))
    

    # Expand list data in tvtropes.clusters.txt into multiple columns
    if filename == 'tvtropes.clusters.txt':
        data = expand_list_data(data, 'data', ['character_name', 'movie_name', 'freebase_map_id', 'actor_name'])

    return data

def get_synonyms(word):
    """
        Returns a list of synonyms of a word.
    """
    return [lemma.name() for syn in wordnet.synsets(word) for lemma in syn.lemmas()]


def percentage_count_words_per_year(df, keyword):
    """
        Computes the percentage and number of movies per year that
        contain the given keyword or its synonmys.
        The dataframe must have columns 'plot', 'movie_release_date' and 'movie_wikipedia_id'
    """

    # Define a list of related keywords
    synonyms = [word.replace('_', ' ') for word in get_synonyms(keyword)]

    # Select movies with at least one of the previous keywords
    has_keyword = df['plot'].apply(lambda x : False if pd.isna(x) else any([word for word in synonyms if word in x]))

    # Count up the number of such movies per year
    movie_count_per_year = df[has_keyword].groupby('movie_release_date')['movie_wikipedia_id'].count()

    # Count up number of movies per year
    movies_per_year = df.groupby('movie_release_date')['movie_wikipedia_id'].count()

    # Compute percentage
    percentage_word_movies_per_year = movie_count_per_year / movies_per_year

    return percentage_word_movies_per_year, movie_count_per_year


def date_to_float(dataset, column_name):
    """
    Inplace. Takes a dataset and a date-valued column name as input, and converts its year to float.
    NaN values are conserved.
    Example : movie_metadata = date_to_float(movie_metadata, 'movie_release_date')
    """
    dataset[column_name] = dataset[column_name].str[0:4].astype(float)
    return dataset

def round_down(m, n):
    """
    Rounds down m to a multiple of n.
    """
    return m - (m % n)

def bin_into_decades(df, column):
    """
        Takes a DataFrame with a column representing years (float) and appends a 'decade' column.

        Parameters:
            (DataFrame) df: a frame with a date-valued column
            (string) column: the name of the date-valued column
    """
    # Copy the original dataframe
    df_copy = df.copy()

    # Append 'decade' column
    df_copy[column+'_decade'] = df_copy[column].apply(lambda x : round_down(x, 10))

    return df_copy

def percent_nans(arr):
    """
        Computes the percentage of NaNs in a pandas Series or array-like.

        Returns float in [0..1].
    """
    if type(arr)==pd.Series:
        return arr.isna().agg('mean')
    else:
        return len([x for x in arr if pd.isnull(x)]) / len(arr)
    
def duplicate_singleton(arr):
    """
        Duplicates a singleton list or pandas Series
    """
    if len(arr) == 1:
        if type(arr)==pd.Series:
            return pd.concat([arr, arr])
        else: 
            return 2*arr
    else:
        return arr
    
def plot_tech_evolution(df, tech_word):
    """
    Plots the evolution of a technology over the years. 
    PARAMETERS:
        - df: hccta dataframe
        - tech_word (str): Technology taht is contained in the hccta dataset
    """
    countries = df.columns[2:]
    data = df[df['Variable'] == tech_word]

    by_year = data[countries].apply(lambda x: x.mean(axis = 0), axis = 1)

    plt.plot(data['Year'].values, by_year)
    plt.title('Evolution of {} over the years'.format(tech_word))
    plt.xlabel('Year')
    plt.show()


def plot_with_confidence(data, column, label, axis):
    """
        Takes a pandas DataFrame and plots its column, as well as confidence
        intervals represented by columns 'high' and 'low' using fill_between,
        and plots on given axis.
    """
    axis.plot(data[column], label=label)
    axis.fill_between(x=data.index, y1=data['high'], y2=data['low'], alpha=0.5)

def get_movie_release_year(page_id):
    """ Retrieves the release year of a movie given its Wikipedia page ID. """
    try:
        # Construct the URL for the Wikipedia page
        url = f"https://en.wikipedia.org/wiki?curid={page_id}"

        # Fetch the HTML content of the page
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page for Wikipedia ID: {page_id}")
            return None

        # Parse the HTML content
        page_parser = BeautifulSoup(response.content, "html.parser")

        # Find the infobox table
        table_data = page_parser.find("table", class_="infobox")
        if not table_data:
            return None

        # Look for the release date entry in the infobox
        for row in table_data.find_all("tr"):
            header = row.find("th")
            if header and "Release date" in header.get_text():
                # Extract and clean the release date text
                release_date_cell = row.find("td")
                release_date = release_date_cell.get_text(separator=" ", strip=True)
                # Remove reference links and other non-text content
                release_date = re.sub(r'\[.*?\]', '', release_date)
                release_date = re.sub(r'\(.*?\)', '', release_date)

                # Extract the year
                year_match = re.search(r'\b\d{4}\b', release_date)
                if year_match:
                    return year_match.group()
                break

        return None

    except Exception as e:
        print(f"Error while fetching data for Wikipedia ID {page_id}: {e}")
        return None
    
def extract_worldwide_revenue(sections):
    """ Extracts the worldwide revenue from the correspondant container """
    worldwide_div = sections[0].find_all('div', class_='a-section a-spacing-none')[-1]
    money_span = worldwide_div.find('span', class_='money')
    
    if money_span:
        return money_span.get_text(strip=True)
    else:
        return None
    
def scrape_box_office(imdb_id):
    """ Retrieves the box office revenues of a movie given its IMDb ID. """
    page_url = f"https://www.boxofficemojo.com/title/{imdb_id}/"
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sections = soup.find_all('div', class_='a-section a-spacing-none mojo-performance-summary-table')
        return extract_worldwide_revenue(sections)
    else:
        return None
    
def word_count(text):
    return len(text.split())

def sentence_count(text):
    return len(nltk.sent_tokenize(text))

def preprocess(text):
    # Lowercasing
    text = text.lower()
    
    # Removing special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
   
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Joining back
    text = ' '.join(tokens)
    return text

def tokenize_sentences(text):
    # Tokenizing the text into sentences
    tokenized_sentences = sent_tokenize(text)
    return tokenized_sentences

def tokenize_words(text):
    # Tokenizing the text into words
    tokenized_words = word_tokenize(text)
    return tokenized_words

def is_wordnet_word(word):
    # Check if a word is in WordNet
    return len(wordnet.synsets(word)) > 0

def clean_sent_advanced(sent):
    # Tokenize and apply filters to remove words that do not make sense 
    words = nltk.wordpunct_tokenize(sent)
    filtered_words = [w for w in words if (is_wordnet_word(w.lower()) or not w.isalpha()) and len(w) < 15]
    return " ".join(filtered_words)

# Function to clean and lowercase movie titles
def clean_title(title):
    if isinstance(title, str):
        return re.sub(r'[^a-z0-9]', '', title.lower())
    else:
        # If the title is not a string, return an empty string or handle as needed
        return ''

# Function to create a combined key of cleaned title and release date
def create_combined_key(title, date):
    cleaned_title = clean_title(title)
    return f"{cleaned_title}_{date}"

def find_techniques(text, techniques):
    """
    Function to find listed techniques in a given review.

    Args:
    text (str): The text to search for techniques.
    techniques (list): A list of techniques to search for in the text.

    Returns:
    list: A list of techniques found in the text.
    """
    return [technique for technique in techniques if technique in text.lower()]

def count_matches(word_tokens, tech_nouns):
    # Count the matching words in two lists
    return sum(word in tech_nouns for word in word_tokens)

def get_matches(word_tokens, tech_nouns):
    # get the matching words in two lists
    matched = []
    for word in tech_nouns:
        if word in word_tokens:
            matched.append(word)
    return matched

def most_frequent_tech_noun(word_tokens, tech_nouns):
    # Filter the tokens to keep only tech nouns
    tech_tokens = [word for word in word_tokens if word in tech_nouns]
    
    # Count the frequency of each tech noun
    freq_count = Counter(tech_tokens)
    
    # Find the most common tech noun (returns a list of tuples, take the first one)
    most_common = freq_count.most_common(1)
    
    # Return the most common tech noun or None if there are none
    return most_common[0][0] if most_common else None

# Function to convert string representation of a list to an actual list of floats and then calculate the mean
def calculate_mean_from_string_list(string_list):
    try:
        # Convert string to list
        numeric_list = ast.literal_eval(string_list)
        # Calculate and return mean
        return np.mean(numeric_list)
    except:
        # Return None or some default value in case of error
        return None
    
# Function to clean and parse words and scores
def clean_and_parse(row):
    # Using regular expressions to clean the word strings
    words = re.findall(r"[\w']+", row['tech_nouns_used'])
    scores = [float(score) for score in row['tech_nouns_scores'].strip('[]').split(', ')]
    return list(zip(words, scores))