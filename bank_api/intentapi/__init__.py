from flask import Blueprint, g, request, abort, current_app
from flask_restful import marshal, fields

import bank_api.api.v1 as bankapi_v1
from bank_api.api.v1.accounts import create_account, account_fields
from bank_api.api.v1.customers import customer_fields
from bank_api.api.v1.transactions import transaction_fields
from bank_api.models import Account, Transaction, Customer, db

intent_api = Blueprint('intent', __name__)

@intent_api.route('/transfer', methods=['POST'])
def transfer():    
    if not request.json:
        abort(400)
    
    # Parse Input
    json = request.get_json()
    if 'senderAccount' not in json or type(json['senderAccount']) != str:
        current_app.logger.info(f"'senderAccount' not found in {json}")
        abort(404)
    if 'receiverAccount' not in json or type(json['receiverAccount']) != str:
        current_app.logger.info(f"'receiverAccount' not found in {json}")
        abort(404)
    if 'amount' not in json or type(json['amount']) != str:
        current_app.logger.info(f"'amount' not found in {json} or type of 'amount' != str: {type(json['amount'])}")        
        abort(404)

    s_an = str(json['senderAccount'])
    r_an = str(json['receiverAccount'])
    amount = float(json['amount'])

    # Retrieve Resources
    s = Account.query.filter_by(account_number=s_an).first()
    if not s:
        current_app.logger.info(f"Couldn't find account with number: {s_an}")
        abort(404)
    r = Account.query.filter_by(account_number=r_an).first()
    if not s:
        current_app.logger.info(f"Couldn't find account with number: {r_an}")
        abort(404)

    # Check sufficient balance
    if s.balance - amount < 0:
        current_app.logger.info(f"Insufficient balance: {s}")
        abort(500)  # Placeholder for more informative response: 'Insufficient Funds'

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
    if not request.json:
        abort(400)
        
    json = request.get_json()
    current_app.logger.info(f"Request received: {json}")
    if 'customerID' not in json or type(json['customerID']) != str:
        current_app.logger.info(f"'customerID' not found in {json}")
        abort(404)
    if 'initialCredit' not in json or type(json['initialCredit']) != str:
        current_app.logger.info(f"'initialCredit' not found in {json}")
        abort(404)

    c_id = json['customerID']
    amount = json['initialCredit']

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
    if not request.json:
        abort(400)

    json = request.get_json()
    current_app.logger.info(f"Request received: {json}")
    if 'customerID' not in json or type(json['customerID']) != str:
        current_app.logger.info(f"'customerID' not found in {json}")
        abort(404)

    c_id = json['customerID']
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
        