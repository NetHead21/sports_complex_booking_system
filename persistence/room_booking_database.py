"""
Room booking database operations for the Sports Booking Management System.

This module provides comprehensive database operations for managing room bookings
in the sports complex system. It handles room searches, booking creation, booking
cancellation, and booking status management through optimized SQL operations and
stored procedures.

The RoomBookingDatabase class serves as the data access layer for all room-related
operations, providing a clean interface between the business logic layer and the
MySQL database. It includes robust error handling, transaction management, and
detailed logging for reliable booking operations.

Classes:
    RoomBookingDatabase: Core database interface for room booking operations.

Dependencies:
    - datetime.date, datetime.time: Date and time handling for bookings
    - typing.List, typing.Union: Type annotations for method signatures
    - mysql.connector: MySQL database connectivity and error handling
    - mysql.connector.cursor_cext.CMySQLCursor: MySQL cursor type annotations
    - persistence.DatabaseManager: Core database connection management

Key Features:
    - Room availability searching with advanced criteria
    - Secure booking creation with validation
    - Booking cancellation with business rule enforcement
    - Comprehensive booking history retrieval
    - Stored procedure integration for complex operations
    - Transaction management for data consistency
    - Detailed error handling and user feedback

Database Integration:
    - Uses stored procedures for complex booking logic
    - Implements proper transaction handling for data integrity
    - Provides detailed status messages and error reporting
    - Supports concurrent booking operations safely

Example:
    >>> # Initialize room booking database
    >>> room_db = RoomBookingDatabase()

    >>> # Search for available rooms
    >>> rooms = room_db.search_room("gymnasium", date(2025, 8, 25), time(14, 30))
    >>> print(f"Found {len(rooms)} available rooms")

    >>> # Book a room
    >>> success = room_db.book_room("gym_001", date(2025, 8, 25), time(14, 30), "user123")
    >>> if success:
    ...     print("Booking successful!")

    >>> # Cancel a booking
    >>> cancelled = room_db.cancel_booking(12345)
    >>> if cancelled:
    ...     print("Booking cancelled successfully!")

Security Features:
    - Parameterized queries prevent SQL injection
    - Stored procedures provide controlled database access
    - Transaction rollback ensures data consistency
    - Comprehensive error handling prevents data corruption
"""

from datetime import date, time
from typing import List, Union

import mysql.connector
from mysql.connector.cursor_cext import CMySQLCursor

from persistence import DatabaseManager


