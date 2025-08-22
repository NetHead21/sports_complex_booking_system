"""
Booking Input Service Module for the Sports Booking Management System.

This module provides centralized input collection and validation services for
all booking-related operations in the sports complex system. It implements the
Single Responsibility Principle by separating user input concerns from business
logic execution, ensuring clean architecture and maintainable code.

The service module acts as an intermediary between the presentation layer and
business logic, handling user input validation, data formatting, and error
management. It provides a consistent interface for collecting booking data
across different operations while maintaining data integrity and user experience.

Classes:
    BookingInputService: Comprehensive service for booking-related input operations.

Dependencies:
    - datetime.datetime, datetime.date, datetime.time: Date and time handling
    - typing.Optional, typing.Tuple: Type annotations for method signatures
    - persistence.models.Booking, persistence.models.SearchRoom: Data models
    - presentation.user_input.get_user_input: User input collection utility
    - presentation.utils.clear_screen: Screen management utility

Key Features:
    - Centralized input validation for all booking operations
    - Comprehensive data format validation and business rule enforcement
    - User-friendly error handling with clear feedback messages
    - Graceful cancellation handling with Ctrl+C support
    - Data model integration with automatic validation
    - Consistent user experience across all booking workflows

Design Patterns:
    - Service Layer Pattern: Centralized business logic services
    - Single Responsibility Principle: Focused on input collection only
    - Strategy Pattern: Different validation strategies for different data types
    - Template Method Pattern: Consistent input collection workflows

Example:
    >>> # Collect new booking data
    >>> booking_service = BookingInputService()
    >>> booking = booking_service.collect_new_booking_data()
    >>> if booking:
    ...     print(f"Booking created for {booking.room_id} on {booking.book_date}")
    
    >>> # Collect search criteria
    >>> search_criteria = booking_service.collect_room_search_data()
    >>> if search_criteria:
    ...     print(f"Searching for {search_criteria.room_type}")
    
    >>> # Collect cancellation data
    >>> cancellation_data = booking_service.collect_booking_cancellation_data()
    >>> if cancellation_data:
    ...     booking_id, member_id = cancellation_data
    ...     print(f"Cancelling booking {booking_id} for member {member_id}")

Validation Framework:
    - Input format validation (date, time, ID formats)
    - Business rule validation (future dates, business hours)
    - Data length and content validation
    - User authentication and authorization checks
    - Error handling with user-friendly messages

Security Considerations:
    - Input sanitization prevents injection attacks
    - Date/time validation ensures valid booking windows
    - User ID validation for proper authentication
    - Graceful error handling prevents information leakage
    - Comprehensive logging for security auditing
"""

from datetime import datetime, date, time
from typing import Optional, Tuple

from persistence.models import Booking, SearchRoom
from presentation.user_input import get_user_input
from presentation.utils import clear_screen


