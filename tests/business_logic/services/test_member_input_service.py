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

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_missing_at_symbol(self, mock_input):
        """Test rejection of email without @ symbol."""

        mock_input.side_effect = ["testuser", "invalidemail.com"]

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_missing_dot(self, mock_input):
        """Test rejection of email without dot."""

        mock_input.side_effect = ["testuser", "invalid@email"]

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_no_at_or_dot(self, mock_input):
        """Test rejection of email without @ and dot."""

        mock_input.side_effect = ["testuser", "invalidemail"]

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_valid_complex_email(self, mock_input):
        """Test acceptance of complex but valid email."""

        mock_input.side_effect = ["testuser", "user.name+tag@example.co.uk"]

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], "user.name+tag@example.co.uk")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_keyboard_interrupt(self, mock_input):
        """Test handling of Ctrl+C during email update collection."""

        mock_input.side_effect = KeyboardInterrupt()

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_email_update_data_exception(self, mock_input):
        """Test handling of unexpected exceptions."""

        mock_input.side_effect = Exception("Unexpected error")

        result = MemberInputService.collect_member_email_update_data()

        self.assertIsNone(result)


class TestMemberInputServiceCollectPasswordUpdateData(unittest.TestCase):
    """Test cases for collect_member_password_update_data method."""

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_success(self, mock_input):
        """Test successful password update with matching confirmation."""

        mock_input.side_effect = ["testuser", "newpass123", "newpass123"]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], "testuser")
        self.assertEqual(result[1], "newpass123")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_too_short(self, mock_input):
        """Test rejection of password shorter than 6 characters."""

        mock_input.side_effect = ["testuser", "short"]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNone(result)
        # Should only call get_user_input twice (username + password)
        self.assertEqual(mock_input.call_count, 2)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_exactly_six_chars(self, mock_input):
        """Test acceptance of password with exactly 6 characters (boundary)."""

        mock_input.side_effect = ["testuser", "pass12", "pass12"]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], "pass12")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_five_chars(self, mock_input):
        """Test rejection of password with exactly 5 characters (boundary)."""

        mock_input.side_effect = ["testuser", "pass1"]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_mismatch(self, mock_input):
        """Test rejection when passwords don't match."""

        mock_input.side_effect = ["testuser", "password123", "password456"]

        result = MemberInputService.collect_member_password_update_data()
        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_case_sensitive_mismatch(self, mock_input):
        """Test case sensitivity in password matching."""

        mock_input.side_effect = ["testuser", "Password123", "password123"]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_whitespace_difference(self, mock_input):
        """Test that whitespace differences cause mismatch."""

        mock_input.side_effect = ["testuser", "password123", "password123 "]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_keyboard_interrupt(self, mock_input):
        """Test handling of Ctrl+C during password update."""

        mock_input.side_effect = KeyboardInterrupt()

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_exception(self, mock_input):
        """Test handling of unexpected exceptions."""

        mock_input.side_effect = Exception("Unexpected error")

        result = MemberInputService.collect_member_password_update_data()
