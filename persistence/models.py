"""
Data models for the Sports Booking Management System using Pydantic.

This module defines the core data models that represent the business entities
in the sports booking system. All models use Pydantic for data validation,
serialization, and type safety, ensuring data integrity throughout the application.

The models serve as the foundation for data transfer between different layers
of the application (presentation, business logic, and persistence) and provide
a consistent data structure for all booking-related operations.

Classes:
    Member: Represents a registered user/member in the system.
    SearchRoom: Represents room search criteria with date and time constraints.
    Booking: Represents a room booking with associated member and schedule details.

Dependencies:
    - datetime.date: Date handling for booking dates
    - datetime.time: Time handling for booking times
    - pydantic.BaseModel: Base class providing validation and serialization

Features:
    - Automatic data validation through Pydantic
    - Type safety with Python type hints
    - JSON serialization/deserialization support
    - Immutable data structures for data integrity
    - Clear separation of business entities

Example:
    >>> # Create a new member
    >>> member = Member(
    ...     id="user123",
    ...     password="securepass",
    ...     email="user@example.com"
    ... )

    >>> # Create search criteria
    >>> search = SearchRoom(
    ...     room_type="gymnasium",
    ...     book_date=date(2025, 8, 25),
    ...     book_time=time(14, 30)
    ... )

    >>> # Create a booking
    >>> booking = Booking(
    ...     room_id="gym_001",
    ...     book_date=date(2025, 8, 25),
    ...     book_time=time(14, 30),
    ...     user="user123"
    ... )

Design Patterns:
    - Data Transfer Object (DTO): Clean data structures for layer communication
    - Value Object: Immutable data representations
    - Domain Model: Business entity representations
"""

from datetime import date, time

from pydantic import BaseModel


class Member(BaseModel):
    """
    Represents a registered member/user in the sports booking system.

    This model encapsulates all essential information about a system member,
    including their unique identifier, authentication credentials, and contact
    information. The model serves as the primary user entity for authentication,
    authorization, and booking operations.

    The Member model enforces data validation through Pydantic, ensuring that
    all member data meets the required format and constraints before being
    processed by the business logic layer.

    Attributes:
        id (str): Unique member identifier. Used for login and as primary key
                 in database operations. Must be unique across all members.
        password (str): Member's authentication password. Should be hashed
                       before storage for security. Used for login verification.
        email (str): Member's email address. Used for communication and
                    potentially as alternative login method.

    Validation Features:
        - Automatic type checking for all fields
        - Data format validation through Pydantic
        - JSON serialization/deserialization support
        - Immutable data structure after creation

    Usage Context:
        - User registration and authentication
        - Member profile management
        - Booking ownership tracking
        - Communication and notifications

    Example:
        >>> # Create a new member
        >>> member = Member(
        ...     id="john_doe_2025",
        ...     password="SecurePassword123!",
        ...     email="john.doe@sportscenter.com"
        ... )
        >>> print(member.id)
        'john_doe_2025'

        >>> # JSON serialization
        >>> member_json = member.model_dump_json()
        >>> print(member_json)
        '{"id":"john_doe_2025","password":"SecurePassword123!","email":"john.doe@sportscenter.com"}'

        >>> # Create from dictionary
        >>> member_data = {
        ...     "id": "alice_smith",
        ...     "password": "MySecretPass",
        ...     "email": "alice@email.com"
        ... }
        >>> member = Member(**member_data)

    Security Considerations:
        - Password should be hashed before database storage
        - Email should be validated for proper format
        - ID should be checked for uniqueness
        - Consider implementing password strength requirements

    Database Mapping:
        This model typically maps to a 'members' table with corresponding
        columns for id, password_hash, and email fields.

    Note:
        This model represents the core member data. Additional profile
        information (name, phone, address) could be added as needed.
    """

    id: str
    password: str
    email: str


