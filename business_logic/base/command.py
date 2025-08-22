"""
Command Pattern base class for the Sports Booking Management System.

This module defines the fundamental Command Pattern interface that serves as the
architectural foundation for all business logic operations in the sports booking
system. It provides a standardized contract for command execution, enabling loose
coupling between the presentation layer and business logic implementation.

The Command Pattern implementation allows for encapsulation of business operations
as objects, supporting features like operation queuing, logging, undo operations,
and macro commands. This design promotes maintainability, testability, and
extensibility throughout the application architecture.

Classes:
    Command: Abstract base class defining the command execution interface.

Dependencies:
    - abc.ABC: Abstract base class support for interface definition
    - abc.abstractmethod: Abstract method decorator for interface enforcement

Design Pattern:
    Command Pattern - Encapsulates operations as objects with a common interface

Key Benefits:
    - Loose coupling between presentation and business logic layers
    - Standardized execution interface across all business operations
    - Support for operation composition and chaining
    - Foundation for advanced features like undo/redo, macro commands
    - Consistent error handling and return value patterns
    - Enhanced testability through interface standardization

Architecture Integration:
    - Base class for all business logic commands
    - Interface contract for presentation layer option execution
    - Foundation for menu system command binding
    - Enables polymorphic command execution
    - Supports command composition and decorator patterns

Example:
    >>> # Implementing a concrete command
    >>> class AddMemberCommand(Command):
    ...     def execute(self, data):
    ...         # Business logic implementation
    ...         if self.validate_member_data(data):
    ...             member_id = self.member_service.create_member(data)
    ...             return True, f"Member {member_id} created successfully"
    ...         return False, "Invalid member data provided"
    
    >>> # Using commands polymorphically
    >>> commands = [AddMemberCommand(), BookRoomCommand(), CancelBookingCommand()]
    >>> for command in commands:
    ...     success, result = command.execute(user_data)
    ...     if success:
    ...         print(f"✅ {result}")
    ...     else:
    ...         print(f"❌ {result}")

Implementation Guidelines:
    - Always return tuple (success: bool, message: str)
    - Handle all exceptions within execute method
    - Validate input data before processing
    - Provide meaningful success/error messages
    - Log operations for audit trails
    - Follow single responsibility principle
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """
    Abstract base class for implementing the Command Pattern in the sports booking system.
    
    This class defines the fundamental interface that all business logic commands must
    implement. It serves as the architectural cornerstone for the entire command-based
    business logic system, ensuring consistent operation execution patterns and enabling
    loose coupling between the presentation layer and business operations.
    
    The Command Pattern implementation provides a standardized way to encapsulate
    business operations as objects with a common interface, supporting advanced
    features like operation composition, logging, error handling, and future
    enhancements such as undo/redo functionality.
    
    Architecture Role:
        - Base interface for all business logic operations
        - Contract definition for command execution
        - Foundation for polymorphic command handling
        - Integration point with presentation layer (Option class)
        - Enabler for command composition and chaining
    
    Design Pattern Benefits:
        - Encapsulation: Business operations wrapped as objects
        - Polymorphism: Uniform interface for different operations
        - Loose Coupling: Presentation layer independent of specific implementations
        - Extensibility: Easy addition of new commands without system changes
        - Testability: Standard interface enables consistent testing patterns
    
    Implementation Requirements:
        All concrete command classes must:
        1. Inherit from this Command base class
        2. Implement the execute() method with proper signature
        3. Return standardized tuple (success: bool, result: str)
        4. Handle all exceptions within the execute method
        5. Validate input data before processing
        6. Provide meaningful user feedback messages
    
    Return Value Convention:
        All execute() methods must return a tuple containing:
        - success (bool): True if operation completed successfully, False otherwise
        - result (str): Human-readable message describing the operation outcome
        
        Success examples:
        - (True, "Member added successfully with ID: M12345")
        - (True, "Room booked for 2025-08-25 at 14:30")
        
        Failure examples:
        - (False, "Invalid email format provided")
        - (False, "Room not available at specified time")
    
    Integration with Presentation Layer:
        The presentation layer's Option class expects this interface:
        ```python
        success, result = command.execute(data)
        if success:
            print(success_message.format(result=result))
        ```
    
    Example Implementations:
        >>> # Member management command
        >>> class AddMemberCommand(Command):
        ...     def execute(self, data):
        ...         try:
        ...             # Validate input
        ...             if not self._validate_member_data(data):
        ...                 return False, "Invalid member data format"
        ...             
        ...             # Execute business logic
        ...             member_id = self.member_service.create_member(data)
        ...             return True, f"Member {member_id} created successfully"
        ...         except Exception as e:
        ...             return False, f"Error creating member: {str(e)}"
        
        >>> # Booking operation command
        >>> class BookRoomCommand(Command):
        ...     def execute(self, data):
        ...         try:
        ...             booking = self._parse_booking_data(data)
        ...             if self.room_service.is_available(booking):
        ...                 booking_id = self.booking_service.create_booking(booking)
        ...                 return True, f"Room booked successfully: {booking_id}"
        ...             return False, "Room not available at specified time"
        ...         except Exception as e:
        ...             return False, f"Booking failed: {str(e)}"
    
    Error Handling Best Practices:
        - Catch all exceptions within execute method
        - Return user-friendly error messages
        - Log technical details for debugging
        - Never let exceptions propagate to presentation layer
        - Provide specific error guidance when possible
    
    Testing Support:
        The standardized interface enables consistent testing:
        ```python
        def test_command_success():
            command = ConcreteCommand()
            success, result = command.execute(valid_data)
            assert success is True
            assert "successfully" in result.lower()
        
        def test_command_failure():
            command = ConcreteCommand()
            success, result = command.execute(invalid_data)
            assert success is False
            assert "error" in result.lower() or "failed" in result.lower()
        ```
    
    Future Enhancements:
        This interface supports advanced patterns:
        - Command queuing and batch execution
        - Operation logging and audit trails
        - Undo/redo functionality
        - Macro command composition
        - Asynchronous command execution
        - Command validation and authorization
    
    Thread Safety:
        Command instances should be stateless or handle concurrency appropriately.
        Business logic services used within commands should be thread-safe.
    
    Note:
        This is an abstract base class and cannot be instantiated directly.
        All concrete implementations must provide the execute() method.
    """
    
    @abstractmethod
    def execute(self, data):
        """
        Execute the command's business logic operation with provided data.
        
        This is the core method that all concrete command implementations must
        provide. It serves as the unified interface for executing business
        operations across the entire sports booking system, ensuring consistent
        behavior and return patterns.
        
        The method encapsulates the complete business operation including input
        validation, business logic execution, error handling, and result formatting.
        It must handle all exceptions internally and return standardized success/failure
        indicators with meaningful user feedback.
        
        Args:
            data: Input data required for the command execution. The type and
                 structure depend on the specific command implementation.
                 Examples:
                 - dict: Member data for registration commands
                 - Booking: Booking object for reservation commands
                 - str: Simple identifiers for deletion commands
                 - None: For commands that don't require input data
        
        Returns:
            tuple: A two-element tuple containing:
                success (bool): True if the operation completed successfully,
                               False if any error occurred or validation failed.
                result (str): Human-readable message describing the operation
                             outcome, suitable for display to end users.
        
        Return Value Examples:
            Success cases:
            - (True, "Member John Doe added successfully with ID: M12345")
            - (True, "Room gymnasium_01 booked for 2025-08-25 at 14:30")
            - (True, "Booking 12345 cancelled successfully")
            - (True, "Found 3 available tennis courts")
            
            Failure cases:
            - (False, "Email address already exists in the system")
            - (False, "Room not available at the specified time")
            - (False, "Booking not found or already cancelled")
            - (False, "Invalid date format provided")
        
        Implementation Requirements:
            1. Input Validation:
               - Validate all input data before processing
               - Check data types, formats, and business constraints
               - Return meaningful error messages for validation failures
            
            2. Exception Handling:
               - Catch all exceptions within the method
               - Never allow exceptions to propagate to calling code
               - Convert technical errors to user-friendly messages
               - Log technical details for debugging purposes
            
            3. Business Logic:
               - Implement the core business operation
               - Ensure data consistency and integrity
               - Follow business rules and constraints
               - Handle edge cases appropriately
            
            4. Return Value:
               - Always return exactly two values: (bool, str)
               - Provide clear, actionable feedback messages
               - Include relevant details in success messages
               - Specify corrective actions in error messages
        
        Example Implementation Pattern:
            ```python
            def execute(self, data):
                try:
                    # 1. Validate input data
                    if not self._validate_input(data):
                        return False, "Invalid input data provided"
                    
                    # 2. Execute business logic
                    result = self._perform_business_operation(data)
                    
                    # 3. Return success with details
                    return True, f"Operation completed successfully: {result}"
                    
                except ValidationError as e:
                    # Handle business rule violations
                    return False, f"Validation failed: {e.message}"
                except ServiceError as e:
                    # Handle service-level errors
                    return False, f"Service error: {e.message}"
                except Exception as e:
                    # Handle unexpected errors
                    logger.error(f"Unexpected error in {self.__class__.__name__}: {e}")
                    return False, "An unexpected error occurred. Please try again."
            ```
        
        Integration Notes:
            - Called by presentation layer Option objects
            - Return values used for user feedback display
            - Success flag determines UI flow continuation
            - Result message displayed directly to users
        
        Testing Considerations:
            - Test both success and failure scenarios
            - Verify return value format consistency
            - Check exception handling completeness
            - Validate user message clarity and usefulness
        
        Performance Guidelines:
            - Keep operations efficient and responsive
            - Use appropriate database transaction boundaries
            - Implement timeout handling for external services
            - Consider caching for frequently accessed data
        
        Security Considerations:
            - Validate and sanitize all input data
            - Implement proper authorization checks
            - Prevent information leakage in error messages
            - Log security-relevant operations for auditing
        
        Raises:
            NotImplementedError: This abstract method must be implemented by
                               all concrete command subclasses.
        
        Note:
            This method should never be called on the abstract Command class
            directly. It must be implemented in concrete subclasses to provide
            specific business logic functionality.
        """
        raise NotImplementedError("You must implement this method")
