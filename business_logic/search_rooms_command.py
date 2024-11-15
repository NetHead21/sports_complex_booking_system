from datetime import datetime, timedelta, time

from mysql.connector.cursor_cext import CMySQLCursor

from business_logic import Command
from business_logic.room_database_manager import db
from persistence.models import SearchRoom


class SearchRoomCommand(Command):
    def execute(self, room: SearchRoom) -> tuple[bool, CMySQLCursor]:
        return True, db.search_room(room.room_type, room.book_date, room.book_time)


if __name__ == "__main__":
    try:
        five_days = datetime.today() + timedelta(days=5)

        room_data = {
            "room_type": "Archery Range",
            "book_date": five_days.strftime("%Y-%m-%d"),
            "book_time": time(13, 0, 0),
        }

        room = SearchRoom(**room_data)

        search_room = SearchRoomCommand()
        print(search_room.execute(room))

    except Exception as e:
        print(e)
