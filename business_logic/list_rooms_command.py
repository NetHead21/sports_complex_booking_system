from mysql.connector.cursor_cext import CMySQLCursor

from business_logic import Command
from business_logic.room_database_manager import db


class ListRoomCommand(Command):
    def execute(self, data=None) -> tuple[bool, CMySQLCursor]:
        return True, db.show_bookings()