class SearchRoom(BaseModel):
    """
    Represents search criteria for finding available rooms in the sports booking system.

    This model encapsulates the parameters used to search for available rooms
    based on room type, desired booking date, and preferred time slot. It serves
    as a structured way to pass search criteria between the presentation layer
    and business logic, ensuring consistent search operations.

    The SearchRoom model enables complex room availability queries while
    maintaining type safety and data validation through Pydantic.

    Attributes:
        room_type (str): Type of sports facility being searched for.
                        Examples: "gymnasium", "tennis_court", "swimming_pool",
                        "basketball_court", "meeting_room", "fitness_studio".
        book_date (date): The date for which room availability is being checked.
                         Must be a valid date object, typically today or future dates.
        book_time (time): The preferred time slot for the booking.
                         Represents the start time of the desired booking period.

    Validation Features:
        - Automatic date/time format validation
        - Type checking for all search parameters
        - Immutable search criteria structure
        - JSON serialization for API compatibility

    Usage Context:
        - Room availability searches
        - Filtering available time slots
        - Booking prerequisite validation
        - Search history tracking

    Example:
        >>> from datetime import date, time

        >>> # Search for gymnasium on specific date and time
        >>> search = SearchRoom(
        ...     room_type="gymnasium",
        ...     book_date=date(2025, 8, 25),
        ...     book_time=time(14, 30)  # 2:30 PM
        ... )

        >>> # Search for tennis court tomorrow morning
        >>> tomorrow = date.today() + timedelta(days=1)
        >>> morning_search = SearchRoom(
        ...     room_type="tennis_court",
        ...     book_date=tomorrow,
        ...     book_time=time(9, 0)  # 9:00 AM
        ... )

        >>> # Convert to dictionary for database queries
        >>> search_params = search.model_dump()
        >>> print(search_params)
        {'room_type': 'gymnasium', 'book_date': datetime.date(2025, 8, 25), 'book_time': datetime.time(14, 30)}

    Business Logic Integration:
        - Used by room search commands to filter available rooms
        - Validates search parameters before database queries
        - Enables complex availability checking algorithms
        - Supports time slot conflict detection

    Database Integration:
        Search criteria are typically used in SQL queries to find rooms where:
        - room_type matches the facility type
        - book_date has available slots
        - book_time doesn't conflict with existing bookings

    Extended Features:
        Future enhancements could include:
        - Duration field for booking length
        - Capacity requirements
        - Equipment preferences
        - Price range filters

    Note:
        The time field represents the start time of the desired booking.
        Booking duration and end time are typically handled in business logic.
    """

    room_type: str
    book_date: date
    book_time: time


