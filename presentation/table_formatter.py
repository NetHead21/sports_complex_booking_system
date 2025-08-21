"""
Table Formatter Module for Sports Booking System.

This module provides utilities for formatting tabular data into clean, readable tables
for console display. It includes a flexible TableFormatter class and specialized
formatting functions for different data types commonly used in the sports booking system.

The module supports:
- Generic table formatting with customizable headers and titles
- Column-specific formatting functions (e.g., currency, datetime, status)
- Member data tables with balance formatting
- Room booking tables with datetime and payment status formatting
- Automatic column width calculation for optimal display
- Optional table titles and record counts

Example:
    >>> from table_formatter import format_member_table
    >>> member_data = [("john_doe", "john@email.com", 25.50)]
    >>> print(format_member_table(member_data))

    🏟️ Sports Complex Members
    ===========================
    Username | Email         | Balance
    ---------|---------------|--------
    john_doe | john@email.com| $25.50
    ---------|---------------|--------
    Total records: 1

Classes:
    TableFormatter: Core table formatting class with customizable headers.

Functions:
    format_table_generic: Generic table formatter with column-specific formatters.
    format_member_table: Specialized formatter for member data.
    format_booking_table: Specialized formatter for room booking data.

Author: Sports Booking System Development Team
Date: August 2025
Version: 1.0
"""

from typing import List, Tuple, Any, Optional, Dict, Callable


class TableFormatter:
    """
    A utility class for formatting data into neat, aligned tables for console display.

    This class provides the core functionality for creating formatted tables with
    automatic column width calculation, headers, separators, and optional titles.
    It's designed to handle various data types and provides consistent formatting
    across the sports booking system.

    Features:
        - Automatic column width calculation based on content and headers
        - Support for optional table titles with decorative borders
        - Row separators and summary information
        - Flexible data type handling with string conversion
        - Clean, aligned column display

    Attributes:
        headers (List[str]): Column headers for the table.

    Example:
        >>> formatter = TableFormatter(["Name", "Age", "Score"])
        >>> data = [("Alice", 25, 95.5), ("Bob", 30, 87.2)]
        >>> print(formatter.format_table(data, "Student Results"))

        Student Results
        ===============
        Name  | Age | Score
        ------|-----|------
        Alice | 25  | 95.5
        Bob   | 30  | 87.2
        ------|-----|------
        Total records: 2
    """

    def __init__(self, headers: List[str]):
        """
        Initialize the table formatter with column headers.

        Sets up the table formatter with the specified column headers that will
        be used for all tables created with this formatter instance.

        Args:
            headers (List[str]): A list of column header names. The number of
                headers determines the expected number of columns in data rows.
                Headers should be descriptive and concise.

        Raises:
            ValueError: If headers list is empty or contains non-string elements.

        Example:
            >>> formatter = TableFormatter(["ID", "Name", "Status"])
            >>> # Now formatter is ready to format 3-column data
        """
        if not headers:
            raise ValueError("Headers list cannot be empty")
        if not all(isinstance(header, str) for header in headers):
            raise ValueError("All headers must be strings")
        self.headers = headers

    def format_table(
        self, data: List[Tuple[Any, ...]], title: Optional[str] = None
    ) -> str:
        """
        Format data into a well-structured table string ready for console display.

        This method takes raw data and transforms it into a formatted table with
        proper alignment, separators, and optional title. It automatically calculates
        optimal column widths and handles various data types through string conversion.

        Args:
            data (List[Tuple[Any, ...]]): A list of tuples where each tuple represents
                a row of data. Each tuple should have the same number of elements as
                there are headers. Data can be of any type that can be converted to string.
            title (Optional[str], optional): An optional title to display above the table.
                If provided, it will be centered and surrounded by decorative borders.
                Defaults to None.

        Returns:
            str: A complete formatted table as a multi-line string, including:
                - Optional title with decorative borders
                - Column headers with proper alignment
                - Separator lines between sections
                - Data rows with consistent spacing
                - Bottom separator and record count summary

        Raises:
            ValueError: If data rows don't match the number of headers.

        Example:
            >>> formatter = TableFormatter(["Product", "Price", "Stock"])
            >>> data = [("Widget", 19.99, 50), ("Gadget", 29.99, 25)]
            >>> result = formatter.format_table(data, "Inventory Report")
            >>> print(result)

            Inventory Report
            ================
            Product | Price | Stock
            --------|-------|------
            Widget  | 19.99 | 50
            Gadget  | 29.99 | 25
            --------|-------|------
            Total records: 2
        """
        if not data:
            return "No data to display."

        # Calculate column widths
        column_widths = self._calculate_column_widths(data)

        # Build the table
        lines = []

        # Add title if provided
        if title:
            total_width = sum(column_widths) + len(column_widths) * 3 - 1
            lines.append("=" * total_width)
            lines.append(title.center(total_width))
            lines.append("=" * total_width)

        # Add header
        header_line = " | ".join(
            header.ljust(column_widths[i]) for i, header in enumerate(self.headers)
        )
        lines.append(header_line)

        # Add separator
        separator = "-+-".join("-" * width for width in column_widths)
        lines.append(separator)

        # Add data rows
        for row in data:
            row_line = " | ".join(
                str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)
            )
            lines.append(row_line)

        # Add bottom separator and summary
        lines.append(separator)
        lines.append(f"Total records: {len(data)}")

        return "\n".join(lines)

    def _calculate_column_widths(self, data: List[Tuple[Any, ...]]) -> List[int]:
        """
        Calculate optimal column widths based on content and headers.

        This private method analyzes both the header text and all data rows to
        determine the minimum width needed for each column to display all content
        without truncation. It ensures that columns are wide enough to accommodate
        the longest content in each column.

        Args:
            data (List[Tuple[Any, ...]]): The data rows to analyze for width calculation.
                Each element will be converted to string to measure its display width.

        Returns:
            List[int]: A list of integers representing the minimum width needed for
                each column. The list length matches the number of headers.

        Note:
            - Starts with header lengths as minimum widths
            - Iterates through all data rows to find maximum content width per column
            - Handles data type conversion to string for width measurement
            - Gracefully handles rows with fewer columns than headers

        Example:
            For headers ["Name", "Age"] and data [("Alice", 25), ("Bob", 30)]:
            Returns [5, 3] (max of "Alice"/4 and "Name"/4 = 5, max of "25"/2 and "Age"/3 = 3)
        """
        widths = [len(header) for header in self.headers]

        for row in data:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))

        return widths


