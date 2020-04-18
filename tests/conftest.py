import pytest

from bank_api import create_app
from bank_api.models import Account, db

@pytest.fixture()
def test_accounts():
    test_account_data = [
        {
            'account_id': 1,
            'name': 'Robin',
            'surname': 'Staunton-Collins',
            'balance': 50,
            'owner_id': 1
        },
        {
            'account_id': 2,
            'name': 'Matin',
            'surname': 'Abbasi',
            'balance': 200,
            'owner_id': 2
        },
        {
            'account_id': 3,
            'name': 'Robin',
            'surname': 'Staunton-Collins',
            'balance': 130,
            'owner_id': 1
        },
        {
            'account_id': 4,
            'name': 'Rodrigo',
            'surname': 'Hammerly',
            'balance': 450,
            'owner_id': 3
        },
    ]
    return [Account(
                name=acc['name'],
                surname=acc['surname'],
                balance=acc['balance'],
                owner_id=acc['owner_id']) for acc in test_account_data]

@pytest.fixture()
def test_client(test_accounts):
    app = create_app('testing')

    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        db.drop_all()
        db.create_all()

        for acc in test_accounts:
            db.session.add(acc)
        db.session.commit()
   
        yield client
        db.drop_all()
        ctx.pop()