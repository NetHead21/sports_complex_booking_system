from datetime import datetime, timedelta, time

from business_logic import Command
from business_logic.room_database_manager import db
from persistence.models import Booking


class BookRoomCommand(Command):
    def execute(self, book: Booking) -> tuple[bool, None]:
        return True, db.book_room(
            book.room_id, book.book_date, book.book_time, book.user
        )


if __name__ == "__main__":
    try:
        five_days = datetime.today() + timedelta(days=5)

        book_data = {
            "room_id": "AR",
            "book_date": five_days.strftime("%Y-%m-%d"),
            "book_time": time(13, 0, 0),
            "user": "NetHead21",
        }

        book = Booking(**book_data)

        book_room = BookRoomCommand()
        print(book_room.execute(book))

    except Exception as e:
        print(e)
