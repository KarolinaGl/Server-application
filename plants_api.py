from flask import Flask
from flask_restful import Api

from database_access import DatabaseAccess
from database_connection import DatabaseConnection
from resources.users import Users
from resources.watering_dates import WateringDates


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    database_connection = DatabaseConnection('python', 'python123', '127.0.0.1', 1521)
    DatabaseAccess.database_connection = database_connection

    api.add_resource(Users, '/users')
    api.add_resource(WateringDates, '/watering_dates')

    app.run(debug=True)
