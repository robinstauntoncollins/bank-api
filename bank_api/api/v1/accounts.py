from typing import Optional
from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models, utils, errors


account_fields = {
    'account_number': fields.Integer,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'uri': fields.Url('api.account')
}

class AccountListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()        
        self.reqparse.add_argument('customer_id', type=int, required=True, location="json")
        self.reqparse.add_argument('balance', type=float, default=0, required=False, location="json")
        super(AccountListAPI, self).__init__()

    def get(self):
        accounts = models.Account.query.all()
        return {'accounts': [marshal(account, account_fields) for account in accounts]}

    def post(self):
        args = self.reqparse.parse_args()
        customer = models.Customer.query.get_or_404(args['customer_id'])
        account = utils.create_account(customer, args['balance'])
        models.db.session.add(account)
        models.db.session.commit()
        return {'account': marshal(account, account_fields)}, 201
        

class AccountAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()        
        self.reqparse.add_argument('balance', type=float, required=False, location="json")
        super(AccountAPI, self).__init__()

    def get(self, id):
        account = models.Account.query.get_or_404(id)
        return {'account': marshal(account, account_fields)}

    def put(self, id):
        account = models.Account.query.get_or_404(id)
        args = self.reqparse.parse_args()
        account.balance = args['balance']
        models.db.session.add(account)
        models.db.session.commit()
        return {'account': marshal(account, account_fields)}

    def delete(self, id):
        account = models.Account.query.get_or_404(id)
        models.db.session.delete(account)
        models.db.session.commit()
        return {'result': True}