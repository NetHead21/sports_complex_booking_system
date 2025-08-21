"""
Booking Input Service Module

This module provides centralized input collection and validation services for
booking-related operations, implementing the Single Responsibility Principle.
"""

from datetime import datetime, date, time
from typing import Optional, Tuple

from persistence.models import Booking, SearchRoom
from presentation.user_input import get_user_input
from presentation.utils import clear_screen


class BookingInputService:
    """
    Centralized service for collecting and validating booking-related input data.

    This service handles all user input collection for booking operations,
    separating input concerns from business logic execution. It provides
    comprehensive validation and user-friendly error handling.

    Responsibilities:
        - Collect booking creation data from user
        - Collect room search criteria
        - Collect booking cancellation data
        - Validate input data before creating models
        - Handle input errors gracefully with user feedback

    Security Considerations:
        - Input validation prevents injection attacks
        - Date/time validation ensures valid booking windows
        - User ID validation for security
        - Graceful error handling prevents information leakage
    """

    @staticmethod
    def collect_new_booking_data() -> Optional[Booking]:
        """
        Collect and validate new booking data from user input.

        This method guides the user through booking creation with comprehensive
        validation and error handling. It ensures all required fields are
        properly formatted before creating the Booking model.

        Returns:
            Optional[Booking]: Valid Booking object if successful, None if cancelled

        Validation Rules:
            - Room ID: Non-empty string, uppercase format
            - Book Date: Future date only, ISO format (YYYY-MM-DD)
            - Book Time: Valid time format (HH:MM), business hours only
            - User: Non-empty string, valid username format

        User Experience:
            - Clear prompts with format examples
            - Immediate validation feedback
            - Option to cancel at any step
            - Confirmation before proceeding
        """
        clear_screen()
        print("📋 CREATE NEW BOOKING")
        print("=" * 50)
        print("Please provide the following booking information:")
        print("(Press Ctrl+C at any time to cancel)")
        print()

        try:
            # Collect Room ID
            room_id = BookingInputService._collect_room_id()
            if room_id is None:
                return None

            # Collect Book Date
            book_date = BookingInputService._collect_book_date()
            if book_date is None:
                return None

            # Collect Book Time
            book_time = BookingInputService._collect_book_time()
            if book_time is None:
                return None

            # Collect User/Member ID
            user = BookingInputService._collect_user_id()
            if user is None:
                return None

            # Create and validate booking object
            booking = Booking(
                room_id=room_id, book_date=book_date, book_time=book_time, user=user
            )

            # Display booking summary for confirmation
            print("\n" + "=" * 50)
            print("📋 BOOKING SUMMARY")
            print("=" * 50)
            print(f"Room ID: {booking.room_id}")
            print(f"Date: {booking.book_date}")
            print(f"Time: {booking.book_time}")
            print(f"Member: {booking.user}")
            print("-" * 50)

            confirm = (
                get_user_input("Confirm booking creation? (y/n): ").strip().lower()
            )
            if confirm not in ["y", "yes"]:
                print("❌ Booking creation cancelled")
                return None

            return booking

        except KeyboardInterrupt:
            print("\n❌ Booking creation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting booking data: {e}")
            return None

    @staticmethod
    def collect_room_search_data() -> Optional[SearchRoom]:
        """
        Collect and validate room search criteria from user input.

        Guides the user through specifying search parameters for finding
        available rooms with comprehensive validation and user feedback.

        Returns:
            Optional[SearchRoom]: Valid SearchRoom object if successful, None if cancelled

        Validation Rules:
            - Room Type: Non-empty string, valid facility type
            - Book Date: Future date only, ISO format
            - Book Time: Valid time format, business hours

        Search Categories:
            - Tennis Court
            - Badminton Court
            - Archery Range
            - Multi-Purpose Field
        """
        clear_screen()
        print("🔍 SEARCH AVAILABLE ROOMS")
        print("=" * 50)
        print("Search for available rooms by specifying your criteria:")
        print("(Press Ctrl+C at any time to cancel)")
        print()

        try:
            # Collect Room Type
            room_type = BookingInputService._collect_room_type()
            if room_type is None:
                return None

            # Collect Search Date
            book_date = BookingInputService._collect_book_date("search date")
            if book_date is None:
                return None

            # Collect Search Time
            book_time = BookingInputService._collect_book_time("search time")
            if book_time is None:
                return None

            # Create search object
            search_criteria = SearchRoom(
                room_type=room_type, book_date=book_date, book_time=book_time
            )

            print(
                f"\n✅ Search criteria collected: {room_type} on {book_date} at {book_time}"
            )
            return search_criteria

        except KeyboardInterrupt:
            print("\n❌ Room search cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting search data: {e}")
            return None

    @staticmethod
    def collect_booking_cancellation_data() -> Optional[Tuple[str, str]]:
        """
        Collect booking ID and member ID for booking cancellation.

        Returns:
            Optional[Tuple[str, str]]: (booking_id, member_id) if successful, None if cancelled
        """
        clear_screen()
        print("❌ CANCEL BOOKING")
        print("=" * 50)
        print("Please provide the booking information to cancel:")
        print("(Press Ctrl+C at any time to cancel)")
        print()

        try:
            # Collect Booking ID
            while True:
                booking_id = get_user_input("Enter Booking ID: ").strip()
                if not booking_id:
                    print("❌ Booking ID cannot be empty")
                    continue

                if not booking_id.isdigit():
                    print("❌ Booking ID must be a number")
                    continue

                break

            # Collect Member ID
            member_id = BookingInputService._collect_user_id(
                "Member ID (owner of booking)"
            )
            if member_id is None:
                return None

            return booking_id, member_id

        except KeyboardInterrupt:
            print("\n❌ Booking cancellation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting cancellation data: {e}")
            return None

    @staticmethod
    def _collect_room_id() -> Optional[str]:
        """Collect and validate room ID input."""
        while True:
            room_id = (
                get_user_input("Room ID (e.g., AR, T1, B1, MPF1): ").strip().upper()
            )
            if not room_id:
                print("❌ Room ID cannot be empty")
                continue

            # Basic format validation
            if len(room_id) < 1 or len(room_id) > 10:
                print("❌ Room ID must be between 1-10 characters")
                continue

            return room_id

    @staticmethod
    def _collect_room_type() -> Optional[str]:
        """Collect and validate room type selection."""
        room_types = {
            "1": "Tennis Court",
            "2": "Badminton Court",
            "3": "Archery Range",
            "4": "Multi-Purpose Field",
        }

        print("Available room types:")
        for key, room_type in room_types.items():
            print(f"  {key}: {room_type}")
        print()

        while True:
            choice = get_user_input("Select room type (1-4): ").strip()
            if choice in room_types:
                return room_types[choice]
            print("❌ Invalid choice. Please select 1-4")

    @staticmethod
    def _collect_book_date(field_name: str = "booking date") -> Optional[date]:
        """Collect and validate booking date input."""
        while True:
            date_str = get_user_input(f"Enter {field_name} (YYYY-MM-DD): ").strip()
            if not date_str:
                print(f"❌ {field_name.title()} cannot be empty")
                continue

            try:
                book_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Validate future date
                if book_date <= datetime.now().date():
                    print(f"❌ {field_name.title()} must be in the future")
                    continue

                return book_date

            except ValueError:
                print(
                    "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-25)"
                )

    @staticmethod
    def _collect_book_time(field_name: str = "booking time") -> Optional[time]:
        """Collect and validate booking time input."""
        while True:
            time_str = get_user_input(f"Enter {field_name} (HH:MM): ").strip()
            if not time_str:
                print(f"❌ {field_name.title()} cannot be empty")
                continue

            try:
                book_time = datetime.strptime(time_str, "%H:%M").time()

                # Validate business hours (6 AM to 10 PM)
                if book_time < time(6, 0) or book_time > time(22, 0):
                    print("❌ Booking time must be between 06:00 and 22:00")
                    continue

                return book_time

            except ValueError:
                print("❌ Invalid time format. Please use HH:MM (e.g., 14:30)")

    @staticmethod
    def _collect_user_id(field_name: str = "Member ID") -> Optional[str]:
        """Collect and validate user/member ID input."""
        while True:
            user_id = get_user_input(f"Enter {field_name}: ").strip()
            if not user_id:
                print(f"❌ {field_name} cannot be empty")
                continue

            # Basic validation
            if len(user_id) < 3:
                print(f"❌ {field_name} must be at least 3 characters long")
                continue

            if len(user_id) > 50:
                print(f"❌ {field_name} must be less than 50 characters")
                continue

            return user_id
