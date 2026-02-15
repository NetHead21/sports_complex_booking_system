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
