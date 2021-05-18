import datetime

import cx_Oracle


class DatabaseConnection:
    def __init__(self, username, password, ip_address, port_number):
        self._username = username
        self._password = password
        self._ip_address = ip_address
        self._port_number = port_number
        # Data source name is the Oracle Database connection string identifying which database service to connect to
        self._dsn = f"(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST={ip_address})(PORT={port_number})))" \
                    f"(CONNECT_DATA=(SID=XE)))"
        # Establish the database connection
        self._connection = cx_Oracle.connect(username, password, self._dsn, encoding="UTF-8")
        print("Successfully connected to Oracle Database")
        # The cursor is the object that allows statements to be executed and results (if any) fetched
        self._cursor = self._connection.cursor()

    def select_all(self, table_name):
        sql_select = f"SELECT * FROM {table_name}"
        return list(self._cursor.execute(sql_select))

    def select_where(self, table_name, conditions):
        keys = list(conditions.keys())
        values = list(conditions.values())
        parsed_keys = []

        for key in keys:
            parsed_keys.append(key + '=:' + key + '_value')

        select_query = f"SELECT * FROM {table_name} WHERE {' AND '.join(parsed_keys)}"
        return list(self._cursor.execute(select_query, values))

    def execute_select_query(self, select_query):
        return list(self._cursor.execute(select_query))

    def insert(self, table_name, parameters):
        keys = list(parameters.keys())
        values = list(parameters.values())
        parsed_keys = []

        for key in keys:
            parsed_keys.append(':' + key + '_value')

        insert_query = f"INSERT INTO {table_name} ({', '.join(keys)}) VALUES ({', '.join(parsed_keys)})"
        self._cursor.execute(insert_query, values)
        self._connection.commit()

    def update(self, table_name, parameters, conditions):
        parameters_keys = list(parameters.keys())
        parameters_values = list(parameters.values())
        parsed_parameters = []

        for key in parameters_keys:
            parsed_parameters.append(key + '=:' + key + '_value')

        conditions_keys = list(conditions.keys())
        conditions_values = list(conditions.values())
        parsed_conditions = []

        for key in conditions_keys:
            parsed_conditions.append(key + '=:' + key + '_value')

        update_query = f"UPDATE {table_name} SET {', '.join(parsed_parameters)} WHERE {' AND '.join(parsed_conditions)}"
        self._cursor.execute(update_query, parameters_values + conditions_values)
        self._connection.commit()

    def delete(self, table_name, conditions):
        conditions_keys = list(conditions.keys())
        conditions_values = list(conditions.values())
        parsed_conditions = []

        for key in conditions_keys:
            parsed_conditions.append(key + '=:' + key + '_value')

        delete_query = f"DELETE FROM {table_name} WHERE {' AND '.join(parsed_conditions)}"
        self._cursor.execute(delete_query, conditions_values)
        self._connection.commit()

    def call_function(self, function_name, function_return_type, function_arguments):
        return self._cursor.callfunc(function_name, function_return_type, function_arguments)


if __name__ == '__main__':
    database_connection = DatabaseConnection('python', 'python123', '127.0.0.1', 1521)

    # database_connection.insert('Users', {'username': 'Adam', 'password': '123'})
    # database_connection.insert('Users', {'username': 'Magda', 'password': '321'})
    # database_connection.insert('Users', {'username': 'Marek', 'password': 'abc'})
    # database_connection.insert('Users', {'username': 'Ala', 'password': '1234'})

    # database_connection.insert('Plants', {'user_ID': 1, 'name': 'Kaktus', 'species': 'Opuntia', 'watering_frequency': 20,
    #                                       'fertilizing_frequency': 120})
    # database_connection.insert('Plants', {'user_ID': 1, 'name': 'Grubosz', 'species': 'Crassula', 'watering_frequency': 14,
    #                                       'fertilizing_frequency': 80})
    # database_connection.insert('Plants', {'user_ID': 1, 'name': 'Paprotka', 'species': 'Polypodiopsida', 'watering_frequency': 10,
    #                                       'fertilizing_frequency': 60})

    # database_connection.insert('Watering_dates', {'plant_ID': 2, 'watering_date': datetime.datetime(2021, 4, 22)})
    # database_connection.insert('Watering_dates', {'plant_ID': 3, 'watering_date': datetime.datetime(2021, 2, 20)})
    # database_connection.insert('Watering_dates', {'plant_ID': 4, 'watering_date': datetime.datetime(2021, 5, 13)})

    database_connection.update('Watering_dates', {'watering_date': datetime.datetime(2013, 4, 22)}, {'watering_date_ID': 7})
