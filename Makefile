#
## PHONY
#
.PHONY: create-dep-list create-venv  boostrap-postgres-db connect-to-postgres 

#
## Includes
#
include Makefile.dagster.mk

## Create requirements.txt
create-dep-list:
	pip freeze --local > requirements.txt

## Creating a virtual environment
create-venv:
	python3.11 -m venv $(VENV_PATH)
	pip install -r requirements.txt

## Start up the PostgresDB
boostrap-postgres-db:
	cd db-setup && docker compose up

## Connect to the PostgresDB
connect-to-postgres:
	psql -p 8085 -U moviemanager -h localhost -d moviestore

