from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models

account_fields = {
    'name': fields.String,
    'surname': fields.String,
    'customer_id': fields.Integer,
    'uri': fields.Url('api.customer')
}

class CustomerListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, default="", location="json")
        self.reqparse.add_argument('surname', type=str, default="", location="json")
        super(AccountListAPI, self).__init__()

    def get(self):
        accounts = models.Account.query.all()
        return {'accounts': [marshal(account, account_fields) for account in accounts]}

    def post(self):
        args = self.reqparse.parse_args()
        account = models.Account.query.filter_by()


class CustomerAPI(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass