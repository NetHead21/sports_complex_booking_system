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
