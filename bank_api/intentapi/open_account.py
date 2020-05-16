from flask import request, current_app
from flask_restful import marshal

from bank_api.errors import make_error
from bank_api.models import Customer, Account, Transaction, db
from bank_api.utils import create_account

from . import intent_api_bp
from .common import account_fields


@intent_api_bp.route('/openAccount', methods=['POST'])
def open_account():
    if not request.json and not request.args:
        return make_error(400, "Missing required parameters")

    c_id = request.args.get('customerID') or request.json.get('customerID')
    if not c_id or type(c_id) != str:
        return make_error(404, f"Missing 'customerID'. Expected 'str' got {type(c_id)}")
    amount = request.args.get('initialCredit') or request.json.get('initialCredit')
    if not amount:
        amount = 0

    # Find customer with 'customerID'
    c = Customer.query.get_or_404(c_id)

    # Create new account
    try:
        a = create_account(c)
    except ValueError as v_err:
        return make_error(403, str(v_err))
    db.session.add(a)
    db.session.commit()
    a = Account.query.filter_by(account_number=a.account_number).first()
    current_app.logger.info(f"Account created: {a}")

    # If initialCredit is zero - return response with new account details
    if float(amount) == 0.0:
        return {
            'result': True,
            'account': marshal(a, account_fields)
        }

    # Generate Transaction
    t = Transaction(account_id=a.id, amount=amount)
    db.session.add(t)

    # Update Account Balance
    a.balance = amount
    db.session.add(a)

    # Commit results
    db.session.commit()

    return {
        'result': True,
        'account': marshal(a, account_fields)
    }
