#!/bin/sh

source $(pipenv --venv)/bin/activate

python ./src/application/app.py < ./test/scenarios/templateScenario
