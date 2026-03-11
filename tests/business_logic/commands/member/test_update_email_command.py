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
