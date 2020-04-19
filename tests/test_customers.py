import os

import pytest

from bank_api import create_app
from bank_api.models import db


class TestCustomers():

    def test_post_customer(self, test_client):
        response = test_client.post(
            '/api/v1/customers',
            json={
                'name': "Robin",
                'surname': 'Staunton-Collins'
            }
        )
        assert response.status_code == 201
        assert response.json == {
            'customer': {
                'name': "Robin",
                'surname': "Staunton-Collins",
                'uri': '/api/v1/customers/1'
            }
        }

    def test_get_customers(self, test_client, test_customers):
        db.session.add_all(test_customers)
        db.session.commit()

        response = test_client.get(
            '/api/v1/customers',
        )
        assert response.status_code == 200
        assert response.json == {
            'customers': [
                {
                    'name': 'Robin',
                    'surname': 'Staunton-Collins',
                    'uri': '/api/v1/customers/1'
                },
                {
                    'name': 'Jerry',
                    'surname': 'Seinfeld',
                    'uri': '/api/v1/customers/2'
                },
            ]
        }
        