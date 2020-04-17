import sqlite3

from db import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)

    asset_name = db.Column(db.String(320))
    transaction_type = db.Column(db.String(20))

    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'))
    politician = db.relationship('PoliticianModel')

    def __init__(self, asset_name, transaction_type, politician_id):

        self.asset_name = asset_name
        self.transaction_type = transaction_type
        self.politician_id = politician_id

    def json(self):
        return {
            'asset_name': self.asset_name,
            'transaction_type': self.transaction_type,
            'politician_id': self.politician_id
        }

    @classmethod
    def find_by_name(cls, asset_name):
        # SELECT * FROM items WHERE name=name
        return TransactionModel.query.filter_by(asset_name=asset_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


"""
class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)

    asset_name = db.Column(db.String(320))
    transaction_type = db.Column(db.String(20))

    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'))
    politician = db.relationship('PoliticianModel')

    def __init__(self, asset_name, transaction_type, politician_id):
        self.asset_name = asset_name
        self.transaction_type = transaction_type
        self.politician_id = politician_id
"""

"""
class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)

    #transaction_id = db.Column(db.String(50))
    asset_name = db.Column(db.String(320))
    #ticker = db.Column(db.String(10))
    #asset_type = db.Column(db.String(70))

    transaction_type = db.Column(db.String(20))
    #transaction_date = db.Column(db.Date())
    #amount = db.Column(db.String(35))
    #owner = db.Column(db.String(20))
    #comment = db.Column(db.String(1200))

    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'))
    politician = db.relationship('PoliticianModel')

#    def __init__(self, asset_name, ticker, asset_type, transaction_type, transaction_date, transaction_id, amount, owner, comment, politician_id):
    def __init__(self, asset_name, transaction_type, politician_id):

        self.asset_name = asset_name
        #self.ticker = ticker
        #self.asset_type = asset_type
        self.transaction_type = transaction_type
        #self.transaction_date = transaction_date
        #self.transaction_id = transaction_id
        #self.amount = amount
        #self.owner = owner
        #self.comment = comment

        self.politician_id = politician_id

    def json(self):
        return {
            'asset_name': self.asset_name,
            #'ticker': self.ticker,
            #'asset_type': self.asset_type,
            'transaction_type': self.transaction_type,
            #'transaction_date': self.transaction_date,
            #'amount': self.amount,
            #'owner': self.owner,
            #'comment': self.comment,
            'politician_id': self.politician_id
        }
"""