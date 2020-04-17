from flask_restful import Resource, reqparse
from models.politician import PoliticianModel

class Politician(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name',
                            type=str,
                            required=True,
                            location = 'json', #https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations
                            help="Every transaction needs a first_name."
                            )
        self.parser.add_argument('last_name',
                            type=str,
                            required=True,
                            location = 'json',
                            help="Every politician needs a last_name."
                            )
        self.parser.add_argument('office',
                            type=str,
                            required=True,
                            location = 'json',
                            help="Every politician needs an office."
                            )
        super(Politician, self).__init__()


    def get(self, name):
        politician = PoliticianModel.find_by_name(name)
        if politician:
            return politician.json()
        return {'message': 'Politician not found'}, 404


    def post(self, name):
        if PoliticianModel.find_by_name(name):
            return {'message': f'A politician with name {name} already exists'}
        
        data = self.parser.parse_args()
        politician = PoliticianModel(name, **data)

        try:
            politician.save_to_db()
        except:
             return {'message': 'An error occurred while registering the politician'}, 500
        
        return politician.json(), 201


    def delete(self, name):
        politician = PoliticianModel.find_by_name(name)

        if politician:
            politician.delete_from_db()

        return {'message': f'Deleted the politician {politician}'}


class PoliticianList(Resource):
    def get(self):
        return {'politicians': [politician.json() for politician in PoliticianModel.query.all()]}