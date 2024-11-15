from business_logic import Command
from business_logic.room_database_manager import db


class CancelBookRoomCommand(Command):
    def execute(self, book_id: int) -> tuple[bool, None]:
        return True, db.cancel_booking(book_id)


if __name__ == "__main__":
    try:
        book_id = 20

        book_room = CancelBookRoomCommand()
        book_room.execute(book_id)

    except Exception as e:
        print(e)
