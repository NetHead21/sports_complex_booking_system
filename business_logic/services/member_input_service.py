"""
Member Input Service Module for Sports Booking System.

This module provides the MemberInputService class, which serves as a centralized
service for collecting, validating, and processing member-related input data.
It implements the Single Responsibility Principle by separating input collection
logic from business command execution.

The service handles all aspects of member data input including:
- New member registration data collection
- Member email update workflows
- Member password update with confirmation
- Member deletion with safety confirmations
- General member lookup operations
- Data validation and error handling
- Consistent user interface formatting

This service is designed to be used by command classes in the business logic
layer, promoting clean architecture and separation of concerns. It provides
robust error handling, user-friendly prompts, and comprehensive validation
to ensure data integrity.

Key Features:
    - Pydantic model integration for data validation
    - Comprehensive input validation with user-friendly error messages
    - Keyboard interrupt handling for graceful cancellation
    - Password confirmation workflows
    - Email format validation
    - Deletion safety mechanisms with confirmation prompts
    - Consistent operation result display formatting

Classes:
    MemberInputService: Static service class for member input operations.

Dependencies:
    - persistence.models.Member: Pydantic model for member data validation
    - presentation.user_input: Utilities for collecting user input
    - typing: Type hints for better code documentation

Example:
    >>> from business_logic.member_input_service import MemberInputService
    >>>
    >>> # Collect new member data
    >>> member = MemberInputService.collect_new_member_data()
    >>> if member:
    ...     print(f"Created member: {member.id}")
    >>>
    >>> # Collect email update data
    >>> update_data = MemberInputService.collect_member_email_update_data()
    >>> if update_data:
    ...     member_id, new_email = update_data
    ...     print(f"Updating {member_id} email to {new_email}")

Author: Sports Booking System Development Team
Date: August 2025
Version: 2.0 (Refactored for Single Responsibility Principle)
"""

from persistence.models import Member
from presentation.user_input import get_user_input
from typing import Optional, Tuple


