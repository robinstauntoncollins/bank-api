import pytest
from bank_api import utils, models, errors

class TestGenerateRandomAccountNumber():

    def test_generate_account_number(self):
        account_num = utils.generate_random_account_number()
        assert len(account_num) == 20
        assert type(account_num) == str


class TestCreateAccount():

    def test_create_account(self, test_client, mock_get_account_number):
        c = models.Customer(name="Robin", surname="Staunton-Collins")
        models.db.session.add(c)
        models.db.session.commit()

        result = utils.create_account(c, 50)
        assert result.export_data() == models.Account(
            account_number='0123456789',
            balance=50,
            customer_id=c.id
        ).export_data()
        assert mock_get_account_number.called_once()

    def test_create_account_collision(self, test_client, mock_get_account_number):
        c = models.Customer(name="Robin", surname="Staunton-Collins")
        a = models.Account(
            account_number='0123456789',
            balance=50,
            customer_id=c.id
        )
        models.db.session.add(a)
        models.db.session.commit()

        with pytest.raises(ValueError):
            utils.create_account(c, 50)


