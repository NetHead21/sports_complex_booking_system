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
