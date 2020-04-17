from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, index=True)
    balance = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<Account> {self.balance} {self.name} {self.surname}"

    def import_data(self, data):
        try:
            self.name = data['name']
            self.surname = data['surname']
            self.owner_id = data['owner_id']
            self.balance = data['balance']
        except KeyError as e:
            raise ValueError('Invalid class - missing ' + e.args[0])
        return self

    def export_data(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'owner_id': self.owner_id,
            'balance': self.balance
        }