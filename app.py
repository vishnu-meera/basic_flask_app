from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required, timedelta
from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.shutdown import ServerShutDown

from resources.store import Store, StoreList


app = Flask(__name__)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = "galieye"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app)

jwt = JWT(app, authenticate, identity_function)
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'userd_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(ServerShutDown, '/shutdown')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5004, debug=True)
