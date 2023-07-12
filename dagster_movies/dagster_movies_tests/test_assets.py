import pytest
import os
import pandas as pd

from dagster import (
    materialize_to_memory,
    build_output_context
)

from unittest.mock import patch

from dagster_movies.assets import imdb_movie_dataset
from dagster_movies.postgres_io_manager import LocalPostgresIOManager


@pytest.fixture()
def mock_data():
    return [
        (0, 'Saving Private Ryan', 'Steven Spielberg', "['Drama', 'War']", 169, 8.6, 1998),
        (1, 'The Sixth Sense', 'M. Night Shyamalan', "['Drama', 'Mystery', 'Thriller']", 107, 8.1, 1999)
    ]


def test_postgres_ingestion(mock_data: list[tuple]):
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.cursor.return_value.__enter__.return_value.fetchall.return_value = mock_data

        result = materialize_to_memory(
            [
                imdb_movie_dataset
            ],
            resources={"postgres_api": mock_connect}
        )

    assert result.success


def test_local_postgres_io_manager_handle_output(mock_data: list[tuple]):
    data = {'result': mock_data}
    target_file = "./test_dataset.csv"

    output_context = build_output_context()
    manager = LocalPostgresIOManager(target_file=target_file)
    manager.handle_output(output_context, data)

    target_file_exists = False
    if os.path.exists(target_file):
        target_file_exists = True

    assert target_file_exists == True

    try:
        act_df = pd.read_csv(target_file)
        expected_output = ["id", "title", "director", "genre", "runtime", "imdb_rating", "release_year"]
        
        assert len(act_df.columns) == len(expected_output)
        assert all(act_column == exp_column for act_column, exp_column in zip(act_df.columns, expected_output))

        exp_df = pd.DataFrame(
            {
                "id": [0, 1],
                "title": ['Saving Private Ryan', 'The Sixth Sense'],
                "director": ['Steven Spielberg', 'M. Night Shyamalan'],
                "genre": ["['Drama', 'War']", "['Drama', 'Mystery', 'Thriller']"],
                "runtime": [169, 107],
                "imdb_rating": [8.6, 8.1],
                "release_year": [1998, 1999]
            }
        )
        pd.testing.assert_frame_equal(left = act_df, right = exp_df)
    finally:
        os.remove(target_file)