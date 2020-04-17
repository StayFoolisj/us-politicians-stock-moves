from flask_restful import Resource, reqparse
from models.trans import TransactionModel
from models.politician import PoliticianModel


class Transaction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "transaction_type",
            type=str,
            required=True,
            help="Every transaction needs a transaction_type.",
        )
        self.parser.add_argument(
            "first_name",
            type=str,
            location="json",  # https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations
            help="Every transaction needs a first_name.",
        )
        self.parser.add_argument(
            "asset_name",
            type=str,
            required=True,
            location="json",  # https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations
            help="Every transaction needs an asset_name.",
        )
        self.parser.add_argument(
            "last_name",
            type=str,
            location="json",
            help="Every transaction needs a last_name.",
        )
        super(Transaction, self).__init__()

    def get(self, name):
        transaction = TransactionModel.find_by_name(name)
        if transaction:
            return transaction.json()
        return {"message": "Transaction not found"}, 404

    def post(self, name):
        if TransactionModel.find_by_name(name):
            return {"message": f"A transaction with name '{name}' already exists."}, 400

        data = self.parser.parse_args()
        politician = PoliticianModel.find_politician(
            data["first_name"], data["last_name"]
        )
        # If exists
        if politician:
            data["politician_id"] = politician.id

        else:
            politician = PoliticianModel('name', data["first_name"], data["last_name"], 'office')
            politician.save_to_db()
            politician.find_politician(data["first_name"], data["last_name"])
            data["politician_id"] = politician.id

        transaction = TransactionModel(
            data["asset_name"], data["transaction_type"], data["politician_id"]
        )
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

        return {"message": f"Deleted the transaction {transaction}"}

    def put(self, name):
        data = Transaction.parser.parse_args()
        transaction = TransactionModel.find_by_name(name)

        if transaction is None:
            transaction = TransactionModel(name, **data)
        else:
            transaction.price = data["price"]

        transaction.save_to_db()
        return transaction.json()


class TransactionList(Resource):
    def get(self):
        return {"transactions": [x.json() for x in TransactionModel.query.all()]}

