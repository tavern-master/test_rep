import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username is missing")
    parser.add_argument('password', type=str, required=True, help="Password is missing")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"A user with that username {data['username']} already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": f"User {data['username']} created successfully"}, 201


