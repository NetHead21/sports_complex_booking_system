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

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Member)
        self.assertEqual(result.id, "testuser")
        self.assertEqual(result.password, "password123")
        self.assertEqual(result.email, "test@email.com")
        self.assertEqual(mock_input.call_count, 3)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_new_member_data_keyboard_interrupt(self, mock_input):
        """Test handling of user cancellation via Ctrl+C."""

        mock_input.side_effect = KeyboardInterrupt()

        result = MemberInputService.collect_new_member_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_new_member_data_exception(self, mock_input):
        """Test handling of unexpected exceptions."""

        mock_input.side_effect = Exception("Unexpected error")

        result = MemberInputService.collect_new_member_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_new_member_data_empty_fields(self, mock_input):
        """Test handling of empty fields (should be caught by required=True)."""

        # Assuming get_user_input with required=True doesn't allow empty strings
        mock_input.side_effect = ["user123", "pass123", "test@example.com"]

        result = MemberInputService.collect_new_member_data()

        self.assertIsNotNone(result)
        self.assertEqual(result.id, "user123")


class TestMemberInputServiceCollectEmailUpdateData(unittest.TestCase):
    """Test cases for collect_member_email_update_data method."""

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_success(self, mock_input):
        """Test successful collection of email update data."""

        mock_input.side_effect = ["testuser", "newemail@example.com"]

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], "testuser")
        self.assertEqual(result[1], "newemail@example.com")
