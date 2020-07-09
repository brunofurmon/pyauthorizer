# Python Transaction Authorizer Example

## Requirements
- Docker (ou Docker for Windows): https://docs.docker.com/install/
- python3 (via apt ou brew)
- python3-pip (via apt ou brew)
- pipenv (via pip: `pip install -g pipenv`)

## Installing and Running
This project is dockerized, so running equals building its image and running. Run:
  - `docker-compose build --no-cache` - Build image called brunofurmon/brunofurmon-pyauthorizer:1.0
  - `docker-compose up` - Executes the image in a container and binds its host:port to the host.

This will run the application/app.py module and insert the `./operations` into the STDIN, which should give the following Input/Output:

STDIN < `./operations`
{ "account": { "activeCard": true, "availableLimit": 100 } }
{ "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z" } }
{ "transaction": { "merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:00:00.000Z" } }

OUTPUT > 
{"account": {"activeCard": true, "availableLimit": 100}, "violations": []}
{"account": {"activeCard": true, "availableLimit": 80}, "violations": []}
{"account": {"activeCard": true, "availableLimit": 80}, "violations": ["insufficient-limit"]}

To test other files, substitute the _operations_ file and run again using the instructions above.

## Development environment activation
This project uses a virtual environment (pipenv), so first you should install and activate like following:
   - `pipenv install --three`
   - `./authorize.sh` (runs a `source $(pipenv --venv)/bin/activate` and a `python ./src/application/app.py < ./test/scenarios/templateScenario`)

## Test Execution 
This projects uses a simple custom runner which overrides stdin with scenario files and invoke the main project so to run them.

### Integration tests
From the root folder, execute:
- `python ./test/run.py`

### Generating new integration tests:
This repo contains a scenario generator under the test folder, in which you can alter its parameters to generate a large and fully customizable scenario.
It will generate a file called `Generated(<random10CharactersString>)` under the `test/scenarios` folder. One of them is included in this Repo
From the root folder, execute:
- `python ./test generator.py`

### Unit tests
From the _test_ directory, the _src_ structure is replicated with _test_*.py_ files testing each source when applicable. To run them, it is required that you activate the virtual environment (`source $(pipenv --venv)/bin/activate`) and have pytest installed via `pip install pytest`. Then run from the root folder, call pytest as a module to avoid problems with module instantiation from "src module":
- `python -m pytest`

## Architecture
_"Simple, not easy"_ - @RonJeffries

### DDD
The folder structure of choice is based on some DDD projects I've been working. Although it adds complexity to the solution, the intent was to separate concerns in a way that it gets easier to extend funcionalities, add/alter logic and do infrastructure readaptation as necessary.

The solution is divided in 

- *Domain* - Where the main business logic and entities are. Models, Commands and Handlers
- *Contracts* - Really raw class in order to give meaningful base names. Also for type assertions along the run
- *Infrastructure* - Everything from the application border and out. In our case, as the bus' and the repositories are implemented as InMemory, here goes the implementation for those instances.
- *Application* - The entrypoint to the solution, which relies on the Domain, applied under the Infrastructure, following the Contracts.

### C ~Q~ RS

Because of the requirements, I felt there was no real need to build a Query Stack.
Input was based on a list of _Commands_, and so I built a CommandBus to dispatch each line of input.

### Virtual Environment
Using Virtual Environments makes it easier for developers to quickly get python applications up and running regardless of its dependencies.
It relies on _pipenv_ module to manage its dependencies state.
