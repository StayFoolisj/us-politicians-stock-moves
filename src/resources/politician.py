from flask_restful import Resource, reqparse
from models.politician import PoliticianModel

class Politician(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name',
                            required=True,
                            location = 'json', #https://flask-restful.readthedocs.io/en/latest/reqparse.html#argument-locations
                            help="Every transaction needs a first_name."
                            )
        self.parser.add_argument('last_name',
                            required=True,
                            location = 'json',
                            help="Every politician needs a last_name."
                            )
        self.parser.add_argument('office',
                            location = 'json',
                            help="Every politician needs an office."
                            )
        super(Politician, self).__init__()


    def get(self, id):
        data = self.parser.parse_args()

        politician = PoliticianModel.find_politician(data['first_name'], data['last_name'])
        if politician:
            return politician.json()
        return {'message': 'Politician not found'}, 404


    def post(self, id): # Try removing id completely
        data = self.parser.parse_args()

        if PoliticianModel.find_politician(data['first_name'], data['last_name']):
            return {'message': f'A politician with that name already exists!'}
        
        politician = PoliticianModel(id, **data)

        try:
            politician.save_to_db()
        except:
             return {'message': 'An error occurred while registering the politician'}, 500
        
        return politician.json(), 201


    def delete(self, id):
        """
        Adopt the similar logic from post() above after testing passes
        """
        politician = PoliticianModel.find_by_id(id)

        if politician:
            politician.delete_from_db()

        return {'message': f'Deleted the politician {politician}'}


class PoliticianList(Resource):
    def get(self):
        return {'politicians': [politician.json() for politician in PoliticianModel.query.all()]}