from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
            if store:
                return store.json(), 200
            return {"message": "Store not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def post(self, name):
        try:
            if StoreModel.find_by_name(name):
                return {'message': "A store with name {} is aleardy exists".format(name)}, 400
            return StoreModel(name).save_to_db(), 201
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def delete(self, name):
        try:
            store = StoreModel.find_by_name(name)
            if not store:
                return {'message': "No store with name {} is present in store list.".format(name)}, 400

            store.delete_from_db()
            return {"messsage": "Store deleted successfully"}, 200
        except Exception as e:
            return {"message": str(e)}, 500


class StoreList(Resource):
    @jwt_required()
    def get(self):
        try:
            return {"stores": [store.json() for store in StoreModel.query.all()]}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        except TypeError as te:
            return {"message": str(te)}, 500
