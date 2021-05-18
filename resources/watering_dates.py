from datetime import datetime

from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess
from select_queries import select_all_watering_dates_from_user


def prepare_watering_dates_post_args():
    watering_dates_post_args = reqparse.RequestParser()
    watering_dates_post_args.add_argument('plant_ID', type=int, help='plant_ID is required', required=True)
    watering_dates_post_args.add_argument('watering_date', type=str, help='watering_date is required', required=True)
    return watering_dates_post_args


def prepare_watering_dates_get_args():
    watering_dates_get_args = reqparse.RequestParser()
    watering_dates_get_args.add_argument('user_ID', type=int, help='user_ID is required', required=True)
    return watering_dates_get_args


def prepare_watering_dates_put_args():
    watering_dates_put_args = reqparse.RequestParser()
    watering_dates_put_args.add_argument('watering_date_ID', type=int, help='watering_date_ID is required', required=True)
    watering_dates_put_args.add_argument('new_watering_date', type=str, help='new_watering_date is required', required=True)
    return watering_dates_put_args


class WateringDates(Resource, DatabaseAccess):
    post_args = prepare_watering_dates_post_args()
    get_args = prepare_watering_dates_get_args()
    put_args = prepare_watering_dates_put_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Plants', {'plant_ID': args['plant_ID']})
        if len(query_result) == 0:
            abort(409, message="Plant not found")
        self.database_connection.insert('Watering_dates', {'plant_ID': args['plant_ID'], 'watering_date':
                                        datetime.strptime(args['watering_date'], '%d-%m-%Y')})
        return '', 201

    def get(self):
        args = self.get_args.parse_args()
        query_result = select_all_watering_dates_from_user(args['user_ID'])
        if len(query_result) == 0:
            abort(404, message="No watering dates found")
        return query_result, 200

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Watering_dates', {'watering_date_ID': args['watering_date_ID']})
        print(query_result)
        if len(query_result) == 0:
            abort(409, message="Watering date not found")
        self.database_connection.update(
            'Watering_dates',
            {'watering_date': datetime.strptime(args['new_watering_date'], '%d-%m-%Y')},
            {'watering_date_ID': args['watering_date_ID']})
        return '', 201
