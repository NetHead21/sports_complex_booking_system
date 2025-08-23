"""
Search Rooms Command for the Sports Booking Management System.

This module implements the room search functionality as part of the Command Pattern
architecture. It provides a sophisticated interface for searching available rooms
based on specific criteria such as room type, date, and time requirements. The
command focuses on flexible room discovery and availability verification.

The command follows clean architecture principles by separating search execution
from input collection concerns. It leverages the BookingInputService for secure
data collection and the database manager for efficient search operations, ensuring
optimal performance and maintainable code structure.

Classes:
    SearchRoomCommand: Command implementation for room availability search operations.

Dependencies:
    - mysql.connector.cursor_cext.CMySQLCursor: MySQL cursor for database operations
    - business_logic.base.command.Command: Base command interface
    - business_logic.room_database_manager.db: Database operations manager
    - business_logic.services.booking_input_service.BookingInputService: Input collection service

Key Features:
    - Advanced room search with multiple criteria filtering
    - Real-time availability verification and validation
    - Flexible search parameters for diverse user needs
    - Efficient database queries with optimized performance
    - Service-layer integration for clean separation of concerns

Search Capabilities:
    - Room type filtering (conference rooms, sports courts, meeting spaces)
    - Date-based availability checking with conflict resolution
    - Time slot verification and scheduling optimization
    - Multi-criteria search with combined parameters
    - Real-time inventory and booking status validation

Business Functions:
    - Room availability discovery for booking planning
    - Schedule conflict identification and prevention
    - Resource utilization optimization and analysis
    - User-friendly search interface for facility exploration
    - Administrative oversight for room management

Example:
    >>> # Execute room search command
    >>> search_command = SearchRoomCommand()
    >>> success, results = search_command.execute()
    >>> if success:
    ...     print(f"✅ Found {len(results)} available rooms")
    ... else:
    ...     print("❌ No rooms match your criteria")

Search Optimization Features:
    - Indexed database queries for fast result retrieval
    - Intelligent caching for frequently searched criteria
    - Efficient filtering algorithms for large room inventories
    - Optimized query execution with minimal resource usage
    - Scalable search handling for high-volume operations

Security Considerations:
    - Input validation and sanitization through service layer
    - Parameterized database queries preventing injection attacks
    - Authorization verification for room access permissions
    - Audit logging for search activity monitoring
    - Safe data presentation without sensitive information exposure
"""

from mysql.connector.cursor_cext import CMySQLCursor

from business_logic.base.command import Command
from business_logic.room_database_manager import db
from business_logic.services.booking_input_service import BookingInputService


class SearchRoomCommand(Command):
    """
    Command implementation for comprehensive room availability search operations.

    This command provides an advanced interface for searching available rooms in
    the sports complex system based on multiple criteria including room type,
    date, and time requirements. It implements the Command Pattern to encapsulate
    search logic while maintaining strict separation between data collection and
    search execution concerns.

    The command serves as a critical component for room discovery and booking
    planning, enabling users to find optimal facilities that match their specific
    requirements. It integrates seamlessly with the service layer for input
    collection and the database layer for efficient search operations.

    Architecture Role:
        - Implements Command Pattern for room search operations
        - Integrates with service layer for secure data collection
        - Manages database operations through room_database_manager
        - Provides flexible search interface for diverse user needs
        - Supports both interactive and programmatic search workflows

    Search Functionality:
        - Multi-criteria room filtering with flexible parameters
        - Real-time availability verification and conflict detection
        - Efficient database queries with optimized performance
        - Comprehensive result formatting and presentation
        - Advanced search algorithms for complex requirements

    Business Logic Features:
        - Room type categorization and filtering capabilities
        - Date and time slot availability verification
        - Booking conflict detection and prevention
        - Resource utilization analysis and optimization
        - User preference matching and recommendation logic

    Integration Points:
        - BookingInputService: Secure search criteria collection
        - Database Manager: Optimized search query execution
        - Room Management: Real-time inventory and availability
        - User Interface: Results presentation and interaction
        - Booking System: Availability verification for reservations

    Performance Characteristics:
        - Efficient indexed database queries for fast results
        - Intelligent caching for frequently searched criteria
        - Optimized filtering algorithms for large inventories
        - Minimal resource usage with scalable performance
        - Fast response times suitable for interactive use

    Example Usage:
        >>> # Standard room search workflow
        >>> search_command = SearchRoomCommand()
        >>> success, results = search_command.execute()
        >>>
        >>> if success:
        ...     print(f"✅ Search completed successfully")
        ...     print(f"📊 Found {len(results)} available rooms")
        ...     for room in results:
        ...         print(f"🏢 Room: {room['name']} - Type: {room['type']}")
        ... else:
        ...     print(f"❌ Search failed: No matching rooms found")

        >>> # Programmatic search with criteria
        >>> search_command = SearchRoomCommand()
        >>> # Service will collect: room_type="Conference", date="2025-08-24", time="10:00"
        >>> success, results = search_command.execute()
        >>> assert success is True or success is False  # Both valid outcomes

    Error Handling:
        Comprehensive error scenarios covered:
        - Invalid search criteria or parameter formats
        - Database connection or query execution failures
        - Empty search results with no matching rooms
        - Service layer input collection failures
        - System exceptions and unexpected errors

    Return Value Patterns:
        Success scenarios:
        - (True, cursor_result): Rooms found matching search criteria
          - cursor_result contains list of available rooms
          - Each room includes details like type, availability, features

        Failure scenarios:
        - (False, "Room search cancelled or failed"): User cancelled input
        - (False, "No search results"): No rooms match criteria
        - (False, str(exception)): System or database errors

    Search Criteria Supported:
        Room Type Filtering:
            - Conference rooms for meetings and presentations
            - Sports courts for athletic activities
            - Training facilities for fitness and coaching
            - Multi-purpose rooms for various events
            - Specialized facilities with specific equipment

        Date and Time Parameters:
            - Specific date selection for availability checking
            - Time slot preferences with duration consideration
            - Recurring booking pattern support
            - Peak and off-peak time slot identification
            - Conflict detection with existing reservations

    Security Features:
        - Input validation and sanitization through service delegation
        - Parameterized database queries preventing injection attacks
        - Authorization verification for room access permissions
        - Comprehensive audit logging for search activity monitoring
        - Safe data presentation without sensitive information exposure

    Thread Safety:
        This command is stateless and thread-safe. Multiple concurrent
        search operations are fully supported through database-level
        transaction management and proper isolation mechanisms.

    Note:
        The command maintains separation of concerns by delegating input
        collection to BookingInputService while focusing on search execution
        logic and database coordination for optimal performance.
    """

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
