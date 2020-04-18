
from bank_api.models import Account, Customer, db


class TestAccountModel():

    def test_account_model_basic(self):
        new_account = Account().import_data({
            'account_number': 1,
            'balance': 0,
        })
        assert new_account.account_number == 1
        assert new_account.balance == 0
        account_data = new_account.export_data()
        assert account_data == {
            'account_number': 1,
            'balance': 0,
        }

    def test_account_model_db(self, test_client):
        new_account = Account().import_data({
            'account_number': 1,
            'balance': 0,
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
