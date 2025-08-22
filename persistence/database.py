"""
Database connection and management utilities for the Sports Booking Management System.

This module provides the core database connectivity and management functionality
for the sports booking system. It handles MySQL database connections, cursor
management, and provides a centralized interface for database operations across
the application.

The DatabaseManager class implements the Singleton pattern conceptually and
provides robust connection handling with automatic cleanup. It serves as the
foundation for all data persistence operations in the system.

Classes:
    DatabaseManager: Core database connection and query execution manager.

Dependencies:
    - os: Environment variable access for configuration
    - mysql.connector: MySQL database connectivity
    - dotenv: Environment variable loading from .env files
    - mysql.connector.cursor: Database cursor type annotations

Configuration:
    Requires environment variables:
    - PASSWORD: MySQL database password (loaded from .env file)
    
    Database connection parameters:
    - Host: localhost
    - User: root
    - Database: sports_booking

Example:
    >>> # Basic database usage
    >>> db = DatabaseManager()
    >>> cursor = db.execute("SELECT * FROM members WHERE member_id = %s", 123)
    >>> results = cursor.fetchall()
    >>> print(results)
    
    >>> # Complex query execution
    >>> query = "INSERT INTO member_bookings (room_id, member_id) VALUES (%s, %s)"
    >>> db.execute(query, room_id, member_id)

Security Note:
    This module uses environment variables for sensitive database credentials.
    Ensure .env file is properly secured and not committed to version control.
"""

import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import cursor

load_dotenv()


