import os

import pytest

from bank_api.models import db, Customer


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

    def test_put_customer(self, test_client):
        c = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(c)
        db.session.commit()

        response = test_client.put(
            'api/v1/customers/1',
            json={
                'name': "Monty",
                'surname': "Python"
            }
        )
        assert response.status_code == 200
        assert response.json == {
            'customer': {
                'name': "Monty",
                'surname': "Python",
                'uri': '/api/v1/customers/1'
            }
        }
        
    def test_delete_customer(self, test_client):
        c = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(c)
        db.session.commit()

        c = Customer.query.first()
        assert c is not None

        response = test_client.delete(
            'api/v1/customers/1'
        )
        assert response.status_code == 200
        assert response.json == {'result': True}

        assert Customer.query.all() == []

    def test_get_customer(self, test_client):
        c = Customer(name="Monty", surname="Python")
        db.session.add(c)
        db.session.commit()

        response = test_client.get(
            'api/v1/customers/1'
        )
        assert response.status_code == 200
        assert response.json == {
            'customer': {
                'name': "Monty",
                'surname': "Python",
                'uri': '/api/v1/customers/1'
            }
        }

    def test_get_customer_not_found(self, test_client):
        response = test_client.get(
            'api/v1/customers/1'
        )
        assert response.status_code == 404
        assert response.json == {
            'message': "No customer with id: 1",
            'status_code': 404
        }



