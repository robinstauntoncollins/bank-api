import os
from flask import current_app
import pytest

from bank_api import create_app

def test_app_exists(test_client):
    assert current_app is not None

def test_app_is_testing(test_client):
    assert current_app.config['TESTING'] == True

    
def test_index(test_client):
    response = test_client.get('/')
    assert response.json == {'version': {
        'v1': {
            'accounts_url': 'http://localhost/api/v1/accounts',
            'customers_url': 'http://localhost/api/v1/customers'
        }}}