import sqlite3

from db import db


class PoliticianModel(db.Model):
    __tablename__ = "politicians"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    last_name = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    office = db.Column(db.String(30))

    transactions = db.relationship("TransactionModel", lazy="dynamic")

    def __init__(self, name, first_name, last_name, office):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.office = office

    def json(self):
        return {
            "name": self.name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "office": self.office,
            "transactions": [
                transaction.json() for transaction in self.transactions.all()
            ],
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM items WHERE name=name

    def find_id_by_name(cls, first_name, last_name):
        query = cls.query.filter_by(last_name=last_name).filter_by(first_name=first_name).first()
        print(query.id)
    
    @classmethod
    def find_politician(cls, first_name, last_name):
        return cls.query.filter_by(last_name=last_name).filter_by(first_name=first_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
