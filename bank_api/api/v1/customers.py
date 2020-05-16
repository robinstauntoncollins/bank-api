from flask_restful import Resource, reqparse, fields, marshal
from bank_api import models, db
from bank_api.errors import make_error

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

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, default="", location="json")
        self.reqparse.add_argument('surname', type=str, default="", location="json")
        super(CustomerAPI, self).__init__()

    def get(self, id):
        c = models.Customer.query.get(id)
        if not c:
            return make_error(404, f"No customer with id: {id}")
        return {'customer': marshal(c, customer_fields)}

    def put(self, id):
        c = models.Customer.query.get_or_404(id)
        args = self.reqparse.parse_args()
        if 'name' in args:
            c.name = args['name']
        if 'surname' in args:
            c.surname = args['surname']
        db.session.add(c)
        db.session.commit()
        return {'customer': marshal(c, customer_fields)}

    def delete(self, id):
        c = models.Customer.query.get_or_404(id)
        db.session.delete(c)
        db.session.commit()
        return {'result': True}
