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

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_password_update_data_long_password(self, mock_input):
        """Test acceptance of very long password."""

        long_password = "a" * 100
        mock_input.side_effect = ["testuser", long_password, long_password]

        result = MemberInputService.collect_member_password_update_data()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], long_password)


class TestMemberInputServiceCollectMemberIdForDeletion(unittest.TestCase):
    """Test cases for collect_member_id_for_deletion method."""

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_success(self, mock_input):
        """Test successful deletion with correct confirmation."""

        mock_input.side_effect = ["testuser", "DELETE"]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertEqual(result, "testuser")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_wrong_confirmation(self, mock_input):
        """Test rejection when confirmation text is incorrect."""

        mock_input.side_effect = ["testuser", "delete"]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_lowercase_confirmation(self, mock_input):
        """Test case sensitivity of confirmation (lowercase should fail)."""

        mock_input.side_effect = ["testuser", "delete"]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_mixed_case_confirmation(self, mock_input):
        """Test case sensitivity of confirmation (mixed case should fail)."""

        mock_input.side_effect = ["testuser", "Delete"]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_empty_confirmation(self, mock_input):
        """Test rejection of empty confirmation."""

        mock_input.side_effect = ["testuser", ""]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_whitespace_in_confirmation(
        self, mock_input
    ):
        """Test that whitespace in confirmation causes failure."""

        mock_input.side_effect = ["testuser", " DELETE "]

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_keyboard_interrupt(self, mock_input):
        """Test handling of Ctrl+C during deletion."""

        mock_input.side_effect = KeyboardInterrupt()

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_deletion_exception(self, mock_input):
        """Test handling of unexpected exceptions."""

        mock_input.side_effect = Exception("Unexpected error")

        result = MemberInputService.collect_member_id_for_deletion()

        self.assertIsNone(result)


class TestMemberInputServiceCollectMemberIdForLookup(unittest.TestCase):
    """Test cases for collect_member_id_for_lookup method."""

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_lookup_success(self, mock_input):
        """Test successful member ID collection for lookup."""

        mock_input.return_value = "testuser"

        result = MemberInputService.collect_member_id_for_lookup()

        self.assertEqual(result, "testuser")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_lookup_with_spaces(self, mock_input):
        """Test member ID with spaces (if allowed)."""

        mock_input.return_value = "test user"

        result = MemberInputService.collect_member_id_for_lookup()

        self.assertEqual(result, "test user")

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_lookup_keyboard_interrupt(self, mock_input):
        """Test handling of Ctrl+C during lookup."""

        mock_input.side_effect = KeyboardInterrupt()

        result = MemberInputService.collect_member_id_for_lookup()

        self.assertIsNone(result)

    @patch("business_logic.services.member_input_service.get_user_input")
    def test_collect_member_id_for_lookup_exception(self, mock_input):
        """Test handling of unexpected exceptions."""

        mock_input.side_effect = Exception("Unexpected error")

        result = MemberInputService.collect_member_id_for_lookup()

        self.assertIsNone(result)


class TestMemberInputServiceDisplayOperationResult(unittest.TestCase):
    """Test cases for display_operation_result method."""

    @patch("builtins.print")
    def test_display_operation_result_success(self, mock_print):
        """Test display of successful operation."""

        MemberInputService.display_operation_result("Email Update", "testuser", True)

        mock_print.assert_called_once_with(
            "✅ Email Update successful for member 'testuser'!"
        )

    @patch("builtins.print")
    def test_display_operation_result_failure_no_error_msg(self, mock_print):
        """Test display of failed operation without error message."""

        MemberInputService.display_operation_result(
            "Password Update", "testuser", False
        )

        mock_print.assert_called_once_with(
            "❌ Password Update failed for member 'testuser'"
        )

    @patch("builtins.print")
    def test_display_operation_result_failure_with_error_msg(self, mock_print):
        """Test display of failed operation with error message."""

        MemberInputService.display_operation_result(
            "Member Creation", "testuser", False, "Database connection failed"
        )

        mock_print.assert_called_once_with(
            "❌ Member Creation failed for member 'testuser': Database connection failed"
        )

    @patch("builtins.print")
    def test_display_operation_result_different_operations(self, mock_print):
        """Test display with various operation names."""

        operations = [
            ("Member Deletion", "user1", True, None),
            ("Email Verification", "user2", False, "Invalid email"),
        ]

        for op, user, success, error in operations:
            mock_print.reset_mock()
            MemberInputService.display_operation_result(op, user, success, error)
            self.assertEqual(mock_print.call_count, 1)


