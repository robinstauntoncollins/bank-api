from flask import current_app


def test_app_exists(test_client):
    assert current_app is not None


def test_app_is_testing(test_client):
    assert current_app.config['TESTING'] is True


def test_index(test_client):
    response = test_client.get('/')
    assert response.json == {
        'version': {
            'v1': {
                'collections': {
                    'accounts_url': 'http://localhost/api/v1/accounts',
                    'customers_url': 'http://localhost/api/v1/customers',
                    'transactions_url': 'http://localhost/api/v1/transactions'
                },
                'actions': {
                    'transfer_url': 'http://localhost/api/v1/transfer',
                    'open_account_url': 'http://localhost/api/v1/openAccount',
                    'get_customer_url': 'http://localhost/api/v1/getCustomerInfo'
                }
            }
        }
    }
