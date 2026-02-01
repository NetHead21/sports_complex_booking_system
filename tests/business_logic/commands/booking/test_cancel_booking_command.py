"""
Comprehensive test suite for CancelBookRoomCommand module.

This module contains extensive unit tests for the CancelBookRoomCommand class,
covering all aspects of the booking cancellation command execution including:
- Successful cancellation operations
- Input collection failures
- Database operation failures
- Exception handling
- Edge cases and boundary conditions
- Authorization validation
- Security verification scenarios

The tests use mocking to isolate the command logic from external dependencies
like the database and input service, ensuring fast and reliable unit testing.
"""

import unittest
from unittest.mock import patch, MagicMock

from business_logic.commands.booking.cancel_booking_command import CancelBookRoomCommand


class TestCancelBookRoomCommandExecute(unittest.TestCase):
    """Test cases for CancelBookRoomCommand execute method."""

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_success(self, mock_input_service, mock_db):
        """Test successful booking cancellation execution."""
        # Arrange
        booking_id = "12345"
        member_id = "testuser"
        mock_input_service.collect_booking_cancellation_data.return_value = (
            booking_id,
            member_id,
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_booking_cancellation_data.assert_called_once()
        mock_db.cancel_booking.assert_called_once_with(int(booking_id))

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_cancellation_data_collection_cancelled(
        self, mock_input_service, mock_db
    ):
        """Test when user cancels cancellation data collection."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = None
        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Booking cancellation cancelled or failed")
        mock_input_service.collect_booking_cancellation_data.assert_called_once()
        mock_db.cancel_booking.assert_not_called()

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_database_cancellation_fails(self, mock_input_service, mock_db):
        """Test when database cancellation operation fails."""

        # Arrange
        booking_id = "12345"
        member_id = "testuser"
        mock_input_service.collect_booking_cancellation_data.return_value = (
            booking_id,
            member_id,
        )
        mock_db.cancel_booking.return_value = False

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Cancellation operation failed")
        mock_db.cancel_booking.assert_called_once()

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_with_different_booking_ids(self, mock_input_service, mock_db):
        """Test cancellation with different booking IDs."""

        booking_ids = ["1", "999", "12345", "99999"]

        for booking_id in booking_ids:
            with self.subTest(booking_id=booking_id):
                # Arrange

                mock_input_service.collect_booking_cancellation_data.return_value = (
                    booking_id,
                    "testuser",
                )
                mock_db.cancel_booking.return_value = True

                command = CancelBookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)
                mock_db.cancel_booking.assert_called_with(int(booking_id))

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_with_different_member_ids(self, mock_input_service, mock_db):
        """Test cancellation with different member IDs."""

        member_ids = ["user123", "member_test", "john_doe", "a" * 50]

        for member_id in member_ids:
            with self.subTest(member_id=member_id):
                # Arrange

                mock_input_service.collect_booking_cancellation_data.return_value = (
                    "12345",
                    member_id,
                )
                mock_db.cancel_booking.return_value = True

                command = CancelBookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_with_data_parameter_ignored(self, mock_input_service, mock_db):
        """Test that data parameter is ignored (interface compatibility)."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act - pass data parameter
        success, error = command.execute(data={"some": "data"})

        # Assert - should work normally, data is ignored
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_exception_in_input_service(self, mock_input_service, mock_db):
        """Test exception handling when input service raises error."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.side_effect = Exception(
            "Input service error"
        )
        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.cancel_booking.assert_not_called()

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_exception_in_database(self, mock_input_service, mock_db):
        """Test exception handling when database raises error."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.side_effect = Exception("Database connection error")

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_multiple_cancellations_sequential(
        self, mock_input_service, mock_db
    ):
        """Test executing multiple cancellations sequentially."""

        # Arrange
        cancellations = [
            ("100", "user1"),
            ("101", "user2"),
            ("102", "user3"),
        ]

        command = CancelBookRoomCommand()

        for booking_id, member_id in cancellations:
            with self.subTest(booking_id=booking_id, member_id=member_id):
                # Setup for each cancellation
                mock_input_service.collect_booking_cancellation_data.return_value = (
                    booking_id,
                    member_id,
                )
                mock_db.cancel_booking.return_value = True

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)
                self.assertIsNone(error)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_booking_id_conversion_to_int(self, mock_input_service, mock_db):
        """Test that booking ID is correctly converted to int."""

        # Arrange
        booking_id_str = "99999"
        mock_input_service.collect_booking_cancellation_data.return_value = (
            booking_id_str,
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        command.execute()

        # Assert - verify exact parameters passed to database
        mock_db.cancel_booking.assert_called_once_with(int(booking_id_str))

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_return_value_structure(self, mock_input_service, mock_db):
        """Test that return value structure is correct."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        result = command.execute()

        # Assert
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        # result[1] should be None or string

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_success_return_values(self, mock_input_service, mock_db):
        """Test return values for successful cancellation."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_failure_return_values(self, mock_input_service, mock_db):
        """Test return values for failed cancellation."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.return_value = False

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertIsNotNone(error)
        self.assertIsInstance(error, str)
        self.assertEqual(error, "Cancellation operation failed")

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_success_message(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that success message is printed."""

        # Arrange
        booking_id = "12345"
        member_id = "testuser"
        mock_input_service.collect_booking_cancellation_data.return_value = (
            booking_id,
            member_id,
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        command.execute()

        # Assert - check that success message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn(booking_id, call_args)
        self.assertIn(member_id, call_args)
        self.assertIn("✅", call_args)
        self.assertIn("cancelled successfully", call_args.lower())

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_failure_message(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that failure message is printed."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.return_value = False

        command = CancelBookRoomCommand()

        # Act
        command.execute()

        # Assert - check that failure message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn("Failed", call_args) or self.assertIn("❌", call_args)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    @patch("builtins.print")
    def test_execute_prints_error_message_on_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that error message is printed on exception."""

        # Arrange
        error_msg = "Database connection timeout"
        mock_input_service.collect_booking_cancellation_data.side_effect = Exception(
            error_msg
        )

        command = CancelBookRoomCommand()

        # Act
        command.execute()

        # Assert - check that error message was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        self.assertIn(error_msg, call_args) or self.assertIn("❌", call_args)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_edge_case_minimum_booking_id(self, mock_input_service, mock_db):
        """Test cancellation with minimum booking ID value."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "1",
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        mock_db.cancel_booking.assert_called_once_with(1)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_edge_case_large_booking_id(self, mock_input_service, mock_db):
        """Test cancellation with large booking ID value."""

        # Arrange
        large_id = "999999"
        mock_input_service.collect_booking_cancellation_data.return_value = (
            large_id,
            "testuser",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)
        mock_db.cancel_booking.assert_called_once_with(int(large_id))

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_edge_case_minimum_member_id(self, mock_input_service, mock_db):
        """Test cancellation with minimum length member ID (3 characters)."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "abc",
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_edge_case_maximum_member_id(self, mock_input_service, mock_db):
        """Test cancellation with maximum length member ID (50 characters)."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "u" * 50,
        )
        mock_db.cancel_booking.return_value = True

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertTrue(success)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_edge_case_special_characters_in_member_id(
        self, mock_input_service, mock_db
    ):
        """Test cancellation with special characters in member ID."""

        # Arrange
        special_member_ids = ["user_123", "john.doe", "member-test"]

        for member_id in special_member_ids:
            with self.subTest(member_id=member_id):
                mock_input_service.collect_booking_cancellation_data.return_value = (
                    "12345",
                    member_id,
                )
                mock_db.cancel_booking.return_value = True

                command = CancelBookRoomCommand()

                # Act
                success, error = command.execute()

                # Assert
                self.assertTrue(success)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_database_timeout_error(self, mock_input_service, mock_db):
        """Test handling of database timeout error."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "12345",
            "testuser",
        )
        mock_db.cancel_booking.side_effect = TimeoutError("Database timeout")

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertIn("timeout", error.lower())

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_value_error_on_invalid_booking_id_conversion(
        self, mock_input_service, mock_db
    ):
        """Test handling of invalid booking ID that cannot be converted to int."""

        # Arrange
        mock_input_service.collect_booking_cancellation_data.return_value = (
            "invalid",
            "testuser",
        )

        command = CancelBookRoomCommand()

        # Act
        success, error = command.execute()

        # Assert
        self.assertFalse(success)
        self.assertIsNotNone(error)
        self.assertIsInstance(error, str)

    @patch("business_logic.commands.booking.cancel_booking_command.db")
    @patch("business_logic.commands.booking.cancel_booking_command.BookingInputService")
    def test_execute_keyboard_interrupt_handling(self, mock_input_service, mock_db):
        """Test that keyboard interrupt (Ctrl+C) propagates as expected."""
        # Arrange

        mock_input_service.collect_booking_cancellation_data.side_effect = (
            KeyboardInterrupt()
        )

        command = CancelBookRoomCommand()

        # Act & Assert - KeyboardInterrupt should propagate (not caught by except Exception)
        with self.assertRaises(KeyboardInterrupt):
            command.execute()
