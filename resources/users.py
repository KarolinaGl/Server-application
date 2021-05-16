from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess
from models.user import User


def prepare_users_post_args():
    users_post_args = reqparse.RequestParser()
    users_post_args.add_argument('username', type=str, help='Username is required', required=True)
    users_post_args.add_argument('password', type=str, help='Password is required', required=True)
    return users_post_args


def prepare_users_get_args():
    users_get_args = reqparse.RequestParser()
    users_get_args.add_argument('user_ID', type=int, help='User ID is required', required=True)
    return users_get_args


def prepare_users_put_args():
    users_put_args = reqparse.RequestParser()
    users_put_args.add_argument('user_ID', type=int, help='User ID is required', required=True)
    users_put_args.add_argument('old_password', type=str, help='Old password is required', required=True)
    users_put_args.add_argument('new_password', type=str, help='New password is required', required=True)
    return users_put_args


def prepare_users_delete_args():
    users_delete_args = reqparse.RequestParser()
    users_delete_args.add_argument('user_ID', type=int, help='User ID is required', required=True)
    users_delete_args.add_argument('password', type=str, help='Password is required', required=True)
    return users_delete_args


class Users(Resource, DatabaseAccess):
    post_args = prepare_users_post_args()
    get_args = prepare_users_get_args()
    put_args = prepare_users_put_args()
    delete_args = prepare_users_delete_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'username': args['username']})
        if len(query_result) > 0:
            abort(409, message="Username already exists")
        self.database_connection.insert('Users', {'username': args['username'], 'password': args['password']})
        return '', 201

    def get(self):
        args = self.get_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['user_ID']})
        if len(query_result) == 0:
            abort(404, message="User not found")
        return {'username': User.get_username(query_result[0])}, 200

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['user_ID']})
        if len(query_result) == 0:
            abort(404, message="User not found")
        if args['old_password'] != User.get_password(query_result[0]):
            abort(404, message="Incorrect old password")
        self.database_connection.update('Users', {'password': args['new_password']}, {'user_ID': args['user_ID']})
        return '', 201

    def delete(self):
        args = self.delete_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['user_ID']})
        if len(query_result) == 0:
            abort(404, message="User not found")
        if args['password'] != User.get_password(query_result[0]):
            abort(404, message="Incorrect password")
        self.database_connection.delete('Users', {'user_ID': args['user_ID']})
        return '', 201
