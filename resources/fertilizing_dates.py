from datetime import datetime

from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess
from select_queries import select_all_fertilizing_dates_from_user


def prepare_fertilizing_dates_post_args():
    fertilizing_dates_post_args = reqparse.RequestParser()
    fertilizing_dates_post_args.add_argument('plant_ID', type=int, help='plant_ID is required', required=True)
    fertilizing_dates_post_args.add_argument('fertilizing_date', type=str, help='fertilizing_date is required', required=True)
    return fertilizing_dates_post_args


def prepare_fertilizing_dates_get_args():
    fertilizing_dates_get_args = reqparse.RequestParser()
    fertilizing_dates_get_args.add_argument('user_ID', type=int, help='user_ID is required', required=True)
    return fertilizing_dates_get_args


def prepare_fertilizing_dates_put_args():
    fertilizing_dates_put_args = reqparse.RequestParser()
    fertilizing_dates_put_args.add_argument('fertilizing_date_ID', type=int, help='fertilizing_date_ID is required',
                                            required=True)
    fertilizing_dates_put_args.add_argument('new_fertilizing_date', type=str, help='new_fertilizing_date is required',
                                            required=True)
    return fertilizing_dates_put_args


class FertilizingDates(Resource, DatabaseAccess):
    post_args = prepare_fertilizing_dates_post_args()
    get_args = prepare_fertilizing_dates_get_args()
    put_args = prepare_fertilizing_dates_put_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Plants', {'plant_ID': args['plant_ID']})
        if len(query_result) == 0:
            abort(409, message="Plant not found")
        self.database_connection.insert('Fertilizing_dates', {'plant_ID': args['plant_ID'], 'fertilizing_date':
                                        datetime.strptime(args['fertilizing_date'], '%d-%m-%Y')})
        return '', 201

    def get(self):
        args = self.get_args.parse_args()
        query_result = select_all_fertilizing_dates_from_user(args['user_ID'])
        if len(query_result) == 0:
            abort(404, message="No fertilizing dates found")
        return query_result, 200

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Fertilizing_dates',
                                                             {'fertilizing_date_ID': args['fertilizing_date_ID']})
        print(query_result)
        if len(query_result) == 0:
            abort(409, message="Fertilizing date not found")
        self.database_connection.update(
            'Fertilizing_dates',
            {'fertilizing_date': datetime.strptime(args['new_fertilizing_date'], '%d-%m-%Y')},
            {'fertilizing_date_ID': args['fertilizing_date_ID']})
        return '', 201
