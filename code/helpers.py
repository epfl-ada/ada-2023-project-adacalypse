import json
import pandas as pd
import numpy as np
import regex as re
import ast  # Evaluate the literal syntax tree of a string
import requests
import nltk
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

def extract_year(date):
    """
    Takes a date as an input, verifies if it is a string,
    searches for a character of length 4 digits and finally returns
    it as an integer.
    Example of usage: movies_df['movie_release_date'] = movies_df['movie_release_date'].apply(extract_year)
                      movies_df['movie_release_date'] = movies_df['movie_release_date'].fillna(0).astype(int)
    """
    if isinstance(date, str):
        match = re.search(r'(\d{4})', date)
        if match:
            return int(match.group(0))
    return None

def date_to_float(dataset, column_name):
    """
    Takes a dataset and its column name corresponding to a date as input, and returns the same dataset with its year converted to float
    Example : movie_metadata = date_to_int(movie_metadata, 'movie_release_date')
    """
    dataset[column_name] = dataset[column_name].str[0:4].astype(float)
    return dataset

def parse_as_date(dataset, column_name):
    """
    Takes a dataset and its column name corresponding to a date as input, and returns the same dataset with its year converted to a pandas DateTime
    Example : movie_metadata = date_to_int(movie_metadata, 'movie_release_date')
    """
    dataset[column_name] = pd.to_datetime(dataset[column_name], format='mixed', errors='coerce')
    return dataset

def bin_into_decades(df, column):
    """
        Takes a DataFrame with a date-valued column and appends a 'decade' column.
        May yield NaTs if the column data cannot be parsed.

        Parameters:
            (DataFrame) df: a frame with a date-valued column
            (string) column: the name of the date-valued column
    """
    # Copy the original dataframe
    df_copy = df.copy()

    # Try to parse column data as timestamps.
    df_copy[column] = pd.to_datetime(df_copy[column], errors='coerce')

    # Compute decade bounds and bins
    start = str(df_copy[column].min().year // 10 * 10)
    end = str((df_copy[column].max().year // 10 + 1) * 10)
    decades = pd.date_range(start=start, end=end, freq='10YS', inclusive='both')

    # Append 'decade' column
    df_copy['decade'] = pd.cut(df_copy[column], bins=decades, labels=decades[:-1], include_lowest=True)

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
        Duplicates a singleton list.
    """
        
    if len(arr) == 1:
        if type(arr)==pd.Series:
            arr[1]=arr[0]
            return arr
        else: 
            return 2*arr
    else:
        return arr


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
    # Tokenize and apply filters
    words = nltk.wordpunct_tokenize(sent)
    filtered_words = [w for w in words if (is_wordnet_word(w.lower()) or not w.isalpha()) and len(w) < 15]
    return " ".join(filtered_words)