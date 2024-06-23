import pandas as pd
import numpy as np
import ast

# Load datasets
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')

# Merge datasets on the 'title' column
movies = movies.merge(credits, on='title')

# Select relevant columns
movies = movies[['movie_id', 'title', 'genres', 'keywords', 'overview', 'cast', 'crew']]

# Drop rows with missing values
movies.dropna(inplace=True)

# Function to convert JSON string to list of names
def convert(obj):
    list = []
    for i in ast.literal_eval(obj):
        list.append(i['name'])
    return list

# Apply conversion functions to 'genres' and 'keywords' columns
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Function to extract top 3 cast members
def convertCast(obj):
    list = []
    ctr = 0
    for i in ast.literal_eval(obj):
        if ctr != 3:
            list.append(i['name'])
            ctr += 1
        else:
            break
    return list

# Apply conversion function to 'cast' column
movies['cast'] = movies['cast'].apply(convertCast)

# Function to fetch director's name from crew
def fetchDirector(obj):
    list = []
    if isinstance(obj, str):
        try:
            for i in ast.literal_eval(obj):
                if i['job'] == 'Director':
                    list.append(i['name'])
                    break
        except ValueError:
            print(f"Error parsing: {obj}")
    return list

# Apply function to 'crew' column
movies['crew'] = movies['crew'].apply(fetchDirector)

# Display the first few rows of the processed dataframe
movies.head()
