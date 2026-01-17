"""
Comprehensive test suite for MemberInputService module.

This module contains extensive unit tests for the MemberInputService class,
covering all input collection, validation, and display methods including:
- New member data collection
- Email update data collection
- Password update data collection with confirmation
- Member deletion with safety confirmations
- Member lookup operations
- Operation result display
- Member data validation

The tests use mocking to simulate user input and verify validation logic,
error handling, security workflows, and data formatting functionality.
"""

import unittest
from unittest.mock import patch, MagicMock, call

from business_logic.services.member_input_service import MemberInputService
from persistence.models import Member


class TestMemberInputServiceCollectNewMemberData(unittest.TestCase):
    """Test cases for collect_new_member_data method."""

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_new_member_data_success(self, mock_input):
        """Test successful collection of new member data."""

        mock_input.side_effect = ["testuser", "password123", "test@email.com"]

        result = MemberInputService.collect_new_member_data()
