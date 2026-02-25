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

        for member in members:
            with self.subTest(member_id=member.id):
                mock_input_service.collect_new_member_data.return_value = member
                mock_db.create_new_member.return_value = None

                success, error = command.execute()

                self.assertTrue(success)
                self.assertIsNone(error)
                mock_db.create_new_member.assert_called_once_with(member)
                mock_db.reset_mock()
                mock_input_service.reset_mock()

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_with_data_none_explicit(self, mock_input_service, mock_db):
        """Test that execute(data=None) behaves identically to execute()."""

        member = Member(id="user123", password="Secret123", email="user@example.com")
        mock_input_service.collect_new_member_data.return_value = member

        command = AddMembersCommand()

        success, error = command.execute(data=None)

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.create_new_member.assert_called_once_with(member)

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_multiple_sequential_calls_same_instance(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test stateless behavior: same instance can be reused for multiple calls."""

        member_a = Member(id="alice", password="Pass1", email="alice@example.com")
        member_b = Member(id="bob", password="Pass2", email="bob@example.com")

        command = AddMembersCommand()

        # First call
        mock_input_service.collect_new_member_data.return_value = member_a
        success_a, error_a = command.execute()
        self.assertTrue(success_a)
        self.assertIsNone(error_a)
        mock_db.create_new_member.assert_called_with(member_a)

        mock_db.reset_mock()
        mock_input_service.reset_mock()
        mock_print.reset_mock()

        # Second call — different member, same command instance
        mock_input_service.collect_new_member_data.return_value = member_b
        success_b, error_b = command.execute()
        self.assertTrue(success_b)
        self.assertIsNone(error_b)
        mock_db.create_new_member.assert_called_once_with(member_b)

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_various_exception_types_return_false_and_str_e(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that all exception types are caught, returning (False, str(e))."""

        exceptions = [
            ValueError("Invalid value"),
            RuntimeError("Runtime failure"),
            ConnectionError("Connection refused"),
            TypeError("Type mismatch"),
            PermissionError("Access denied"),
        ]

        command = AddMembersCommand()

        for exc in exceptions:
            with self.subTest(exception_type=type(exc).__name__):
                mock_input_service.collect_new_member_data.side_effect = exc
                mock_db.reset_mock()
                mock_print.reset_mock()

                success, error = command.execute()

                self.assertFalse(success)
                self.assertEqual(error, str(exc))
                self.assertIsInstance(error, str)
                mock_db.create_new_member.assert_not_called()
                mock_print.assert_called_once_with(f"\u274c Database Error: {exc}")

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_error_second_element_is_exact_str_of_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the error tuple element is exactly str(exception)."""

        exc = Exception("exact error message")
        mock_input_service.collect_new_member_data.side_effect = exc

        command = AddMembersCommand()
        _, error = command.execute()

        self.assertEqual(error, str(exc))
        self.assertEqual(error, "exact error message")

    @patch("business_logic.commands.member.add_member_command.db")
    @patch("business_logic.commands.member.add_member_command.MemberInputService")
    def test_execute_cancelled_second_element_exact_message(
        self, mock_input_service, mock_db
    ):
        """Test the exact cancellation error string."""
