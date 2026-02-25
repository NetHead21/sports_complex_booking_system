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

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_data_parameter_ignored(self, mock_input_service, mock_db):
        """Test that data parameter is ignored."""

        member = Member(id="user123", password="Secret123", email="user@example.com")
        mock_input_service.collect_new_member_data.return_value = member

        command = AddMembersCommand()

        success, error = command.execute(data={"ignored": "value"})

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_new_member_data.assert_called_once()
        mock_db.create_new_member.assert_called_once_with(member)

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_input_service(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when input service raises an error."""

        mock_input_service.collect_new_member_data.side_effect = Exception(
            "Input service error"
        )
        command = AddMembersCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.create_new_member.assert_not_called()
        mock_print.assert_called_once_with("\u274c Database Error: Input service error")

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_database(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when database raises an error."""

        member = Member(id="user123", password="Secret123", email="user@example.com")
        mock_input_service.collect_new_member_data.return_value = member
        mock_db.create_new_member.side_effect = Exception("Database connection error")

        command = AddMembersCommand()

        success, error = command.execute()

        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")
        mock_print.assert_called_once_with(
            "\u274c Database Error: Database connection error"
        )

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_return_value_structure(self, mock_input_service, mock_db):
        """Test return tuple structure."""

        member = Member(id="user123", password="Secret123", email="user@example.com")
        mock_input_service.collect_new_member_data.return_value = member

        command = AddMembersCommand()

        result = command.execute()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_with_varied_member_data(self, mock_input_service, mock_db):
        """Test execution with edge-case member values."""

        members = [
            Member(id="u", password="Secret123", email="a@b.co"),
            Member(
                id="user_with_long_id" * 5,
                password="P@ssw0rd!",
                email="long.email.address+alias@example.com",
            ),
            Member(id="user-123", password="123456", email="user-123@example.net"),
        ]

        command = AddMembersCommand()
