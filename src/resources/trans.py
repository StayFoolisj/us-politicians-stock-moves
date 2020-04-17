from flask_restful import Resource, reqparse
from models.trans import TransactionModel
from models.politician import PoliticianModel


class Transaction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('transaction_type',
                            type=str,
                            required=True,
                            help="Every transaction needs a transaction_type."
                            )
        self.parser.add_argument('politician_id',
                            type=int,
                            required=True,
                            help="Every transaction needs a politician_id."
                            )
        super(Transaction, self).__init__()

    def get(self, name): 
        transaction = TransactionModel.find_by_name(name)
        if transaction:
            return transaction.json()
        return {'message': 'Transaction not found'}, 404

    def post(self, name):
        if TransactionModel.find_by_name(name):
            return {'message': f"A transaction with name '{name}' already exists."}, 400

        data = self.parser.parse_args()

        transaction = TransactionModel(name, **data)
        print(transaction)

        try:
            transaction.save_to_db()
        except:
            return {"message": "An error occurred inserting the transaction."}, 500

        return transaction.json(), 201

    def delete(self, name):
        transaction = TransactionModel.find_by_name(name)
        if transaction:
            transaction.delete_from_db()

        return {'message': f'Deleted the transaction {transaction}'}

    def put(self, name):
        data = Transaction.parser.parse_args()
        transaction = TransactionModel.find_by_name(name)

        if transaction is None:
            transaction = TransactionModel(name, **data)
        else:
            transaction.price = data['price']

        transaction.save_to_db()
        return transaction.json()


class TransactionList(Resource):
    def get(self):
        return {'transactions': [x.json() for x in TransactionModel.query.all()]}