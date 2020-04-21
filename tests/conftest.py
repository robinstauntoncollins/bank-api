from datetime import datetime
import pytest

from bank_api import create_app
from bank_api.models import Account, Customer, Transaction, db


@pytest.fixture()
def test_client():
    app = create_app('testing')

    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        db.drop_all()
        db.create_all()
   
        yield client
        db.drop_all()
        ctx.pop()


@pytest.fixture()
def test_customers():
    customers = [
        {
            'name': "Robin",
            'surname': "Staunton-Collins"
        },
        {
            'name': "Jerry",
            'surname': "Seinfeld"
        },
    ]
    return [Customer().import_data(customer) for customer in customers]



@pytest.fixture()
def test_accounts():
    accounts = [
        {
            'account_number': 12345678901234567890,
            'customer_id': 1,
            'balance': 0
        },
        {
            'account_number': 98765432109876543210,
            'customer_id': 1,
            'balance': 100
        }
    ]
    return [Account().import_data(account) for account in accounts]


@pytest.fixture()
def test_transactions():
    transactions = [
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 20
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -20
        }
    ]
    return [Transaction().import_data(transaction) for transaction in transactions]


@pytest.fixture()
def lots_of_transactions():
    transactions = [
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 20
        },
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 21
        },
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 25
        },
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 2756
        },
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 2354
        },
        {
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 220
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -20
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -99.89
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 13.72
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -12.54
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -144
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': 735
        },
        {
            'account_id': 2,
            'time': datetime(2020, 4, 19, 15, 0, 0),
            'amount': -35
        },
    ]
    return [Transaction().import_data(transaction) for transaction in transactions]
