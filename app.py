from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = "galieye"
api = Api(app)
items = []

jwt = JWT(app,authenticate,identity)
print(jwt)

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True
    )

    @jwt_required()
    def get(self,name):
        # item = list(filter(lambda x: x["name"]==name,items))[0]
        item = next(filter(lambda x: x["name"]==name,items),None)
        return {"item":item}, 200 if item else 404

    @jwt_required()
    def post(self,name):
        if next(filter(lambda x: x["name"]==name,items),None):
            return {'message':"An item with name {} is aleardy exists".format(name)}, 400
        
        request_data = Item.parser.parse_args()
        new_item = {"name":name, "price":request_data["price"]}
        items.append(new_item)
        return new_item ,201
    
    @jwt_required()
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] !=name, items))
        return {'message':"item deleted"}

    @jwt_required()
    def put(self,name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"]==name,items),None)
        if item is None:
            item = {"name":name, "price":request_data["price"]}
            items.append(item)
        else:
            item.update(request_data)

        return item ,201

        
class ItemList(Resource):
    def get(self):
        return {"items":items}

    def post(self):
        # request_data = request.get_json()
        pass

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5004)