class Booking(BaseModel):
    """
    Represents a confirmed room booking in the sports booking system.

    This model encapsulates all essential information about a completed booking,
    including the reserved room, scheduled date and time, and the member who
    made the reservation. It serves as the primary entity for tracking and
    managing all booking operations in the system.

    The Booking model ensures data integrity for confirmed reservations and
    provides a structured format for booking-related operations including
    creation, modification, cancellation, and reporting.

    Attributes:
        room_id (str): Unique identifier of the booked room/facility.
                      References a specific room in the room inventory.
                      Examples: "gym_001", "tennis_a", "pool_main", "studio_2".
        book_date (date): The date when the room is booked/reserved.
                         Must be a valid date, typically today or future dates.
        book_time (time): The start time of the booking period.
                         Represents when the member's reservation begins.
        user (str): Identifier of the member who made the booking.
                   References the Member.id field for ownership tracking.

    Validation Features:
        - Automatic date/time validation through Pydantic
        - Type safety for all booking attributes
        - Immutable booking record after creation
        - JSON serialization for storage and API operations

    Business Rules:
        - Each booking represents a time slot reservation
        - One booking per room per time slot (no double booking)
        - Member must exist in the system (foreign key relationship)
        - Room must be available for the specified date/time

    Usage Context:
        - Confirmed reservation records
        - Booking history tracking
        - Schedule conflict checking
        - Payment and billing operations
        - Cancellation and modification tracking

    Example:
        >>> from datetime import date, time

        >>> # Create a new booking
        >>> booking = Booking(
        ...     room_id="gymnasium_01",
        ...     book_date=date(2025, 8, 25),
        ...     book_time=time(15, 30),  # 3:30 PM
        ...     user="member_123"
        ... )

        >>> # Convert to dictionary for database storage
        >>> booking_data = booking.model_dump()
        >>> print(booking_data)
        {
            'room_id': 'gymnasium_01',
            'book_date': datetime.date(2025, 8, 25),
            'book_time': datetime.time(15, 30),
            'user': 'member_123'
        }

        >>> # Create booking from API data
        >>> api_data = {
        ...     "room_id": "tennis_court_a",
        ...     "book_date": "2025-08-26",
        ...     "book_time": "10:00:00",
        ...     "user": "alice_smith"
        ... }
        >>> booking = Booking(**api_data)

        >>> # Access booking details
        >>> print(f"Room: {booking.room_id}")
        >>> print(f"Date: {booking.book_date}")
        >>> print(f"Time: {booking.book_time}")
        >>> print(f"Member: {booking.user}")

    Database Integration:
        This model typically maps to a 'bookings' or 'member_bookings' table with:
        - Primary key (booking_id, often auto-generated)
        - Foreign key to rooms table (room_id)
        - Foreign key to members table (user)
        - Date and time fields for scheduling
        - Additional fields like payment_status, created_at, etc.

    State Management:
        Bookings can have various states:
        - Confirmed: Active reservation
        - Cancelled: User-cancelled booking
        - Completed: Past booking that occurred
        - No-show: Booking where member didn't appear

    Extended Features:
        Future enhancements could include:
        - Booking duration (end_time field)
        - Payment status and amount
        - Booking status (confirmed, cancelled, completed)
        - Special requirements or notes
        - Recurring booking support

    Note:
        This model represents the core booking data. Additional booking
        metadata (payment info, status, timestamps) are typically stored
        in related database tables or extended models.
    """

    room_id: str
    book_date: date
    book_time: time
    user: str


if __name__ == "__main__":
    """
    Demonstration and testing module for Pydantic models.
    
    This section provides practical examples of model usage, demonstrating
    how to create, validate, and work with the sports booking system models.
    It serves both as documentation and as a basic test to verify model
    functionality and validation capabilities.
    
    The examples show:
    - Model instantiation with valid data
    - Automatic validation through Pydantic
    - JSON serialization capabilities
    - Model representation and display
    
    Usage:
        Run this module directly to see model examples:
        $ python models.py
    
    Expected Output:
        Display of a sample Member object with all its attributes
        formatted according to Pydantic's default representation.
    
    Example Output:
        Member(id='shalow21', password='HelloWorld21', email='shalow21@gmail.com')
    
    Additional Examples:
        The following examples demonstrate extended model usage:
    """
    # Original example - Member creation and display
    member = Member(id="shalow21", password="HelloWorld21", email="shalow21@gmail.com")
    print("Member Example:")
    print(member)
    print()

    # Additional examples for demonstration
    from datetime import date, time

    # SearchRoom example
    search = SearchRoom(
        room_type="gymnasium", book_date=date(2025, 8, 25), book_time=time(14, 30)
    )
    print("SearchRoom Example:")
    print(search)
    print(
        f"Searching for: {search.room_type} on {search.book_date} at {search.book_time}"
    )
    print()

    # Booking example
    booking = Booking(
        room_id="gym_001",
        book_date=date(2025, 8, 25),
        book_time=time(14, 30),
        user="shalow21",
    )
    print("Booking Example:")
    print(booking)
    print(
        f"Booking: {booking.room_id} for {booking.user} on {booking.book_date} at {booking.book_time}"
    )
    print()

    # JSON serialization example
    print("JSON Serialization Examples:")
    print("Member JSON:", member.model_dump_json())
    print("SearchRoom JSON:", search.model_dump_json())
    print("Booking JSON:", booking.model_dump_json())
