"""
Comprehensive test suite for BookRoomCommand module.

This module contains extensive unit tests for the BookRoomCommand class,
covering all aspects of the room booking command execution including:
- Successful booking operations
- Input collection failures
- Database operation failures
- Exception handling
- Edge cases and boundary conditions

The tests use mocking to isolate the command logic from external dependencies
like the database and input service, ensuring fast and reliable unit testing.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, time

from business_logic.commands.booking.book_room_command import BookRoomCommand
from persistence.models import Booking


class TestBookRoomCommandExecute(unittest.TestCase):
    """Test cases for BookRoomCommand execute method."""

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_success(self, mock_input_service, mock_db):
        """Test successful room booking execution."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_new_booking_data.assert_called_once()
        mock_db.book_room.assert_called_once_with(
            "T1", date(2026, 12, 25), time(14, 30), "testuser"
        )

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_booking_data_collection_cancelled(
        self, mock_input_service, mock_db
    ):
        """Test when user cancels booking data collection."""
        # Arrange
        mock_input_service.collect_new_booking_data.return_value = None
        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Booking creation cancelled or failed")
        mock_input_service.collect_new_booking_data.assert_called_once()
        mock_db.book_room.assert_not_called()

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_database_booking_fails(self, mock_input_service, mock_db):
        """Test when database booking operation fails."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = False

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Booking operation failed")
        mock_db.book_room.assert_called_once()

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_with_different_room_types(self, mock_input_service, mock_db):
        """Test booking with different room types."""
        room_types = ["T1", "B1", "AR", "MPF1"]

        for room_id in room_types:
            with self.subTest(room_id=room_id):
                # Arrange
                mock_booking = Booking(
                    room_id=room_id,
                    book_date=date(2026, 12, 25),
                    book_time=time(14, 30),
                    user="testuser",
                )
                mock_input_service.collect_new_booking_data.return_value = mock_booking
                mock_db.book_room.return_value = True

                command = BookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_with_different_times(self, mock_input_service, mock_db):
        """Test booking with different time slots."""
        times = [
            time(6, 0),  # Start of business hours
            time(12, 0),  # Midday
            time(18, 30),  # Evening
            time(22, 0),  # End of business hours
        ]

        for book_time in times:
            with self.subTest(book_time=book_time):
                # Arrange
                mock_booking = Booking(
                    room_id="T1",
                    book_date=date(2026, 12, 25),
                    book_time=book_time,
                    user="testuser",
                )
                mock_input_service.collect_new_booking_data.return_value = mock_booking
                mock_db.book_room.return_value = True

                command = BookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_with_different_dates(self, mock_input_service, mock_db):
        """Test booking with various future dates."""
        dates = [
            date(2026, 1, 6),  # Tomorrow
            date(2026, 1, 31),  # End of month
            date(2026, 12, 31),  # End of year
        ]

        for book_date in dates:
            with self.subTest(book_date=book_date):
                # Arrange
                mock_booking = Booking(
                    room_id="T1",
                    book_date=book_date,
                    book_time=time(14, 30),
                    user="testuser",
                )
                mock_input_service.collect_new_booking_data.return_value = mock_booking
                mock_db.book_room.return_value = True

                command = BookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_with_different_users(self, mock_input_service, mock_db):
        """Test booking with different user IDs."""
        users = ["user123", "member_test", "john_doe", "a" * 50]

        for user in users:
            with self.subTest(user=user):
                # Arrange
                mock_booking = Booking(
                    room_id="T1",
                    book_date=date(2026, 12, 25),
                    book_time=time(14, 30),
                    user=user,
                )
                mock_input_service.collect_new_booking_data.return_value = mock_booking
                mock_db.book_room.return_value = True

                command = BookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_with_data_parameter_ignored(self, mock_input_service, mock_db):
        """Test that data parameter is ignored (interface compatibility)."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act - pass data parameter
        success, error = command.execute(data={"some": "data"})

        # Assert - should work normally, data is ignored
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_exception_in_input_service(self, mock_input_service, mock_db):
        """Test exception handling when input service raises error."""
        # Arrange
        mock_input_service.collect_new_booking_data.side_effect = Exception(
            "Input service error"
        )
        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.book_room.assert_not_called()

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_exception_in_database(self, mock_input_service, mock_db):
        """Test exception handling when database raises error."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.side_effect = Exception("Database connection error")

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_multiple_bookings_sequential(self, mock_input_service, mock_db):
        """Test executing multiple bookings sequentially."""
        # Arrange
        bookings = [
            Booking(
                room_id="T1",
                book_date=date(2026, 12, 25),
                book_time=time(10, 0),
                user="user1",
            ),
            Booking(
                room_id="T2",
                book_date=date(2026, 12, 26),
                book_time=time(11, 0),
                user="user2",
            ),
            Booking(
                room_id="B1",
                book_date=date(2026, 12, 27),
                book_time=time(12, 0),
                user="user3",
            ),
        ]

        command = BookRoomCommand()

        for booking in bookings:
            with self.subTest(booking=booking):
                # Setup for each booking
                mock_input_service.collect_new_booking_data.return_value = booking
                mock_db.book_room.return_value = True

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_booking_values_passed_correctly(self, mock_input_service, mock_db):
        """Test that all booking values are passed correctly to database."""
        # Arrange
        room_id = "AR"
        book_date = date(2026, 6, 15)
        book_time = time(16, 45)
        user = "special_user_123"

        mock_booking = Booking(
            room_id=room_id, book_date=book_date, book_time=book_time, user=user
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        command.execute()

        # Assert - verify exact parameters passed to database
        mock_db.book_room.assert_called_once_with(room_id, book_date, book_time, user)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_return_value_structure(self, mock_input_service, mock_db):
        """Test that return value structure is correct."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        result = command.execute()

        # Assert
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        # result[1] should be None or string

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_success_return_values(self, mock_input_service, mock_db):
        """Test return values for successful booking."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_failure_return_values(self, mock_input_service, mock_db):
        """Test return values for failed booking."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = False

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertIsNotNone(error)
        self.assertIsInstance(error, str)
        self.assertEqual(error, "Booking operation failed")

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_success_message(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that success message is printed."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        command.execute()

        # Assert - check that success message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn("T1", call_args)
        self.assertIn("testuser", call_args)
        self.assertIn("✅", call_args)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_failure_message(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that failure message is printed."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = False

        command = BookRoomCommand()

        # Act
        command.execute()

        # Assert - check that failure message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn("Failed", call_args) or self.assertIn("❌", call_args)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_error_message_on_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that error message is printed on exception."""
        # Arrange
        error_msg = "Database connection timeout"
        mock_input_service.collect_new_booking_data.side_effect = Exception(error_msg)

        command = BookRoomCommand()

        # Act
        command.execute()

        # Assert - check that error message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn(error_msg, call_args) or self.assertIn("❌", call_args)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_edge_case_long_room_id(self, mock_input_service, mock_db):
        """Test booking with maximum length room ID."""
        # Arrange
        mock_booking = Booking(
            room_id="A" * 10,  # Maximum 10 characters
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_edge_case_short_room_id(self, mock_input_service, mock_db):
        """Test booking with single character room ID."""
        # Arrange
        mock_booking = Booking(
            room_id="A",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_edge_case_minimum_user_id(self, mock_input_service, mock_db):
        """Test booking with minimum length user ID (3 characters)."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="abc",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_execute_edge_case_maximum_user_id(self, mock_input_service, mock_db):
        """Test booking with maximum length user ID (50 characters)."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="u" * 50,
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)


class TestBookRoomCommandIntegration(unittest.TestCase):
    """Integration tests for BookRoomCommand."""

    def test_command_instantiation(self):
        """Test that command can be instantiated."""
        command = BookRoomCommand()
        self.assertIsNotNone(command)

    def test_command_has_execute_method(self):
        """Test that command has execute method."""
        command = BookRoomCommand()
        self.assertTrue(hasattr(command, "execute"))
        self.assertTrue(callable(getattr(command, "execute")))

    @patch("business_logic.commands.booking.book_room_command.db")
    @patch("business_logic.commands.booking.book_room_command.BookingInputService")
    def test_command_interface_compliance(self, mock_input_service, mock_db):
        """Test that command follows Command interface."""
        # Arrange
        mock_booking = Booking(
            room_id="T1",
            book_date=date(2026, 12, 25),
            book_time=time(14, 30),
            user="testuser",
        )
        mock_input_service.collect_new_booking_data.return_value = mock_booking
        mock_db.book_room.return_value = True

        command = BookRoomCommand()

        # Act
        result = command.execute()

        # Assert - check it returns tuple with expected structure
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_multiple_command_instances(self):
        """Test that multiple command instances can coexist."""
        command1 = BookRoomCommand()
        command2 = BookRoomCommand()
        command3 = BookRoomCommand()

        self.assertIsNotNone(command1)
        self.assertIsNotNone(command2)
        self.assertIsNotNone(command3)
        self.assertIsNot(command1, command2)
        self.assertIsNot(command2, command3)


if __name__ == "__main__":
    unittest.main()