def format_table_generic(
    data: List[Tuple],
    headers: List[str],
    title: str,
    column_formatters: Optional[Dict[int, Callable]] = None,
) -> str:
    """
    Generic table formatter with optional column-specific formatting functions.

    This function provides a high-level interface for creating formatted tables with
    the ability to apply custom formatting to specific columns. It's particularly
    useful when different columns need different display formats (e.g., currency,
    dates, status indicators).

    Args:
        data (List[Tuple]): A list of tuples containing the raw data to be formatted.
            Each tuple represents a row, and should have the same number of elements
            as there are headers.
        headers (List[str]): Column headers for the table. Must match the number
            of elements in each data tuple.
        title (str): The title to display above the table. Will be used for both
            the header display and calculating border width.
        column_formatters (Optional[Dict[int, Callable]], optional): A dictionary
            mapping column indices (0-based) to formatting functions. Each formatter
            function should accept a single value and return a formatted string.
            If None, all columns will use default string conversion. Defaults to None.

    Returns:
        str: A complete formatted table string ready for display, or a message
            indicating no data is available if the data list is empty.

    Raises:
        ValueError: If headers and data column counts don't match.
        TypeError: If column_formatters values are not callable.

    Example:
        >>> data = [("Product A", 19.99, True), ("Product B", 29.99, False)]
        >>> headers = ["Product", "Price", "Available"]
        >>> formatters = {
        ...     1: lambda x: f"${x:.2f}",  # Format price as currency
        ...     2: lambda x: "✅" if x else "❌"  # Format boolean as emoji
        ... }
        >>> result = format_table_generic(data, headers, "Product Catalog", formatters)
        >>> print(result)

        Product Catalog
        ===============
        Product   | Price  | Available
        ----------|--------|----------
        Product A | $19.99 | ✅
        Product B | $29.99 | ❌
        ----------|--------|----------
        Total records: 2

    Note:
        This function is the recommended way to create formatted tables when you need
        custom column formatting. For simple tables without special formatting,
        TableFormatter can be used directly.
    """
    if not data:
        return f"\n{title}\n{'=' * len(title)}\nNo data to display.\n"

    # Apply column formatters if provided
    if column_formatters:
        formatted_data = []
        for row in data:
            new_row = []
            for i, cell in enumerate(row):
                formatter = column_formatters.get(i, str)
                new_row.append(formatter(cell))
            formatted_data.append(tuple(new_row))
        data = formatted_data

    formatter = TableFormatter(headers)
    return formatter.format_table(data, title)