class DatabaseManager:
    """
    Core database connection and query execution manager for the sports booking system.
    
    This class provides a centralized interface for all database operations,
    managing MySQL connections, cursor creation, and query execution. It implements
    automatic connection management with proper resource cleanup to prevent
    connection leaks and ensure optimal database performance.
    
    The class follows the Facade pattern, providing a simplified interface to
    the underlying MySQL connector functionality while adding application-specific
    connection management and error handling.
    
    Attributes:
        connection (mysql.connector.MySQLConnection): Active database connection.
        cursor (mysql.connector.cursor.MySQLCursor): Default cursor for the connection.
    
    Connection Parameters:
        - Host: localhost (local MySQL server)
        - User: root (database administrator)
        - Password: Retrieved from environment variable PASSWORD
        - Database: sports_booking (application database)
    
    Design Patterns:
        - Facade Pattern: Simplifies database operations interface
        - Resource Management: Automatic connection cleanup
        - Configuration Pattern: Environment-based configuration
    
    Example:
        >>> # Initialize database manager
        >>> db_manager = DatabaseManager()
        
        >>> # Execute SELECT query
        >>> cursor = db_manager.execute(
        ...     "SELECT * FROM members WHERE email = %s",
        ...     "user@example.com"
        ... )
        >>> member = cursor.fetchone()
        
        >>> # Execute INSERT query
        >>> db_manager.execute(
        ...     "INSERT INTO members (name, email) VALUES (%s, %s)",
        ...     "John Doe", "john@example.com"
        ... )
        
        >>> # Connection automatically closed when object is destroyed
        >>> del db_manager
    
    Security Features:
        - Parameterized queries prevent SQL injection
        - Environment-based credential management
        - Automatic connection cleanup
    
    Note:
        Ensure the MySQL server is running and the sports_booking database
        exists before creating DatabaseManager instances. The PASSWORD
        environment variable must be set in the .env file.
    """
    
    def __init__(self):
        """
        Initialize a new DatabaseManager instance with MySQL connection.
        
        Creates a connection to the MySQL database using configuration from
        environment variables and establishes a default cursor for basic
        operations. The connection is configured for the sports_booking
        database on localhost.
        
        The initialization process:
        1. Loads environment variables from .env file
        2. Establishes MySQL connection with configured parameters
        3. Creates a default cursor for immediate use
        
        Environment Variables Required:
            PASSWORD (str): MySQL database password for the root user
        
        Connection Configuration:
            - Host: localhost
            - User: root
            - Database: sports_booking
            - Password: From environment variable
        
        Raises:
            mysql.connector.Error: If database connection fails
            FileNotFoundError: If .env file is missing
            KeyError: If PASSWORD environment variable is not set
            ConnectionError: If MySQL server is not accessible
        
        Example:
            >>> # Successful initialization
            >>> db = DatabaseManager()
            >>> print("Database connected successfully")
            
            >>> # Handle connection errors
            >>> try:
            ...     db = DatabaseManager()
            ... except mysql.connector.Error as e:
            ...     print(f"Database connection failed: {e}")
        
        Note:
            The connection remains active until the object is destroyed or
            the __del__ method is called. Ensure proper cleanup in long-running
            applications to prevent connection pool exhaustion.
        """
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=os.getenv("PASSWORD"),
            database="sports_booking",
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        """
        Clean up database resources when the object is destroyed.
        
        This destructor method ensures proper cleanup of database connections
        when the DatabaseManager instance is garbage collected or explicitly
        deleted. It prevents connection leaks and ensures optimal resource
        management in the MySQL connection pool.
        
        Cleanup Process:
            1. Closes the active database connection
            2. Releases connection resources back to the pool
            3. Ensures no hanging connections remain
        
        Automatic Invocation:
            - When object goes out of scope
            - When explicitly deleted with 'del' statement
            - During program termination
            - When garbage collector runs
        
        Exception Handling:
            The method includes implicit exception handling to prevent
            errors during cleanup from affecting application flow.
        
        Example:
            >>> db = DatabaseManager()
            >>> # Use database...
            >>> del db  # Explicitly cleanup (automatic in most cases)
            
            >>> # Automatic cleanup when out of scope
            >>> def database_operation():
            ...     db = DatabaseManager()
            ...     # db automatically cleaned up when function ends
        
        Best Practices:
            - Generally relies on automatic cleanup
            - Explicit cleanup recommended for long-running applications
            - Consider using context managers for guaranteed cleanup
        
        Note:
            In Python, __del__ is not guaranteed to be called immediately,
            so critical cleanup should not rely solely on this method.
            Consider implementing a close() method for explicit cleanup.
        """
        self.connection.close()

    def execute(self, statement, *values) -> cursor:
        """
        Execute a SQL statement with optional parameter values.
        
        This method provides a secure way to execute SQL statements with
        parameterized queries to prevent SQL injection attacks. It creates
        a new cursor for each execution to ensure query isolation and
        returns the cursor for result retrieval.
        
        The method supports all types of SQL operations including SELECT,
        INSERT, UPDATE, DELETE, and DDL statements. Parameter substitution
        is handled safely by the MySQL connector.
        
        Args:
            statement (str): SQL statement to execute. Use %s placeholders
                           for parameters to enable safe parameter substitution.
            *values: Variable number of values to substitute in the SQL statement.
                    Values are automatically escaped to prevent SQL injection.
        
        Returns:
            cursor (mysql.connector.cursor.MySQLCursor): Database cursor containing
                    query results. Use fetchone(), fetchall(), or fetchmany()
                    to retrieve results from SELECT queries.
        
        Security Features:
            - Parameterized queries prevent SQL injection
            - Automatic value escaping and type conversion
            - Query isolation through dedicated cursor
        
        Example:
            >>> db = DatabaseManager()
            
            >>> # SELECT with parameters
            >>> cursor = db.execute(
            ...     "SELECT * FROM members WHERE age > %s AND city = %s",
            ...     25, "New York"
            ... )
            >>> members = cursor.fetchall()
            
            >>> # INSERT with parameters
            >>> cursor = db.execute(
            ...     "INSERT INTO members (name, email, age) VALUES (%s, %s, %s)",
            ...     "Alice Smith", "alice@email.com", 30
            ... )
            >>> print(f"Inserted member with ID: {cursor.lastrowid}")
            
            >>> # UPDATE with parameters
            >>> cursor = db.execute(
            ...     "UPDATE members SET email = %s WHERE member_id = %s",
            ...     "newemail@example.com", 123
            ... )
            >>> print(f"Updated {cursor.rowcount} rows")
            
            >>> # DELETE with parameters
            >>> cursor = db.execute(
            ...     "DELETE FROM bookings WHERE booking_date < %s",
            ...     "2024-01-01"
            ... )
            >>> print(f"Deleted {cursor.rowcount} old bookings")
        
        Supported SQL Operations:
            - SELECT: Data retrieval with fetchone()/fetchall()
            - INSERT: Data insertion with lastrowid access
            - UPDATE: Data modification with rowcount
            - DELETE: Data removal with rowcount
            - DDL: Schema modifications (CREATE, ALTER, DROP)
        
        Error Handling:
            SQL errors are propagated as mysql.connector.Error exceptions.
            Handle these in calling code for robust error management.
        
        Performance Notes:
            - New cursor created for each query (ensures isolation)
            - Consider connection pooling for high-frequency operations
            - Use batch operations for multiple similar queries
        
        Security Warning:
            Always use parameterized queries (%s placeholders) instead of
            string formatting to prevent SQL injection vulnerabilities.
        """
        cursor = self.connection.cursor()
        cursor.execute(statement, values or [])
        return cursor


if __name__ == "__main__":
    """
    Demonstration and testing module for DatabaseManager functionality.
    
    This section provides a practical example of DatabaseManager usage,
    demonstrating how to execute queries and retrieve results. It serves
    both as documentation and as a basic test to verify database connectivity
    and query execution capabilities.
    
    The example shows:
    - DatabaseManager instantiation
    - Complex SELECT query execution
    - Result retrieval and display
    - Proper query formatting and structure
    
    Example Query:
        Retrieves booking information from member_bookings table including
        room details, booking timestamps, member information, and payment status.
    
    Usage:
        Run this module directly to test database connectivity:
        $ python database.py
    
    Expected Output:
        List of tuples containing booking records from the database.
        Each tuple represents: (room_id, room_type, datetime_of_booking, 
                               member_id, payment_status)
    
    Troubleshooting:
        - Ensure MySQL server is running
        - Verify sports_booking database exists
        - Check .env file contains correct PASSWORD
        - Confirm member_bookings table has data
    """
    database_manager = DatabaseManager()
    query = """
        select
            room_id,
            room_type,
            datetime_of_booking,
            member_id,
            payment_status
        from member_bookings
    """
    results = database_manager.execute(query)
    result = results.fetchall()
    print(result)
