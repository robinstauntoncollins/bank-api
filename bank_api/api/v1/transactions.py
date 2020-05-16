from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models


transaction_fields = {
    'amount': fields.Float,
    'account_id': fields.Integer,
    'time': fields.DateTime(dt_format='iso8601'),
    'uri': fields.Url('api.transaction')
}


class TransactionListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account_id', type=int, required=True, location="json")
        self.reqparse.add_argument('amount', type=float, required=True, location="json")
        super(TransactionListAPI, self).__init__()

    def get(self):
        transactions = models.Transaction.query.all()
        return {'transactions': [marshal(transaction, transaction_fields) for transaction in transactions]}

    def post(self):
        args = self.reqparse.parse_args()
        transaction = models.Transaction().import_data(args)
        models.db.session.add(transaction)
        models.db.session.commit()
        return {'transaction': marshal(transaction, transaction_fields)}, 201


class TransactionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account_id', type=int, required=True, location="json")
        self.reqparse.add_argument('amount', type=float, required=False, location="json")
        super(TransactionAPI, self).__init__()

    def get(self, id):
        transaction = models.Transaction.query.get_or_404(id)
        return {'transaction': marshal(transaction, transaction_fields)}
