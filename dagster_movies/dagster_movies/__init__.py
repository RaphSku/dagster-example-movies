import psycopg2
import os
import dotenv

from dagster import Definitions, load_assets_from_modules, resource, InitResourceContext, ResourceDefinition

from . import assets
from dagster_movies.postgres_io_manager import LocalPostgresIOManager
from dagster_movies.json_io_manager import JSONIOManager

dotenv.load_dotenv()

all_assets = load_assets_from_modules([assets])

@resource(config_schema={"host": str, "port": str, "database": str, "user": str, "password": str})
def postgres_api(init_context: InitResourceContext):
    database_connection = {
        'host': init_context.resource_config["host"],
        'port': init_context.resource_config["port"],
        'database': init_context.resource_config["database"],
        'user': init_context.resource_config["user"],
        'password': init_context.resource_config["password"]
    }

    return psycopg2.connect(**database_connection)

def get_configured_postgres_api() -> ResourceDefinition:
    return postgres_api.configured(
        {
            'host': os.environ["POSTGRES_HOST"],
            'port': os.environ["POSTGRES_PORT"],
            'database': os.environ["POSTGRES_DB"],
            'user': os.environ["POSTGRES_USER"],
            'password': os.environ["POSTGRES_PW"]
        }
    )

defs = Definitions(
    assets=all_assets,
    resources={
        'postgres_api': get_configured_postgres_api(),
        'local_postgres_io_manager': LocalPostgresIOManager(target_file="./data/movies.csv"),
        'json_io_manager': JSONIOManager(target_file="./data/statistics.json")
    }
)
