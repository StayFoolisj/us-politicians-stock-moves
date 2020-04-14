"""
TODO
Remember to switch Flask Debug mode OFF in production
TODO
"""
from flask import Flask
from flask_restful import Api

from resources.trans import Transaction, TransactionList
from resources.politician import Politician, PoliticianList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(PoliticianList, '/politicians', endpoint = 'politicians')
api.add_resource(Politician, '/politician/<string:name>', endpoint = 'politician')
api.add_resource(TransactionList, '/transactions', endpoint = 'transactions')
api.add_resource(Transaction, '/transaction/<string:name>', endpoint = 'transaction')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True) # REMOVE IN PRODUCTION