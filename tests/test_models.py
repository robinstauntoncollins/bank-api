
from bank_api.models import Account

def test_account_model():
    new_account = Account().import_data({
        'name': 'Robin',
        'surname': 'Staunton-Collins',
        'balance': 0,
        'owner_id': 1
    })
    assert new_account.name == "Robin"
    assert new_account.surname == "Staunton-Collins"
    assert new_account.balance == 0
    assert new_account.owner_id == 1
    account_data = new_account.export_data()
    assert account_data == {
        'name': 'Robin',
        'surname': 'Staunton-Collins',
        'balance': 0,
        'owner_id': 1
    }