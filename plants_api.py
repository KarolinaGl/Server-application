from flask import Flask
from flask_restful import Api

from database_access import DatabaseAccess
from database_connection import DatabaseConnection
from resources.fertilizing_dates import FertilizingDates
from resources.liking_users import LikingUsers
from resources.logging import Logging
from resources.photos import Photos
from resources.photos_publish import PhotosPublished
from resources.plants import Plants
from resources.users import Users
from resources.watering_dates import WateringDates


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    database_connection = DatabaseConnection('python', 'python123', '127.0.0.1', 1521)
    DatabaseAccess.database_connection = database_connection

    api.add_resource(Users, '/users')
    api.add_resource(WateringDates, '/watering_dates')
    api.add_resource(FertilizingDates, '/fertilizing_dates')
    api.add_resource(Plants, '/plants')
    api.add_resource(Photos, '/photos')
    api.add_resource(PhotosPublished, '/photos_publish')
    api.add_resource(LikingUsers, '/liking_users')
    api.add_resource(Logging, '/logging')

    app.run(debug=True)
