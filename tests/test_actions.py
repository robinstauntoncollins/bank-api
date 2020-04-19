import os

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

        
class TestOpenAccount():

    def test_open_account(self, test_client):

        new_customer = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(new_customer)
        db.session.commit()
        c = Customer.query.first()

        response = test_client.post(
            '/api/v1/openAccount',
            json={
                'customerID': str(c.id),
                'initialCredit': str(50)
            }
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