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
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 50.0,
                'owner_id': 1,
                'uri': '/api/v1/accounts/1'
            },
            {
                'name': 'Matin',
                'surname': 'Abbasi',
                'balance': 200.0,
                'owner_id': 2,
                'uri': '/api/v1/accounts/2'
            },
            {
                'name': 'Robin',
                'surname': 'Staunton-Collins',
                'balance': 130.0,
                'owner_id': 1,
                'uri': '/api/v1/accounts/3'
            },
            {
                'name': 'Rodrigo',
                'surname': 'Hammerly',
                'balance': 450.0,
                'owner_id': 3,
                'uri': '/api/v1/accounts/4'
            },
        ]
    }
    