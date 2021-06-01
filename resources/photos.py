from datetime import datetime

from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess


def prepare_photos_post_args():
    photos_post_args = reqparse.RequestParser()
    photos_post_args.add_argument('plant_ID', type=int, help='plant_ID is required', required=True)
    photos_post_args.add_argument('photo', type=str, help='photo is required', required=True)
    return photos_post_args


def prepare_photos_put_args():
    photos_put_args = reqparse.RequestParser()
    photos_put_args.add_argument('photo_ID', type=int, help='photo_ID is required', required=True)
    photos_put_args.add_argument('new_description', type=str, help='new_description is required', required=True)
    return photos_put_args


class Photos(Resource, DatabaseAccess):
    post_args = prepare_photos_post_args()
    put_args = prepare_photos_put_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Plants', {'plant_ID': args['plant_ID']})
        if len(query_result) == 0:
            abort(409, message="Plant not found")
        photo_URL = 'photo_URL'
        self.database_connection.insert('Photos', {'plant_ID': args['plant_ID'],
                                                   'photo_URL': photo_URL,
                                                   'number_of_likes': 0,
                                                   'is_published': 'F',
                                                   'publish_date': datetime.now(),
                                                   'description': ''})
        return '', 201

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Photos', {'photo_ID': args['photo_ID']})
        if len(query_result) == 0:
            abort(409, message="Photo not found")
        self.database_connection.update('Photos', {'description': args['new_description']}, {'photo_ID': args['photo_ID']})
        return '', 201
