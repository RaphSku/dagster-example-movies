import pandas as pd
import numpy as np
import math
from dagster import asset, OpExecutionContext
from dagster_movies.utilities import convert_to_list, count_words_in_series


@asset(required_resource_keys={"postgres_api"}, group_name="movies", io_manager_key="local_postgres_io_manager")
def imdb_movie_dataset(context: OpExecutionContext):
    sql_statement = """
        select id, title, director, genre, runtime, imdb_rating, release_year from movies;
    """

    with context.resources.postgres_api.cursor() as cursor:
        cursor.execute(sql_statement)
        result = cursor.fetchall()

    return {'result': result}


@asset(group_name="movies", io_manager_key="json_io_manager")
def imdb_movie_dataset_statistics(imdb_movie_dataset: pd.DataFrame):
    genres_series = imdb_movie_dataset["genre"].apply(lambda x: convert_to_list(x))
    genre_counts = count_words_in_series(genres_series)

    mean_runtime = math.floor(imdb_movie_dataset["runtime"].mean())
    mean_imdb_rating = np.round(imdb_movie_dataset["imdb_rating"].mean(), 2)
    min_release_year = imdb_movie_dataset["release_year"].min()
    max_release_year = imdb_movie_dataset["release_year"].max()

    statistics = {
        'genre_counts': genre_counts,
        'mean_runtime': int(mean_runtime),
        'mean_imdb_rating': float(mean_imdb_rating),
        'min_release_year': int(min_release_year),
        'max_release_year': int(max_release_year)
    }

    return {'statistics': statistics}