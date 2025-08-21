"""
Presentation Utilities Module for Sports Booking System.

This module provides common utility functions for the presentation layer of the
sports booking system. It includes functions for screen management, input validation,
and menu display formatting to enhance the user interface experience.

The utilities in this module are designed to be cross-platform compatible and
provide consistent behavior across different operating systems and terminal
environments.

Functions:
    clear_screen: Cross-platform screen clearing utility.
    option_choice_is_valid: Validates user menu choices against available options.
    print_options: Displays menu options in a formatted, user-friendly manner.

Dependencies:
    - os: For cross-platform system command execution

Example:
    >>> from utils import clear_screen, print_options
    >>> options = {"A": "Add Member", "B": "View Members", "Q": "Quit"}
    >>> clear_screen()
    >>> print_options(options)
    (A) Add Member
    (B) View Members
    (Q) Quit
"""

import os


def clear_screen() -> None:
    """
    Clear the terminal/console screen in a cross-platform compatible manner.

    This function automatically detects the operating system and executes the
    appropriate system command to clear the screen. It provides a consistent
    way to refresh the display across different platforms without requiring
    platform-specific code in the calling functions.

    Platform Support:
        - Windows (nt): Uses 'cls' command
        - Unix/Linux/macOS (posix): Uses 'clear' command
        - Other platforms: Defaults to 'clear' command

    Returns:
        None: This function performs a side effect (clearing screen) and
              returns nothing.

    Raises:
        OSError: May be raised if the system command fails to execute,
                though this is rare in normal terminal environments.

    Example:
        >>> clear_screen()  # Screen is cleared regardless of OS

    Note:
        This function uses os.system() which executes a shell command.
        While generally safe for this specific use case, be aware that
        it's executing system commands. The commands used ('cls', 'clear')
        are standard system utilities available on their respective platforms.

        For applications requiring higher security, consider using alternative
        methods like ANSI escape sequences, though they may not work in all
        terminal environments.
    """
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)


def option_choice_is_valid(choice: str, options: dict) -> bool:
    """
    Validate whether a user's menu choice exists in the available options.

    This function checks if a user's input corresponds to a valid menu option
    by verifying that the choice exists as a key in the options dictionary.
    It's designed to be case-sensitive to match the exact key format used
    in menu systems.

    Args:
        choice (str): The user's input choice to validate. This should be a
                     string representing the menu option key (e.g., "A", "B", "1", "2").
        options (dict): A dictionary containing the available menu options where
                       keys represent the choice identifiers and values represent
                       the option descriptions or objects.

    Returns:
        bool: True if the choice exists as a key in the options dictionary,
              False otherwise.

    Example:
        >>> menu_options = {
        ...     "A": "Add Member",
        ...     "B": "View Members",
        ...     "Q": "Quit"
        ... }
        >>> option_choice_is_valid("A", menu_options)
        True
        >>> option_choice_is_valid("X", menu_options)
        False
        >>> option_choice_is_valid("a", menu_options)  # Case sensitive
        False

    Note:
        - This function is case-sensitive. "A" and "a" are treated as different choices.
        - The function only checks for key existence, not the validity of the
          associated option value.
        - Works with any hashable key type, though string keys are most common
          in menu systems.

    Common Usage:
        Used in menu validation loops to ensure user input corresponds to a
        valid menu option before attempting to execute the associated command.
    """
    return choice in options


def print_options(options: dict) -> None:
    """
    Display menu options in a formatted, user-friendly manner.

    This function takes a dictionary of menu options and prints them to the console
    in a consistent format with each option on its own line. The format includes
    the option key in parentheses followed by the option description, making it
    easy for users to understand their choices and the corresponding input required.

    Args:
        options (dict): A dictionary containing menu options where:
                       - Keys: Option identifiers (typically single characters like "A", "B")
                       - Values: Option descriptions or Option objects with __str__ method
                       The values should be convertible to string for display.

    Returns:
        None: This function performs output to console and returns nothing.

    Output Format:
        Each option is printed on a separate line in the format:
        (key) value

        Where 'key' is the dictionary key and 'value' is the string representation
        of the dictionary value.

    Example:
        >>> menu_options = {
        ...     "A": "Add New Member",
        ...     "B": "View All Members",
        ...     "C": "Update Member",
        ...     "Q": "Quit"
        ... }
        >>> print_options(menu_options)
        (A) Add New Member
        (B) View All Members
        (C) Update Member
        (Q) Quit

    Example with Option Objects:
        >>> from presentation.options import Option
        >>> from business_logic.add_member_command import AddMemberCommand
        >>> options = {
        ...     "A": Option("Add Member", AddMemberCommand()),
        ...     "B": Option("View Members", ViewMembersCommand())
        ... }
        >>> print_options(options)
        (A) Add Member
        (B) View Members

    Note:
        - The function preserves the order of options as they appear in the dictionary.
          For Python 3.7+, this is the insertion order.
        - If option values have custom __str__ methods (like Option objects), those
          will be used for display.
        - The function does not add any additional formatting like borders, colors,
          or spacing beyond the basic (key) value format.

    Common Usage:
        Used in menu systems throughout the sports booking application to display
        available choices to users in a consistent, readable format.
    """
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
