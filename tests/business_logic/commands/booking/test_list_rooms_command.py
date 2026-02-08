"""
Comprehensive test suite for ListRoomCommand module.

This module contains extensive unit tests for the ListRoomCommand class,
covering all aspects of the room listing command execution including:
- Successful listing operations with various data scenarios
- Empty booking list handling
- Database operation failures
- Table formatting integration
- Exception handling
- Edge cases and boundary conditions
- Output verification
- Thread safety considerations

The tests use mocking to isolate the command logic from external dependencies
like the database and table formatter, ensuring fast and reliable unit testing.
"""

import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO

from business_logic.commands.booking.list_rooms_command import ListRoomCommand


class TestListRoomCommandExecute(unittest.TestCase):
    """Test cases for ListRoomCommand execute method."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_success_with_bookings(self, mock_db, mock_format_table):
        """Test successful execution with booking data."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user1", "2026-02-10", "10:00:00"),
            (2, "B1", "user2", "2026-02-11", "14:00:00"),
            (3, "AR", "user3", "2026-02-12", "16:30:00"),
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Formatted Table Output"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_bookings.assert_called_once()
        mock_format_table.assert_called_once_with(mock_bookings)
        mock_print.assert_called_once_with("Formatted Table Output")

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_success_with_empty_bookings(self, mock_db, mock_format_table):
        """Test successful execution with no bookings (empty list)."""

        # Arrange
        mock_bookings = []
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "No bookings found"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_bookings.assert_called_once()
        mock_format_table.assert_called_once_with(mock_bookings)
        mock_print.assert_called_once_with("No bookings found")

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_none_data_parameter(self, mock_db, mock_format_table):
        """Test execution with None as data parameter (default)."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute(data=None)

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_bookings.assert_called_once()

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_arbitrary_data_parameter(self, mock_db, mock_format_table):
        """Test execution ignores arbitrary data parameter as it's unused."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute(data={"arbitrary": "data"})

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_bookings.assert_called_once()

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_single_booking(self, mock_db, mock_format_table):
        """Test execution with exactly one booking (boundary case)."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Single booking table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(mock_bookings)
        mock_print.assert_called_once_with("Single booking table")

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_large_booking_list(self, mock_db, mock_format_table):
        """Test execution with a large number of bookings."""

        # Arrange
        mock_bookings = [
            (i, f"Room{i}", f"user{i}", "2026-02-10", "10:00:00") for i in range(1, 101)
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Large table with 100 bookings"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_bookings.assert_called_once()
        mock_format_table.assert_called_once_with(mock_bookings)
        mock_print.assert_called_once()

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_various_room_types(self, mock_db, mock_format_table):
        """Test execution with different room types."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user1", "2026-02-10", "10:00:00"),
            (2, "T2", "user2", "2026-02-10", "11:00:00"),
            (3, "B1", "user3", "2026-02-10", "12:00:00"),
            (4, "B2", "user4", "2026-02-10", "13:00:00"),
            (5, "AR", "user5", "2026-02-10", "14:00:00"),
            (6, "MPF1", "user6", "2026-02-10", "15:00:00"),
            (7, "MPF2", "user7", "2026-02-10", "16:00:00"),
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Mixed room types table"

        command = ListRoomCommand()
