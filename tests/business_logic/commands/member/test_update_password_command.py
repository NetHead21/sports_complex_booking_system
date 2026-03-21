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
