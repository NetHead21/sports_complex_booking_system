from mysql.connector.cursor_cext import CMySQLCursor

from business_logic.base.command import Command
from business_logic.room_database_manager import db
from presentation.table_formatter import format_booking_table


class ListRoomCommand(Command):
    def execute(self, data=None) -> tuple[bool, None]:
        bookings = db.show_bookings()

        # Format and print the table
        formatted_table = format_booking_table(bookings)
        print(formatted_table)

        # Return None as result since we already printed the formatted table
        return True, None
