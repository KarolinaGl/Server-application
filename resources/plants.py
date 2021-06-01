from flask_restful import Resource, abort, reqparse

from database_access import DatabaseAccess


def prepare_plants_post_args():
    plants_post_args = reqparse.RequestParser()
    plants_post_args.add_argument('owner_ID', type=int, help='owner_ID is required', required=True)
    plants_post_args.add_argument('name', type=str, help='name is required', required=True)
    plants_post_args.add_argument('watering_frequency', type=int, help='watering_frequency is required', required=True)
    plants_post_args.add_argument('fertilizing_frequency', type=int, help='fertilizing_frequency is required',
                                  required=True)
    return plants_post_args


def prepare_plants_put_args():
    plants_put_args = reqparse.RequestParser()
    plants_put_args.add_argument('plant_ID', type=int, help='plant_ID is required', required=True)
    plants_put_args.add_argument('new_watering_frequency', type=int, help='', required=False)
    plants_put_args.add_argument('new_fertilizing_frequency', type=int, help='', required=False)
    return plants_put_args


def prepare_plants_delete_args():
    plants_delete_args = reqparse.RequestParser()
    plants_delete_args.add_argument('plant_ID', type=int, help='plant_ID is required', required=True)
    return plants_delete_args


class Plants(Resource, DatabaseAccess):
    post_args = prepare_plants_post_args()
    put_args = prepare_plants_put_args()
    delete_args = prepare_plants_delete_args()

    def post(self):
        args = self.post_args.parse_args()
        query_result = self.database_connection.select_where('Users', {'user_ID': args['owner_ID']})
        if len(query_result) == 0:
            abort(409, message="User not found")
        species = 'species'
        self.database_connection.insert('Plants', {'owner_ID': args['owner_ID'],
                                                   'name': args['name'],
                                                   'species': species,
                                                   'watering_frequency': args['watering_frequency'],
                                                   'fertilizing_frequency': args['fertilizing_frequency']})
        return '', 201

    def put(self):
        args = self.put_args.parse_args()
        query_result = self.database_connection.select_where('Plants', {'plant_ID': args['plant_ID']})
        if len(query_result) == 0:
            abort(409, message="Plant not found")

        if args['new_watering_frequency'] is not None:
            self.database_connection.update('Plants', {'watering_frequency': args['new_watering_frequency']},
                                            {'plant_ID': args['plant_ID']})
        elif args['new_fertilizing_frequency'] is not None:
            self.database_connection.update('Plants', {'fertilizing_frequency': args['new_fertilizing_frequency']},
                                            {'plant_ID': args['plant_ID']})
        else:
            abort(409, message="new_watering_frequency or new_fertilizing_frequency is required")
        return '', 201

    def delete(self):
        args = self.delete_args.parse_args()
        query_result = self.database_connection.select_where('Plants', {'plant_ID': args['plant_ID']})
        if len(query_result) == 0:
            abort(409, message="Plant not found")
        self.database_connection.delete('Plants', {'plant_ID': args['plant_ID']})
        return '', 201
