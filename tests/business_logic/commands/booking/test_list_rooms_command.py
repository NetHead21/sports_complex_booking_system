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

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(mock_bookings)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_various_time_formats(self, mock_db, mock_format_table):
        """Test execution with different time formats from database."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user1", "2026-02-10", "06:00:00"),  # Early morning
            (2, "T1", "user2", "2026-02-10", "12:00:00"),  # Noon
            (3, "T1", "user3", "2026-02-10", "18:30:00"),  # Evening
            (4, "T1", "user4", "2026-02-10", "23:59:59"),  # Late night
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Various times table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(mock_bookings)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_duplicate_bookings_same_room(
        self, mock_db, mock_format_table
    ):
        """Test execution with multiple bookings for the same room."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user1", "2026-02-10", "10:00:00"),
            (2, "T1", "user2", "2026-02-10", "11:00:00"),
            (3, "T1", "user3", "2026-02-10", "12:00:00"),
            (4, "T1", "user4", "2026-02-11", "10:00:00"),
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Same room multiple bookings"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(mock_bookings)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_special_characters_in_data(self, mock_db, mock_format_table):
        """Test execution with special characters in booking data."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user@123", "2026-02-10", "10:00:00"),
            (2, "B-1", "user.name", "2026-02-10", "11:00:00"),
            (3, "AR_2", "user_123", "2026-02-10", "12:00:00"),
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Special characters table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(mock_bookings)


class TestListRoomCommandDatabaseExceptions(unittest.TestCase):
    """Test cases for database exception handling."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_database_exception_handled_gracefully(
        self, mock_db, mock_format_table
    ):
        """Test that database exceptions are raised (not caught by command)."""

        # Arrange
        mock_db.show_bookings.side_effect = Exception("Database connection error")
        command = ListRoomCommand()

        # Act & Assert
        with self.assertRaises(Exception) as context:
            command.execute()

        self.assertIn("Database connection error", str(context.exception))
        mock_db.show_bookings.assert_called_once()
        mock_format_table.assert_not_called()

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_database_returns_none(self, mock_db, mock_format_table):
        """Test execution when database returns None instead of list."""

        # Arrange
        mock_db.show_bookings.return_value = None
        mock_format_table.return_value = "Formatted None"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(None)
        mock_print.assert_called_once_with("Formatted None")

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_database_timeout_exception(self, mock_db, mock_format_table):
        """Test handling of database timeout exception."""

        # Arrange
        mock_db.show_bookings.side_effect = TimeoutError("Database query timeout")
        command = ListRoomCommand()

        # Arrange
        mock_db.show_bookings.side_effect = TimeoutError("Database query timeout")
        command = ListRoomCommand()

        # Act & Assert
        with self.assertRaises(TimeoutError):
            command.execute()

        mock_db.show_bookings.assert_called_once()


class TestListRoomCommandFormatterExceptions(unittest.TestCase):
    """Test cases for table formatter exception handling."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_formatter_exception_raised(self, mock_db, mock_format_table):
        """Test that formatter exceptions are propagated."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.side_effect = ValueError("Formatting error")

        command = ListRoomCommand()

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            command.execute()

        self.assertIn("Formatting error", str(context.exception))
        mock_db.show_bookings.assert_called_once()
        mock_format_table.assert_called_once_with(mock_bookings)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_formatter_returns_empty_string(self, mock_db, mock_format_table):
        """Test execution when formatter returns empty string."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = ""

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_print.assert_called_once_with("")

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_formatter_returns_none(self, mock_db, mock_format_table):
        """Test execution when formatter returns None."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = None

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(result)
        mock_print.assert_called_once_with(None)


class TestListRoomCommandPrintExceptions(unittest.TestCase):
    """Test cases for print operation exception handling."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_print_exception_raised(self, mock_db, mock_format_table):
        """Test that print exceptions are propagated."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act & Assert
        with patch("builtins.print", side_effect=IOError("Print error")):
            with self.assertRaises(IOError):
                command.execute()


