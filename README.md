# Poker

This is a personal project for building a backend API that can support a multiplayer game of poker. It is a work in progress so please check out the open issues to see what work still needs to be done. It is a Flask web app powered by a PostgreSQL database.

## Getting Started

To get the project running, all you have to do is pull this repo and use Docker-compose to run the project.
```
docker-compose up
```

### Prerequisites

You will need Docker, Python3 and PostgreSQL installed in order to work with this project.

### Installing

This project includes Pipfile.lock for deterministic builds.

```
pip install pipenv
pipenv install
```

## Running the tests

The tests require a database. In poker/tests/conftest.py, update the TEST_DB_URI to point to your test database.

```
pytest
```

## Authors

* **Hanson Yu**

## Acknowledgments

* The inspiration for this project was from me wanting to learn more about Flask and Docker.
