import pytest
from bank_api import utils

class TestGenerateRandomAccountNumber():

    def test_generate_account_number(self):
        account_num = utils.generate_random_account_number()
        assert len(account_num) == 20
        assert type(account_num) == str