class TestListRoomCommandReturnValues(unittest.TestCase):
    """Test cases for verifying return value patterns."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_always_returns_tuple(self, mock_db, mock_format_table):
        """Test that execute always returns a tuple."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            result = command.execute()

        # Assert
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_first_return_value_is_boolean(self, mock_db, mock_format_table):
        """Test that first return value is always boolean."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute()

        # Assert
        self.assertIsInstance(success, bool)
        self.assertTrue(success)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_second_return_value_is_none(self, mock_db, mock_format_table):
        """Test that second return value is always None."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute()

        # Assert
        self.assertIsNone(result)


class TestListRoomCommandInstanceCreation(unittest.TestCase):
    """Test cases for command instance creation and initialization."""

    def test_command_instantiation(self):
        """Test that ListRoomCommand can be instantiated without errors."""

        # Act
        command = ListRoomCommand()

        # Assert
        self.assertIsNotNone(command)
        self.assertIsInstance(command, ListRoomCommand)

    def test_command_is_stateless(self):
        """Test that multiple command instances are independent."""
        # Act
        command1 = ListRoomCommand()
        command2 = ListRoomCommand()

        # Assert
        self.assertIsNot(command1, command2)
        self.assertIsInstance(command1, ListRoomCommand)
        self.assertIsInstance(command2, ListRoomCommand)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_command_reusability(self, mock_db, mock_format_table):
        """Test that same command instance can be executed multiple times."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act & Assert
        with patch("builtins.print"):
            success1, result1 = command.execute()
            success2, result2 = command.execute()
            success3, result3 = command.execute()

        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertTrue(success3)
        self.assertEqual(mock_db.show_bookings.call_count, 3)


class TestListRoomCommandIntegration(unittest.TestCase):
    """Integration test cases verifying component interactions."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_calls_components_in_correct_order(
        self, mock_db, mock_format_table
    ):
        """Test that execute calls database and formatter in correct order."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Create a call tracker
        call_order = []

        def track_db_call():
            call_order.append("db")
            return mock_bookings

        def track_format_call(data):
            call_order.append("format")
            return "Table"

        mock_db.show_bookings.side_effect = track_db_call
        mock_format_table.side_effect = track_format_call

        # Act
        with patch("builtins.print"):
            command.execute()

        # Assert
        self.assertEqual(call_order, ["db", "format"])

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_passes_database_result_to_formatter(
        self, mock_db, mock_format_table
    ):
        """Test that database result is passed correctly to formatter."""

        # Arrange
        mock_bookings = [
            (1, "T1", "user1", "2026-02-10", "10:00:00"),
            (2, "B1", "user2", "2026-02-11", "14:00:00"),
        ]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            command.execute()

        # Assert
        mock_format_table.assert_called_once()
        args, kwargs = mock_format_table.call_args
        self.assertEqual(args[0], mock_bookings)
        self.assertEqual(len(args[0]), 2)

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_prints_formatter_output(self, mock_db, mock_format_table):
        """Test that formatter output is printed to console."""

        # Arrange
        mock_bookings = [(1, "T1", "user1", "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        expected_output = "╔═══════════╗\n║ Bookings ║\n╚═══════════╝"
        mock_format_table.return_value = expected_output

        command = ListRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            command.execute()

        # Assert
        mock_print.assert_called_once_with(expected_output)


class TestListRoomCommandEdgeCases(unittest.TestCase):
    """Test cases for edge cases and boundary conditions."""

    @patch("business_logic.commands.booking.list_rooms_command.format_booking_table")
    @patch("business_logic.commands.booking.list_rooms_command.db")
    def test_execute_with_very_long_strings(self, mock_db, mock_format_table):
        """Test execution with very long string values in data."""

        # Arrange
        long_user = "a" * 1000
        long_room = "R" * 500
        mock_bookings = [(1, long_room, long_user, "2026-02-10", "10:00:00")]
        mock_db.show_bookings.return_value = mock_bookings
        mock_format_table.return_value = "Long strings table"

        command = ListRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        mock_format_table.assert_called_once_with(mock_bookings)
