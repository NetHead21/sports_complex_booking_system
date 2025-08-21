from business_logic.command import Command
from business_logic.room_database_manager import db
from business_logic.booking_input_service import BookingInputService


class BookRoomCommand(Command):
    """Command responsible for booking rooms in the system."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the book room command.

        Single responsibility: Execute the database operation for booking a room.
        Input collection and booking creation are delegated to BookingInputService.
        """
        try:
            # Delegate input collection and booking creation to service
            booking = BookingInputService.collect_new_booking_data()

            if booking is None:
                return False, "Booking creation cancelled or failed"

            # Focus solely on database execution
            success = db.book_room(
                booking.room_id, booking.book_date, booking.book_time, booking.user
            )

            if success:
                print(
                    f"✅ Room '{booking.room_id}' booked successfully for {booking.user} on {booking.book_date} at {booking.book_time}!"
                )
                return True, None
            else:
                print("❌ Failed to book room. Please try again.")
                return False, "Booking operation failed"

        except Exception as e:
            print(f"❌ Booking Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    """
    Test the BookRoomCommand with the new BookingInputService.
    This demonstrates the separation of concerns - the command now focuses
    solely on execution while the service handles all input collection.
    """
    try:
        print("Testing BookRoomCommand with BookingInputService")
        print("=" * 50)

        book_room_command = BookRoomCommand()
        success, result = book_room_command.execute()

        if success:
            print("✅ Test completed successfully")
        else:
            print(f"❌ Test failed: {result}")

    except Exception as e:
        print(f"❌ Test error: {e}")
