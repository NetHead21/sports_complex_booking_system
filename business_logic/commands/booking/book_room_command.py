"""
Book Room Command Module.

This module implements the BookRoomCommand class, which handles the business logic
for booking sports facility rooms within the sports booking system. The command
follows the Single Responsibility Principle by delegating input collection and
validation to BookingInputService and focusing solely on executing the database
booking operation.

The module integrates with the room booking database to perform actual booking
operations and provides comprehensive error handling and user feedback.

Classes:
    BookRoomCommand: Command class for booking rooms in the sports facility.

Dependencies:
    - Command: Base command interface from the command pattern
    - room_database_manager: Database operations for room booking management
    - BookingInputService: Service for collecting and validating booking input data

Example:
    Basic room booking:
    >>> command = BookRoomCommand()
    >>> success, error = command.execute()
    >>> if success:
    ...     print("Room booked successfully")
    ... else:
    ...     print(f"Booking failed: {error}")

Architecture:
    This command is part of a clean architecture implementation where:
    - BookRoomCommand handles business logic execution
    - BookingInputService handles input collection and validation
    - room_database_manager handles data persistence

Author: Sports Booking System Team
Version: 2.0
Last Modified: August 2025
"""

from business_logic.base.command import Command
from business_logic.room_database_manager import db
from business_logic.services.booking_input_service import BookingInputService


class BookRoomCommand(Command):
    """
    Command for booking sports facility rooms in the booking system.

    This class implements the Command pattern and adheres to the Single Responsibility
    Principle by focusing exclusively on executing the database operation for room
    booking. All input collection, validation, and booking object creation are
    delegated to the BookingInputService to maintain clear separation of concerns.

    The command handles the complete booking workflow including:
    - Delegating data collection to BookingInputService
    - Executing the database booking operation
    - Providing user feedback on operation results
    - Comprehensive error handling and reporting

    Attributes:
        None (inherits from Command base class)

    Methods:
        execute(data=None): Execute the room booking operation

    Example:
        >>> booking_command = BookRoomCommand()
        >>> success, error_msg = booking_command.execute()
        >>> if success:
        ...     print("✅ Room successfully booked!")
        ... else:
        ...     print(f"❌ Booking failed: {error_msg}")

    Integration:
        - Uses BookingInputService for input collection and validation
        - Uses room_database_manager for database operations
        - Follows the established command pattern in the sports booking system

    Note:
        This command requires:
        - Valid database connection through room_database_manager
        - Interactive input capability for BookingInputService
        - Proper room and member data in the database
    """

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the room booking command.

        This method orchestrates the complete room booking process by delegating
        input collection to BookingInputService and executing the database operation
        through the room database manager. It provides comprehensive error handling
        and user feedback throughout the process.

        Single responsibility: Execute the database operation for booking a room.
        Input collection and booking creation are delegated to BookingInputService.

        Args:
            data (any, optional): Additional data for command execution.
                Currently not used in this implementation but maintained for
                interface compatibility with the Command base class.
                Defaults to None.

        Returns:
            tuple[bool, any]: A tuple containing:
                - bool: True if room was successfully booked, False otherwise
                - any: None if successful, error message string if failed

        Raises:
            Exception: Any booking-related exceptions are caught and converted
                to return values for graceful error handling.

        Example:
            >>> command = BookRoomCommand()
            >>> success, error = command.execute()
            >>> if success:
            ...     print("Room booking completed successfully")
            >>> else:
            ...     print(f"Booking process failed: {error}")

        Flow:
            1. Delegate booking data collection to BookingInputService
            2. Validate that booking object was created successfully
            3. Execute database operation to book the room
            4. Provide detailed user feedback on operation result
            5. Return success status and any error information

        Database Operations:
            The method calls db.book_room() which handles:
            - Room availability validation
            - Member existence verification
            - Booking conflict detection
            - Payment status initialization
            - Audit trail creation

        User Feedback:
            - Success: Displays confirmation with booking details
            - Failure: Shows specific error messages for troubleshooting
            - Cancellation: Handles user cancellation gracefully

        Note:
            The method prints status messages directly to the console for
            immediate user feedback, following the established UX pattern
            in the sports booking system.
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
    Module test runner for BookRoomCommand.
    
    This section provides comprehensive testing functionality when the module
    is run directly. It demonstrates the integration between BookRoomCommand
    and BookingInputService, showcasing the separation of concerns achieved
    through the Single Responsibility Principle.
    
    The test runner:
    - Creates a BookRoomCommand instance
    - Executes the booking process interactively
    - Displays comprehensive results and error handling
    - Validates the command pattern implementation
    
    Usage:
        python book_rooms_command.py
    
    Expected Behavior:
        1. Interactive prompts for booking data (room, date, time, member)
        2. Input validation and error handling
        3. Database booking operation execution
        4. Clear success/failure feedback
        5. Final test result summary
    
    Test Scenarios Covered:
        - Successful room booking flow
        - Input validation failures
        - Database operation errors
        - User cancellation handling
        - Exception management
    
    Example Output:
        Testing BookRoomCommand with BookingInputService
        ==================================================
        [Interactive booking prompts...]
        ✅ Room 'T1' booked successfully for member123 on 2025-08-25 at 14:00:00!
        ✅ Test completed successfully
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