class MemberInputService:
    """
    Centralized service for collecting and validating member-related input data.

    This class provides static methods for handling all member input collection
    workflows in the sports booking system. It implements the Single Responsibility
    Principle by focusing solely on input collection, validation, and user interaction,
    while leaving business logic execution to command classes.

    The service provides a consistent, user-friendly interface for all member
    operations and includes comprehensive error handling, input validation,
    and safety mechanisms for destructive operations.

    Design Principles:
        - Single Responsibility: Handles only input collection and validation
        - Static Methods: No instance state, can be used without instantiation
        - User-Friendly: Provides clear prompts and error messages
        - Safe Operations: Includes confirmation for destructive actions
        - Robust Error Handling: Gracefully handles interruptions and errors

    Methods:
        collect_new_member_data(): Collects data for new member registration
        collect_member_email_update_data(): Collects data for email updates
        collect_member_password_update_data(): Collects data for password updates
        collect_member_id_for_deletion(): Collects and confirms member deletion
        collect_member_id_for_lookup(): Collects member ID for lookup operations
        display_operation_result(): Displays operation results consistently
        validate_member_data(): Validates member data before database operations

    Return Value Patterns:
        - Returns None when operations are cancelled or fail validation
        - Returns validated data objects/tuples when successful
        - Uses Optional type hints to indicate nullable returns
        - Provides tuple returns for multi-value operations

    Error Handling:
        - Catches KeyboardInterrupt for graceful user cancellation
        - Validates input data before returning
        - Provides clear error messages for validation failures
        - Handles unexpected exceptions with generic error reporting

    Example:
        >>> # Collect new member data with validation
        >>> member = MemberInputService.collect_new_member_data()
        >>> if member:
        ...     # Proceed with member creation
        ...     database.create_member(member)
        >>> else:
        ...     # Handle cancellation or validation failure
        ...     print("Member creation cancelled")

        >>> # Collect email update with confirmation
        >>> email_data = MemberInputService.collect_member_email_update_data()
        >>> if email_data:
        ...     member_id, new_email = email_data
        ...     # Proceed with update
        ...     success = database.update_email(member_id, new_email)
        ...     MemberInputService.display_operation_result(
        ...         "Email Update", member_id, success
        ...     )
    """

    @staticmethod
    def collect_new_member_data() -> Optional[Member]:
        """
        Collect and validate member registration information from user input.

        This method guides the user through the member registration process,
        collecting all required information (username, password, email) and
        creating a validated Member object using Pydantic. It provides a
        user-friendly interface with clear prompts and error handling.

        The method performs the following steps:
        1. Display registration header with clear formatting
        2. Collect member username (ID) with required validation
        3. Collect password with required validation
        4. Collect email address with required validation
        5. Create and validate Member object using Pydantic model
        6. Handle validation errors and user cancellation gracefully

        Returns:
            Optional[Member]: A validated Member object containing the user's input
                if all data is valid and the user completes the process.
                Returns None if:
                - User cancels the operation (Ctrl+C)
                - Pydantic validation fails (invalid data format)
                - Any unexpected error occurs during collection

        Validation:
            - All fields are required (enforced by get_user_input)
            - Member object validation is handled by Pydantic model
            - Email format validation is performed by Member model
            - Password requirements are enforced by Member model

        User Interface:
            - Clear section header: "📝 Adding New Member"
            - Consistent prompt formatting
            - Detailed error messages for validation failures
            - Graceful handling of user cancellation

        Error Handling:
            - ValueError: Pydantic validation failures (e.g., invalid email format)
            - KeyboardInterrupt: User cancellation via Ctrl+C
            - Exception: Any other unexpected errors during input collection

        Example:
            >>> member = MemberInputService.collect_new_member_data()
            >>> if member:
            ...     print(f"Member created: {member.id}")
            ...     print(f"Email: {member.email}")
            ... else:
            ...     print("Member creation was cancelled or failed validation")

        Note:
            This method does not perform database operations. It only collects
            and validates input data. The calling command is responsible for
            database persistence and business logic execution.
        """
        try:
            print("\n📝 Adding New Member")
            print("-" * 30)

            # Collect member information from user
            member_id = get_user_input("Enter member username", required=True)
            password = get_user_input("Enter password", required=True)
            email = get_user_input("Enter email", required=True)

            # Create and validate Member object using Pydantic
            member = Member(id=member_id, password=password, email=email)
            return member

        except ValueError as e:
            print(f"❌ Validation Error: {e}")
            return None
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    @staticmethod
    def collect_member_email_update_data() -> Optional[Tuple[str, str]]:
        """
        Collect member identification and new email address for email update operations.

        This method facilitates the email update workflow by collecting the member's
        username and their new email address. It includes basic email format validation
        to catch obvious formatting errors before attempting database operations.

        Workflow:
        1. Display email update header with clear formatting
        2. Collect member username for identification
        3. Collect new email address with basic format validation
        4. Validate email format (contains @ and . characters)
        5. Return validated data as a tuple for further processing

        Args:
            None: This is a static method that collects input interactively

        Returns:
            Optional[Tuple[str, str]]: A tuple containing (member_id, new_email)
                if collection is successful and validation passes.
                Returns None if:
                - User cancels the operation (Ctrl+C)
                - Email format validation fails
                - Any unexpected error occurs during collection

        Validation:
            - Member ID: Must be provided (enforced by get_user_input required=True)
            - Email format: Must contain both '@' and '.' characters
            - Basic email length and format checking

        User Interface:
            - Clear section header: "📧 Updating Member Email"
            - Descriptive input prompts
            - Validation error messages for invalid email format
            - Cancellation handling with appropriate messaging

        Error Handling:
            - KeyboardInterrupt: Graceful handling of user cancellation
            - Email validation: Clear error message for invalid format
            - Exception: Generic error handling for unexpected issues

        Example:
            >>> email_data = MemberInputService.collect_member_email_update_data()
            >>> if email_data:
            ...     member_id, new_email = email_data
            ...     print(f"Updating {member_id}'s email to {new_email}")
            ...     # Proceed with database update
            ... else:
            ...     print("Email update cancelled or validation failed")

        Note:
            This method performs only basic email format validation. More sophisticated
            email validation (DNS checking, deliverability) should be handled at the
            business logic layer if required. The method focuses on collecting valid
            input data for handoff to command execution.
        """
        try:
            print("\n📧 Updating Member Email")
            print("-" * 30)

            member_id = get_user_input("Enter member username", required=True)
            new_email = get_user_input("Enter new email address", required=True)

            # Basic email validation (you could enhance this with regex)
            if "@" not in new_email or "." not in new_email:
                print("❌ Invalid email format")
                return None

            return member_id, new_email

        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting email data: {e}")
            return None

    @staticmethod
    def collect_member_password_update_data() -> Optional[Tuple[str, str]]:
        """
        Collect member identification and new password with confirmation for password updates.

        This method implements a secure password update workflow that includes password
        confirmation to prevent accidental password changes. It enforces basic password
        security requirements and ensures the user enters the same password twice for
        verification before proceeding with the update.

        Security Workflow:
        1. Display password update header with clear formatting
        2. Collect member username for identification
        3. Collect new password with minimum length validation
        4. Collect password confirmation for verification
        5. Verify that both password entries match exactly
        6. Return validated credentials as a tuple

        Args:
            None: This is a static method that collects input interactively

        Returns:
            Optional[Tuple[str, str]]: A tuple containing (member_id, new_password)
                if collection is successful and all validations pass.
                Returns None if:
                - User cancels the operation (Ctrl+C)
                - Password is shorter than 6 characters
                - Password confirmation does not match
                - Any unexpected error occurs during collection

        Password Requirements:
            - Minimum length: 6 characters
            - Must match confirmation entry exactly
            - Cannot be empty or whitespace-only (enforced by get_user_input)

        User Interface:
            - Clear section header: "🔐 Updating Member Password"
            - Descriptive prompts for each input step
            - Clear validation error messages
            - Security-focused messaging for password confirmation

        Security Features:
            - Double-entry password confirmation
            - Minimum length enforcement
            - Clear error messaging for security failures
            - Graceful cancellation handling

        Error Handling:
            - Password length validation with specific error message
            - Password mismatch detection with clear feedback
            - KeyboardInterrupt: Graceful user cancellation
            - Exception: Generic error handling for unexpected issues

        Example:
            >>> password_data = MemberInputService.collect_member_password_update_data()
            >>> if password_data:
            ...     member_id, new_password = password_data
            ...     print(f"Password collected for {member_id}")
            ...     # Proceed with secure password update
            ... else:
            ...     print("Password update cancelled or validation failed")

        Note:
            This method does not hash or encrypt passwords - it only collects and
            validates the plaintext input. Password hashing should be handled by
            the database layer or business logic layer according to security
            requirements. The method focuses on ensuring password policy compliance
            and user confirmation.
        """
        try:
            print("\n� Updating Member Password")
            print("-" * 30)

            member_id = get_user_input("Enter member username", required=True)
            new_password = get_user_input("Enter new password", required=True)

            # Basic password validation
            if len(new_password) < 6:
                print("❌ Password must be at least 6 characters long")
                return None

            # Confirm password
            confirm_password = get_user_input("Confirm new password", required=True)

            if new_password != confirm_password:
                print("❌ Passwords do not match")
                return None

            return member_id, new_password

        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting password data: {e}")
            return None

    @staticmethod
    def collect_member_id_for_deletion() -> Optional[str]:
        """
        Collect member identification with comprehensive safety confirmations for deletion.

        This method implements a high-security workflow for member deletion operations,
        including multiple warnings, consequence explanations, and explicit confirmation
        requirements. It is designed to prevent accidental deletions while still allowing
        authorized users to perform necessary cleanup operations.

        Safety Workflow:
        1. Display deletion header with warning indicators
        2. Show prominent warning about irreversible nature
        3. Collect member username for identification
        4. Display detailed consequences of deletion operation
        5. Require explicit "DELETE" confirmation text
        6. Verify exact match of confirmation text (case-sensitive)
        7. Return member ID only after full confirmation chain

        Args:
            None: This is a static method that collects input interactively

        Returns:
            Optional[str]: The member ID (username) if all confirmations are satisfied.
                Returns None if:
                - User cancels the operation (Ctrl+C)
                - User enters incorrect confirmation text
                - Any unexpected error occurs during collection

        Safety Features:
            - Multiple warning displays with prominent visual indicators
            - Detailed explanation of deletion consequences
            - Explicit confirmation text requirement ("DELETE")
            - Case-sensitive confirmation matching
            - Clear cancellation messaging for failed confirmations

        User Interface:
            - Warning header: "🗑️ Delete Member"
            - Prominent warning: "⚠️ WARNING: This action cannot be undone!"
            - Detailed consequence list with bullet points
            - Clear confirmation requirement messaging
            - Visual emphasis with emojis and formatting

        Consequences Explained:
            - Member removal from database
            - Cancellation of existing bookings
            - Irreversible nature of the operation

        Confirmation Requirements:
            - User must type exactly "DELETE" (case-sensitive)
            - Any other input cancels the operation
            - Clear feedback for failed confirmation attempts

        Error Handling:
            - Confirmation mismatch: Clear cancellation message
            - KeyboardInterrupt: Graceful user cancellation
            - Exception: Generic error handling for unexpected issues

        Example:
            >>> member_id = MemberInputService.collect_member_id_for_deletion()
            >>> if member_id:
            ...     print(f"Confirmed deletion for member: {member_id}")
            ...     # Proceed with deletion operation
            ... else:
            ...     print("Deletion cancelled - member preserved")

        Security Note:
            This method implements the "confirm with explicit text" pattern commonly
            used in critical operations. The confirmation text must match exactly,
            and the consequences are clearly explained to ensure informed consent
            from the user before proceeding with destructive operations.
        """
        try:
            print("\n🗑️ Delete Member")
            print("-" * 30)
            print("⚠️ WARNING: This action cannot be undone!")

            member_id = get_user_input("Enter member username to delete", required=True)

            # Show warning and ask for confirmation
            print(f"\n⚠️ You are about to delete member: '{member_id}'")
            print("This will:")
            print("  • Remove the member from the database")
            print("  • Cancel any existing bookings")
            print("  • This action is IRREVERSIBLE")

            confirm = get_user_input("Type 'DELETE' to confirm deletion", required=True)

            if confirm == "DELETE":
                return member_id
            else:
                print("❌ Deletion cancelled - confirmation text does not match")
                return None

        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    @staticmethod
    def collect_member_id_for_lookup() -> Optional[str]:
        """
        Collect member identification for general lookup and query operations.

        This method provides a simple, streamlined interface for collecting member
        usernames when performing non-destructive lookup operations such as viewing
        member details, checking booking history, or verifying member existence.
        It offers a lightweight alternative to the more complex collection methods
        used for modifications or deletions.

        Use Cases:
            - Member profile lookups
            - Booking history queries
            - Member existence verification
            - General member information retrieval
            - Non-destructive member operations

        Args:
            None: This is a static method that collects input interactively

        Returns:
            Optional[str]: The member ID (username) if provided by the user.
                Returns None if:
                - User cancels the operation (Ctrl+C)
                - Any unexpected error occurs during collection

        Validation:
            - Member ID: Must be provided (enforced by get_user_input required=True)
            - No additional validation required for lookup operations
            - Existence verification handled by calling business logic

        User Interface:
            - Simple header: "🔍 Member Lookup"
            - Clear, straightforward input prompt
            - Minimal interface for quick operations
            - Standard cancellation handling

        Error Handling:
            - KeyboardInterrupt: Graceful user cancellation
            - Exception: Generic error handling for unexpected issues
            - No validation errors (handled by business logic layer)

        Example:
            >>> member_id = MemberInputService.collect_member_id_for_lookup()
            >>> if member_id:
            ...     member_details = database.get_member(member_id)
            ...     if member_details:
            ...         print(f"Found member: {member_details}")
            ...     else:
            ...         print(f"Member {member_id} not found")
            ... else:
            ...     print("Lookup operation cancelled")

        Note:
            This method is intentionally simple and does not perform existence
            validation or complex error checking. It serves as a lightweight
            input collection utility for operations where the business logic
            layer will handle member validation and error reporting.
        """
        try:
            print("\n🔍 Member Lookup")
            print("-" * 30)

            member_id = get_user_input("Enter member username", required=True)
            return member_id

        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    @staticmethod
    def display_operation_result(
        operation: str, member_id: str, success: bool, error_msg: str = None
    ):
        """
        Display standardized operation results with consistent formatting and visual indicators.

        This method provides a centralized way to display the results of member operations
        with consistent visual formatting, emoji indicators, and detailed error reporting.
        It ensures that all member operations provide uniform feedback to users regardless
        of which command executed the operation.

        The method supports both success and failure scenarios, with optional detailed
        error messaging for debugging and user information. It uses visual indicators
        to make success/failure status immediately apparent to users.

        Args:
            operation (str): A descriptive name for the operation that was performed.
                Examples: "Email Update", "Password Update", "Member Creation", "Member Deletion"
            member_id (str): The username/ID of the member involved in the operation.
                Used to provide specific feedback about which member was affected.
            success (bool): Whether the operation completed successfully.
                True: Display success message with ✅ indicator
                False: Display failure message with ❌ indicator
            error_msg (str, optional): Detailed error message for failed operations.
                If provided, includes specific error details in the failure message.
                If None, displays a generic failure message. Defaults to None.

        Returns:
            None: This method performs console output and returns nothing.

        Output Formats:
            Success: "✅ {operation} successful for member '{member_id}'!"
            Failure with error: "❌ {operation} failed for member '{member_id}': {error_msg}"
            Failure without error: "❌ {operation} failed for member '{member_id}'"

        Visual Indicators:
            - ✅ Green checkmark emoji for successful operations
            - ❌ Red X emoji for failed operations
            - Consistent formatting with member ID in quotes for clarity

        Example:
            >>> # Display successful email update
            >>> MemberInputService.display_operation_result(
            ...     "Email Update", "john_doe", True
            ... )
            # Output: ✅ Email Update successful for member 'john_doe'!

            >>> # Display failed password update with error details
            >>> MemberInputService.display_operation_result(
            ...     "Password Update", "jane_smith", False, "Database connection failed"
            ... )
            # Output: ❌ Password Update failed for member 'jane_smith': Database connection failed

            >>> # Display failed operation without specific error
            >>> MemberInputService.display_operation_result(
            ...     "Member Creation", "bob_wilson", False
            ... )
            # Output: ❌ Member Creation failed for member 'bob_wilson'

        Use Cases:
            - Command execution result reporting
            - Database operation feedback
            - User notification for completed operations
            - Error reporting with contextual information
            - Consistent user experience across all member operations

        Note:
            This method is designed to be called by command classes after executing
            business operations. It provides the presentation layer functionality
            while remaining in the service layer for consistency and reusability.
        """
        if success:
            print(f"✅ {operation} successful for member '{member_id}'!")
        else:
            if error_msg:
                print(f"❌ {operation} failed for member '{member_id}': {error_msg}")
            else:
                print(f"❌ {operation} failed for member '{member_id}'")

    @staticmethod
    def validate_member_data(
        member_id: str, email: str = None, password: str = None
    ) -> Tuple[bool, str]:
        """
        Perform comprehensive validation of member data before database operations.

        This method provides centralized validation logic for member data, ensuring
        consistent validation rules across all member operations. It performs both
        individual field validation and cross-field validation to maintain data
        integrity and enforce business rules.

        The method supports partial validation by accepting optional parameters,
        allowing it to be used for various scenarios from complete member validation
        during registration to single-field validation during updates.

        Args:
            member_id (str): The member username/ID to validate. This is always required
                as it serves as the primary identifier for member records.
            email (str, optional): Email address to validate. If provided, will be
                checked for format requirements and length constraints. Pass None
                to skip email validation. Defaults to None.
            password (str, optional): Password to validate. If provided, will be
                checked for security requirements and content validation. Pass None
                to skip password validation. Defaults to None.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if all provided data passes validation, False otherwise
                - str: Empty string if validation passes, detailed error message if validation fails

        Validation Rules:
            Member ID:
                - Cannot be empty or whitespace-only
                - Minimum length: 3 characters
                - Required for all operations

            Email (when provided):
                - Must contain '@' symbol (basic format check)
                - Must contain '.' symbol (domain validation)
                - Minimum length: 5 characters
                - Format validation for email structure

            Password (when provided):
                - Minimum length: 6 characters
                - Cannot be whitespace-only
                - Must contain actual content (not just spaces)

        Error Messages:
            - "Member ID cannot be empty"
            - "Member ID must be at least 3 characters long"
            - "Invalid email format"
            - "Email too short"
            - "Password must be at least 6 characters long"
            - "Password cannot contain only whitespace"

        Example:
            >>> # Validate complete member data
            >>> is_valid, error = MemberInputService.validate_member_data(
            ...     "john_doe", "john@email.com", "securepass123"
            ... )
            >>> if is_valid:
            ...     print("All data is valid")
            ... else:
            ...     print(f"Validation failed: {error}")

            >>> # Validate only member ID and email
            >>> is_valid, error = MemberInputService.validate_member_data(
            ...     "jane_smith", email="jane@example.com"
            ... )

            >>> # Validate only member ID
            >>> is_valid, error = MemberInputService.validate_member_data("bob_wilson")

        Use Cases:
            - Pre-database validation in command execution
            - Input validation before API calls
            - Data integrity checks before updates
            - Business rule enforcement
            - Consistent validation across different operations

        Note:
            This method performs business-level validation and should be used
            in addition to, not instead of, Pydantic model validation. It focuses
            on business rules and constraints that may not be captured in the
            data model validation layer.
        """
        # Validate member ID
        if not member_id or len(member_id.strip()) == 0:
            return False, "Member ID cannot be empty"

        if len(member_id) < 3:
            return False, "Member ID must be at least 3 characters long"

        # Validate email if provided
        if email is not None:
            if "@" not in email or "." not in email:
                return False, "Invalid email format"

            if len(email) < 5:
                return False, "Email too short"

        # Validate password if provided
        if password is not None:
            if len(password) < 6:
                return False, "Password must be at least 6 characters long"

            if password.isspace():
                return False, "Password cannot contain only whitespace"

        return True, ""
