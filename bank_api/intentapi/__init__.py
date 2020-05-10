from flask import Blueprint, g, request, abort, current_app, url_for
from flask_restful import marshal, fields

import bank_api.api.v1 as bankapi_v1
from bank_api.api.v1.customers import customer_fields
from bank_api.models import Account, Transaction, Customer, db
from bank_api.errors import make_error
from bank_api.utils import create_account

intent_api = Blueprint('intent', __name__)

@intent_api.route('/transfer', methods=['POST'])
def transfer():    
    if not request.json:
        return make_error(400, "Missing required parameters")
    
    # Parse Input
    json = request.get_json()
    if 'senderAccount' not in json or type(json['senderAccount']) != str:
        current_app.logger.info(f"'senderAccount' not found in {json}")
        return make_error(404, f"Missing 'senderAccount'. Expected 'str' got {type(json.get('senderAccount'))}")
    if 'receiverAccount' not in json or type(json['receiverAccount']) != str:
        current_app.logger.info(f"'receiverAccount' not found in {json}")
        return make_error(404, f"Missing 'receiverAccount'. Expected 'str' got {type(json.get('receiverAccount'))}")
    if 'amount' not in json or type(json['amount']) != str:
        current_app.logger.info(f"'amount' not found in {json} or type of 'amount' != str: {type(json.get('amount'))}")
        return make_error(404, f"Missing 'amount'. Expected 'str' got {type(json.get('amount'))}")

    s_an = str(json['senderAccount'])
    r_an = str(json['receiverAccount'])
    amount = float(json['amount'])

    # Retrieve Resources
    s = Account.query.filter_by(account_number=s_an).first()
    if not s:
        return make_error(404, f"Couldn't find account: {s_an}")
    r = Account.query.filter_by(account_number=r_an).first()
    if not r:
        return make_error(404, f"Couldn't find account: {r_an}")

    # Check sufficient balance
    if s.balance - amount < 0:
        return make_error(403, "Insufficient balance")

    # Generate transactions
    s_transaction = Transaction(account_id=s.id, amount=-amount)
    db.session.add(s_transaction)

    r_transaction = Transaction(account_id=r.id, amount=amount)
    db.session.add(r_transaction)

    # Perform operations
    s.balance -= amount
    db.session.add(s)

    r.balance += amount
    db.session.add(r)

    # Commit results
    db.session.commit()

    return {'result': True}

account_fields = {
    'account_number': fields.Integer,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'uri': fields.Url('intent.get_customer_info')
}

@intent_api.route('/openAccount', methods=['POST'])
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


transaction_fields = {
    'amount': fields.Float,
    'account_id': fields.Integer,
    'time': fields.DateTime(dt_format='iso8601'),
}

account_fields_with_transactions = {
    'account_number': fields.Integer,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'transactions': fields.List(fields.Nested(transaction_fields))
}

customer_info_fields = {
    'name': fields.String,
    'surname': fields.String,
    'accounts': fields.List(fields.Nested(account_fields_with_transactions))
}


@intent_api.route('/getCustomerInfo', methods=['GET'])
def get_customer_info():
    current_app.logger.info(f"Request parameters: {request.args}")
    current_app.logger.info(f"Request data: {request.json}")
    if not request.json and not request.args:
        return make_error(400, "Missing required parameters")

    c_id = request.args.get('customerID') or request.json.get('customerID')
    if not c_id or type(c_id) != str:
        return make_error(404, f"Missing 'customerID'. Expected 'str' got {type(c_id)}")

    page = request.args.get('page', 1, type=int)
    
    c = Customer.query.get_or_404(c_id)
    return {'customer': marshal(c, customer_info_fields)}


def get_catelog():
    return {
        'transfer_url': url_for('intent.transfer', _external=True),
        'open_account_url': url_for('intent.open_account', _external=True),
        'get_customer_url': url_for('intent.get_customer_info', _external=True)
    }        