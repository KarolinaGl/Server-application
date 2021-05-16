class User:
    @staticmethod
    def get_id(user_row):
        return user_row[0]

    @staticmethod
    def get_username(user_row):
        return user_row[1]

    @staticmethod
    def get_password(user_row):
        return user_row[2]
