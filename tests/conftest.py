import pytest

from bank_api import create_app
from bank_api.models import Account, Customer, db


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