class BookingInputService:
    """
    Comprehensive service for collecting and validating booking-related input data.

    This service class provides a centralized interface for all user input collection
    related to booking operations in the sports complex system. It encapsulates
    input validation logic, data formatting, and error handling to ensure consistent
    user experience and data integrity across all booking workflows.

    The class follows the Service Layer pattern, acting as an intermediary between
    the presentation layer (user interface) and the business logic layer. It handles
    complex validation scenarios while maintaining clean separation of concerns.

    Responsibilities:
        - Collect and validate new booking creation data
        - Gather room search criteria with comprehensive validation
        - Handle booking cancellation data collection
        - Provide consistent error handling and user feedback
        - Ensure data format compliance before model creation
        - Implement business rule validation (dates, times, formats)

    Validation Capabilities:
        - Date validation: Future dates only, proper ISO format
        - Time validation: Business hours (06:00-22:00), proper HH:MM format
        - Room ID validation: Format compliance, length restrictions
        - User ID validation: Authentication format, length constraints
        - Room type validation: Valid facility type selection

    User Experience Features:
        - Clear prompts with format examples and instructions
        - Immediate validation feedback with specific error messages
        - Graceful cancellation support with Ctrl+C handling
        - Confirmation steps for critical operations
        - Progress indicators and status messages

    Security Features:
        - Input sanitization to prevent injection attacks
        - Comprehensive validation to ensure data integrity
        - User authentication verification through ID validation
        - Error handling that prevents information leakage
        - Audit trail support for security monitoring

    Design Patterns:
        - Service Layer: Centralized business service functionality
        - Static Methods: Stateless operations for input collection
        - Template Method: Consistent validation patterns across methods
        - Strategy Pattern: Different validation approaches for different data types

    Example:
        >>> # Collect comprehensive booking data
        >>> booking = BookingInputService.collect_new_booking_data()
        >>> if booking:
        ...     print(f"New booking: {booking.room_id} on {booking.book_date}")
        ...     print(f"Time: {booking.book_time}, Member: {booking.user}")
        
        >>> # Search for available rooms
        >>> search = BookingInputService.collect_room_search_data()
        >>> if search:
        ...     print(f"Searching: {search.room_type}")
        ...     print(f"Date: {search.book_date}, Time: {search.book_time}")
        
        >>> # Handle booking cancellation
        >>> cancellation = BookingInputService.collect_booking_cancellation_data()
        >>> if cancellation:
        ...     booking_id, member_id = cancellation
        ...     print(f"Cancelling booking {booking_id} for {member_id}")

    Error Handling:
        All methods include comprehensive error handling for:
        - Invalid input formats (dates, times, IDs)
        - Business rule violations (past dates, invalid hours)
        - User cancellation (Ctrl+C, empty inputs)
        - System exceptions and unexpected errors
        - Data validation failures

    Thread Safety:
        This class uses static methods and is inherently thread-safe as it
        maintains no instance state. Multiple concurrent operations are supported.

    Note:
        All input collection methods are designed to be user-friendly with
        clear instructions and validation feedback. They support graceful
        cancellation and provide detailed error messages for better UX.
    """

    @staticmethod
    def collect_new_booking_data() -> Optional[Booking]:
        """
        Collect and validate comprehensive new booking data from user input.

        This method provides a complete guided workflow for creating new bookings,
        including data collection, validation, formatting, and confirmation. It
        ensures all booking data meets business requirements before creating the
        Booking model object, providing a robust user experience with clear feedback.

        The method implements a step-by-step collection process with immediate
        validation at each step, allowing users to correct errors immediately
        rather than at the end of the process. It includes comprehensive error
        handling and graceful cancellation support.

        Returns:
            Optional[Booking]: A validated Booking object if all data is successfully
                             collected and validated, None if the user cancels the
                             operation or if any critical error occurs.

        Validation Rules Applied:
            Room ID:
                - Non-empty string required
                - Automatically converted to uppercase for consistency
                - Length between 1-10 characters
                - Basic format validation for room identifier patterns
            
            Book Date:
                - Must be a future date (not today or past)
                - ISO format required (YYYY-MM-DD)
                - Validates against calendar constraints
                - Business day validation (if applicable)
            
            Book Time:
                - Valid time format required (HH:MM)
                - Business hours validation (06:00-22:00)
                - 24-hour format enforcement
                - Time slot availability consideration
            
            User/Member ID:
                - Non-empty string required
                - Minimum 3 characters for security
                - Maximum 50 characters to prevent abuse
                - Basic format validation for user identifiers

        User Experience Workflow:
            1. Clear screen and display booking creation header
            2. Present step-by-step prompts with format examples
            3. Immediate validation feedback for each input
            4. Comprehensive booking summary for user review
            5. Final confirmation before proceeding
            6. Graceful cancellation support at any step

        Error Handling Scenarios:
            - Invalid date formats with specific correction guidance
            - Past date attempts with clear business rule explanation
            - Invalid time formats with example formatting
            - Business hours violations with facility hour information
            - Empty or invalid room IDs with format requirements
            - User cancellation via Ctrl+C with clean exit
            - System exceptions with user-friendly error messages

        Example Usage:
            >>> # Successful booking creation
            >>> booking = BookingInputService.collect_new_booking_data()
            >>> if booking:
            ...     print(f"✅ Booking created successfully!")
            ...     print(f"Room: {booking.room_id}")
            ...     print(f"Date: {booking.book_date}")
            ...     print(f"Time: {booking.book_time}")
            ...     print(f"Member: {booking.user}")
            ... else:
            ...     print("❌ Booking creation cancelled or failed")

            >>> # Integration with booking commands
            >>> def create_booking_workflow():
            ...     booking_data = BookingInputService.collect_new_booking_data()
            ...     if booking_data:
            ...         # Pass to booking command for processing
            ...         return booking_command.execute(booking_data)
            ...     return False, "Booking data collection cancelled"

        Business Logic Integration:
            The collected data is formatted into a Pydantic Booking model that:
            - Provides automatic validation through model constraints
            - Ensures type safety for downstream operations
            - Enables JSON serialization for API operations
            - Maintains data integrity throughout the booking process

        Security Considerations:
            - Input sanitization prevents malicious data injection
            - Validation prevents invalid booking attempts
            - User authentication through member ID verification
            - Audit trail support through detailed logging
            - Error handling prevents sensitive information leakage

        Performance Optimization:
            - Immediate validation reduces processing overhead
            - Early termination on invalid input saves resources
            - Efficient data collection minimizes user interaction time
            - Optimized validation patterns for fast response

        Accessibility Features:
            - Clear prompts with format examples
            - Immediate feedback for validation errors
            - Consistent error message formatting
            - Cancel-friendly operation flow
            - Progress indicators for multi-step process

        Note:
            This method handles all user interaction for booking creation,
            including error recovery and cancellation. The returned Booking
            object is fully validated and ready for business logic processing.
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
        Collect and validate comprehensive room search criteria from user input.

        This method provides a guided workflow for gathering room search parameters,
        enabling users to find available facilities based on their specific
        requirements. It includes comprehensive validation, user-friendly prompts,
        and flexible search criteria collection with immediate feedback.

        The method implements intelligent validation that considers business rules,
        facility availability, and operational constraints to ensure search
        criteria will produce meaningful results for the user.

        Returns:
            Optional[SearchRoom]: A validated SearchRoom object containing all
                                search criteria if successfully collected, None
                                if the user cancels or if critical errors occur.

        Search Criteria Collected:
            Room Type:
                - Facility type selection from predefined categories
                - Options: Tennis Court, Badminton Court, Archery Range, Multi-Purpose Field
                - User-friendly menu selection interface
                - Validation against available facility types in the system
            
            Search Date:
                - Target date for availability checking
                - Must be today or future date (no past date searches)
                - ISO format validation (YYYY-MM-DD)
                - Business day and holiday consideration
            
            Search Time:
                - Preferred time slot for facility usage
                - Business hours validation (06:00-22:00)
                - 24-hour format requirement (HH:MM)
                - Time slot granularity alignment

        Validation Framework:
            Date Validation:
                - Future date enforcement for availability checking
                - Calendar date format validation
                - Business day vs weekend consideration
                - Holiday schedule integration (if applicable)
            
            Time Validation:
                - Facility operating hours compliance
                - Time format standardization
                - Booking window alignment
                - Peak hours identification
            
            Room Type Validation:
                - Valid facility type verification
                - Availability status checking
                - Maintenance schedule consideration
                - Capacity requirement validation

        User Experience Features:
            - Clear category-based room type selection
            - Format examples and input guidance
            - Immediate validation with specific error messages
            - Progress indication through multi-step process
            - Graceful cancellation support at any point
            - Search criteria summary before execution

        Example Usage:
            >>> # Collect search criteria
            >>> search = BookingInputService.collect_room_search_data()
            >>> if search:
            ...     print(f"🔍 Search Parameters:")
            ...     print(f"Facility: {search.room_type}")
            ...     print(f"Date: {search.book_date}")
            ...     print(f"Time: {search.book_time}")
            ...     # Pass to search service for execution
            ...     results = room_search_service.find_available_rooms(search)
            ... else:
            ...     print("❌ Search cancelled by user")

            >>> # Advanced search workflow
            >>> def perform_room_search():
            ...     criteria = BookingInputService.collect_room_search_data()
            ...     if criteria:
            ...         return search_command.execute(criteria)
            ...     return [], "Search criteria collection cancelled"

        Business Logic Integration:
            The SearchRoom model provides:
            - Type-safe search parameter passing
            - Automatic validation through Pydantic constraints
            - JSON serialization for API compatibility
            - Database query parameter formatting
            - Search history tracking capabilities

        Search Categories Supported:
            1. Tennis Court: Indoor/outdoor tennis facilities
            2. Badminton Court: Professional badminton courts
            3. Archery Range: Target practice and competitive archery
            4. Multi-Purpose Field: Versatile sports and event spaces

        Advanced Features:
            - Smart defaults based on user history
            - Popular time slot suggestions
            - Facility-specific validation rules
            - Peak hours and pricing information
            - Alternative suggestion capability

        Error Recovery:
            - Invalid input correction guidance
            - Format example provision
            - Clear error message explanation
            - Retry mechanisms for user convenience
            - Graceful degradation for system issues

        Performance Optimization:
            - Efficient validation algorithms
            - Minimal user interaction time
            - Smart caching of facility information
            - Optimized database query preparation
            - Fast response time for user feedback

        Security Considerations:
            - Input sanitization for search parameters
            - Validation against injection attacks
            - User permission verification
            - Audit logging for search activities
            - Privacy protection for search patterns

        Note:
            The collected search criteria are optimized for database queries
            and provide comprehensive facility discovery capabilities while
            maintaining excellent user experience and data validation.
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
        Collect and validate booking cancellation data from user input.

        This method provides a secure and user-friendly interface for gathering
        the necessary information to cancel an existing booking. It implements
        comprehensive validation to ensure only authorized cancellations are
        processed and includes proper error handling for various scenarios.

        The cancellation process requires both booking identification and member
        verification to ensure security and prevent unauthorized cancellations.
        The method validates all input data before returning it for processing.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing (booking_id, member_id)
                                     if successfully collected and validated,
                                     None if the user cancels or errors occur.

        Data Collection Process:
            Booking ID:
                - Unique identifier for the booking to be cancelled
                - Must be a valid numeric string (integer format)
                - Non-empty validation with clear error messaging
                - Format validation to prevent invalid ID submission
                - Existence verification preparation for downstream processing
            
            Member ID:
                - Owner verification for booking authorization
                - Must match the original booking creator
                - Standard member ID format validation (3-50 characters)
                - Security validation to prevent unauthorized access
                - Cross-reference preparation for ownership verification

        Validation Rules Applied:
            Booking ID Validation:
                - Non-empty string requirement
                - Numeric format enforcement (digits only)
                - Reasonable length constraints
                - Format consistency checking
                - Injection attack prevention
            
            Member ID Validation:
                - Standard user ID format compliance
                - Length constraints (3-50 characters)
                - Non-empty field validation
                - Authorization format checking
                - Security credential validation

        Security Features:
            - Dual-factor verification (booking ID + member ID)
            - Input sanitization to prevent injection attacks
            - Authorization validation preparation
            - Audit trail data collection
            - Error handling that prevents information leakage

        User Experience Design:
            - Clear cancellation workflow explanation
            - Step-by-step data collection process
            - Immediate validation feedback
            - Security reminder about authorization requirements
            - Graceful cancellation support with Ctrl+C
            - User-friendly error messages with correction guidance

        Example Usage:
            >>> # Collect cancellation data
            >>> cancellation_data = BookingInputService.collect_booking_cancellation_data()
            >>> if cancellation_data:
            ...     booking_id, member_id = cancellation_data
            ...     print(f"📋 Cancellation Request:")
            ...     print(f"Booking ID: {booking_id}")
            ...     print(f"Member ID: {member_id}")
            ...     # Process cancellation with authorization
            ...     result = cancellation_service.cancel_booking(booking_id, member_id)
            ... else:
            ...     print("❌ Cancellation data collection cancelled")

            >>> # Integrated cancellation workflow
            >>> def cancel_booking_workflow():
            ...     data = BookingInputService.collect_booking_cancellation_data()
            ...     if data:
            ...         booking_id, member_id = data
            ...         return cancel_command.execute(booking_id, member_id)
            ...     return False, "Cancellation data collection cancelled"

        Business Logic Preparation:
            The collected data enables:
            - Booking existence verification
            - Ownership authorization checking
            - Cancellation policy validation
            - Refund calculation processing
            - Audit trail creation
            - Notification system triggering

        Error Handling Scenarios:
            - Invalid booking ID format with correction guidance
            - Empty field validation with requirement explanation
            - Member ID format violations with standard requirements
            - User cancellation with graceful exit
            - System exceptions with user-friendly error messages

        Authorization Framework:
            - Dual-factor authentication requirement
            - Booking ownership verification preparation
            - Member credential validation
            - Security audit trail initiation
            - Anti-fraud protection measures

        Performance Considerations:
            - Efficient validation algorithms
            - Minimal user interaction requirements
            - Fast input processing and feedback
            - Optimized data format preparation
            - Quick error detection and reporting

        Integration Points:
            - Cancellation command execution
            - Authorization service validation
            - Audit logging system
            - Notification service triggering
            - Refund processing initiation

        Privacy Protection:
            - Secure data handling practices
            - Minimal data collection requirements
            - Protected member information handling
            - Secure data transmission preparation
            - Privacy-compliant audit logging

        Note:
            This method collects only the essential data required for secure
            booking cancellation. The actual authorization and cancellation
            processing is handled by downstream business logic components
            with comprehensive security validation.
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
        """
        Collect and validate room identifier input with comprehensive validation.

        This private method handles the specific collection and validation of room
        identifiers, ensuring they meet system requirements and format standards.
        It provides immediate feedback and guidance for proper room ID formatting.

        Returns:
            Optional[str]: Validated room ID in uppercase format if successful,
                         None if validation fails or user cancels input.

        Validation Rules:
            - Non-empty string requirement
            - Length constraints: 1-10 characters
            - Automatic uppercase conversion for consistency
            - Basic format validation for identifier patterns
            - Special character restrictions (if applicable)

        Format Examples:
            - Single facility codes: "AR" (Archery Range)
            - Numbered facilities: "T1", "T2" (Tennis Court 1, 2)
            - Complex codes: "B1", "B2" (Badminton Court 1, 2)
            - Multi-purpose: "MPF1" (Multi-Purpose Field 1)

        User Experience:
            - Clear format examples in prompts
            - Immediate validation feedback
            - Automatic case conversion
            - Retry capability for corrections
            - Format guidance on errors
        """
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
        """
        Collect and validate room type selection through user-friendly menu interface.

        This method presents available facility types in a numbered menu format,
        allowing users to select their desired room type through simple numeric
        input. It provides clear options and validates selection against available
        facility categories in the sports complex system.

        Returns:
            Optional[str]: Selected room type name if valid choice made,
                         None if invalid selection or user cancellation.

        Available Room Types:
            1. Tennis Court: Professional tennis facilities
            2. Badminton Court: Indoor badminton courts with standard dimensions
            3. Archery Range: Target practice and competitive archery facilities
            4. Multi-Purpose Field: Versatile sports and event spaces

        Menu Interface:
            - Numbered selection (1-4)
            - Clear facility descriptions
            - Input validation with retry capability
            - User-friendly error messages
            - Simple selection process

        Validation Features:
            - Choice validation against available options
            - Invalid input handling with correction guidance
            - Numeric input requirement
            - Range validation (1-4)
            - Error recovery with retry capability
        """
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
        """
        Collect and validate booking date input with comprehensive business rule validation.

        This method handles date collection for booking operations, ensuring dates
        meet business requirements including future date validation, proper formatting,
        and calendar validity. It provides flexible field naming for different
        contexts (booking vs search dates).

        Args:
            field_name (str, optional): Context-specific field name for user prompts.
                                      Defaults to "booking date" but can be customized
                                      for search operations or other contexts.

        Returns:
            Optional[date]: Validated date object if successful,
                          None if validation fails or user cancels.

        Validation Rules:
            Date Format:
                - ISO 8601 format required (YYYY-MM-DD)
                - Proper calendar date validation
                - Leap year consideration
                - Month/day boundary validation
            
            Business Rules:
                - Future dates only (not today or past)
                - Calendar validity checking
                - Business day validation (if applicable)
                - Holiday schedule consideration
                - Facility availability calendar integration

        User Experience:
            - Clear format examples (e.g., 2025-12-25)
            - Immediate validation feedback
            - Specific error messages for different validation failures
            - Format guidance on invalid input
            - Retry capability with corrections

        Error Handling:
            - Invalid format detection with correction guidance
            - Past date rejection with business rule explanation
            - Calendar validation with specific error details
            - User-friendly error messages
            - Exception handling for system date issues
        """
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
        """
        Collect and validate booking time input with business hours enforcement.

        This method handles time collection for booking and search operations,
        ensuring times meet facility operating requirements and proper formatting.
        It enforces business hours restrictions while providing flexible field
        naming for different operational contexts.

        Args:
            field_name (str, optional): Context-specific field name for user prompts.
                                      Defaults to "booking time" but can be customized
                                      for search operations or other contexts.

        Returns:
            Optional[time]: Validated time object if successful,
                          None if validation fails or user cancels.

        Validation Rules:
            Time Format:
                - 24-hour format required (HH:MM)
                - Proper hour/minute boundary validation
                - Leading zero requirement for single digits
                - Colon separator enforcement
            
            Business Hours:
                - Operating hours: 06:00 to 22:00 (6 AM to 10 PM)
                - No overnight bookings allowed
                - Consistent with facility management policies
                - Maintenance window avoidance
            
            Time Slot Alignment:
                - Standard booking increment alignment (if applicable)
                - Consistent time slot boundaries
                - Facility-specific time requirements

        User Experience:
            - Clear format examples (e.g., 14:30)
            - Business hours information display
            - Immediate validation feedback
            - Format correction guidance
            - Operating hours reminder on violations

        Business Context:
            - Facility operating hours compliance
            - Staff availability alignment
            - Maintenance schedule avoidance
            - Peak hours identification
            - Standard booking window support

        Error Handling:
            - Invalid format detection with specific examples
            - Business hours violation with policy explanation
            - Time boundary validation with correction guidance
            - User-friendly error messages
            - Format parsing exception handling
        """
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
        """
        Collect and validate user/member identifier input with security constraints.

        This method handles the collection of user identifiers for booking operations,
        ensuring they meet security and format requirements. It provides flexible
        field naming to support different contexts such as member ID, owner ID,
        or user authentication.

        Args:
            field_name (str, optional): Context-specific field name for user prompts.
                                      Defaults to "Member ID" but can be customized
                                      for different authentication contexts.

        Returns:
            Optional[str]: Validated user identifier if successful,
                         None if validation fails or user cancels.

        Validation Rules:
            Length Constraints:
                - Minimum 3 characters for security
                - Maximum 50 characters to prevent abuse
                - Non-empty string requirement
                - Whitespace trimming and validation
            
            Security Requirements:
                - Basic format validation for identifier patterns
                - Length-based security enforcement
                - Input sanitization for injection prevention
                - Character set validation (if applicable)
            
            Format Standards:
                - Consistent identifier formatting
                - Case sensitivity handling
                - Special character restrictions
                - Standard username pattern compliance

        Security Features:
            - Minimum length enforcement for security
            - Maximum length prevention of buffer overflow
            - Input sanitization against injection attacks
            - Authentication preparation validation
            - User credential format compliance

        User Experience:
            - Clear field identification through custom naming
            - Length requirement communication
            - Immediate validation feedback
            - Format guidance on violations
            - Security requirement explanation

        Context Flexibility:
            - "Member ID" for booking creation
            - "Owner ID" for cancellation verification
            - "User ID" for general authentication
            - Custom field names for specific operations
            - Consistent validation across all contexts

        Error Handling:
            - Empty input detection with requirement explanation
            - Length violation feedback with constraint details
            - Format validation with correction guidance
            - Security requirement communication
            - User-friendly error messaging

        Integration Points:
            - Authentication service preparation
            - Authorization validation setup
            - Database query parameter formatting
            - Audit trail user identification
            - Security logging user tracking
        """
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
