from flask_restful import Resource, Api, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    def post(self):
        try:
            data = UserRegister.parser.parse_args()

            if UserModel.find_by_username(data['username']):
                return {"message": "User is already present"}, 400

            newUser = UserModel(**data)
            newUser.insert()

            return {"message": "User registered successfully"}, 201
        except Exception as e:
            return {"message": str(e)}, 500
