import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import cursor

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=os.getenv("PASSWORD"),
            database="sports_booking",
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def execute(self, statement, *values) -> cursor:
        cursor = self.connection.cursor()
        cursor.execute(statement, values or [])
        return cursor


    # # Show bookings
    # query = """
    #     select
    #         room_id,
    #         room_type,
    #         datetime_of_booking,
    #         member_id,
    #         payment_status
    #     from member_bookings
    # """
    #
    # cursor.execute(query)
    # results = cursor.fetchall()


if __name__ == "__main__":
    database_manager = DatabaseManager()
    query = """
        select
            room_id,
            room_type,
            datetime_of_booking,
            member_id,
            payment_status
        from member_bookings
    """
    results = database_manager.execute(query)
    result = results.fetchall()
    print(result)