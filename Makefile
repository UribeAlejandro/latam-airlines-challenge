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
# 	@Checking uv installation ...
# 	which uv > /dev/null || (echo "uv is not installed. Please install uv (https://pypi.org/project/uv/) and try again." && exit 1)
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

.PHONY: stress-test
stress-test:
	mkdir reports || true
	uv run locust

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

.PHONY: run
run:			## Run the API locally
	uv run fastapi run challenge/api.py --port 8000
