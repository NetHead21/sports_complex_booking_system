"""
Add Member Command Module.

This module implements the AddMembersCommand class, which is responsible for handling
the business logic of adding new members to the sports booking system. The command
follows the Single Responsibility Principle by delegating input collection to
MemberInputService and focusing solely on executing the database operation.

Classes:
    AddMembersCommand: Command class for adding new members to the database.

Dependencies:
    - Command: Base command interface
    - member_database_manager: Database operations for member management
    - MemberInputService: Service for collecting and validating member input data

Example:
    Basic usage:
    >>> command = AddMembersCommand()
    >>> success, error = command.execute()
    >>> if success:
    ...     print("Member added successfully")
    ... else:
    ...     print(f"Failed to add member: {error}")
"""

from business_logic.base.command import Command
from business_logic.member_database_manager import db
from business_logic.services.member_input_service import MemberInputService


class AddMembersCommand(Command):
    """
    Command for adding new members to the sports booking system database.

    This class implements the Command pattern and follows the Single Responsibility
    Principle by focusing solely on executing the database operation for adding
    a new member. Input collection, validation, and member object creation are
    delegated to the MemberInputService.

    The command handles all database-related errors and provides clear feedback
    about the operation's success or failure.

    Attributes:
        None (inherits from Command base class)

    Methods:
        execute(data=None): Execute the add member operation

    Example:
        >>> add_command = AddMembersCommand()
        >>> success, error_msg = add_command.execute()
        >>> if success:
        ...     print("Member successfully added to database")
        ... else:
        ...     print(f"Failed to add member: {error_msg}")

    Note:
        This command requires a valid database connection through the
        member_database_manager module. The actual member data collection
        is handled by MemberInputService to maintain separation of concerns.
    """

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the add member command.

        This method orchestrates the process of adding a new member to the database.
        It delegates input collection to MemberInputService and handles the database
        operation execution with proper error handling.

        Single Responsibility: Execute the database operation for adding a member.
        Input collection and member creation are delegated to MemberInputService.

        Args:
            data (any, optional): Additional data for the command execution.
                Currently not used in this implementation but maintained for
                interface compatibility with the Command base class.
                Defaults to None.

        Returns:
            tuple[bool, any]: A tuple containing:
                - bool: True if member was successfully added, False otherwise
                - any: None if successful, error message string if failed

        Raises:
            Exception: Any database-related exceptions are caught and converted
                to return values for graceful error handling.

        Example:
            >>> command = AddMembersCommand()
            >>> success, error = command.execute()
            >>> if success:
            ...     print("✅ Member added successfully!")
            ... else:
            ...     print(f"❌ Error adding member: {error}")

        Flow:
            1. Delegate member data collection to MemberInputService
            2. Validate that member object was created successfully
            3. Execute database operation to create new member
            4. Provide user feedback on operation result
            5. Return success status and any error information

        Note:
            The method prints status messages directly to the console for
            immediate user feedback. This follows the established pattern
            in the sports booking system for user interaction.
        """
        try:
            # Delegate input collection and member creation to service
            member = MemberInputService.collect_new_member_data()

            if member is None:
                return False, "Member creation cancelled or failed"

            # Focus solely on database execution
            db.create_new_member(member)
            print(f"✅ Member '{member.id}' registered successfully!")
            return True, None

        except Exception as e:
            print(f"❌ Database Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    """
    Module test runner.
    
    This section provides a simple test when the module is run directly.
    It creates an instance of AddMembersCommand and executes it to verify
    the basic functionality works as expected.
    
    Usage:
        python add_member_command.py
    
    Expected Output:
        - Interactive prompts for member data collection
        - Success or error messages from the execution
        - Final result summary showing command execution status
    """
    # Test the command
    add_member = AddMembersCommand()
    success, result = add_member.execute()
    print(f"Command result: Success={success}, Result={result}")
