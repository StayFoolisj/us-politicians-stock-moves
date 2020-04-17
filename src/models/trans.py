import sqlite3

from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(70))

    asset_name = db.Column(db.String(320))
    asset_type = db.Column(db.String(70))
    ticker = db.Column(db.String(10))
    owner = db.Column(db.String(20))

    transaction_type = db.Column(db.String(20))
    transaction_date = db.Column(db.String(20))
    amount = db.Column(db.String(35))
    comment = db.Column(db.String(1200))

    politician_id = db.Column(db.Integer, db.ForeignKey("politicians.id"))
    politician = db.relationship("PoliticianModel")

    def __init__(
        self,
        transaction_id,
        asset_name,
        asset_type,
        ticker,
        owner,
        transaction_type,
        transaction_date,
        amount,
        comment,
        politician_id,
    ):

        self.asset_name = asset_name
        self.asset_type = asset_type
        self.ticker = ticker
        self.owner = owner
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date  # CHANGE TO DATETIME
        self.amount = amount
        self.comment = comment

        self.politician_id = politician_id

    def json(self):
        return {
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "ticker": self.ticker,
            "owner": self.owner,
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "transaction_date": self.transaction_date,
            "amount": self.amount,
            "comment": self.comment,
            "politician_id": self.politician_id,
        }

    @classmethod
    def find_transaction(cls, transaction_id):
        return cls.query.filter_by(transaction_id=transaction_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
