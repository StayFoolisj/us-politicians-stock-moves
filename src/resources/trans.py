from flask_restful import Resource, reqparse
from models.trans import TransactionModel
from models.politician import PoliticianModel
from pprint import pprint

class Transaction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations
        # DOCUMENT PROPERTIES
        # POLITICIAN PROPERTIES
        self.parser.add_argument(
            "first_name",
            location="json",
            help="Every transaction needs a first_name.",
        )
        self.parser.add_argument(
            "last_name",
            location="json",
            help="Every transaction needs a last_name.",
        )
        self.parser.add_argument(
            "office",
            location="json",
            help="Every transaction needs an office.",
        )
        # TRANSACTION PROPERTIES
        self.parser.add_argument(
            "asset_name",
            required=True,
            location="json",  
            help="Every transaction needs an asset_name.",
        )
        self.parser.add_argument(
            "asset_type",
            required=True,
            help="Every transaction needs a asset_type.",
        )
        self.parser.add_argument(
            "ticker",
            required=False,
        )
        self.parser.add_argument(
            "owner",
            required=True,
            help="Every transaction needs an owner.",
        )
        self.parser.add_argument(
            "transaction_type",
            required=True,
            help="Every transaction needs a transaction_type.",
        )
        self.parser.add_argument( # CHANGE TO DATETIME
            "transaction_date", # CHANGE TO DATETIME
            required=True, # CHANGE TO DATETIME
            help="Every transaction needs a transaction_date.", # CHANGE TO DATETIME
        )
        self.parser.add_argument(
            "amount",
            required=True,
            help="Every transaction needs a amount.",
        )
        self.parser.add_argument(
            "comment",
            required=False,
        )
        self.parser.add_argument("document_id")
        self.parser.add_argument("document_url")
        self.parser.add_argument("document_type")
        self.parser.add_argument("filing_date")
        
        super(Transaction, self).__init__()

    def get(self, transaction_id):
        transaction = TransactionModel.find_transaction(transaction_id)
        if transaction:
            return transaction.json()
        return {"message": "Transaction not found"}, 404

    def post(self, transaction_id):
        """
        We POST new transactions without knowledge of the unique politician_id. Only first_name and last_name. 
        For this reason, we first query our db for the politician. If not found, we create the politician first
        """
        print(transaction_id)
        if TransactionModel.find_transaction(transaction_id):
            return {"message": f"A transaction with name '{transaction_id}' already exists."}, 400

        data = self.parser.parse_args()

        politician = PoliticianModel.find_politician(
            data["first_name"], data["last_name"]
        )

        # If politician already exists, we simply get their politician_id from the db
        if politician:
            data["politician_id"] = politician.id

        # If not found, we create, save to db and get their politician_id
        else:
            politician = PoliticianModel(
                data["first_name"], data["last_name"], data["office"]
            )

            politician.save_to_db()
            politician.find_politician(data["first_name"], data["last_name"])

            data["politician_id"] = politician.id

        del(data['first_name'])
        del(data['last_name'])
        del(data['office'])
        pprint(data)

        transaction = TransactionModel(transaction_id, **data)
 
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
        """
        This needs an update. What use is a put
        """
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
