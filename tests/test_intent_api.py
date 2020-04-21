import os
from datetime import datetime
import pytest

from bank_api.models import db, Account, Transaction, Customer

class TestTransfer():

    def test_transfer(self, test_client, test_accounts):
        db.session.add_all(test_accounts)
        db.session.commit()

        response = test_client.post(
            '/api/v1/transfer',
            json={
                'senderAccount': '98765432109876543210',
                'receiverAccount': '12345678901234567890',
                'amount': '50'
            }
        )
        assert response.status_code == 200
        json = response.get_json()
        assert json == {
            'result': True
        }
        sender = Account.query.filter_by(account_number='98765432109876543210').first()
        receiver = Account.query.filter_by(account_number='12345678901234567890').first()
        assert sender.balance == 50.0
        assert receiver.balance == 50.0

        sending_transaction = Transaction.query.filter_by(account_id=sender.id).first()
        receiving_transaction = Transaction.query.filter_by(account_id=receiver.id).first()
        assert sending_transaction.amount == -50.0
        assert sending_transaction.account.id == sender.id
        assert receiving_transaction.amount == 50.0
        assert receiving_transaction.account.id == receiver.id

    test_transfer_error_data = [
        (
            {},
            {
                'message': "Missing required parameters",
                'status_code': 400
            }
        ),
        (
            {
                'receiverAccount': 'doesnt_matter'
            },
            {
                'message': "Missing 'senderAccount'. Expected 'str' got <class 'NoneType'>",
                'status_code': 404
            }
        ),
        (
            {
                'senderAccount': 12345
            },
            {
                'message': "Missing 'senderAccount'. Expected 'str' got <class 'int'>",
                'status_code': 404
            }
        ),
        (
            {
                'senderAccount': '12345',
            },
            {
                'message': "Missing 'receiverAccount'. Expected 'str' got <class 'NoneType'>",
                'status_code': 404
            }
        ),
        (
            {
                'senderAccount': '12345',
                'receiverAccount': '54321'
            },
            {
                'message': "Missing 'amount'. Expected 'str' got <class 'NoneType'>",
                'status_code': 404
            }
        ),

    ]

    @pytest.mark.parametrize("data,expected", test_transfer_error_data)
    def test_transfer_errors(self, test_client, data, expected):
        response = test_client.post(
            '/api/v1/transfer',
            json=data
        )
        assert response.json == expected

        
class TestOpenAccount():

    test_data = [
        (
            '/api/v1/openAccount',
            {'customerID': '1', 'initialCredit': 50}
        ),
        (
            '/api/v1/openAccount?customerID=1&initialCredit=50',
            None
        )
    ]

    @pytest.mark.parametrize("url,data", test_data)
    def test_open_account(self, test_client, url, data):
        new_customer = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(new_customer)
        db.session.commit()
        c = Customer.query.first()

        response = test_client.post(
            url,
            json=data
        )
        assert response.status_code == 200
        json = response.get_json()
        assert len(str(json['account']['account_number'])) == 20
        assert json['account']['uri'] == '/api/v1/accounts/1'
        assert json['account']['balance'] == 50.0
        assert json['account']['customer_id'] == c.id

        t = Transaction.query.first()
        a = Account.query.first()
        print(t)
        print(a)

        assert a.customer_id == c.id
        assert a.balance == 50.0

        assert t.account_id == a.id
        assert t.amount == a.balance

        assert a.balance == 50.0
        assert a.owner.id == c.id
        assert a.transactions.first() == t

    def test_open_account_zero_initial_credit(self, test_client):
        new_customer = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(new_customer)
        db.session.commit()
        c = Customer.query.first()

        response = test_client.post(
            '/api/v1/openAccount',
            json={
                'customerID': str(c.id),
                'initialCredit': str(0)
            }
        )
        assert response.status_code == 200
        json = response.get_json()
        assert len(str(json['account']['account_number'])) == 20
        assert json['account']['uri'] == '/api/v1/accounts/1'
        assert json['account']['balance'] == 0.0
        assert json['account']['customer_id'] == c.id

        a = Account.query.first()

        assert Transaction.query.all() == []
        assert a.customer_id == c.id
        assert a.balance == 0.0
        assert a.owner.id == c.id
        assert a.transactions.all() == []

    test_error_data = [
        (
            {},
            {
                'message': "Missing required parameters",
                'status_code': 400
            }
        ),
        (
            {
                'initialCredit': 'doesnt_matter'
            },
            {
                'message': "Missing 'customerID'. Expected 'str' got <class 'NoneType'>",
                'status_code': 404
            }
        )
    ]

    @pytest.mark.parametrize("data,expected", test_error_data)
    def test_errors(self, test_client, data, expected):
        response = test_client.post(
            '/api/v1/openAccount',
            json=data
        )
        assert response.json == expected        

    
class TestGetCustomerInfo():

    test_data = [
        (
            '/api/v1/getCustomerInfo',
            {'customerID': '1'}
        ),
        (
            '/api/v1/getCustomerInfo?customerID=1',
            None
        )
    ]

    @pytest.mark.parametrize("url,data", test_data)
    def test_get_customer_info_data(self, test_client, url, data):
        customer = Customer(name="Monty", surname="Python")
        db.session.add(customer)
        db.session.commit()
        c = Customer.query.first()

        account = Account(account_number=1234, balance=100, customer_id=c.id)
        db.session.add(account)
        db.session.commit()
        a = Account.query.first()

        t1 = Transaction(amount=-20, time=datetime(2020, 4, 20, 21), account_id=a.id)
        t2 = Transaction(amount=50, time=datetime(2020, 4, 19, 15), account_id=a.id)
        db.session.add_all([t1, t2])
        db.session.commit()

        response = test_client.get(
            url,
            json=data
        )

        assert response.status_code == 200
        json = response.get_json()
        assert json['customer'] == {
            'name': "Monty",
            'surname': "Python",
            'uri': '/api/v1/customers/1'
        }
        assert json['accounts'] == [
            {
                'uri': '/api/v1/accounts/1',
                'account_number': 1234,
                'balance': 100.0,
                'customer_id': c.id
            }
        ]
        assert json['transactions'] == [
            {
                'amount': -20.0,
                'account_id': 1,
                'time': datetime(2020, 4, 20, 21).isoformat(),
                'uri': '/api/v1/transactions/1'
            },
            {
                'amount': 50.0,
                'account_id': 1,
                'time': datetime(2020, 4, 19, 15).isoformat(),
                'uri': '/api/v1/transactions/2'
            },
        ]

    test_error_data = [
        (
            {},
            {
                'message': "Missing required parameters",
                'status_code': 400
            }
        ),
        (
            {
                'doesntmatter': 'doesnt_matter'
            },
            {
                'message': "Missing 'customerID'. Expected 'str' got <class 'NoneType'>",
                'status_code': 404
            }
        )
    ]

    @pytest.mark.parametrize("data,expected", test_error_data)
    def test_errors(self, test_client, data, expected):
        response = test_client.get(
            '/api/v1/getCustomerInfo',
            json=data
        )
        assert response.json == expected     