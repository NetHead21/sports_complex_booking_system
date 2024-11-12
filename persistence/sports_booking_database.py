from datetime import date, time

import mysql
from mysql.connector.cursor_cext import CMySQLCursor

from persistence import DatabaseManager, Member


class SportsBookingDatabase:
    def __init__(self):
        self.db = DatabaseManager()

    def show_bookings(self) -> CMySQLCursor:
        """
        # Show bookings
        query = '''
            select
                room_id,
                room_type,
                datetime_of_booking,
                member_id,
                payment_status
            from member_bookings
        '''

        cursor.execute(query)
        results = cursor.fetchall()

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

    def create_new_member(self, member: Member) -> None:
        """
        Original pure MySQL and Python code

        create new member
        user = {
            "id": "PrinceElle",
            "password": "HelloWorld21",
            "email": "princesaavedragmail.com"
        }

        member1 = Member(**user)

        query = '''
            call insert_new_member(%s, %s, %s)
        '''

        cursor.execute(query, (member1.id, member1.password, member1.email))
        conn.commit()

        :param member: Member Class Object
        :return: None
        """

        query = """
            class insert_new_member(%s, %s, %s)
        """
        self.db.execute(query, member.id, member.password, member.email)
        self.db.connection.commit()

    def delete_member(self, member_id: int) -> None:
        """
        Deleting a member
        member_id = "marvin1"
        query = '''
            call delete_member(%s)
        '''
        cursor.execute(query, (member_id))
        conn.commit()

        :param member_id: int
        :return: None
        """

        try:
            query = """
                call delete_member(%s)
            """
            self.db.execute(query, (member_id,))
            self.db.connection.commit()
        except Exception:
            print(f"Member with ID {member_id} does not exist.")

    def update_member_password(self, member_id: int, password: str) -> None:
        """
        Update Member Password
        member_id = "noah51"
        new_password = "Hello_World21"

        query = '''
            call update_member_password(%s, %s)
        '''
        cursor.execute(query, (member_id, new_password))
        conn.commit()

        :param member_id: int
        :param password: str
        :return: None
        """

        query = """
            call update_member_password(%s, %s)
        """
        self.db.execute(query, (member_id, password))
        self.db.connection.commit()

    def update_member_email(self, member_id: int, email: str) -> None:
        """
        Update Member Email
        Update Member Email
        member_id = "noah51"
        new_email = "noah51@gmail.com"

        query = '''
            call update_member_email(%s, %s)
        '''
        cursor.execute(query, (member_id, new_email))
        conn.commit()

        :param member_id: int
        :param email: str
        :return: None
        """

        query = """
            call update_member_email(%s, %s)
        """
        self.db.execute(query, (member_id, email))
        self.db.connection.commit()

    def search_room(self, room_id: int, book_date: date, book_time: time) -> CMySQLCursor:
        """
        Search Room
        room_type = 'Archery Range'"'
        date = '2017-12-26'
        time = '13:00:00'

        query = '''
        call search_room(%s, %s, %s)
        '''

        cursor.execute(query, (room_type, date, time))
        results = cursor.fetchall()
        """

        query = """
            call search_room(%s, %s, %s)
        """

        results = self.db.execute(query, (room_id, book_date, book_time))
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

    def book_room(self, room_id: int, book_date: date, book_time: time, user_id: str) -> None:
        """
        Book Room or sports complex room
        Usage:
            room_id = "AR"
            date = "2017-12-26"
            time = "13:00:00"
            user = "noah51"

            query = '''
                call make_booking(%s, %s, %s, %s)
            '''

            try:
                cursor.execute(query, (room_id, date, time, user))
                conn.commit()
                print("Room booked successfully")
            except mysql.connector.Error as err:
                print(err)
        :param room_id: int, the room_id to book
        :param book_date: date, what is the date of booking
        :param book_time: time, what is the time of booking
        :param user_id: str, what user_id book the room
        :return: None
        """

        query = """
            call book_room(%s, %s, %s)
        """

        try:
            self.db.execute(query, (room_id, book_date, book_time, user_id))
            self.db.connection.commit()
            print("Room booked successfully!")
        except mysql.connector.Error as err:
            print(err)


    # Cancel Booking
    # book_id = 17
    # message = ""
    #
    # query1 = f"""
    #     call cancel_booking({book_id}, @message);
    # """
    #
    # query2 = """
    #     select @message;
    # """
    #
    # try:
    #     cursor.execute(query1)
    #     cursor.execute(query2)
    #     message = cursor.fetchone()
    #     print(message)
    #     conn.commit()
    # except mysql.connector.Error as err:
    #     print(err)

    #
    # # Show members
    # query = """
    #     select
    #         id,
    #         email,
    #         payment_due
    #     from members
    #     order by member_since desc;
    # """
    #
    # cursor.execute(query)
    # results = cursor.fetchall()
    #
    #
    # table = PrettyTable()
    # field_names: list[str] = [
    #     "Id",
    #     "Email",
    #     "Payment_Due"
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
