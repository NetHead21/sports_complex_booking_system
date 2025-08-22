from mysql.connector.cursor_cext import CMySQLCursor

from business_logic.base.command import Command
from business_logic.room_database_manager import db
from business_logic.services.booking_input_service import BookingInputService


class SearchRoomCommand(Command):
    """Command responsible for searching available rooms."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the search room command.

        Single responsibility: Execute the database operation for searching rooms.
        Input collection and search criteria creation are delegated to BookingInputService.
        """
        try:
            # Delegate input collection and search criteria creation to service
            search_criteria = BookingInputService.collect_room_search_data()

            if search_criteria is None:
                return False, "Room search cancelled or failed"

            # Focus solely on database execution
            cursor_result = db.search_room(
                search_criteria.room_type,
                search_criteria.book_date,
                search_criteria.book_time,
            )

            if cursor_result:
                print(
                    f"✅ Search completed for {search_criteria.room_type} on {search_criteria.book_date} at {search_criteria.book_time}"
                )
                return True, cursor_result
            else:
                print("❌ No rooms found matching your criteria.")
                return False, "No search results"

        except Exception as e:
            print(f"❌ Search Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    """
    Test the SearchRoomCommand with the new BookingInputService.
    This demonstrates the separation of concerns - the command now focuses
    solely on execution while the service handles all input collection.
    """
    try:
        print("Testing SearchRoomCommand with BookingInputService")
        print("=" * 50)

        search_command = SearchRoomCommand()
        success, result = search_command.execute()

        if success:
            print("✅ Test completed successfully")
            print(f"Search results: {result}")
        else:
            print(f"❌ Test failed: {result}")

    except Exception as e:
        print(f"❌ Test error: {e}")
