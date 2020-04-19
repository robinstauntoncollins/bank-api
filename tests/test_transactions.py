import os
from datetime import datetime

import pytest

from bank_api import create_app
from bank_api.models import db, Transaction, Account

class TestTransactions():

    def test_get_transactions(self, test_client, test_transactions):
        db.session.add_all(test_transactions)
        db.session.commit()
        response = test_client.get('/api/v1/transactions')
        assert response.json == {
            'transactions': [
                {
                    'account_id': 1,
                    'amount': 20,
                    'time': datetime(2020, 4, 19, 15).isoformat(),
                    'uri': '/api/v1/transactions/1'
                },
                {
                    'account_id': 2,
                    'amount': -20,
                    'time': datetime(2020, 4, 19, 15).isoformat(),
                    'uri': '/api/v1/transactions/2'
                },
            ]
        }
    
    def test_post_transactions(self, test_client):
        a = Account(account_number=123456789, customer_id=1, balance=50)
        db.session.add(a)
        db.session.commit()
        response = test_client.post(
            '/api/v1/transactions',
            json={
                'amount': 300_000,
                'account_id': a.id
            })
        assert response.status_code == 201
        json = response.get_json()
        assert json['transaction']['amount'] == 300000.0
        assert json['transaction']['uri'] == '/api/v1/transactions/1'
        assert json['transaction']['account_id'] == 1

    def test_get_transaction(self, test_client, test_transactions):
        db.session.add_all(test_transactions)
        db.session.commit()

        response = test_client.get(
            '/api/v1/transactions/1'
        )
        assert response.status_code == 200
        assert response.json == {
            'transaction': {
                'amount': 20.0,
                'account_id': 1,
                'time': datetime(2020, 4, 19, 15).isoformat(),
                'uri': '/api/v1/transactions/1'
            }
        }
