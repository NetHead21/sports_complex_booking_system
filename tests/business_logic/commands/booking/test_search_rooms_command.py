"""
Comprehensive test suite for SearchRoomCommand module.

This module contains extensive unit tests for the SearchRoomCommand class,
covering all aspects of the room search command execution including:
- Successful search operations with various criteria
- Search operations with no results
- Input collection failures
- Database operation failures
- Exception handling
- Edge cases and boundary conditions
- Different room types, dates, and times
- Print output verification
- Thread safety considerations

The tests use mocking to isolate the command logic from external dependencies
like the database and input service, ensuring fast and reliable unit testing.
"""

import unittest
from unittest.mock import patch, MagicMock, call
from datetime import date, time

from business_logic.commands.booking.search_rooms_command import SearchRoomCommand
from persistence.models import SearchRoom


class TestSearchRoomCommandExecute(unittest.TestCase):
    """Test cases for SearchRoomCommand execute method."""

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_success_with_results(self, mock_input_service, mock_db):
        """Test successful search execution with results found."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria

        mock_cursor_result = MagicMock()
        mock_cursor_result.__bool__.return_value = True  # Truthy cursor result
        mock_db.search_room.return_value = mock_cursor_result

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertEqual(result, mock_cursor_result)
        mock_input_service.collect_room_search_data.assert_called_once()
        mock_db.search_room.assert_called_once_with(
            "Tennis Court", date(2026, 3, 15), time(14, 30)
        )

        # Verify success message was printed
        mock_print.assert_called_with(
            "✅ Search completed for Tennis Court on 2026-03-15 at 14:30:00"
        )

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_success_with_no_results(self, mock_input_service, mock_db):
        """Test successful search execution but no rooms found."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Badminton Court",
            book_date=date(2026, 4, 20),
            book_time=time(18, 0),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_db.search_room.return_value = None  # No results

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(result, "No search results")
        mock_db.search_room.assert_called_once()

        # Verify no results message was printed
        mock_print.assert_called_with("❌ No rooms found matching your criteria.")

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_input_collection_cancelled(self, mock_input_service, mock_db):
        """Test when user cancels search criteria collection."""

        # Arrange
        mock_input_service.collect_room_search_data.return_value = None
        command = SearchRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(result, "Room search cancelled or failed")
        mock_input_service.collect_room_search_data.assert_called_once()
        mock_db.search_room.assert_not_called()

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_different_room_types(self, mock_input_service, mock_db):
        """Test search with different room types."""

        room_types = [
            "Tennis Court",
            "Badminton Court",
            "Archery Range",
            "Multi-Purpose Field",
        ]

        for room_type in room_types:
            with self.subTest(room_type=room_type):
                # Arrange
                mock_search_criteria = SearchRoom(
                    room_type=room_type,
                    book_date=date(2026, 3, 15),
                    book_time=time(14, 30),
                )
                mock_input_service.collect_room_search_data.return_value = (
                    mock_search_criteria
                )
                mock_cursor = MagicMock()
                mock_cursor.__bool__.return_value = True
                mock_db.search_room.return_value = mock_cursor

                command = SearchRoomCommand()

                # Act
                with patch("builtins.print"):
                    success, result = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertEqual(result, mock_cursor)
                mock_db.search_room.assert_called_with(
                    room_type, date(2026, 3, 15), time(14, 30)
                )

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_different_dates(self, mock_input_service, mock_db):
        """Test search with various future dates."""

        dates = [
            date(2026, 2, 16),  # Tomorrow
            date(2026, 2, 28),  # End of month
            date(2026, 12, 31),  # End of year
            date(2027, 1, 1),  # Next year
        ]

        for book_date in dates:
            with self.subTest(book_date=book_date):
                # Arrange
                mock_search_criteria = SearchRoom(
                    room_type="Tennis Court",
                    book_date=book_date,
                    book_time=time(14, 30),
                )
                mock_input_service.collect_room_search_data.return_value = (
                    mock_search_criteria
                )
                mock_cursor = MagicMock()
                mock_cursor.__bool__.return_value = True
                mock_db.search_room.return_value = mock_cursor

                command = SearchRoomCommand()

                # Act
                with patch("builtins.print"):
                    success, result = command.execute()

                # Assert
                self.assertTrue(success)
                mock_db.search_room.assert_called_with(
                    "Tennis Court", book_date, time(14, 30)
                )

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_different_times(self, mock_input_service, mock_db):
        """Test search with different time slots."""

        times = [
            time(6, 0),  # Start of business hours
            time(9, 30),  # Morning
            time(12, 0),  # Midday
            time(15, 45),  # Afternoon
            time(18, 30),  # Evening
            time(22, 0),  # End of business hours
        ]

        for book_time in times:
            with self.subTest(book_time=book_time):
                # Arrange
                mock_search_criteria = SearchRoom(
                    room_type="Tennis Court",
                    book_date=date(2026, 3, 15),
                    book_time=book_time,
                )
                mock_input_service.collect_room_search_data.return_value = (
                    mock_search_criteria
                )
                mock_cursor = MagicMock()
                mock_cursor.__bool__.return_value = True
                mock_db.search_room.return_value = mock_cursor

                command = SearchRoomCommand()

                # Act
                with patch("builtins.print"):
                    success, result = command.execute()

                # Assert
                self.assertTrue(success)
                mock_db.search_room.assert_called_with(
                    "Tennis Court", date(2026, 3, 15), book_time
                )

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_database_exception(self, mock_input_service, mock_db):
        """Test when database search operation raises an exception."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_db.search_room.side_effect = Exception("Database connection error")

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(result, "Database connection error")
        # Verify error message was printed
        mock_print.assert_called_with("❌ Search Error: Database connection error")

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_input_service_exception(self, mock_input_service, mock_db):
        """Test when input service raises an exception."""

        # Arrange
        mock_input_service.collect_room_search_data.side_effect = Exception(
            "Input validation error"
        )
        command = SearchRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(result, "Input validation error")
        mock_db.search_room.assert_not_called()
        # Verify error message was printed
        mock_print.assert_called_with("❌ Search Error: Input validation error")

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_data_parameter_none(self, mock_input_service, mock_db):
        """Test execution with None as data parameter (default)."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = True
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute(data=None)

        # Assert
        self.assertTrue(success)
        self.assertEqual(result, mock_cursor)
        mock_input_service.collect_room_search_data.assert_called_once()

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_data_parameter_value(self, mock_input_service, mock_db):
        """Test execution with data parameter (should be ignored)."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = True
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute(data={"ignored": "parameter"})

        # Assert
        self.assertTrue(success)
        # Data parameter should be ignored, input service still called
        mock_input_service.collect_room_search_data.assert_called_once()

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_empty_cursor_result(self, mock_input_service, mock_db):
        """Test when database returns an empty cursor (falsy)."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria

        # Mock an empty cursor that evaluates to False
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = False
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print") as mock_print:
            success, result = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(result, "No search results")
        mock_print.assert_called_with("❌ No rooms found matching your criteria.")

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_return_value_tuple_structure(self, mock_input_service, mock_db):
        """Test that execute returns proper tuple structure."""

        # Arrange - Success case
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )
        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = True
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print"):
            result = command.execute()

        # Assert
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_multiple_calls_independence(self, mock_input_service, mock_db):
        """Test that multiple execute calls are independent (thread safety)."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(14, 30),
        )

        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = True
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act - Execute multiple times
        with patch("builtins.print"):
            result1 = command.execute()
            result2 = command.execute()

        # Assert - Both calls should succeed independently
        self.assertTrue(result1[0])
        self.assertTrue(result2[0])
        self.assertEqual(mock_input_service.collect_room_search_data.call_count, 2)
        self.assertEqual(mock_db.search_room.call_count, 2)


class TestSearchRoomCommandEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions for SearchRoomCommand."""

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_boundary_time_early_morning(
        self, mock_input_service, mock_db
    ):
        """Test search at earliest business hour (6:00 AM)."""

        # Arrange
        mock_search_criteria = SearchRoom(
            room_type="Tennis Court",
            book_date=date(2026, 3, 15),
            book_time=time(6, 0),  # Earliest business hour
        )

        mock_input_service.collect_room_search_data.return_value = mock_search_criteria
        mock_cursor = MagicMock()
        mock_cursor.__bool__.return_value = True
        mock_db.search_room.return_value = mock_cursor

        command = SearchRoomCommand()

        # Act
        with patch("builtins.print"):
            success, result = command.execute()

        # Assert
        self.assertTrue(success)
        mock_db.search_room.assert_called_with(
            "Tennis Court", date(2026, 3, 15), time(6, 0)
        )

    @patch("business_logic.commands.booking.search_rooms_command.db")
    @patch("business_logic.commands.booking.search_rooms_command.BookingInputService")
    def test_execute_with_boundary_time_late_evening(self, mock_input_service, mock_db):
        """Test search at latest business hour (10:00 PM)."""
