import os

import pytest

from bank_api import create_app


def test_index(test_client):
    response = test_client.get('/')
    assert response.json == {'version': {
        'v1': {
            'accounts_url': 'http://localhost:5000/api/v1/accounts'
        }}}


def test_get_accounts(test_client):
    response = test_client.get('/api/v1/accounts')
    assert response.json == {
        'accounts': [
            {
                'account_number': 1,
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 50.0,
                'customer_id': 1,
                'uri': '/api/v1/accounts/1'
            },
            {
                'account_number': 2,
                'name': 'Matin',
                'surname': 'Abbasi',
                'balance': 200.0,
                'customer_id': 2,
                'uri': '/api/v1/accounts/2'
            },
            {
                'account_number': 3,
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 130.0,
                'customer_id': 1,
                'uri': '/api/v1/accounts/3'
            },
            {
                'account_number': 4,
                'name': 'Rodrigo',
                'surname': 'Hammerly',
                'balance': 450.0,
                'customer_id': 3,
                'uri': '/api/v1/accounts/4'
            },
        ]
    }
    
def test_post_account(test_client):
    response = test_client.post(
        '/api/v1/accounts',
        data={
            'name': 'Steve',
            'surname': 'Carell',
            'balance': 300_000,
            'customer_id': 5
        }
    )
    assert response.json == {
        'account_number': 5,
        'name': 'Steve',
        'surname': 'Carell',
        'balance': 300_000.0,
        'uri': '/api/v1/accounts/5'
    }