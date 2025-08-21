from datetime import date, time
from typing import List, Union

import mysql.connector
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

    def search_room(
        self, room_type: str, book_date: date, book_time: time
    ) -> List[tuple]:
        """
        Search for an available sports complex room using enhanced search procedure.

        :param room_type: str, the type of room to search for
        :param book_date: date, the date of booking
        :param book_time: time, the time of booking
        :return: list of available rooms or empty list if none found
        """
        try:
            cursor = self.db.connection.cursor()

            # Prepare the call with proper output variables
            call_query = """
                CALL search_room(%s, %s, %s, @status, @message)
            """
            
            # Execute the procedure call
            cursor.execute(call_query, (room_type, book_date, book_time))

            # Get the search results first (if any)
            room_data = []
            try:
                # Try to fetch results in case the procedure returns a result set
                room_data = cursor.fetchall()
            except:
                # If no result set, that's fine - some procedures don't return data
                pass

            # Get the output parameters
            cursor.execute("SELECT @status, @message")
            status_result = cursor.fetchone()

            if status_result:
                status, message = status_result
                print(f"📋 Search Status: {message}")

                if status == "SUCCESS":
                    cursor.close()
                    return room_data
                else:
                    cursor.close()
                    return []
            else:
                cursor.close()
                return room_data

        except mysql.connector.Error as err:
            print(f"❌ Database Error during room search: {err}")
            return []
        except Exception as e:
            print(f"❌ Unexpected Error during room search: {e}")
            return []

    def book_room(
        self, room_id: str, book_date: date, book_time: time, user_id: str
    ) -> bool:
        """
        Book Room or sports complex room using the enhanced make_booking procedure.

        This method calls the enhanced make_booking stored procedure which includes
        comprehensive validation and returns detailed status information.

        :param room_id: str, the room_id to book
        :param book_date: date, what is the date of booking
        :param book_time: time, what is the time of booking
        :param user_id: str, what user_id book the room
        :return: bool, True if booking successful, False otherwise
        """
        try:
            # Call enhanced stored procedure with output parameters
            cursor = self.db.connection.cursor()

            # Prepare the call with proper output variables
            call_query = """
                CALL make_booking(%s, %s, %s, %s, @booking_id, @status, @message)
            """
            
            # Execute the procedure call
            cursor.execute(call_query, (room_id, book_date, book_time, user_id))
            
            # Retrieve the output parameter values
            cursor.execute("SELECT @booking_id, @status, @message")
            result = cursor.fetchone()

            if result:
                booking_id, status, message = result

                if status == "SUCCESS":
                    print(f"✅ {message}")
                    print(f"📋 Booking ID: {booking_id}")
                    self.db.connection.commit()
                    cursor.close()
                    return True
                else:
                    print(f"❌ Booking failed: {message}")
                    print(f"📋 Status: {status}")
                    self.db.connection.rollback()
                    cursor.close()
                    return False
            else:
                print("❌ Unexpected error: No result from stored procedure")
                self.db.connection.rollback()
                cursor.close()
                return False

        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")
            if self.db.connection:
                self.db.connection.rollback()
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False

    def cancel_booking(self, booking_id: int) -> bool:
        """
        Cancel Booking using the enhanced cancel_booking procedure.

        This method calls the cancel_booking stored procedure which includes
        business logic validation and returns detailed status information.

        :param booking_id: int, the booking id to cancel booking
        :return: bool, True if cancellation successful, False otherwise
        """
        try:
            cursor = self.db.connection.cursor()

            # Prepare the call with proper output variables
            call_query = """
                CALL cancel_booking(%s, @message)
            """
            
            # Execute the procedure call
            cursor.execute(call_query, (booking_id,))

            # Retrieve the output parameter value
            cursor.execute("SELECT @message")
            result = cursor.fetchone()

            if result:
                message = result[0]

                # Check if cancellation was successful based on message content
                if "cancelled" in message.lower() and "error" not in message.lower():
                    print(f"✅ {message}")
                    self.db.connection.commit()
                    cursor.close()
                    return True
                else:
                    print(f"❌ Cancellation failed: {message}")
                    self.db.connection.rollback()
                    cursor.close()
                    return False
            else:
                print("❌ Unexpected error: No result from stored procedure")
                self.db.connection.rollback()
                cursor.close()
                return False

        except mysql.connector.Error as err:
            print(f"❌ Database Error: {err}")
            if self.db.connection:
                self.db.connection.rollback()
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False


if __name__ == "__main__":
    room_booking = RoomBookingDatabase()
