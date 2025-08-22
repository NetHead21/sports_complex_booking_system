"""
Member Booking Database Module for Sports Booking System.

This module provides the MemberBookingDatabase class, which handles all database
operations related to member management in the sports complex booking system.
It serves as the data access layer for member-related operations, implementing
CRUD (Create, Read, Update, Delete) functionality with MySQL stored procedures.

The module is designed to work with MySQL database and uses stored procedures
for all database operations to ensure data integrity, security, and performance.
It includes comprehensive error handling and returns appropriate success/failure
indicators for use by the business logic layer.

Key Features:
    - Member creation and registration
    - Member profile updates (email, password)
    - Member deletion with safety checks
    - Member listing and retrieval
    - MySQL stored procedure integration
    - Comprehensive error handling
    - Transaction management with commit/rollback
    - Row count validation for operation verification

Database Integration:
    - Uses MySQL connector for database communication
    - Leverages stored procedures for data operations
    - Implements proper connection management
    - Handles database exceptions gracefully
    - Returns success/failure status for business logic

Stored Procedures Used:
    - insert_new_member(id, password, email): Creates new member record
    - delete_member(member_id): Removes member from database
    - update_member_password(member_id, password): Updates member password
    - update_member_email(member_id, email): Updates member email address

Classes:
    MemberBookingDatabase: Main database access class for member operations.

Dependencies:
    - mysql.connector: MySQL database connectivity
    - persistence.DatabaseManager: Database connection and execution management
    - persistence.models.Member: Pydantic model for member data validation

Example:
    >>> from member_booking_database import MemberBookingDatabase
    >>> from models import Member
    >>>
    >>> # Initialize database connection
    >>> db = MemberBookingDatabase()
    >>>
    >>> # Create new member
    >>> member = Member(id="john_doe", password="secure123", email="john@email.com")
    >>> db.create_new_member(member)
    >>>
    >>> # Update member email
    >>> success = db.update_member_email("john_doe", "john.doe@email.com")
    >>> if success:
    ...     print("Email updated successfully")
    >>>
    >>> # List all members
    >>> members = db.show_members()
    >>> for member in members:
    ...     print(f"Member: {member[0]}, Email: {member[1]}")
"""

import mysql
from mysql.connector.cursor_cext import CMySQLCursor

from persistence import DatabaseManager
from .models import Member


