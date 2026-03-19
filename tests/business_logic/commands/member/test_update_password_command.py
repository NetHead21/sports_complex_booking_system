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
