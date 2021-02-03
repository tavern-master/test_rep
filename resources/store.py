from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Field store name is empty!")

    @jwt_required()
    def get(self, name):
        store = Store.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Store.parser.parse_args()
        # force = True send data without headers
        # sielense = True - return None without any errors

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occured"}, 500 #Internal server error

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

    def put(self, name):

        data = Store.parser.parse_args()

        item = StoreModel.find_by_name(name)

        if item is None:
            item = StoreModel(name)
        else:
            item.name = data['name']

        item.save_to_db()

        return item.json()


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'store': list(map(lambda x: x.json(), StoreModel.query.all()))}
    #   return {'item': [item.json() for item in ItemModel.query.all()]} is better