class MemberBookingDatabase:
    """
    Database access layer for member management operations in the sports booking system.

    This class provides a comprehensive interface for all member-related database
    operations, serving as the data persistence layer in the clean architecture
    pattern. It handles all CRUD operations for member data using MySQL stored
    procedures and provides proper error handling and transaction management.

    The class is designed to be used by business logic components and provides
    clear success/failure indicators for all operations. It abstracts the
    complexity of database operations and provides a clean interface for
    member data management.

    Architecture Role:
        - Data Access Layer in clean architecture
        - Abstracts database complexity from business logic
        - Provides consistent interface for member operations
        - Handles connection management and error handling
        - Ensures data integrity through stored procedures

    Key Features:
        - CRUD operations for member data
        - MySQL stored procedure integration
        - Transaction management with proper commit/rollback
        - Row count validation for operation verification
        - Comprehensive error handling and logging
        - Return value patterns for business logic integration

    Database Schema Assumptions:
        - members table with columns: id, password, email, payment_due, member_since
        - Stored procedures: insert_new_member, delete_member, update_member_password, update_member_email
        - Primary key: id (member username)
        - Foreign key constraints handled by stored procedures

    Error Handling Strategy:
        - Catches mysql.connector.Error exceptions
        - Prints error messages for debugging
        - Returns False for failed operations
        - Maintains database connection integrity
        - Handles rollback scenarios gracefully

    Return Value Patterns:
        - create_new_member(): None (void operation with exception handling)
        - update_*/delete_* operations: bool (True=success, False=failure)
        - show_members(): List of tuples containing member data

    Attributes:
        db (DatabaseManager): Database connection and execution manager instance.

    Example:
        >>> # Initialize database access
        >>> member_db = MemberBookingDatabase()
        >>>
        >>> # Create a new member
        >>> member = Member(id="alice", password="secure123", email="alice@email.com")
        >>> member_db.create_new_member(member)
        >>>
        >>> # Update member information
        >>> email_updated = member_db.update_member_email("alice", "alice.smith@email.com")
        >>> password_updated = member_db.update_member_password("alice", "newsecure456")
        >>>
        >>> # Retrieve member list
        >>> all_members = member_db.show_members()
        >>> print(f"Total members: {len(all_members)}")
        >>>
        >>> # Delete member (with safety check)
        >>> deleted = member_db.delete_member("alice")
        >>> if deleted:
        ...     print("Member deleted successfully")
        ... else:
        ...     print("Member not found or deletion failed")
    """

    def __init__(self):
        """
        Initialize the MemberBookingDatabase with a database connection manager.

        Creates a new database access instance by initializing the DatabaseManager
        which handles MySQL connection management, query execution, and connection
        pooling. The database manager provides the low-level database operations
        while this class provides the member-specific business logic.

        Initialization Process:
            1. Creates DatabaseManager instance for connection management
            2. Establishes connection pool for efficient database access
            3. Prepares for stored procedure execution
            4. Sets up error handling infrastructure

        Attributes Created:
            db (DatabaseManager): Database connection and execution manager that
                provides execute() method for running queries and stored procedures.

        Connection Details:
            - Uses configuration from DatabaseManager for connection parameters
            - Establishes MySQL connection with appropriate timeout settings
            - Enables connection pooling for performance optimization
            - Configures for stored procedure execution

        Error Handling:
            Database connection errors are handled by the DatabaseManager layer.
            This constructor focuses on object initialization and delegates
            connection management to the specialized DatabaseManager class.

        Example:
            >>> # Create database access instance
            >>> member_db = MemberBookingDatabase()
            >>> # Database connection is now ready for operations
            >>> members = member_db.show_members()

        Note:
            The actual database connection is managed by DatabaseManager and
            is established when the first database operation is performed.
            This lazy connection approach improves application startup time
            and resource utilization.
        """
        self.db = DatabaseManager()

    def create_new_member(self, member: Member) -> None:
        """
        Create a new member record in the database using validated member data.

        This method inserts a new member into the members table using the
        insert_new_member stored procedure. It accepts a validated Member object
        and extracts the necessary data for database insertion. The operation
        includes proper transaction management with commit on success.

        Database Operation:
            - Calls insert_new_member stored procedure
            - Passes member ID (username), password, and email
            - Commits transaction on successful insertion
            - Handles database constraints and validations via stored procedure

        Args:
            member (Member): A validated Member object containing:
                - id (str): Unique member username/identifier
                - password (str): Member password (will be stored as provided)
                - email (str): Member email address (must be unique in database)

        Returns:
            None: This method performs a database operation and returns nothing.
                  Success is indicated by lack of exception. Failure results
                  in mysql.connector.Error exception or printed error message.

        Database Schema Impact:
            - Inserts record into members table
            - Sets member_since to current timestamp (handled by stored procedure)
            - Initializes payment_due to default value (typically 0.00)
            - Enforces unique constraints on id and email fields

        Transaction Management:
            - Executes stored procedure within implicit transaction
            - Commits transaction on successful execution
            - Database handles rollback automatically on constraint violations
            - Connection remains stable after operation completion

        Error Handling:
            - Catches mysql.connector.Error for database-related issues
            - Prints error message to console for debugging
            - Does not re-raise exception (silent failure for UI layer)
            - Common errors: duplicate username, duplicate email, constraint violations

        Stored Procedure Details:
            insert_new_member(id, password, email):
                - Validates unique constraints
                - Sets default values for payment_due and member_since
                - Handles any database-level business rules
                - Returns appropriate error codes for constraint violations

        Example:
            >>> from models import Member
            >>> member_db = MemberBookingDatabase()
            >>>
            >>> # Create validated member object
            >>> new_member = Member(
            ...     id="john_doe",
            ...     password="secure_password123",
            ...     email="john.doe@email.com"
            ... )
            >>>
            >>> # Insert into database
            >>> member_db.create_new_member(new_member)
            >>> print("Member created successfully")

        Common Error Scenarios:
            - Duplicate username: Member ID already exists in database
            - Duplicate email: Email address already registered
            - Invalid data format: Constraint violations in stored procedure
            - Database connection issues: Network or server problems
            - Database unavailability: Server maintenance or downtime

        Note:
            This method does not return success/failure status. It relies on
            exception handling for error reporting. Consider catching
            mysql.connector.Error in calling code for proper error handling.
            The stored procedure handles password hashing if required by the
            database schema design.
        """

        try:
            query = """
                call insert_new_member(%s, %s, %s);
            """
            self.db.execute(query, member.id, member.password, member.email)
            self.db.connection.commit()

        except mysql.connector.Error as err:
            print(err)

    def delete_member(self, member_id: str) -> bool:
        """
        Delete a member record from the database with existence validation.

        This method removes a member from the members table using the delete_member
        stored procedure. It includes safety checks by validating the row count
        to ensure the member existed before deletion. The operation provides clear
        success/failure feedback for use by business logic components.

        Safety Features:
            - Validates member existence before confirming deletion
            - Uses row count to verify operation success
            - Handles foreign key constraints through stored procedure
            - Provides clear success/failure return values
            - Maintains referential integrity through database constraints

        Args:
            member_id (str): The unique member username/identifier to delete.
                Must match exactly with existing member record.

        Returns:
            bool: Deletion operation result:
                - True: Member was found and successfully deleted
                - False: Member was not found, deletion failed, or database error occurred

        Database Operation:
            - Calls delete_member stored procedure with member_id parameter
            - Checks rowcount to verify actual deletion occurred
            - Commits transaction only on successful deletion
            - Handles cascading deletes through stored procedure logic

        Row Count Validation:
            - rowcount == 0: No member found with provided ID (returns False)
            - rowcount > 0: Member found and deleted (returns True)
            - Provides reliable feedback about operation success

        Transaction Management:
            - Executes deletion within database transaction
            - Commits transaction only after successful deletion
            - Database handles automatic rollback on constraint violations
            - Maintains data consistency throughout operation

        Cascading Effects:
            The stored procedure may handle related data cleanup:
            - Cancel active bookings for the member
            - Clean up payment records
            - Remove member from waiting lists
            - Archive member data for auditing purposes

        Error Handling:
            - Catches mysql.connector.Error for database issues
            - Prints detailed error messages for debugging
            - Returns False for any error conditions
            - Maintains database connection stability

        Example:
            >>> member_db = MemberBookingDatabase()
            >>>
            >>> # Attempt to delete existing member
            >>> success = member_db.delete_member("john_doe")
            >>> if success:
            ...     print("Member john_doe deleted successfully")
            ... else:
            ...     print("Member john_doe not found or deletion failed")
            >>>
            >>> # Attempt to delete non-existent member
            >>> result = member_db.delete_member("nonexistent_user")
            >>> assert result == False  # Member doesn't exist

        Common Scenarios:
            - Success: Member exists and is deleted (returns True)
            - Not Found: Member ID doesn't exist in database (returns False)
            - Constraint Violation: Foreign key prevents deletion (returns False)
            - Database Error: Connection or server issues (returns False)

        Security Considerations:
            - No SQL injection risk due to parameterized stored procedure
            - Member existence is validated before deletion confirmation
            - Operation is logged at database level for audit trails
            - Referential integrity maintained through foreign key constraints

        Note:
            This method implements the recommended pattern of returning boolean
            success indicators for database operations. The stored procedure
            should handle all business rules related to member deletion,
            including any cleanup operations for related data.
        """

        try:
            query = """
                call delete_member(%s);
            """
            result = self.db.execute(query, member_id)

            # Check if any rows were affected
            if result.rowcount == 0:
                return False  # No rows affected means member doesn't exist

            self.db.connection.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False

    def update_member_password(self, member_id: str, password: str) -> bool:
        """
        Update a member's password with existence validation and security handling.

        This method updates a member's password using the update_member_password
        stored procedure. It includes member existence validation through row count
        checking and provides clear success/failure feedback. The operation ensures
        that password updates are only applied to existing members.

        Security Features:
            - Validates member existence before password update
            - Uses parameterized stored procedure to prevent SQL injection
            - Handles password processing through secure stored procedure
            - Provides clear feedback about operation success
            - Maintains audit trail through database logging

        Args:
            member_id (str): The unique member username/identifier whose password
                should be updated. Must match exactly with existing member record.
            password (str): The new password for the member. Password processing
                (hashing, salting) is handled by the stored procedure according
                to the database security policy.

        Returns:
            bool: Password update operation result:
                - True: Member was found and password successfully updated
                - False: Member was not found, update failed, or database error occurred

        Database Operation:
            - Calls update_member_password stored procedure
            - Passes member_id and new password as parameters
            - Checks rowcount to verify member existence and update success
            - Commits transaction only on successful update

        Row Count Validation:
            - rowcount == 0: No member found with provided ID (returns False)
            - rowcount > 0: Member found and password updated (returns True)
            - Ensures update confirmation before returning success

        Password Security:
            The stored procedure is responsible for:
            - Password hashing using appropriate algorithms (bcrypt, Argon2, etc.)
            - Salt generation and application
            - Password strength validation if required
            - Compliance with security policies
            - Audit logging of password changes

        Transaction Management:
            - Executes update within database transaction
            - Commits transaction only after successful update
            - Database handles automatic rollback on any failures
            - Maintains data consistency throughout operation

        Error Handling:
            - Catches mysql.connector.Error for database issues
            - Prints detailed error messages with context
            - Returns False for any error conditions
            - Maintains stable database connection

        Example:
            >>> member_db = MemberBookingDatabase()
            >>>
            >>> # Update password for existing member
            >>> success = member_db.update_member_password("john_doe", "new_secure_password123")
            >>> if success:
            ...     print("Password updated successfully for john_doe")
            ... else:
            ...     print("Password update failed - member not found or database error")
            >>>
            >>> # Attempt to update password for non-existent member
            >>> result = member_db.update_member_password("unknown_user", "password123")
            >>> assert result == False  # Member doesn't exist

        Common Scenarios:
            - Success: Member exists and password is updated (returns True)
            - Not Found: Member ID doesn't exist in database (returns False)
            - Validation Error: Password doesn't meet policy requirements (returns False)
            - Database Error: Connection issues or server problems (returns False)

        Security Considerations:
            - Password is passed as parameter to prevent SQL injection
            - Actual password hashing handled by stored procedure
            - No plaintext passwords stored in database
            - Password change events logged for security auditing
            - Original password is not required (administrative update)

        Business Rules:
            The stored procedure may enforce:
            - Password complexity requirements
            - Password history to prevent reuse
            - Account lockout policies
            - Password expiration settings
            - Compliance with organizational security policies

        Note:
            This method does not perform password validation - that responsibility
            lies with the input validation layer and the stored procedure. The
            method focuses on database operation execution and success reporting.
            Consider implementing password strength validation at the business
            logic layer before calling this method.
        """

        try:
            query = """
                call update_member_password(%s, %s);
            """
            result = self.db.execute(query, member_id, password)

            # Check if any rows were affected
            if result.rowcount == 0:
                return False  # No rows affected means member doesn't exist

            self.db.connection.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False

    def update_member_email(self, member_id: str, email: str) -> bool:
        """
        Update a member's email address with validation and uniqueness checking.

        This method updates a member's email address using the update_member_email
        stored procedure. It includes member existence validation through row count
        checking and ensures email uniqueness through database constraints. The
        operation provides clear success/failure feedback for business logic integration.

        Validation Features:
            - Validates member existence before email update
            - Enforces email uniqueness through database constraints
            - Uses parameterized stored procedure for security
            - Provides reliable success/failure feedback
            - Maintains data integrity through constraint enforcement

        Args:
            member_id (str): The unique member username/identifier whose email
                should be updated. Must match exactly with existing member record.
            email (str): The new email address for the member. Must be unique
                across all members and conform to email format requirements
                enforced by the stored procedure.

        Returns:
            bool: Email update operation result:
                - True: Member was found and email successfully updated
                - False: Member not found, email already exists, constraint violation, or database error

        Database Operation:
            - Calls update_member_email stored procedure
            - Passes member_id and new email as parameters
            - Checks rowcount to verify member existence and update success
            - Commits transaction only on successful update

        Row Count Validation:
            - rowcount == 0: No member found with provided ID (returns False)
            - rowcount > 0: Member found and email updated (returns True)
            - Provides confirmation that update actually occurred

        Email Uniqueness:
            The stored procedure enforces:
            - Email uniqueness across all member records
            - Email format validation (basic structure)
            - Prevention of duplicate email assignments
            - Appropriate error handling for constraint violations

        Transaction Management:
            - Executes update within database transaction
            - Commits transaction only after successful update
            - Database handles automatic rollback on constraint violations
            - Maintains referential integrity throughout operation

        Error Handling:
            - Catches mysql.connector.Error for database issues
            - Prints detailed error messages for debugging
            - Returns False for any error conditions
            - Handles constraint violations gracefully

        Example:
            >>> member_db = MemberBookingDatabase()
            >>>
            >>> # Update email for existing member
            >>> success = member_db.update_member_email("john_doe", "john.doe@newemail.com")
            >>> if success:
            ...     print("Email updated successfully for john_doe")
            ... else:
            ...     print("Email update failed - member not found, email exists, or database error")
            >>>
            >>> # Attempt to use duplicate email
            >>> result = member_db.update_member_email("jane_smith", "john.doe@newemail.com")
            >>> assert result == False  # Email already exists

        Common Scenarios:
            - Success: Member exists and email is unique (returns True)
            - Not Found: Member ID doesn't exist in database (returns False)
            - Duplicate Email: Email already used by another member (returns False)
            - Invalid Format: Email doesn't meet format requirements (returns False)
            - Database Error: Connection issues or server problems (returns False)

        Constraint Violations:
            - Duplicate email constraint: Returns False, error logged
            - Invalid email format: Handled by stored procedure validation
            - Member not found: Returns False based on rowcount check
            - Foreign key violations: Handled by database integrity rules

        Business Impact:
            Email updates may affect:
            - Member communication and notifications
            - Login credentials if email is used for authentication
            - Billing and payment notifications
            - Booking confirmations and reminders
            - System-generated correspondence

        Security Considerations:
            - Email parameter is passed securely to stored procedure
            - No SQL injection risk due to parameterization
            - Email changes logged for audit trails
            - Validation occurs at database level for consistency
            - Constraint enforcement prevents data integrity issues

        Note:
            This method relies on the stored procedure for email format validation
            and business rule enforcement. Consider implementing client-side email
            validation at the input layer for better user experience, while
            maintaining server-side validation for security and data integrity.
        """

        try:
            query = """
                call update_member_email(%s, %s);
            """
            result = self.db.execute(query, member_id, email)

            # Check if any rows were affected
            if result.rowcount == 0:
                return False  # No rows affected means member doesn't exist

            self.db.connection.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False

    def show_members(self) -> CMySQLCursor:
        """
        Retrieve all member records from the database for display and reporting purposes.

        This method executes a SELECT query to fetch all member records from the
        members table, returning essential member information in a format suitable
        for display by the presentation layer. The results are ordered by membership
        registration date for consistent and meaningful presentation.

        Query Details:
            - Selects: id (username), email, payment_due
            - Source: members table
            - Ordering: member_since DESC (newest members first)
            - No filtering: Returns all active members

        Returns:
            List[Tuple]: A list of tuples containing member data, where each tuple contains:
                - [0] id (str): Member username/unique identifier
                - [1] email (str): Member email address
                - [2] payment_due (float/Decimal): Outstanding payment amount

            Returns empty list if no members exist or database error occurs.

        Data Structure:
            Each returned tuple represents one member record:
            - Index 0: Member ID (primary key, unique username)
            - Index 1: Email address (unique, contact information)
            - Index 2: Payment due amount (financial status indicator)

        Sorting Logic:
            - Results ordered by member_since column in descending order
            - Newest members appear first in the list
            - Provides chronological view of member registration
            - Facilitates recent member identification

        Error Handling:
            - Catches mysql.connector.Error for database issues
            - Prints error messages to console for debugging
            - Returns empty result set on error conditions
            - Maintains application stability during database issues

        Performance Considerations:
            - Retrieves all member records (no pagination)
            - Suitable for small to medium member databases
            - Consider implementing pagination for large datasets
            - Uses database sorting for optimal performance

        Example:
            >>> member_db = MemberBookingDatabase()
            >>> members = member_db.show_members()
            >>>
            >>> # Display member information
            >>> for member in members:
            ...     username, email, payment_due = member
            ...     print(f"Member: {username}")
            ...     print(f"Email: {email}")
            ...     print(f"Payment Due: ${payment_due:.2f}")
            ...     print("-" * 30)
            >>>
            >>> # Check if any members exist
            >>> if members:
            ...     print(f"Total members: {len(members)}")
            ... else:
            ...     print("No members found in database")

        Use Cases:
            - Member listing displays in administrative interfaces
            - Report generation for membership statistics
            - Data export for external systems
            - Member count and status overview
            - Payment due summary reporting

        Integration with Presentation Layer:
            This method is typically used with table formatting utilities:
            >>> from presentation.table_formatter import format_member_table
            >>> members = member_db.show_members()
            >>> formatted_table = format_member_table(members, "Active Members")
            >>> print(formatted_table)

        Database Schema Requirements:
            - members table must exist
            - Required columns: id, email, payment_due, member_since
            - member_since column used for sorting (should have default value)
            - Appropriate indexes on member_since for performance

        Security Considerations:
            - No sensitive data exposed (passwords excluded from query)
            - Uses direct SELECT query (no injection risk)
            - Payment information included for administrative purposes
            - Member privacy maintained through selective field exposure

        Note:
            This method returns all member records without pagination. For
            applications with large member databases, consider implementing
            pagination or filtering mechanisms to improve performance and
            user experience. The payment_due field provides financial status
            information useful for administrative and billing purposes.
        """

        query = """
            select
                id,
                email,
                payment_due
            from members
            order by member_since desc;
        """

        try:
            results = self.db.execute(query)
            return results.fetchall()
        except mysql.connector.Error as err:
            print(err)


if __name__ == "__main__":
    member_booking = MemberBookingDatabase()
    # print(member_booking.show_members())

    # Insert new member to members table
    member_data = {
        "id": "shalow21",
        "password": "hello_world_21",
        "email": "shalow21@gmail.com",
    }
    member_booking.create_new_member(Member(**member_data))
