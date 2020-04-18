from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models

customer_fields = {
    'name': fields.String,
    'surname': fields.String,
    'uri': fields.Url('api.customer')
}

class CustomerListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, default="", location="json")
        self.reqparse.add_argument('surname', type=str, default="", location="json")
        super(CustomerListAPI, self).__init__()

    def get(self):
        customers = models.Customer.query.all()
        return {'customers': [marshal(customer, customer_fields) for customer in customers]}

    def post(self):
        args = self.reqparse.parse_args()
        customer = models.Customer().import_data(args)
        models.db.session.add(customer)
        models.db.session.commit()
        return {'customer': marshal(customer, customer_fields)}, 201


class CustomerAPI(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass