from flask import Blueprint, g
from flask_restful import Api


API_VERSION_V1 = 1


api_v1_bp = Blueprint('api', __name__)
api = Api(api_v1_bp)


from . import accounts
api.add_resource(accounts.AccountListAPI, '/accounts', '/accounts/', endpoint='accounts')
api.add_resource(accounts.AccountAPI, '/accounts/<int:id>', '/accounts/<int:id>/', endpoint='account')


def get_catelog():
    return {
        'accounts_url': api.url_for(accounts.AccountListAPI, _external=True)
    }