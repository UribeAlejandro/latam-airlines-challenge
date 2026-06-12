.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:             	## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: venv
venv:			## Create a virtual environment
	@echo "Creating virtualenv ..."
	uv venv --clear
	@echo "Virtualenv created at .venv"

.PHONY: install
install:		## Install dependencies
	@echo "Installing Python"
	uv python install
	@echo "Installing dependencies"
	uv sync --all-groups
	@echo "Installing pre-commit hooks"
	uv run pre-commit install

STRESS_URL = https://flight-delay-api-493027879117.us-central1.run.app
.PHONY: stress-test
stress-test:
	mkdir reports || true
	uv run locust -H $(STRESS_URL)

.PHONY: model-test
model-test:			## Run tests and coverage
	mkdir reports || true
	uv run pytest --cov=challenge tests/model

.PHONY: api-test
api-test:			## Run tests and coverage
	mkdir reports || true
	uv run pytest  --cov=challenge tests/api

.PHONY: build
build:			## Build locally the python artifact
	uv build --wheel

.PHONY: build-docker
build-docker:		## Build the docker image locally
	docker build -t latam-challenge:latest .

.PHONY: run
run:			## Run the API locally
	uv runfastapi dev challenge/api.py --port 8000

.PHONY: run-docker
run-docker:		## Run the API in a docker container
	docker run --env-file .env -p 8000:8000 latam-challenge:latest
