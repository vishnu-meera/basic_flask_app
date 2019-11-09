from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required

class ServerShutDown(Resource):
    @jwt_required()
    def post(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'
