import os
import pandas as pd
import pydantic
import json

from dagster import (
    ConfigurableIOManager,
    OutputContext, 
    InputContext
)


class JSONIOManager(ConfigurableIOManager):
    target_file: str = pydantic.Field(
        description="Path for the json file"
    )

    def handle_output(self, context: OutputContext, obj: dict) -> None:
        os.makedirs(os.path.dirname(self.target_file), exist_ok=True)

        with open(self.target_file, 'w') as file:
            json.dump(obj["statistics"], file)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        with open(self.target_file) as json_file:
            return json.load(json_file)