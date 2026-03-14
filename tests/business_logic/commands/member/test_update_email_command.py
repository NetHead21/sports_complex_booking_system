"""
Comprehensive test suite for UpdateMembersEmailCommand module.

This module contains detailed unit tests for UpdateMembersEmailCommand.execute,
covering success flows, failure cases, exception handling, and edge scenarios
with various email and member data configurations.

Coverage Areas:
    - Successful email update (happy path)
    - User cancellation (service returns None)
    - Member not found scenario
    - Service exception handling
    - Database exception handling
    - Email format edge cases (valid and invalid)
    - Member ID edge cases
    - data= parameter ignored
    - Exact success/failure message formats
    - Return tuple structure
    - Multiple sequential calls (statelessness)
    - Various exception types
    - Edge case email addresses
    - Edge case member IDs
    - Display operation result integration
    - Database error with member not found
    - Multiple exception types handling
"""

import unittest
from unittest.mock import patch, MagicMock, call

from business_logic.commands.member.update_email_command import (
    UpdateMembersEmailCommand,
)


class TestUpdateMembersEmailCommandExecute(unittest.TestCase):
    """Test cases for UpdateMembersEmailCommand.execute."""

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_success(self, mock_print, mock_input_service, mock_db):
        """Test successful member email update."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "user123",
            "newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        command = UpdateMembersEmailCommand()

        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_email_update_data.assert_called_once()
        mock_db.update_member_email.assert_called_once_with(
            "user123", "newemail@example.com"
        )
        mock_input_service.display_operation_result.assert_called_once_with(
            "Email Update", "user123", True
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_email_update_cancelled(self, mock_input_service, mock_db):
        """Test when user cancels email data collection."""

        mock_input_service.collect_member_email_update_data.return_value = None
        command = UpdateMembersEmailCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Email update cancelled or failed")
        mock_input_service.collect_member_email_update_data.assert_called_once()
        mock_db.update_member_email.assert_not_called()
        mock_input_service.display_operation_result.assert_not_called()

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_member_not_found(self, mock_input_service, mock_db):
        """Test when member does not exist in database."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "nonexistent_user",
            "newemail@example.com",
        )
        mock_db.update_member_email.return_value = False

        command = UpdateMembersEmailCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member 'nonexistent_user' does not exist")
        mock_db.update_member_email.assert_called_once_with(
            "nonexistent_user", "newemail@example.com"
        )
        mock_input_service.display_operation_result.assert_called_once_with(
            "Email Update", "nonexistent_user", False, "Member not found"
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_input_service(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when input service raises an error."""

        mock_input_service.collect_member_email_update_data.side_effect = Exception(
            "Input service error"
        )
        command = UpdateMembersEmailCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.update_member_email.assert_not_called()
        mock_print.assert_called_once_with("❌ Database Error: Input service error")

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_database(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when database raises an error."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "user123",
            "newemail@example.com",
        )
        mock_db.update_member_email.side_effect = Exception("Database connection error")

        command = UpdateMembersEmailCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")
        mock_print.assert_called_once_with(
            "❌ Database Error: Database connection error"
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_data_parameter_ignored(self, mock_input_service, mock_db):
        """Test that data parameter is ignored."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "user123",
            "newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        command = UpdateMembersEmailCommand()

        success, error = command.execute(data={"ignored": "value"})

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_email_update_data.assert_called_once()
        mock_db.update_member_email.assert_called_once_with(
            "user123", "newemail@example.com"
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_return_value_structure(self, mock_input_service, mock_db):
        """Test return tuple structure."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "user123",
            "newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        command = UpdateMembersEmailCommand()

        result = command.execute()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_with_data_none_explicit(self, mock_input_service, mock_db):
        """Test that execute(data=None) behaves identically to execute()."""

        mock_input_service.collect_member_email_update_data.return_value = (
            "user123",
            "newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        command = UpdateMembersEmailCommand()

        success, error = command.execute(data=None)

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_email.assert_called_once_with(
            "user123", "newemail@example.com"
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_multiple_sequential_calls_same_instance(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test stateless behavior: same instance can be reused for multiple calls."""

        command = UpdateMembersEmailCommand()

        # First call
        mock_input_service.collect_member_email_update_data.return_value = (
            "alice",
            "alice.newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        success_a, error_a = command.execute()

        self.assertTrue(success_a)
        self.assertIsNone(error_a)
        mock_db.update_member_email.assert_called_with(
            "alice", "alice.newemail@example.com"
        )

        mock_db.reset_mock()
        mock_input_service.reset_mock()
        mock_print.reset_mock()

        # Second call — different member, same command instance
        mock_input_service.collect_member_email_update_data.return_value = (
            "bob",
            "bob.newemail@example.com",
        )
        mock_db.update_member_email.return_value = True

        success_b, error_b = command.execute()

        self.assertTrue(success_b)
        self.assertIsNone(error_b)
        mock_db.update_member_email.assert_called_once_with(
            "bob", "bob.newemail@example.com"
        )

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_various_exception_types_return_false_and_str_e(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that all exception types are caught, returning (False, str(e))."""

        exceptions = [
            ValueError("Invalid email value"),
            RuntimeError("Runtime failure"),
            ConnectionError("Connection refused"),
            TypeError("Type mismatch"),
            PermissionError("Access denied"),
        ]

        command = UpdateMembersEmailCommand()

        for exc in exceptions:
            with self.subTest(exception_type=type(exc).__name__):
                mock_input_service.collect_member_email_update_data.side_effect = exc
                mock_db.reset_mock()
                mock_print.reset_mock()

                success, error = command.execute()

                self.assertFalse(success)
                self.assertEqual(error, str(exc))
                self.assertIsInstance(error, str)
                mock_db.update_member_email.assert_not_called()
                mock_print.assert_called_once_with(f"❌ Database Error: {exc}")

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_error_second_element_is_exact_str_of_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the error tuple element is exactly str(exception)."""

        exc = Exception("exact error message")
        mock_input_service.collect_member_email_update_data.side_effect = exc

        command = UpdateMembersEmailCommand()
        _, error = command.execute()

        self.assertEqual(error, str(exc))
        self.assertEqual(error, "exact error message")

    @patch("business_logic.commands.member.update_email_command.db")
    @patch("business_logic.commands.member.update_email_command.MemberInputService")
    def test_execute_cancelled_second_element_exact_message(
        self, mock_input_service, mock_db
    ):
        """Test the exact cancellation error string."""

        mock_input_service.collect_member_email_update_data.return_value = None