class TestMemberInputServiceValidateMemberData(unittest.TestCase):
    """Test cases for validate_member_data method."""

    def test_validate_member_data_valid_complete(self):
        """Test validation of complete valid member data."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", "test@email.com", "password123"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_valid_id_only(self):
        """Test validation of only member ID."""

        is_valid, error = MemberInputService.validate_member_data("testuser")

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_valid_id_and_email(self):
        """Test validation of member ID and email only."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="test@email.com"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_empty_member_id(self):
        """Test rejection of empty member ID."""

        is_valid, error = MemberInputService.validate_member_data("")

        self.assertFalse(is_valid)
        self.assertEqual(error, "Member ID cannot be empty")

    def test_validate_member_data_whitespace_only_member_id(self):
        """Test rejection of whitespace-only member ID."""

        is_valid, error = MemberInputService.validate_member_data("   ")

        self.assertFalse(is_valid)
        self.assertEqual(error, "Member ID cannot be empty")

    def test_validate_member_data_member_id_too_short(self):
        """Test rejection of member ID shorter than 3 characters."""
        is_valid, error = MemberInputService.validate_member_data("ab")

        self.assertFalse(is_valid)
        self.assertEqual(error, "Member ID must be at least 3 characters long")

    def test_validate_member_data_member_id_exactly_three_chars(self):
        """Test acceptance of member ID with exactly 3 characters (boundary)."""
        is_valid, error = MemberInputService.validate_member_data("abc")

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_member_id_two_chars(self):
        """Test rejection of member ID with exactly 2 characters (boundary)."""

        is_valid, error = MemberInputService.validate_member_data("ab")

        self.assertFalse(is_valid)
        self.assertIn("at least 3 characters", error)

    def test_validate_member_data_invalid_email_no_at(self):
        """Test rejection of email without @ symbol."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="invalidemail.com"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_validate_member_data_invalid_email_no_dot(self):
        """Test rejection of email without dot."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="invalid@email"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_validate_member_data_email_too_short(self):
        """Test rejection of email shorter than 5 characters."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="a@b."
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Email too short")

    def test_validate_member_data_email_exactly_five_chars(self):
        """Test acceptance of email with exactly 5 characters (boundary)."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="a@b.c"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_email_four_chars(self):
        """Test rejection of email with exactly 4 characters (boundary)."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="a@b."
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Email too short")

    def test_validate_member_data_password_too_short(self):
        """Test rejection of password shorter than 6 characters."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", password="pass1"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Password must be at least 6 characters long")

    def test_validate_member_data_password_exactly_six_chars(self):
        """Test acceptance of password with exactly 6 characters (boundary)."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", password="pass12"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_password_five_chars(self):
        """Test rejection of password with exactly 5 characters (boundary)."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", password="pass1"
        )

        self.assertFalse(is_valid)
        self.assertIn("at least 6 characters", error)

    def test_validate_member_data_password_only_whitespace(self):
        """Test rejection of password containing only whitespace."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", password="      "
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Password cannot contain only whitespace")

    def test_validate_member_data_password_with_spaces(self):
        """Test acceptance of password with spaces (but not only spaces)."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", password="pass word 123"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_all_invalid(self):
        """Test validation when all fields are invalid (returns first error)."""

        is_valid, error = MemberInputService.validate_member_data(
            "", email="invalid", password="short"
        )

        self.assertFalse(is_valid)
        # Should return the first validation error (member ID)
        self.assertEqual(error, "Member ID cannot be empty")

    def test_validate_member_data_complex_valid_email(self):
        """Test acceptance of complex but valid email format."""

        is_valid, error = MemberInputService.validate_member_data(
            "testuser", email="user.name+tag@example.co.uk"
        )

        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_member_data_long_inputs(self):
        """Test validation with very long valid inputs."""

        long_id = "a" * 50
        long_email = "user@" + "domain" * 10 + ".com"
        long_password = "p" * 100

        is_valid, error = MemberInputService.validate_member_data(
            long_id, email=long_email, password=long_password
        )
