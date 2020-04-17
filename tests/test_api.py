import os

import pytest

from bank_api import create_app
from bank_api.models import Account, db


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


def test_index(test_client):
    response = test_client.get('/')
    assert response.json == {'version': {
        'v1': {
            'accounts_url': 'http://localhost:5000/api/v1/accounts'
        }}}


def test_account_model():
    new_account = Account().import_data({
        'name': 'Robin',
        'surname': 'Staunton-Collins',
        'balance': 0,
        'owner_id': 1
    })
    assert new_account.name == "Robin"
    assert new_account.surname == "Staunton-Collins"
    assert new_account.balance == 0
    assert new_account.owner_id == 1
    account_data = new_account.export_data()
    assert account_data == {
        'name': 'Robin',
        'surname': 'Staunton-Collins',
        'balance': 0,
        'owner_id': 1
    }



def test_get_accounts(test_client):
    response = test_client.get('/api/v1/accounts')
    assert response.json == {
        'accounts': [
            {
                'account_id': 1,
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 50,
                'owner_id': 1
            },
            {
                'account_id': 2,
                'name': 'Matin',
                'surname': 'Abbasi',
                'balance': 200,
                'owner_id': 2
            },
            {
                'account_id': 3,
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 130,
                'owner_id': 1
            },
            {
                'account_id': 4,
                'name': 'Rodrigo',
                'surname': 'Hammerly',
                'balance': 450,
                'owner_id': 3
            },
        ]
    }
    