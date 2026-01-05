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
