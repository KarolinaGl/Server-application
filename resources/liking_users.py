from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess


def prepare_liking_users_post_args():
    liking_users_post_args = reqparse.RequestParser()
    liking_users_post_args.add_argument('user_ID', type=int, help='user_ID is required', required=True)
    liking_users_post_args.add_argument('photo_ID', type=int, help='photo_ID is required', required=True)
    return liking_users_post_args


def prepare_liking_users_delete_args():
    liking_users_delete_args = reqparse.RequestParser()
    liking_users_delete_args.add_argument('user_ID', type=int, help='user_ID is required', required=True)
    liking_users_delete_args.add_argument('photo_ID', type=int, help='photo_ID is required', required=True)
    return liking_users_delete_args


class LikingUsers(Resource, DatabaseAccess):
    post_args = prepare_liking_users_post_args()
    delete_args = prepare_liking_users_delete_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['user_ID']})
        if len(query_result) == 0:
            abort(409, message="User not found")
        query_result = self.database_connection.select_where('Photos', {'photo_ID': args['photo_ID']})
        if len(query_result) == 0:
            abort(409, message="Photo not found")
        self.database_connection.insert('Liking_users', {'user_ID': args['user_ID'],
                                                         'photo_ID': args['photo_ID']})
        return '', 201

    def delete(self):
        args = self.delete_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['user_ID']})
        if len(query_result) == 0:
            abort(409, message="User not found")
        query_result = self.database_connection.select_where('Photos', {'photo_ID': args['photo_ID']})
        if len(query_result) == 0:
            abort(409, message="Photo not found")
        self.database_connection.delete('Liking_users', {'user_ID': args['user_ID'],
                                                         'photo_ID': args['photo_ID']})
        return '', 201
