from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess


def prepare_logging_get_args():
    logging_get_args = reqparse.RequestParser()
    logging_get_args.add_argument('username', type=str, help='Username is required', required=True)
    logging_get_args.add_argument('password', type=str, help='Password is required', required=True)
    return logging_get_args


class Logging(Resource, DatabaseAccess):
    get_args = prepare_logging_get_args()

    def get(self):
        args = self.get_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'username': args['username']})
        if len(query_result) == 0:
            abort(404, message="User not found")
        query_result = self.database_connection.select_where('Users', {'username': args['username'],
                                                                       'password': args['password']})
        if len(query_result) == 0:
            abort(404, message="Incorrect password")
        return query_result[0][0]
