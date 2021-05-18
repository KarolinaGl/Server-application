import datetime

from database_connection import DatabaseConnection

database_connection = DatabaseConnection('python', 'python123', '127.0.0.1', 1521)


def select_all_watering_dates_from_user(user_ID):
    query = f"""select Plants.plant_ID, Plants.name, Watering_dates.watering_date_ID, Watering_dates.watering_date
                from Plants
                inner join Watering_dates on Watering_dates.plant_ID=Plants.plant_ID
                inner join Users on Users.user_ID=Plants.user_ID
                where Users.user_ID={user_ID}"""

    query_result = database_connection.execute_select_query(query)
    output = dict()

    for row in query_result:
        plant_ID, name, *_ = row
        next_watering_date = database_connection.call_function('get_next_watering_date', datetime.datetime, [plant_ID])
        output[plant_ID] = {'name': name, 'watering_dates': [],
                            'next_watering_date': next_watering_date.strftime('%d-%m-%Y')}

    for row in query_result:
        plant_ID, _, watering_date_ID, watering_date = row
        output[plant_ID]['watering_dates'].append({'watering_date_ID': watering_date_ID,
                                                   'watering_date': watering_date.strftime('%d-%m-%Y')})

    return output


def select_all_fertilizing_dates_from_user(user_ID):
    query = f"""select Plants.plant_ID, Plants.name, Fertilizing_dates.fertilizing_date_ID, Fertilizing_dates.fertilizing_date
                from Plants
                inner join Fertilizing_dates on Fertilizing_dates.plant_ID=Plants.plant_ID
                inner join Users on Users.user_ID=Plants.user_ID
                where Users.user_ID={user_ID}"""

    query_result = database_connection.execute_select_query(query)
    output = dict()

    for row in query_result:
        plant_ID, name, *_ = row
        next_fertilizing_date = database_connection.call_function('get_next_fertilizing_date',
                                                                  datetime.datetime, [plant_ID])
        output[plant_ID] = {'name': name, 'fertilizing_dates': [],
                            'next_fertilizing_date': next_fertilizing_date.strftime('%d-%m-%Y')}

    for row in query_result:
        plant_ID, _, fertilizing_date_ID, fertilizing_date = row
        output[plant_ID]['fertilizing_dates'].append({'fertilizing_date_ID': fertilizing_date_ID,
                                                      'fertilizing_date': fertilizing_date.strftime('%d-%m-%Y')})

    return output