[![Build Status](https://travis-ci.org/robinstauntoncollins/bank-api.svg?branch=master)](https://travis-ci.org/robinstauntoncollins/bank-api)
[![Coverage Status](https://coveralls.io/repos/github/robinstauntoncollins/bank-api/badge.svg?branch=master)](https://coveralls.io/github/robinstauntoncollins/bank-api?branch=master)

# Bank API Coding Assignment

A simple Bank API built as part of a coding interview using Python, Flask and SQLite

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Install Python 3.6+ and git.

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the repo

```
git clone https://github.com/robinstauntoncollins/bank-api.git
cd bank-api
```

Create virtual environment

```
python -m venv venv/
```

Activate virtual environment

On Linux
```
source venv/bin/activate
```
On Windows

```
source venv/Scripts/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run tests

```
pytest
```

## Start Server Locally

Start server

Windows
```
python bankapi.py
```

Linux
```
./bankapi.py
```


### Make requests

I like [HTTPie CLI](https://httpie.org/)

List of available endpoints

```
curl http://localhost:5000/
```


## Running the tests

TODO

Explain how to run the automated tests for this system

### Break down into end to end tests

TODO

Explain what these tests test and why

```
Give an example
```

### And coding style tests

TODO

Explain what these tests test and why

```
Give an example
```

## Deployment

### Docker

Build image

```
docker built -t bankapi:latest .
```

Start container

```
docker run --name bankapi -d -p 5000:5000 --rm bankapi:latest
```

## Built With

* [Flask](https://flask.palletsprojects.com) - The web framework used
* [FlaskRESTful](https://flask-restful.readthedocs.io/) - Flask extension for building REST APIs
* [FlaskSQLALchemy](https://flask-sqlalchemy.palletsprojects.com) - Flask extension which adds support for the SQLAlchemy ORM
* [FlaskMigrate](https://github.com/miguelgrinberg/Flask-Migrate) - Flask extension which adds support for database migrations using Alembic

## License

This project is licensed under The Unlicense - see the [LICENSE.md](LICENSE.md) file for details


