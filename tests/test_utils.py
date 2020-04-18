import pytest
from bank_api import utils

class TestGenerateRandomAccountNumber():

    account_nums = {}

    @pytest.mark.parametrize('execution_number', range(100))
    def test_generate_account_number(self, execution_number):
        """Hardcoded in the number of time this test should be executed"""
        account_num = utils.generate_random_account_number()
        assert len(str(account_num)) == 20

