from flask import Blueprint, g, request, abort, current_app
from flask_restful import marshal, fields

import bank_api.api.v1 as bankapi_v1
from bank_api.api.v1.accounts import create_account, account_fields
from bank_api.api.v1.customers import customer_fields
from bank_api.api.v1.transactions import transaction_fields
from bank_api.models import Account, Transaction, Customer, db
from bank_api.errors import make_error

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
        current_app.logger.info(f"Couldn't find account with number: {s_an}")
        return make_error(404, f"Couldn't find account: {s_an}")
    r = Account.query.filter_by(account_number=r_an).first()
    if not s:
        current_app.logger.info(f"Couldn't find account with number: {r_an}")
        return make_error(404, f"Couldn't find account: {r_an}")

    # Check sufficient balance
    if s.balance - amount < 0:
        current_app.logger.info(f"Insufficient balance: {s}")
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
    a = create_account(c)
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


@intent_api.route('/getCustomerInfo', methods=['GET'])
def get_customer_info():
    current_app.logger.info(f"Request parameters: {request.args}")
    current_app.logger.info(f"Request data: {request.json}")
    if not request.json and not request.args:
        return make_error(400, "Missing required parameters")

    c_id = request.args.get('customerID') or request.json.get('customerID')
    if not c_id or type(c_id) != str:
        return make_error(404, f"Missing 'customerID'. Expected 'str' got {type(c_id)}")

    c = Customer.query.get_or_404(c_id)

    response = {'customer': marshal(c, customer_fields)}

    c_accounts = c.accounts.all()
    response['accounts'] = [marshal(account, account_fields) for account in c_accounts]

    transactions = []
    for account in c_accounts:
        for t in account.transactions.all():
            transactions.append(t)
    response['transactions'] = [marshal(t, transaction_fields) for t in transactions]

    return response
        