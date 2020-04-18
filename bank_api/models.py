from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True, unique=True)
    balance = db.Column(db.Float, default=0)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return f"<Account {self.account_number}> Balance: {self.balance} Owner: {self.customer_id}"

    def import_data(self, data):
        try:
            self.account_number = data['account_number']
            self.balance = data['balance']
        except KeyError as e:
            raise ValueError('Invalid class - missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'account_number': self.account_number,
            'balance': self.balance
        }

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    accounts = db.relationship('Account', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f"<Customer {self.name} {self.surname}>"

    def import_data(self, data):
        try:
            self.name = data['name']
            self.surname = data['surname']
        except KeyError as e:
            raise ValueError('Invalid class - missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'name': self.name,
            'surname': self.surname
        }