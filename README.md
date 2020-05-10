# Bank API Coding Assignment

[![Build Status](https://travis-ci.org/robinstauntoncollins/bank-api.svg?branch=master)](https://travis-ci.org/robinstauntoncollins/bank-api)
[![Coverage Status](https://coveralls.io/repos/github/robinstauntoncollins/bank-api/badge.svg?branch=master)](https://coveralls.io/github/robinstauntoncollins/bank-api?branch=master)

A simple Bank API built as part of a coding interview using Python, Flask and SQLite

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Install Python 3.6+ and git.

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the repo

```bash
git clone https://github.com/robinstauntoncollins/bank-api.git
cd bank-api
```

Create virtual environment

```bash
python -m venv venv/
```

Activate virtual environment

On Linux

```bash
source venv/bin/activate
```

On Windows

```bash
source venv/Scripts/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Initialize database

```bash
flask db upgrade
```

Run tests

```bash
pytest
```

## Start Server Locally

Start server

Windows

```bash
python bankapi.py
```

Linux

```bash
./bankapi.py
```

### Make requests

I like [HTTPie CLI](https://httpie.org/) but curl works too.

List of available endpoints

```bash
>> http GET http://localhost:5000/

HTTP/1.0 200 OK
Content-Length: 521
Content-Type: application/json
Date: Tue, 21 Apr 2020 21:17:57 GMT
Server: Werkzeug/1.0.1 Python/3.7.0

{
    "version": {
        "v1": {
            "actions": {
                "get_customer_url": "http://localhost:5000/api/v1/getCustomerInfo",
                "open_account_url": "http://localhost:5000/api/v1/openAccount",
                "transfer_url": "http://localhost:5000/api/v1/transfer"
            },
            "collections": {
                "accounts_url": "http://localhost:5000/api/v1/accounts",
                "customers_url": "http://localhost:5000/api/v1/customers",
                "transactions_url": "http://localhost:5000/api/v1/transactions"
            }
        }
    }
}
```

Make new customer

```bash
>> http POST http://localhost:5000/api/v1/customers name="Monty" surname="Python"
HTTP/1.0 201 CREATED
Content-Length: 119
Content-Type: application/json
Date: Tue, 21 Apr 2020 21:24:42 GMT
Server: Werkzeug/1.0.1 Python/3.7.0

{
    "customer": {
        "name": "Monty",
        "surname": "Python",
        "uri": "/api/v1/customers/1"
    }
}
```

Open new account for the newly created customer

```bash
>> http POST http://localhost:5000/api/v1/openAccount customerID=1 initialCredit=500
HTTP/1.0 200 OK
Content-Length: 170
Content-Type: application/json
Date: Tue, 21 Apr 2020 21:26:25 GMT
Server: Werkzeug/1.0.1 Python/3.7.0

{
    "account": {
        "account_number": 11210932237993115648,
        "balance": 500.0,
        "customer_id": 1,
        "uri": "/api/v1/getCustomerInfo"
    },
    "result": true
}
```

View all customer information: accounts, transactions

```bash
λ http GET http://localhost:5000/api/v1/getCustomerInfo customerID=1
HTTP/1.0 200 OK
Content-Length: 1071
Content-Type: application/json
Date: Tue, 21 Apr 2020 21:28:06 GMT
Server: Werkzeug/1.0.1 Python/3.7.0

{
    "customer": {
        "accounts": [
            {
                "account_number": 11210932237993115648,
                "balance": 500.0,
                "customer_id": 1,
                "transactions": [
                    {
                        "account_id": 1,
                        "amount": 500.0,
                        "time": "2020-04-20T19:37:22.160495"
                    }
                ]
            }
        ],
        "name": "Monty",
        "surname": "Python"
    }
}
```

### Other commands

Initialize database with preloaded data (Optional)

```bash
flask createdb
```

## Running the tests

Run with coverage report:

```bash
pytest --cov=bank_api tests/
```

## Deployment

### Docker

Build image

```bash
docker build -t bankapi:latest .
```

Start container

```bash
docker run --name bankapi -d -p 5000:5000 --rm bankapi:latest
```

## Built With

* [Flask](https://flask.palletsprojects.com) - The web framework used
* [FlaskRESTful](https://flask-restful.readthedocs.io/) - Flask extension for building REST APIs
* [FlaskSQLALchemy](https://flask-sqlalchemy.palletsprojects.com) - Flask extension which adds support for the SQLAlchemy ORM
* [FlaskMigrate](https://github.com/miguelgrinberg/Flask-Migrate) - Flask extension which adds support for database migrations using Alembic

## License

This project is licensed under The Unlicense - see the [LICENSE.md](LICENSE.md) file for details
