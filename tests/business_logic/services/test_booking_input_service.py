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
