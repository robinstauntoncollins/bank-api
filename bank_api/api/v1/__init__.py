from flask import Blueprint
from flask_restful import Api


API_VERSION_V1 = 1


api_v1_bp = Blueprint('api', __name__)
api = Api(api_v1_bp)

from . import accounts, customers, transactions
api.add_resource(accounts.AccountListAPI, '/accounts', '/accounts/', endpoint='accounts')
api.add_resource(accounts.AccountAPI, '/accounts/<int:id>', '/accounts/<int:id>/', endpoint='account')

api.add_resource(customers.CustomerListAPI, '/customers', '/customers/', endpoint='customers')
api.add_resource(customers.CustomerAPI, '/customers/<int:id>', '/customers/<int:id>', endpoint='customer')

api.add_resource(transactions.TransactionListAPI, '/transactions', '/transactions/', endpoint='transactions')
api.add_resource(
    transactions.TransactionAPI,
    '/transactions/<int:id>',
    '/transactions/<int:id>',
    endpoint='transaction'
)


def get_catelog():
    return {
        'accounts_url': api.url_for(accounts.AccountListAPI, _external=True),
        'customers_url': api.url_for(customers.CustomerListAPI, _external=True),
        'transactions_url': api.url_for(transactions.TransactionListAPI, _external=True)
    }
