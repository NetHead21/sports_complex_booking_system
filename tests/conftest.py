"""
Pytest configuration and fixtures for the test suite.

This module provides shared fixtures and configuration that mocks database
connections at import time to allow tests to run without requiring a live
database connection. This is essential for unit testing in isolation.
"""

import sys
from unittest.mock import MagicMock

# Mock the database modules before they are imported
# This prevents database connection attempts during import
sys.modules["persistence.database"] = MagicMock()
sys.modules["persistence.member_booking_database"] = MagicMock()
sys.modules["persistence.room_booking_database"] = MagicMock()
