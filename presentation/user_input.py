"""
User input handling utilities for the Sports Booking Management System.

This module provides standardized functions for collecting and validating user input
from the command-line interface. It ensures consistent input handling throughout
the presentation layer while providing robust validation and error handling.

The module follows the DRY (Don't Repeat Yourself) principle by centralizing
common input operations and validation logic used across multiple presentation
components.

Functions:
    get_user_input: Collects text input with optional requirement validation.
    get_options_choice: Handles menu option selection with validation.

Dependencies:
    - typing.Any: For flexible return type annotations
    - presentation.utils.option_choice_is_valid: Validation utility function

Example:
    >>> # Collect required user input
    >>> name = get_user_input("Enter your name", required=True)
    
    >>> # Collect optional input
    >>> phone = get_user_input("Phone number (optional)", required=False)
    
    >>> # Handle menu choices
    >>> options = {"A": add_member, "B": book_room, "Q": quit}
    >>> choice = get_options_choice(options)
    >>> choice()  # Execute selected function
"""

from typing import Any

from presentation.utils import option_choice_is_valid


def get_user_input(label: str, required: bool = True) -> str:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_options_choice(options: dict) -> Any:
    choice = input("Choose an option: ").upper()
    while not option_choice_is_valid(choice, options):
        print("Invalid choice!")
        choice = input("Choose an option: ").upper()
    return options[choice]
