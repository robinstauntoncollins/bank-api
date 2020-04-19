from datetime import datetime
import pytest
from bank_api.models import Account, Customer, Transaction, db


class TestAccountModel():

    def test_basic(self):
        new_account = Account().import_data({
            'account_number': 1,
            'balance': 0,
            'customer_id': 1
        })
        assert new_account.account_number == '1'
        assert new_account.balance == 0
        account_data = new_account.export_data()
        assert account_data == {
            'account_number': 1,
            'balance': 0,
            'customer_id': 1
        }

    def test_invalid_data(self):
        with pytest.raises(ValueError):
            Account().import_data({
                'balance': 0,
                'customer_id': 1
            })

    def test_repr(self, test_client):
        new_account = Account().import_data({
            'account_number': 1,
            'balance': 0,
            'customer_id': 1
        })
        db.session.add(new_account)
        db.session.commit()
        a = Account.query.first()
        assert repr(a) == "<Account ID: 1> Balance: 0.0 Owner ID: 1"

    def test_db(self, test_client):
        new_account = Account().import_data({
            'account_number': '1',
            'balance': 0,
            'customer_id': 1
        })
        db.session.add(new_account)
        db.session.commit()
        account = Account.query.first()
        assert account == new_account

    def test_account_owner(self, test_client):
        customer = Customer(name="Robin", surname="Staunton-Collins")
        db.session.add(customer)
        c = Customer.query.first()
        new_account = Account(account_number=1234, balance=50, owner=c)
        db.session.add(new_account)
        db.session.commit()
        acc = Account.query.first()
        assert acc.owner == c


class TestCustomerModel():

    def test_customer_model_basic(self):
        new_customer = Customer().import_data({
            'name': 'Robin',
            'surname': 'Staunton-Collins'
        })
        assert new_customer.name == 'Robin'
        assert new_customer.surname == 'Staunton-Collins'
        customer_data = new_customer.export_data()
        assert customer_data == {
            'name': 'Robin',
            'surname': 'Staunton-Collins'
        }

    def test_invalid_data(self):
        with pytest.raises(ValueError):
            Customer().import_data({
                'name': 0,
            })

    def test_repr(self, test_client):
        new_customer = Customer().import_data({
            'name': 'Robin',
            'surname': 'Staunton-Collins'
        })
        db.session.add(new_customer)
        db.session.commit()
        c = Customer.query.first()
        assert repr(c) == "<Customer Robin Staunton-Collins>"
    
    def test_customer_model_db(self, test_client):
        new_customer = Customer().import_data({
            'name': 'Robin',
            'surname': 'Staunton-Collins'
        })
        db.session.add(new_customer)
        db.session.commit()
        customer = Customer.query.first()
        assert customer == new_customer

    
    def test_customer_accounts(self, test_client):
        customer = Customer(name="Robin", surname="Staunton-Collins")
        first_account = Account(account_number=1234, balance=50, owner=customer)
        second_account = Account(account_number=2345, balance=14000, owner=customer)
        db.session.add_all([customer, first_account, second_account])
        db.session.commit()
        c = Customer.query.first()
        assert c.accounts.all() == [
            first_account,
            second_account
        ]


class TestTransactionModel():

    def test_basic(self, test_client):
        new_trans = Transaction().import_data({
            'account_id': 1,
            'amount': 50
        })
        db.session.add(new_trans)
        db.session.commit()
        added_trans = Transaction.query.first()
        assert added_trans == new_trans
        transaction_Data = added_trans.export_data()
        assert transaction_Data == {
            'account_id': 1,
            'amount': 50.0
        }

    def test_repr(self, test_client):
        new_trans = Transaction().import_data({
            'account_id': 1,
            'time': datetime(2020, 4, 19, 15),
            'amount': 50
        })
        db.session.add(new_trans)
        db.session.commit()
        t = Transaction.query.first()
        assert repr(t) == "<Transaction - t_id: 1 time: 2020-04-19 15:00:00 account_id: 1 amount: 50.0>"


    def test_transactions_on_account(self, test_client):
        a = Account(account_number='12345', balance=50, customer_id=1)
        db.session.add(a)
        db.session.commit()
        a = Account.query.first()
        t = Transaction(amount=25, account_id=a.id)
        db.session.add(t)
        db.session.commit()
        t = Transaction.query.first()
        a = Account.query.first()
        assert t.account_id == a.id
        assert a.transactions.first() == t