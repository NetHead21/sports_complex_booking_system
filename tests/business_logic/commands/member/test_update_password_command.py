"""
Comprehensive test suite for UpdateMembersPasswordCommand module.

This module contains detailed unit tests for UpdateMembersPasswordCommand.execute,
covering success flows, failure cases, exception handling, and edge scenarios
with various password and member data configurations.

Coverage Areas:
    - Successful password update (happy path)
    - User cancellation (service returns None)
    - Member not found scenario
    - Service exception handling
    - Database exception handling
    - Password format edge cases (valid and invalid)
    - Member ID edge cases
    - data= parameter ignored
    - Exact success/failure message formats
    - Return tuple structure
    - Multiple sequential calls (statelessness)
    - Various exception types
    - Edge case passwords (weak, strong, special chars)
    - Edge case member IDs (numeric, alphanumeric, special chars)
    - Display operation result integration
    - Database error with member not found
    - Multiple exception types handling
    - Security considerations
"""

import unittest
from unittest.mock import patch, MagicMock, call

from business_logic.commands.member.update_password_command import (
    UpdateMembersPasswordCommand,
)


class TestUpdateMembersPasswordCommandExecute(unittest.TestCase):
    """Test cases for UpdateMembersPasswordCommand.execute."""

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_success(self, mock_print, mock_input_service, mock_db):
        """Test successful member password update."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "SecurePass123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()

        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_password_update_data.assert_called_once()
        mock_db.update_member_password.assert_called_once_with(
            "user123", "SecurePass123!"
        )
        mock_input_service.display_operation_result.assert_called_once_with(
            "Password Update", "user123", True
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_password_update_cancelled(self, mock_input_service, mock_db):
        """Test when user cancels password data collection."""

        mock_input_service.collect_member_password_update_data.return_value = None
        command = UpdateMembersPasswordCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Password update cancelled or failed")
        mock_input_service.collect_member_password_update_data.assert_called_once()
        mock_db.update_member_password.assert_not_called()
        mock_input_service.display_operation_result.assert_not_called()

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_member_not_found(self, mock_input_service, mock_db):
        """Test when member does not exist in database."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "nonexistent_user",
            "NewPassword123!",
        )
        mock_db.update_member_password.return_value = False

        command = UpdateMembersPasswordCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member 'nonexistent_user' does not exist")
        mock_db.update_member_password.assert_called_once_with(
            "nonexistent_user", "NewPassword123!"
        )
        mock_input_service.display_operation_result.assert_called_once_with(
            "Password Update", "nonexistent_user", False, "Member not found"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_input_service(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when input service raises an error."""

        mock_input_service.collect_member_password_update_data.side_effect = Exception(
            "Input service error"
        )
        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.update_member_password.assert_not_called()
        mock_print.assert_called_once_with("❌ Database Error: Input service error")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_database(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when database raises an error."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "NewPassword123!",
        )
        mock_db.update_member_password.side_effect = Exception(
            "Database connection error"
        )

        command = UpdateMembersPasswordCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")
        mock_print.assert_called_once_with(
            "❌ Database Error: Database connection error"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_data_parameter_ignored(self, mock_input_service, mock_db):
        """Test that data parameter is ignored."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "NewPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()

        success, error = command.execute(data={"ignored": "value"})

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_password_update_data.assert_called_once()
        mock_db.update_member_password.assert_called_once_with(
            "user123", "NewPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_return_value_structure(self, mock_input_service, mock_db):
        """Test return tuple structure."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "NewPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()

        result = command.execute()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_with_data_none_explicit(self, mock_input_service, mock_db):
        """Test that execute(data=None) behaves identically to execute()."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "NewPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()

        success, error = command.execute(data=None)

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_password_update_data.assert_called_once()
        mock_db.update_member_password.assert_called_once_with(
            "user123", "NewPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_multiple_sequential_calls_same_instance(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test stateless behavior: same instance can be reused for multiple calls."""

        command = UpdateMembersPasswordCommand()

        # First call
        mock_input_service.collect_member_password_update_data.return_value = (
            "alice",
            "AliceNewPass123!",
        )
        mock_db.update_member_password.return_value = True

        success_a, error_a = command.execute()

        self.assertTrue(success_a)
        self.assertIsNone(error_a)
        mock_db.update_member_password.assert_called_with("alice", "AliceNewPass123!")

        mock_db.reset_mock()
        mock_input_service.reset_mock()
        mock_print.reset_mock()

        # Second call — different member, same command instance
        mock_input_service.collect_member_password_update_data.return_value = (
            "bob",
            "BobNewPass456!",
        )
        mock_db.update_member_password.return_value = True

        success_b, error_b = command.execute()

        self.assertTrue(success_b)
        self.assertIsNone(error_b)
        mock_db.update_member_password.assert_called_once_with("bob", "BobNewPass456!")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_various_exception_types_return_false_and_str_e(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that all exception types are caught, returning (False, str(e))."""

        exceptions = [
            ValueError("Invalid password value"),
            RuntimeError("Runtime failure"),
            ConnectionError("Connection refused"),
            TypeError("Type mismatch"),
            PermissionError("Access denied"),
        ]

        command = UpdateMembersPasswordCommand()

        for exc in exceptions:
            with self.subTest(exception_type=type(exc).__name__):
                mock_input_service.collect_member_password_update_data.side_effect = exc
                mock_db.reset_mock()
                mock_print.reset_mock()

                success, error = command.execute()

                self.assertFalse(success)
                self.assertEqual(error, str(exc))
                self.assertIsInstance(error, str)
                mock_db.update_member_password.assert_not_called()
                mock_print.assert_called_once_with(f"❌ Database Error: {exc}")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_error_second_element_is_exact_str_of_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the error tuple element is exactly str(exception)."""

        exc = Exception("exact error message")
        mock_input_service.collect_member_password_update_data.side_effect = exc

        command = UpdateMembersPasswordCommand()
        _, error = command.execute()

        self.assertEqual(error, str(exc))
        self.assertEqual(error, "exact error message")

    # ========================
    # Edge Case Tests
    # ========================

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_empty_string_member_id(
        self, mock_input_service, mock_db
    ):
        """Test with empty string member ID."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "",
            "ValidPassword123!",
        )
        mock_db.update_member_password.return_value = False

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member '' does not exist")
        mock_db.update_member_password.assert_called_once_with("", "ValidPassword123!")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_empty_string_password(self, mock_input_service, mock_db):
        """Test with empty string password."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "",
        )
        mock_db.update_member_password.return_value = False

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member 'user123' does not exist")
        mock_db.update_member_password.assert_called_once_with("user123", "")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_very_long_password(self, mock_input_service, mock_db):
        """Test with very long password."""

        long_password = "A" * 1000 + "b1!"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            long_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with("user123", long_password)

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_password_with_special_characters(
        self, mock_input_service, mock_db
    ):
        """Test password with special characters and unicode."""

        special_password = "Pass!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            special_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "user123", special_password
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_password_with_unicode_characters(
        self, mock_input_service, mock_db
    ):
        """Test password with unicode characters."""

        unicode_password = "Pässwörd123!™€"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            unicode_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "user123", unicode_password
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_password_with_whitespace(
        self, mock_input_service, mock_db
    ):
        """Test password containing spaces and tabs."""

        whitespace_password = "Pass word\twith\tspaces123!"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            whitespace_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "user123", whitespace_password
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_very_long_member_id(self, mock_input_service, mock_db):
        """Test with very long member ID."""

        long_member_id = "member_" + "x" * 1000
        mock_input_service.collect_member_password_update_data.return_value = (
            long_member_id,
            "ValidPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            long_member_id, "ValidPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_numeric_member_id(self, mock_input_service, mock_db):
        """Test with purely numeric member ID."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "12345",
            "ValidPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "12345", "ValidPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_member_id_with_special_characters(
        self, mock_input_service, mock_db
    ):
        """Test with member ID containing special characters."""

        special_member_id = "user-123_test@domain"
        mock_input_service.collect_member_password_update_data.return_value = (
            special_member_id,
            "ValidPassword123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            special_member_id, "ValidPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_case_sensitive_member_id(
        self, mock_input_service, mock_db
    ):
        """Test that member ID is treated case-sensitively."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "User123",
            "ValidPassword123!",
        )
        mock_db.update_member_password.return_value = False

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member 'User123' does not exist")
        # Verify that exact member ID was passed to db
        mock_db.update_member_password.assert_called_once_with(
            "User123", "ValidPassword123!"
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_password_only_numbers(self, mock_input_service, mock_db):
        """Test password containing only numbers."""

        number_password = "123456789012"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            number_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "user123", number_password
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_edge_case_password_only_letters(self, mock_input_service, mock_db):
        """Test password containing only letters."""

        letter_password = "OnlyLettersPassword"
        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            letter_password,
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.update_member_password.assert_called_once_with(
            "user123", letter_password
        )

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_database_error_after_service_success(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test database error even though service successfully collected data."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "user123",
            "ValidPassword123!",
        )
        mock_db.update_member_password.side_effect = RuntimeError("Database locked")

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Database locked")
        mock_print.assert_called_once_with("❌ Database Error: Database locked")

    @patch("business_logic.commands.member.update_password_command.db")
    @patch("business_logic.commands.member.update_password_command.MemberInputService")
    def test_execute_success_displays_correct_operation_result_format(
        self, mock_input_service, mock_db
    ):
        """Test that success response displays operation result with correct format."""

        mock_input_service.collect_member_password_update_data.return_value = (
            "testuser",
            "NewPass123!",
        )
        mock_db.update_member_password.return_value = True

        command = UpdateMembersPasswordCommand()
        success, error = command.execute()

        # Verify exact call signature for success
        mock_input_service.display_operation_result.assert_called_once_with(
            "Password Update", "testuser", True
        )
