# Datasets

This README describes the primary data sources 📜, intermediary data 🧻, and data we did not end up using ❌ for the project, in alphabetical order.

+ 📜 *all_lost_films.csv* for lost film analysis, downloaded from [List of Lost Films, Wikipedia](https://en.wikipedia.org/wiki/List_of_lost_films)
+ 📜 *character_metadata.csv* for actor career analysis, from the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/)
+ 🧻 *column_names.txt* a list of pandas DataFrame columns names to associate with features the CMU Movie Summary Corpus
+ 📁/📜 *country_shape_data* used to generate country plots from [Natural Earth](https://www.naturalearthdata.com/)
+ 📜 *hccta.txt* for historical correlation analysis, from the [Historical Cross Country Technology Adoption Dataset](https://www.nber.org/research/data/historical-cross-country-technology-adoption-hccta-dataset)
+ 📜 *missing_box_office.csv* extra box office data, scraped from [Box Office Mojo](https://www.boxofficemojo.com/)
+ 📜 *missing_release_date.csv* extra release date data, scraped from [Wikipedia](https://en.wikipedia.org/wiki/Main_Page)
+ 📜 *movie_metadata.csv* for general film statistics, from the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/)
+ ❌ *name.clusters.txt* film character names, from the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/)
+ 🧻 *phrases_early_movies.txt* quality phrases, and the plots of the earliest movies with the highest box office containing that phrase
+ 📜 *plot_summaries.txt* plot summaries, from the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/)
+ 🧻 *quality_phrases.txt* a list of phrases lifted from plot_summaries.txt that AutoPhrase deemed high quality
+ ❌ *ratings.tsv* a list of film ratings, from  [IMDb](https://developer.imdb.com/non-commercial-datasets/)
+ 📜 *rotten_tomatoes_critic_reviews.zip* a list of movie reviews, from [Rotten Tomatoes](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset/data?select=rotten_tomatoes_critic_reviews.csv)
+ 📜 *rotten_tomatoes_movies.csv* used in sentiment analysis, metadata about movies on [Rotten Tomatoes](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset?select=rotten_tomatoes_movies.csv)
+ 🧻 *top_phrases.txt* for each decade, highest TF-IDF phrases with the earliest associated movie, used for final quality phrase table
+ ❌ *tvtropes.clusters.txt* character archetypes, from the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/)
+ 📜 *wikidata_freebase_imdb.tsv* used for data augmentation, a mapping between Wikidata, Freebase, and IMDb Ids, queried from [Wikidata Query Service](https://query.wikidata.org/) by [Linkai Dai](https://duckduckgo.com/?q=Linkai+Dai&atb=v314-1&ia=web)
