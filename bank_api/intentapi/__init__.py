from flask import url_for, Blueprint

intent_api_bp = Blueprint('intent', __name__)

from . import transfer, open_account, get_customer_info


def get_catelog():
    return {
        'transfer_url': url_for('intent.transfer', _external=True),
        'open_account_url': url_for('intent.open_account', _external=True),
        'get_customer_url': url_for('intent.get_customer_info', _external=True)
    }
