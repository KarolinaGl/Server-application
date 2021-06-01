from datetime import datetime

from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess


def prepare_photos_publish_put_args():
    photos_publish_put_args = reqparse.RequestParser()
    photos_publish_put_args.add_argument('photo_ID', type=int, help='photo_ID is required', required=True)
    photos_publish_put_args.add_argument('description', type=str, help='description is required', required=True)
    return photos_publish_put_args


class PhotosPublished(Resource, DatabaseAccess):
    put_args = prepare_photos_publish_put_args()

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Photos', {'photo_ID': args['photo_ID']})
        if len(query_result) == 0:
            abort(409, message="Photo not found")
        self.database_connection.update('Photos', {'is_published': 'T', 'description': args['description']},
                                        {'photo_ID': args['photo_ID']})
        return '', 201
