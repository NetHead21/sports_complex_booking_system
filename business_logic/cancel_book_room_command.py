from business_logic.command import Command
from business_logic.room_database_manager import db
from business_logic.booking_input_service import BookingInputService


class CancelBookRoomCommand(Command):
    """Command responsible for cancelling room bookings."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the cancel booking command.

        Single responsibility: Execute the database operation for cancelling a booking.
        Input collection is delegated to BookingInputService.
        """
        try:
            # Delegate input collection to service
            cancellation_data = BookingInputService.collect_booking_cancellation_data()

            if cancellation_data is None:
                return False, "Booking cancellation cancelled or failed"

            booking_id, member_id = cancellation_data

            # Focus solely on database execution
            success = db.cancel_booking(int(booking_id))

            if success:
                print(
                    f"✅ Booking #{booking_id} cancelled successfully for member {member_id}!"
                )
                return True, None
            else:
                print(
                    "❌ Failed to cancel booking. Please verify booking ID and try again."
                )
                return False, "Cancellation operation failed"

        except Exception as e:
            print(f"❌ Cancellation Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    """
    Test the CancelBookRoomCommand with the new BookingInputService.
    This demonstrates the separation of concerns - the command now focuses
    solely on execution while the service handles all input collection.
    """
    try:
        print("Testing CancelBookRoomCommand with BookingInputService")
        print("=" * 50)

        cancel_command = CancelBookRoomCommand()
        success, result = cancel_command.execute()

        if success:
            print("✅ Test completed successfully")
        else:
            print(f"❌ Test failed: {result}")

    except Exception as e:
        print(f"❌ Test error: {e}")
