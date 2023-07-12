#
## Variables
#
PROJECT_NAME ?= dagster_movies

#
## PHONY
#
.PHONY: create-dagster-project install-project-dep start-dagster test

## By default, start the dagster dev server
default: start-dagster

## Bootstrap a dagster project
create-dagster-project:
	dagster project scaffold --name $(PROJECT_NAME)

## Install project dependencies
install-project-dep:
	cd $(PROJECT_NAME) && pip install -e ".[dev]"

## Start the Dagster dev server
start-dagster:
	cd $(PROJECT_NAME) && dagster dev

## Run tests
test:
	cd dagster_movies/dagster_movies_tests && pytest