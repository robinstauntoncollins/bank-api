from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models

account_fields = {
    'account_number': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'uri': fields.Url('api.account')
}

class AccountListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account_number', type=int, required=True, location="json")
        self.reqparse.add_argument('name', type=str, default="", location="json")
        self.reqparse.add_argument('surname', type=str, default="", location="json")
        self.reqparse.add_argument('balance', type=float, required=False, location="json")
        self.reqparse.add_argument('customer_id', type=int, required=True, location="json")
        super(AccountListAPI, self).__init__()

    def get(self):
        accounts = models.Account.query.all()
        return {'accounts': [marshal(account, account_fields) for account in accounts]}

    def post(self):
        args = self.reqparse.parse_args()
        account = models.Account.query.filter_by()


class AccountAPI(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass