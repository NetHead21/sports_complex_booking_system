"""
Comprehensive test suite for BookingInputService module.

This module contains extensive unit tests for the BookingInputService class,
covering all input collection and validation methods including:
- New booking data collection
- Room search criteria collection
- Booking cancellation data collection
- All private helper methods for input validation

The tests use mocking to simulate user input and verify validation logic,
error handling, and data formatting functionality.
"""

import unittest
from datetime import datetime, date, time
from unittest.mock import patch, MagicMock, call

from business_logic.services.booking_input_service import BookingInputService
from persistence.models import Booking, SearchRoom


class TestBookingInputServiceCollectNewBookingData(unittest.TestCase):
    """Test cases for collect_new_booking_data method."""

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_date"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_time"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_user_id"
    )
    @patch("business_logic.services.booking_input_service.get_user_input")
    def test_collect_new_booking_data_success(
        self, mock_input, mock_user_id, mock_time, mock_date, mock_room_id, mock_clear
    ):
        """Test successful collection of new booking data with user confirmation."""

        # Setup mock returns
        mock_room_id.return_value = "T1"
        mock_date.return_value = date(2026, 12, 25)
        mock_time.return_value = time(14, 30)
        mock_user_id.return_value = "user123"
        mock_input.return_value = "y"  # User confirms

        # Execute
        result = BookingInputService.collect_new_booking_data()

        # Verify
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Booking)
        self.assertEqual(result.room_id, "T1")
        self.assertEqual(result.book_date, date(2026, 12, 25))
        self.assertEqual(result.book_time, time(14, 30))
        self.assertEqual(result.user, "user123")

        # Verify all helper methods were called
        mock_clear.assert_called_once()
        mock_room_id.assert_called_once()
        mock_date.assert_called_once()
        mock_time.assert_called_once()
        mock_user_id.assert_called_once()

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_date"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_time"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_user_id"
    )
    @patch("business_logic.services.booking_input_service.get_user_input")
    def test_collect_new_booking_data_user_declines_confirmation(
        self, mock_input, mock_user_id, mock_time, mock_date, mock_room_id, mock_clear
    ):
        """Test user declines confirmation after entering booking data."""

        # Setup mock returns
        mock_room_id.return_value = "T1"
        mock_date.return_value = date(2026, 12, 25)
        mock_time.return_value = time(14, 30)
        mock_user_id.return_value = "user123"
        mock_input.return_value = "n"  # User declines

        # Execute
        result = BookingInputService.collect_new_booking_data()

        # Verify
        self.assertIsNone(result)

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    def test_collect_new_booking_data_room_id_cancelled(self, mock_room_id, mock_clear):
        """Test cancellation during room ID collection."""

        mock_room_id.return_value = None

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)
        mock_room_id.assert_called_once()

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_date"
    )
    def test_collect_new_booking_data_date_cancelled(
        self, mock_date, mock_room_id, mock_clear
    ):
        """Test cancellation during date collection."""

        mock_room_id.return_value = "T1"
        mock_date.return_value = None

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_date"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_time"
    )
    def test_collect_new_booking_data_time_cancelled(
        self, mock_time, mock_date, mock_room_id, mock_clear
    ):
        """Test cancellation during time collection."""

        mock_room_id.return_value = "T1"
        mock_date.return_value = date(2026, 12, 25)
        mock_time.return_value = None

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_date"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_book_time"
    )
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_user_id"
    )
    def test_collect_new_booking_data_user_id_cancelled(
        self, mock_user_id, mock_time, mock_date, mock_room_id, mock_clear
    ):
        """Test cancellation during user ID collection."""

        mock_room_id.return_value = "T1"
        mock_date.return_value = date(2026, 12, 25)
        mock_time.return_value = time(14, 30)
        mock_user_id.return_value = None

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    def test_collect_new_booking_data_keyboard_interrupt(
        self, mock_room_id, mock_clear
    ):
        """Test handling of Ctrl+C (KeyboardInterrupt)."""

        mock_room_id.side_effect = KeyboardInterrupt()

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)

    @patch("business_logic.services.booking_input_service.clear_screen")
    @patch(
        "business_logic.services.booking_input_service.BookingInputService._collect_room_id"
    )
    def test_collect_new_booking_data_exception(self, mock_room_id, mock_clear):
        """Test handling of unexpected exceptions."""

        mock_room_id.side_effect = Exception("Unexpected error")

        result = BookingInputService.collect_new_booking_data()

        self.assertIsNone(result)
