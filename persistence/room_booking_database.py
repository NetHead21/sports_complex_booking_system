from datetime import date, time

import mysql
from mysql.connector.cursor_cext import CMySQLCursor

from persistence import DatabaseManager


class RoomBookingDatabase:
    def __init__(self):
        self.db = DatabaseManager()

    def show_bookings(self) -> CMySQLCursor:
        """
        Show all booking records from the booking table
        It will retrieve the room_id, room_type, date_of_booking
        member_id of the member who booked the room and the payment
        status either paid or unpaid

        :return: CMySQLCursor Select Results
        """
        query = """
            select
                room_id,
                room_type,
                datetime_of_booking,
                member_id,
                payment_status
            from member_bookings
        """
        results = self.db.execute(query)
        return results.fetchall()

    # table = PrettyTable()
    # field_names: list[str] = [
    #     "Room_ID",
    #     "Room_Type",
    #     "Date and Time",
    #     "Booked_By",
    #     "Status"
    # ]
    #
    # table.field_names = field_names
    #
    #
    # for result in results:
    #     table.add_row(list(result))
    #
    # table.align = "l"
    # print(table)

    def search_room(
        self, room_type: str, book_date: date, book_time: time
    ) -> CMySQLCursor:
        """
        Search for an available sports complex room
        :param room_type: str, the room_id to book
        :param book_date: date, the date of booking
        :param book_time: time, the time of booking
        :return:
        """

        query = """
            call search_room(%s, %s, %s)
        """

        results = self.db.execute(query, room_type, book_date, book_time)
        return results.fetchall()

    #
    # if results:
    #     table = PrettyTable()
    #     field_names: list[str] = [
    #         "Id",
    #         "Room_Type",
    #         "Price"
    #     ]
    #
    #     table.field_names = field_names
    #
    #
    #     for result in results:
    #         table.add_row(list(result))
    #
    #     table.align = "l"
    #     print(table)
    # else:
    #     print("No results found, try another date and time.")

    def book_room(
        self, room_id: str, book_date: date, book_time: time, user_id: str
    ) -> None:
        """
        Book Room or sports complex room
        :param room_id: str, the room_id to book
        :param book_date: date, what is the date of booking
        :param book_time: time, what is the time of booking
        :param user_id: str, what user_id book the room
        :return: None
        """

        query = """
            call make_booking(%s, %s, %s, %s)
        """

        try:
            self.db.execute(query, room_id, book_date, book_time, user_id)
            self.db.connection.commit()
            print("Room booked successfully!")
        except mysql.connector.Error as err:
            print(err)

    def cancel_booking(self, booking_id: int) -> None:
        """
        Cancel Booking

        :param booking_id: int, the booking id to cancel booking
        :return: None
        """

        cancel_booking_query = f"""
            call cancel_booking({booking_id}, @message);
        """
        sql_message_query = """
            select @message;
        """

        try:
            self.db.execute(cancel_booking_query)
            message = self.db.execute(sql_message_query)
            message = message.fetchone()
            print(message)
            self.db.connection.commit()
        except mysql.connector.Error as err:
            print(err)


if __name__ == "__main__":
    room_booking = RoomBookingDatabase()
    # print(room_booking.show_bookings())

    # booking_date = date(2018, 4, 15)
    # booking_time = time(14, 0)
    # print(room_booking.search_room("Badminton Court", booking_date, booking_time))

    # booking_date = date(2018, 4, 15)
    # booking_time = time(14, 0, 0)
    #
    # room_data = {
    #     "room_type": "Archery Range",
    #     "book_date": booking_date,
    #     "book_time": booking_time,
    # }
    #
    # room = SearchRoom(**room_data)
    # print(room_booking.search_room(room.room_type, room.book_date, room.book_time))

    # room_type = "AR"
    # book_date = date(2024, 11, 25)
    # book_time = time(13, 0, 0)
    # user_id = "NetHead21"
    # room_booking.book_room(room_type, book_date, book_time, user_id)

    # room_booking.cancel_booking(19)
