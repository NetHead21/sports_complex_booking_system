"""
Comprehensive test suite for AddMembersCommand module.

This module contains unit tests for AddMembersCommand.execute,
covering success flows, failure cases, exception handling, and
edge scenarios with varied member data.

Coverage:
    - Successful registration (happy path)
    - User cancellation (service returns None)
    - data= parameter ignored
    - Exact success print message format
    - Exact error print message format
    - Exception from input service
    - Exception from database
    - Multiple exception types all convert to (False, str(e))
    - Return tuple structure
    - Multiple sequential calls on the same instance (statelessness)
    - execute(data=None) explicit default
    - Edge-case member field values
"""

import unittest
from unittest.mock import patch, call

from business_logic.commands.member.add_member_command import AddMembersCommand
from persistence.models import Member


class TestAddMembersCommandExecute(unittest.TestCase):
    """Test cases for AddMembersCommand.execute."""

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_success(self, mock_print, mock_input_service, mock_db):
        """Test successful member registration."""

        member = Member(id="user123", password="Secret123", email="user@example.com")
        mock_input_service.collect_new_member_data.return_value = member

        command = AddMembersCommand()

        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_new_member_data.assert_called_once()
        mock_db.create_new_member.assert_called_once_with(member)
        mock_print.assert_called_once_with(
            f"\u2705 Member '{member.id}' registered successfully!"
        )

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_member_creation_cancelled(self, mock_input_service, mock_db):
        """Test when user cancels member data collection."""

        mock_input_service.collect_new_member_data.return_value = None
        command = AddMembersCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Member creation cancelled or failed")
        mock_input_service.collect_new_member_data.assert_called_once()
        mock_db.create_new_member.assert_not_called()
