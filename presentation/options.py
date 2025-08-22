"""
Presentation layer option handling for the Sports Booking Management System.

This module provides the Option class that encapsulates menu options with their
associated commands, preparation callbacks, and success message formatting.
The Option class serves as a bridge between the presentation layer (menu system)
and the business logic layer (commands), providing a clean separation of concerns.

Classes:
    Option: Represents a selectable menu option with command execution capabilities.

Dependencies:
    - typing.Callable: For type hinting preparation callback functions
    - Command objects: Business logic commands that implement execute() method

Example:
    >>> from business_logic.commands.member.add_member_command import AddMemberCommand
    >>> add_command = AddMemberCommand()
    >>> option = Option("Add Member", add_command, prep_call=get_member_data)
    >>> option.choose()  # Executes the command with prepared data
"""

from typing import Callable


class Option:
    """
    Represents a selectable menu option with associated command execution.
    
    The Option class encapsulates a menu choice that can execute a business logic
    command with optional data preparation and formatted success messaging. This
    design pattern provides loose coupling between the presentation layer and
    business logic, allowing for flexible menu construction and command execution.
    
    Attributes:
        name (str): Display name for the menu option.
        command (object): Business logic command object with execute() method.
        prep_call (Callable, optional): Function to prepare data before command execution.
        success_message (str): Template string for formatting success messages.
    
    Design Pattern:
        - Command Pattern: Encapsulates command execution with parameters
        - Strategy Pattern: Allows different preparation strategies via prep_call
        - Template Method: Standardizes option execution flow
    
    Example:
        >>> def get_user_input():
        ...     return {"name": "John", "email": "john@email.com"}
        >>> 
        >>> add_cmd = AddMemberCommand()
        >>> option = Option(
        ...     name="Add New Member",
        ...     command=add_cmd,
        ...     prep_call=get_user_input,
        ...     success_message="Successfully added: {result}"
        ... )
        >>> option.choose()  # Prompts for input and executes command
    """
    
    def __init__(
        self,
        name: str,
        command: object,
        prep_call: Callable = None,
        success_message="{result}",
    ) -> None:
        """
        Initialize a new Option instance.
        
        Creates a menu option with the specified name, command, optional data
        preparation callback, and success message template. The option can be
        executed to run the associated command with proper data handling.
        
        Args:
            name (str): The display name for this menu option.
            command (object): Command object that implements execute() method.
                            Must return tuple (success: bool, result: str).
            prep_call (Callable, optional): Function to call before command execution
                                           to prepare input data. Defaults to None.
            success_message (str, optional): Template string for success messages.
                                           Uses {result} placeholder for command result.
                                           Defaults to "{result}".
        
        Raises:
            TypeError: If command doesn't implement execute() method.
            ValueError: If name is empty or None.
        
        Example:
            >>> option = Option(
            ...     name="Delete Member",
            ...     command=DeleteMemberCommand(),
            ...     prep_call=lambda: input("Enter member ID: "),
            ...     success_message="Member {result} deleted successfully!"
            ... )
        """
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message

    def choose(self) -> None:
        """
        Execute the option's command with optional data preparation.
        
        This method implements the core option execution flow:
        1. Calls prep_call function if provided to gather input data
        2. Executes the associated command with or without prepared data
        3. Displays formatted success message if command succeeds
        4. Handles command failures gracefully (errors handled by command)
        
        The method follows the Command Pattern, delegating actual business logic
        to the command object while handling presentation concerns locally.
        
        Execution Flow:
            prep_call() -> command.execute(data) -> format_message(result)
        
        Returns:
            None: This method handles output directly via print statements.
        
        Raises:
            AttributeError: If command doesn't have execute() method.
            Exception: Any exception from prep_call or command execution
                      (should be handled by calling code).
        
        Example:
            >>> # Option with data preparation
            >>> option = Option("Update Email", update_cmd, get_email_data)
            >>> option.choose()
            # Calls get_email_data(), passes result to update_cmd.execute()
            # Prints formatted success message
            
            >>> # Simple option without preparation
            >>> option = Option("List All", list_cmd)
            >>> option.choose()
            # Calls list_cmd.execute() directly, prints result
        """
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data) if data else self.command.execute()

        if success:
            print(self.success_message.format(result=result))

    def __str__(self) -> str:
        """
        Return string representation of the option.
        
        Provides a clean string representation using the option's display name.
        This method is called when the option is converted to string for menu
        display purposes, ensuring consistent presentation formatting.
        
        Returns:
            str: The display name of the option.
        
        Example:
            >>> option = Option("Add New Member", add_command)
            >>> str(option)
            'Add New Member'
            >>> print(option)  # Calls __str__ implicitly
            Add New Member
        """
        return self.name
