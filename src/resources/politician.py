from flask_restful import Resource
from models.politician import PoliticianModel

class Politician(Resource):


    def get(self, name):
        politician = PoliticianModel.find_by_name(name)
        if politician:
            return politician.json()
        return {'message': 'Politician not found'}, 404


    def post(self, name):
        if PoliticianModel.find_by_name(name):
            return {'message': f'A politician with name {name} already exists'}
        
        store = PoliticianModel(name)

        try:
            store.save_to_db()
        except:
             return {'message': 'An error occurred while registering the politician'}, 500
        
        return store.json(), 201


    def delete(self, name):
        politician = PoliticianModel.find_by_name(name)

        if politician:
            politician.delete_from_db()

        return {'message': f'Deleted the politician {politician}'}


class PoliticianList(Resource):
    def get(self):
        return {'politicians': [x.json() for x in PoliticianModel.query.all()]}