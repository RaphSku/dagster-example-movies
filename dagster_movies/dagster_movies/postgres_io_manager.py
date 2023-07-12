import os
import csv
import pandas as pd
import pydantic

from dagster import (
    ConfigurableIOManager,
    OutputContext, 
    InputContext
)

class LocalPostgresIOManager(ConfigurableIOManager):
    target_file: str = pydantic.Field(
        description="Path for the csv file"
    )

    def handle_output(self, context: OutputContext, obj: dict) -> None:
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)

        result = obj["result"]
        with open(self.target_file, 'w', newline='') as file:
            target_csv = csv.writer(file)
            target_csv.writerow(['id', 'title', 'director', 'genre', 'runtime', 'imdb_rating', 'release_year'])
            for row in result:
                target_csv.writerow(row)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        return pd.read_csv(self.target_file)