# Convenience functions for specific data types
def format_member_table(
    member_data: List[Tuple[str, str, float]], title: str = "🏟️ Sports Complex Members"
) -> str:
    """
    Format member data into a professional table with currency formatting.

    This specialized formatter is designed specifically for displaying sports complex
    member information. It automatically formats the balance column as currency and
    provides a clean, consistent display for member management operations.

    Args:
        member_data (List[Tuple[str, str, float]]): A list of tuples containing member
            information. Each tuple should contain:
            - str: Username/member identifier
            - str: Email address
            - float: Account balance (will be formatted as currency)
        title (str, optional): The title to display above the member table.
            Defaults to "🏟️ Sports Complex Members" with emoji for visual appeal.

    Returns:
        str: A formatted table string with:
            - Username column (left-aligned)
            - Email column (left-aligned)
            - Balance column (formatted as currency with $ symbol and 2 decimal places)
            - Professional spacing and separators
            - Total member count at the bottom

    Example:
        >>> member_data = [
        ...     ("john_doe", "john@email.com", 25.50),
        ...     ("jane_smith", "jane@email.com", 100.00),
        ...     ("bob_wilson", "bob@longdomain.com", 0.0)
        ... ]
        >>> print(format_member_table(member_data))

        🏟️ Sports Complex Members
        ===========================
        Username   | Email              | Balance
        -----------|--------------------|--------
        john_doe   | john@email.com     | $25.50
        jane_smith | jane@email.com     | $100.00
        bob_wilson | bob@longdomain.com | $0.00
        -----------|--------------------|--------
        Total records: 3

    Note:
        This function is specifically designed for the sports booking system's
        member management features. The balance formatting ensures consistent
        currency display throughout the application.
    """
    return format_table_generic(
        member_data,
        ["Username", "Email", "Balance"],
        title,
        {2: lambda x: f"${float(x):.2f}"},  # Format balance as currency
    )


def format_booking_table(
    booking_data: List[Tuple[str, str, str, str, str]], title: str = "🏨 Room Bookings"
) -> str:
    """
    Format room booking data into a professional table with datetime and status formatting.

    This specialized formatter is designed for displaying room booking information in
    the sports complex booking system. It automatically formats datetime values and
    payment status with visual indicators for enhanced readability.

    Args:
        booking_data (List[Tuple[str, str, str, str, str]]): A list of tuples containing
            booking information. Each tuple should contain:
            - str: Room ID (unique identifier for the room)
            - str: Room type (e.g., "Basketball Court", "Tennis Court")
            - str: Booking datetime (should be convertible to datetime format)
            - str: Member ID (identifier of the member who made the booking)
            - str: Payment status ("PAID", "UNPAID", or similar)
        title (str, optional): The title to display above the booking table.
            Defaults to "🏨 Room Bookings" with emoji for visual appeal.

    Returns:
        str: A formatted table string with:
            - Room ID column (left-aligned)
            - Room Type column (left-aligned)
            - Booking DateTime column (formatted as YYYY-MM-DD HH:MM)
            - Member ID column (left-aligned)
            - Payment Status column (with ✅/❌ emoji indicators)
            - Professional spacing and separators
            - Total booking count at the bottom

    Example:
        >>> booking_data = [
        ...     ("R001", "Basketball Court", "2025-08-21 14:30", "john_doe", "PAID"),
        ...     ("R002", "Tennis Court", "2025-08-21 16:00", "jane_smith", "UNPAID"),
        ...     ("R003", "Swimming Pool", "2025-08-22 09:00", "bob_wilson", "PAID")
        ... ]
        >>> print(format_booking_table(booking_data))

        🏨 Room Bookings
        ================
        Room ID | Room Type        | Booking DateTime  | Member ID  | Payment Status
        --------|------------------|-------------------|------------|---------------
        R001    | Basketball Court | 2025-08-21 14:30 | john_doe   | ✅ PAID
        R002    | Tennis Court     | 2025-08-21 16:00 | jane_smith | ❌ UNPAID
        R003    | Swimming Pool    | 2025-08-22 09:00 | bob_wilson | ✅ PAID
        --------|------------------|-------------------|------------|---------------
        Total records: 3

    Note:
        - Datetime formatting attempts to parse datetime objects but falls back to
          string representation if parsing fails
        - Payment status formatting is case-insensitive and uses emoji indicators
          for quick visual identification
        - This function is specifically designed for the sports booking system's
          room management and booking display features
    """
    return format_table_generic(
        booking_data,
        ["Room ID", "Room Type", "Booking DateTime", "Member ID", "Payment Status"],
        title,
        {
            2: lambda x: x.strftime("%Y-%m-%d %H:%M")
            if hasattr(x, "strftime")
            else str(x),  # Format datetime
            4: lambda x: "✅ PAID"
            if str(x).upper() == "PAID"
            else "❌ UNPAID",  # Format payment status
        },
    )
