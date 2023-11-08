
import json
import pandas as pd

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
                'plot_summaries.txt'] 
    """

    # Load table of column names 
    names = pd.read_table(folder + 'column_names.txt', sep=' ', 
                  converters={'columns': lambda x: str.split(x, sep=',')})

    # Converters for initial formatting
    converters = {'data': lambda x: list(json.loads(x).values())} if filename == 'tvtropes.clusters.txt' else None

    # Load data with column names
    data = pd.read_table(folder + filename, names = list(names[names['filename']==filename]['columns'])[0], converters=converters)

    # Expand list data in tvtropes.clusters.txt into multiple columns
    if filename == 'tvtropes.clusters.txt':
        data = expand_list_data(data, 'data', ['character_name', 'movie_name', 'freebase_map_id', 'actor_name'])

    return data

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
    df_copy[column] = pd.to_datetime(df_copy[column], format='mixed', errors='coerce')

    # Compute decade bounds and bins
    start = str(df_copy[column].min().year // 10 * 10)
    end = str((df_copy[column].max().year // 10 + 1) * 10)
    decades = pd.date_range(start=start, end=end, freq='10YS', inclusive='both')

    # Append 'decade' column
    df_copy['decade'] = pd.cut(df_copy[column], bins=decades, labels=decades[:-1], include_lowest=True)

    return df_copy