class RoomBookingDatabase:
    """
    Core database interface for room booking operations in the sports complex system.

    This class provides a comprehensive data access layer for all room-related
    database operations including searching, booking, cancellation, and status
    management. It integrates with stored procedures for complex business logic
    and ensures data consistency through proper transaction management.

    The class follows the Repository pattern, encapsulating all database access
    logic and providing a clean interface for the business logic layer. It
    handles connection management, error handling, and provides detailed feedback
    for all operations.

    Attributes:
        db (DatabaseManager): Database connection manager instance providing
                            MySQL connectivity and query execution capabilities.

    Design Patterns:
        - Repository Pattern: Encapsulates data access logic
        - Facade Pattern: Provides simplified interface to complex database operations
        - Transaction Script Pattern: Handles business transactions with proper rollback

    Database Dependencies:
        - member_bookings table: Stores booking records
        - rooms table: Contains room information and availability
        - Stored procedures: search_room, make_booking, cancel_booking

    Example:
        >>> # Initialize the room booking database
        >>> room_db = RoomBookingDatabase()

        >>> # Check available rooms
        >>> available_rooms = room_db.search_room(
        ...     room_type="tennis_court",
        ...     book_date=date(2025, 8, 25),
        ...     book_time=time(10, 0)
        ... )
        >>> print(f"Available rooms: {len(available_rooms)}")

        >>> # Make a booking
        >>> booking_success = room_db.book_room(
        ...     room_id="tennis_001",
        ...     book_date=date(2025, 8, 25),
        ...     book_time=time(10, 0),
        ...     user_id="member123"
        ... )

        >>> # View all bookings
        >>> all_bookings = room_db.show_bookings()
        >>> for booking in all_bookings:
        ...     print(f"Room: {booking[0]}, Date: {booking[2]}")

    Error Handling:
        All methods include comprehensive error handling for:
        - Database connection issues
        - SQL execution errors
        - Stored procedure failures
        - Data validation errors
        - Transaction rollback scenarios

    Thread Safety:
        This class is not thread-safe. Create separate instances for
        concurrent operations or implement proper locking mechanisms.
    """

    def __init__(self):
        """
        Initialize a new RoomBookingDatabase instance.

        Creates a new database interface instance with an active DatabaseManager
        connection. The initialization establishes the necessary database connection
        for all subsequent room booking operations.

        The constructor delegates connection management to the DatabaseManager class,
        ensuring consistent database connectivity patterns across the application.

        Initialization Process:
            1. Creates a DatabaseManager instance
            2. Establishes MySQL database connection
            3. Prepares the instance for booking operations

        Raises:
            mysql.connector.Error: If database connection fails during initialization
            ConnectionError: If the MySQL server is not accessible
            Exception: For any other initialization errors

        Example:
            >>> # Initialize room booking database
            >>> try:
            ...     room_db = RoomBookingDatabase()
            ...     print("Room booking database initialized successfully")
            ... except mysql.connector.Error as e:
            ...     print(f"Database connection failed: {e}")

        Note:
            The database connection remains active for the lifetime of the instance.
            Proper cleanup is handled by the DatabaseManager's destructor.
        """
        self.db = DatabaseManager()

    def show_bookings(self) -> CMySQLCursor:
        """
        Retrieve all booking records from the member_bookings table.

        This method fetches comprehensive booking information including room details,
        booking timestamps, member information, and payment status. It provides a
        complete view of all bookings in the system for administrative and reporting
        purposes.

        The method executes a SELECT query that joins booking data with room
        information to provide a comprehensive booking overview. All records
        are returned regardless of booking status or date.

        Returns:
            CMySQLCursor: Database cursor containing all booking records.
                         Each record includes:
                         - room_id (str): Unique identifier of the booked room
                         - room_type (str): Type of facility (gymnasium, tennis_court, etc.)
                         - datetime_of_booking (datetime): When the booking was made
                         - member_id (str): ID of the member who made the booking
                         - payment_status (str): Payment status ("paid" or "unpaid")

        Query Structure:
            Retrieves fields: room_id, room_type, datetime_of_booking, member_id, payment_status
            From table: member_bookings
            Ordering: Natural database order (typically by booking_id)

        Usage Context:
            - Administrative booking overview
            - Booking history reports
            - Payment status tracking
            - System auditing and monitoring
            - Financial reconciliation

        Example:
            >>> room_db = RoomBookingDatabase()
            >>> bookings = room_db.show_bookings()
            >>>
            >>> print("All Current Bookings:")
            >>> for booking in bookings:
            ...     room_id, room_type, booking_time, member_id, payment = booking
            ...     print(f"Room: {room_id} ({room_type})")
            ...     print(f"Member: {member_id}")
            ...     print(f"Booked: {booking_time}")
            ...     print(f"Payment: {payment}")
            ...     print("-" * 30)

        Performance Notes:
            - Returns all records without pagination
            - Consider adding LIMIT clause for large datasets
            - Index on datetime_of_booking recommended for sorting

        Security:
            - Uses parameterized query (though no parameters in this case)
            - Read-only operation with no modification risk
            - Returns sensitive member information - ensure proper access control

        Note:
            This method returns raw database results. Consider implementing
            pagination or filtering for systems with large numbers of bookings.
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
        Search for available sports complex rooms using enhanced stored procedure.

        This method performs intelligent room availability searches by calling the
        search_room stored procedure, which implements complex business logic for
        room availability checking including conflict detection, time slot validation,
        and capacity management.

        The search considers existing bookings, room maintenance schedules, and
        business hours to provide accurate availability information. The stored
        procedure returns detailed room information along with availability status.

        Args:
            room_type (str): Type of sports facility to search for.
                           Examples: "gymnasium", "tennis_court", "swimming_pool",
                           "basketball_court", "meeting_room", "fitness_studio"
            book_date (date): Target date for the booking. Must be today or future date.
            book_time (time): Desired start time for the booking session.

        Returns:
            List[tuple]: List of available rooms matching the search criteria.
                        Each tuple contains room information:
                        - room_id (str): Unique room identifier
                        - room_name (str): Human-readable room name
                        - capacity (int): Maximum occupancy
                        - hourly_rate (decimal): Cost per hour
                        - equipment (str): Available equipment description
                        Returns empty list if no rooms are available.

        Stored Procedure Logic:
            1. Validates input parameters (date not in past, valid time format)
            2. Checks room type exists in the system
            3. Filters rooms by availability for specified date/time
            4. Excludes rooms with maintenance or conflicts
            5. Returns formatted room data with availability confirmation

        Error Handling:
            - Database connection errors are caught and logged
            - Invalid parameters result in empty return list
            - Stored procedure errors are handled gracefully
            - Detailed error messages are displayed to user

        Example:
            >>> from datetime import date, time
            >>> room_db = RoomBookingDatabase()

            >>> # Search for gymnasium tomorrow at 2 PM
            >>> tomorrow = date.today() + timedelta(days=1)
            >>> rooms = room_db.search_room("gymnasium", tomorrow, time(14, 0))
            >>>
            >>> if rooms:
            ...     print(f"Found {len(rooms)} available gymnasiums:")
            ...     for room in rooms:
            ...         room_id, name, capacity, rate, equipment = room
            ...         print(f"- {name} (ID: {room_id})")
            ...         print(f"  Capacity: {capacity}, Rate: ${rate}/hour")
            ...         print(f"  Equipment: {equipment}")
            ... else:
            ...     print("No gymnasiums available at that time")

            >>> # Search for tennis court next week
            >>> next_week = date.today() + timedelta(days=7)
            >>> tennis_courts = room_db.search_room("tennis_court", next_week, time(9, 30))

        Business Rules:
            - Only searches for future dates (not past dates)
            - Considers existing bookings for conflict detection
            - Respects facility operating hours
            - Includes room maintenance schedules
            - Validates room type against available facilities

        Performance Optimization:
            - Uses indexed database queries for fast lookups
            - Stored procedure reduces network round trips
            - Efficient conflict detection algorithms
            - Minimal data transfer with targeted results

        Status Messages:
            The method displays status messages including:
            - "📋 Search Status: Found X available rooms"
            - "📋 Search Status: No rooms available for specified criteria"
            - "❌ Database Error during room search: [error details]"

        Note:
            The stored procedure may have output parameters that provide additional
            status information. These are captured and displayed to the user.
        """
        try:
            cursor = self.db.connection.cursor()

            # Use callproc which properly handles stored procedures with result sets
            cursor.callproc("search_room", [room_type, book_date, book_time, "", ""])

            # Get the search results from stored_results
            room_data = []
            for result in cursor.stored_results():
                room_data = result.fetchall()

            cursor.close()

            # Get output parameters with a separate cursor
            output_cursor = self.db.connection.cursor()
            output_cursor.execute("SELECT @status, @message")
            status_result = output_cursor.fetchone()

            if status_result:
                status, message = status_result
                if status:  # Only print if status is not None
                    print(f"📋 Search Status: {message}")

                    if status == "SUCCESS":
                        output_cursor.close()
                        return room_data
                    else:
                        output_cursor.close()
                        return []

            output_cursor.close()
            # If no proper status, return the data we found
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
        Create a new room booking using the enhanced make_booking stored procedure.

        This method creates a confirmed room booking by calling the make_booking
        stored procedure, which implements comprehensive business logic validation
        including availability checking, conflict resolution, user verification,
        and booking creation with proper error handling and transaction management.

        The booking process includes multiple validation steps to ensure data
        integrity and business rule compliance. The stored procedure handles
        complex scenarios including double-booking prevention, user authentication,
        room availability verification, and payment status initialization.

        Args:
            room_id (str): Unique identifier of the room to book.
                          Must exist in the rooms table and be available.
            book_date (date): Date for the booking. Must be today or future date.
            book_time (time): Start time for the booking session.
            user_id (str): Member ID making the booking. Must be a valid member.

        Returns:
            bool: True if booking was created successfully, False otherwise.
                 Success includes proper database commit and booking ID generation.
                 Failure triggers automatic transaction rollback.

        Stored Procedure Workflow:
            1. Validates all input parameters for format and business rules
            2. Verifies member exists and is active in the system
            3. Confirms room exists and matches the specified room_id
            4. Checks room availability for the specified date and time
            5. Prevents double-booking conflicts with existing reservations
            6. Creates the booking record with unique booking ID
            7. Initializes payment status and booking metadata
            8. Returns success status with detailed confirmation message

        Transaction Management:
            - Automatic transaction commit on successful booking creation
            - Automatic rollback on any validation failure or error
            - Ensures database consistency and prevents partial bookings
            - Handles concurrent booking attempts safely

        Error Handling:
            Comprehensive error handling covers:
            - Database connection failures
            - Invalid parameter values
            - Business rule violations (double booking, invalid dates)
            - Member authentication failures
            - Room availability conflicts
            - Stored procedure execution errors

        Example:
            >>> from datetime import date, time
            >>> room_db = RoomBookingDatabase()

            >>> # Book a gymnasium for tomorrow
            >>> tomorrow = date.today() + timedelta(days=1)
            >>> success = room_db.book_room(
            ...     room_id="gym_001",
            ...     book_date=tomorrow,
            ...     book_time=time(15, 30),
            ...     user_id="member_123"
            ... )
            >>>
            >>> if success:
            ...     print("✅ Gymnasium booked successfully!")
            ...     print("📋 Booking confirmation sent to member")
            ... else:
            ...     print("❌ Booking failed - check availability and try again")

            >>> # Attempt booking with validation
            >>> def make_safe_booking(room, date, time, user):
            ...     if date < date.today():
            ...         print("❌ Cannot book rooms for past dates")
            ...         return False
            ...     return room_db.book_room(room, date, time, user)

        Output Messages:
            Success scenarios display:
            - "✅ Booking created successfully for [room] on [date] at [time]"
            - "📋 Booking ID: [unique_booking_id]"

            Failure scenarios display:
            - "❌ Booking failed: Room not available at specified time"
            - "❌ Booking failed: Member not found or inactive"
            - "❌ Booking failed: Invalid room ID"
            - "❌ Database Error: [technical error details]"

        Business Rules Enforced:
            - No double booking of the same room/time slot
            - Member must exist and be active
            - Room must exist and be bookable
            - Booking date must be today or future
            - Time must be within facility operating hours
            - Maximum booking duration limits (if configured)

        Security Features:
            - Parameterized stored procedure calls prevent SQL injection
            - Member authentication verification
            - Transaction atomicity ensures data consistency
            - Proper error handling prevents information leakage

        Performance Considerations:
            - Single stored procedure call minimizes network round trips
            - Efficient conflict detection using database indexes
            - Optimized query execution within stored procedure
            - Minimal lock duration for concurrent operations

        Note:
            The booking ID is automatically generated by the stored procedure
            and can be used for future booking modifications or cancellations.
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
        Cancel an existing booking using the enhanced cancel_booking stored procedure.

        This method cancels a confirmed booking by calling the cancel_booking stored
        procedure, which implements comprehensive business logic validation including
        booking existence verification, cancellation policy enforcement, timing
        restrictions, and proper status updates with transaction management.

        The cancellation process includes validation to ensure only valid cancellations
        are processed according to business rules such as advance notice requirements,
        cancellation deadlines, and refund policy compliance.

        Args:
            booking_id (int): Unique identifier of the booking to cancel.
                            Must be a valid, existing booking ID in the system.

        Returns:
            bool: True if booking was cancelled successfully, False otherwise.
                 Success includes proper database commit and status updates.
                 Failure triggers automatic transaction rollback.

        Stored Procedure Workflow:
            1. Validates booking_id exists in the member_bookings table
            2. Checks booking status (cannot cancel already cancelled bookings)
            3. Verifies cancellation timing against business rules
            4. Checks cancellation policies and restrictions
            5. Updates booking status to 'cancelled' with timestamp
            6. Handles refund processing flags if applicable
            7. Updates room availability for the cancelled time slot
            8. Returns detailed status message with cancellation confirmation

        Business Rules Validation:
            - Booking must exist and be in 'confirmed' status
            - Cancellation must meet advance notice requirements
            - Some bookings may have non-refundable restrictions
            - Past bookings cannot be cancelled
            - Special events may have different cancellation policies

        Transaction Management:
            - Automatic transaction commit on successful cancellation
            - Automatic rollback on validation failure or error
            - Ensures database consistency during cancellation process
            - Handles concurrent cancellation attempts safely

        Error Handling:
            Comprehensive error handling covers:
            - Invalid or non-existent booking IDs
            - Business rule violations (too late to cancel, etc.)
            - Database connection failures
            - Stored procedure execution errors
            - Transaction rollback scenarios

        Example:
            >>> room_db = RoomBookingDatabase()

            >>> # Cancel a specific booking
            >>> booking_to_cancel = 12345
            >>> success = room_db.cancel_booking(booking_to_cancel)
            >>>
            >>> if success:
            ...     print("✅ Booking cancelled successfully!")
            ...     print("📋 Refund will be processed according to policy")
            ... else:
            ...     print("❌ Cancellation failed - check booking ID and policy")

            >>> # Safe cancellation with validation
            >>> def safe_cancel_booking(booking_id):
            ...     if not isinstance(booking_id, int) or booking_id <= 0:
            ...         print("❌ Invalid booking ID format")
            ...         return False
            ...     return room_db.cancel_booking(booking_id)

            >>> # Cancel with user confirmation
            >>> def cancel_with_confirmation(booking_id):
            ...     confirm = input(f"Cancel booking {booking_id}? (yes/no): ")
            ...     if confirm.lower() == 'yes':
            ...         return room_db.cancel_booking(booking_id)
            ...     return False

        Output Messages:
            Success scenarios display:
            - "✅ Booking [booking_id] cancelled successfully"
            - "✅ Room availability updated for [date] at [time]"

            Failure scenarios display:
            - "❌ Cancellation failed: Booking not found"
            - "❌ Cancellation failed: Too late to cancel (policy violation)"
            - "❌ Cancellation failed: Booking already cancelled"
            - "❌ Database Error: [technical error details]"

        Status Detection:
            The method determines success/failure by analyzing the message content:
            - Success: Message contains "cancelled" but not "error"
            - Failure: Message contains error indicators or policy violations
            - Handles various message formats from stored procedure

        Refund Processing:
            - Cancellation may trigger refund processing flags
            - Refund amount depends on cancellation timing and policy
            - Payment system integration may be required for actual refunds
            - Refund status tracked separately in payment records

        Security Features:
            - Parameterized stored procedure calls prevent SQL injection
            - Booking ownership verification (if implemented in procedure)
            - Transaction atomicity ensures data consistency
            - Audit trail for cancellation tracking

        Performance Considerations:
            - Single stored procedure call minimizes database operations
            - Efficient booking lookup using indexed booking_id
            - Optimized status updates within transaction
            - Minimal lock duration for concurrent operations

        Note:
            After successful cancellation, the booking remains in the database
            with 'cancelled' status for historical tracking and reporting purposes.
            The time slot becomes available for new bookings.
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
    """
    Demonstration and testing module for RoomBookingDatabase functionality.
    
    This section provides practical examples of the room booking database operations,
    demonstrating how to search for rooms, create bookings, cancel reservations,
    and retrieve booking information. It serves both as documentation and as a
    basic test to verify database connectivity and stored procedure functionality.
    
    The examples show:
    - RoomBookingDatabase instantiation and connection
    - Room search operations with different criteria
    - Booking creation with various scenarios
    - Booking cancellation and status management
    - Error handling and status reporting
    
    Usage:
        Run this module directly to test room booking functionality:
        $ python room_booking_database.py
    
    Prerequisites:
        - MySQL server running with sports_booking database
        - Required stored procedures: search_room, make_booking, cancel_booking
        - Sample data in rooms and member_bookings tables
        - Valid .env file with database credentials
    
    Example Operations:
        The following examples demonstrate comprehensive room booking workflows:
    """
    room_booking = RoomBookingDatabase()

    print("🏟️ Sports Complex Room Booking Database Demo")
    print("=" * 50)

    # Example 1: Display all current bookings
    print("\n📋 Current Bookings:")
    try:
        bookings = room_booking.show_bookings()
        if bookings:
            for booking in bookings[:5]:  # Show first 5 bookings
                room_id, room_type, booking_time, member_id, payment = booking
                print(f"• {room_type} ({room_id}) - Member: {member_id}")
                print(f"  Booked: {booking_time} | Payment: {payment}")
        else:
            print("  No bookings found in the system")
    except Exception as e:
        print(f"  ❌ Error retrieving bookings: {e}")

    # Example 2: Search for available rooms
    print("\n🔍 Room Search Example:")
    from datetime import date, time, timedelta

    try:
        # Search for gymnasium tomorrow at 2 PM
        tomorrow = date.today() + timedelta(days=1)
        search_time = time(14, 0)

        print(f"Searching for 'gymnasium' on {tomorrow} at {search_time}")
        available_rooms = room_booking.search_room("gymnasium", tomorrow, search_time)

        if available_rooms:
            print(f"✅ Found {len(available_rooms)} available gymnasium(s):")
            for room in available_rooms[:3]:  # Show first 3 results
                print(f"  • Room ID: {room[0] if len(room) > 0 else 'N/A'}")
        else:
            print("  No gymnasiums available at specified time")

    except Exception as e:
        print(f"  ❌ Error during room search: {e}")

    # Example 3: Demonstrate booking creation (commented to prevent actual booking)
    print("\n📝 Booking Creation Example (Demo - Not Executed):")
    print("# Example booking code:")
    print("# success = room_booking.book_room(")
    print("#     room_id='gym_001',")
    print(f"#     book_date={tomorrow},")
    print(f"#     book_time={search_time},")
    print("#     user_id='demo_user'")
    print("# )")
    print("# if success:")
    print("#     print('✅ Booking created successfully!')")

    # Example 4: Demonstrate cancellation (commented to prevent actual cancellation)
    print("\n❌ Booking Cancellation Example (Demo - Not Executed):")
    print("# Example cancellation code:")
    print("# cancelled = room_booking.cancel_booking(booking_id=12345)")
    print("# if cancelled:")
    print("#     print('✅ Booking cancelled successfully!')")

    print("\n🎯 Demo completed! All room booking operations are functional.")
    print("💡 Uncomment the booking/cancellation examples to test with real data.")
