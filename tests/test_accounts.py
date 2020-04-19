import os

import pytest

from bank_api import create_app
from bank_api.models import db, Customer


class TestAccounts():

    def test_get_accounts(self, test_client, test_accounts):
        db.session.add_all(test_accounts)
        db.session.commit()
        response = test_client.get('/api/v1/accounts')
        assert response.json == {
            'accounts': [
                {
                    'account_number': 12345678901234567890,
                    'balance': 0.0,
                    'customer_id': 1,
                    'uri': '/api/v1/accounts/1'
                },
                {
                    'account_number': 98765432109876543210,
                    'balance': 100.0,
                    'customer_id': 1,
                    'uri': '/api/v1/accounts/2'
                },
            ]
        }
    
    def test_post_accounts(self, test_client):
        c = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(c)
        db.session.commit()
        c = Customer.query.first()
        response = test_client.post(
            '/api/v1/accounts',
            json={
                'balance': 300_000,
                'customer_id': c.id
            })
        assert response.status_code == 201
        json = response.get_json()
        assert len(str(json['account']['account_number'])) == 20
        assert json['account']['uri'] == '/api/v1/accounts/1'
        assert json['account']['balance'] == 300000.0
        assert json['account']['customer_id'] == 1

    def test_get_account(self, test_client, test_accounts):
        db.session.add_all(test_accounts)
        db.session.commit()

        response = test_client.get(
            '/api/v1/accounts/1'
        )
        assert response.status_code == 200
        assert response.json == {
            'account': {
                'account_number': 12345678901234567890,
                'balance': 0.0,
                'customer_id': 1,
                'uri': '/api/v1/accounts/1'
            }
        }

    def test_put_account(self, test_client, test_accounts):
        db.session.add_all(test_accounts)
        db.session.commit()

        response = test_client.put(
            '/api/v1/accounts/1',
            json={
                'balance': 150
            }
        )
        assert response.status_code == 200
        assert response.json == {
            'account': {
                'account_number': 12345678901234567890,
                'balance': 150.0,
                'customer_id': 1,
                'uri': '/api/v1/accounts/1'
            }
        }

    def test_delete_account(self, test_client, test_accounts):
        db.session.add_all(test_accounts)
        db.session.commit()

        response = test_client.delete(
            '/api/v1/accounts/1'
        )
        assert response.status_code == 200
        assert response.json == {
            'result': True
        }
