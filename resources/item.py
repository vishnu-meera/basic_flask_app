from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="The price field is essential")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Item needs a store id.")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                return item.json(), 200
            return {"message": "Item not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def post(self, name):
        try:
            if ItemModel.find_by_name(name):
                return {'message': "An item with name {} is aleardy exists".format(name)}, 400

            data = Item.parser.parse_args()
            newItem = ItemModel(name, **data)
            result = newItem.save_to_db()
            return result, 201
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if not item:
                return {'message': "No item with name {} is present in items.".format(name)}, 400

            item.delete_from_db()
            return {"messsage": "Item deleted successfully"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def put(self, name):
        try:
            data = Item.parser.parse_args()
            item = ItemModel.find_by_name(name)
            if not item:
                item = ItemModel(name, **data)
            else:
                item.price = data['price']
                item.store_id = data['store_id']

            result = item.save_to_db()
            return result, 200
        except Exception as e:
            return {"message": str(e)}, 500


class ItemList(Resource):
    @jwt_required()
    def get(self):
        try:
            return {"items": [item.json() for item in ItemModel.query.all()]}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        except TypeError as te:
            return {"message": str(te)}, 500
