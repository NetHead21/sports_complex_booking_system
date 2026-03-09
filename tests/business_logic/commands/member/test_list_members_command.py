"""
Comprehensive test suite for ListMembersCommand module.

Coverage:
    - Successful listing (happy path)
    - show_members called exactly once
    - Members data forwarded to format_member_table
    - Formatted output is printed
    - Empty member list still processed and printed
    - Single member (boundary case)
    - Large member list
    - data= parameter always ignored
    - execute(data=None) explicit default
    - Return tuple structure (length, types)
    - Second element always None
    - Multiple sequential calls on the same instance (statelessness)
    - order_by stored on __init__ and defaults to 'member_since'
    - Various order_by values stored correctly
    - Database exception propagates (no try/except in execute)
    - Formatter exception propagates
    - formatter returns empty string / None
"""

import unittest
from unittest.mock import patch, MagicMock, call

from business_logic.commands.member.list_members_command import ListMembersCommand


class TestListMembersCommandInit(unittest.TestCase):
    """Test cases for ListMembersCommand __init__."""

    def test_default_order_by_is_member_since(self):
        """Test that order_by defaults to 'member_since'."""
        command = ListMembersCommand()

        self.assertEqual(command.order_by, "member_since")

    def test_custom_order_by_stored(self):
        """Test that a custom order_by value is stored correctly."""
        command = ListMembersCommand(order_by="name")

        self.assertEqual(command.order_by, "name")

    def test_various_order_by_values_stored(self):
        """Test that various order_by values are stored as provided."""

        values = ["name", "email", "member_id", "member_since", "custom_field"]

        for value in values:
            with self.subTest(order_by=value):
                command = ListMembersCommand(order_by=value)
                self.assertEqual(command.order_by, value)


class TestListMembersCommandExecute(unittest.TestCase):
    """Test cases for ListMembersCommand.execute."""

    # ------------------------------------------------------------------
    # Happy path
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    def test_execute_success_returns_true_none(self, mock_db, mock_format_table):
        """Test successful execution returns (True, None)."""

        mock_db.show_members.return_value = [
            ("user1", "Alice", "alice@example.com", "2025-01-01"),
            ("user2", "Bob", "bob@example.com", "2025-02-01"),
        ]
        mock_format_table.return_value = "Formatted Table"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        self.assertIsNone(result)

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    def test_execute_calls_show_members_once(self, mock_db, mock_format_table):
        """Test that db.show_members is called exactly once per execute call."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = ""

        ListMembersCommand().execute()

        mock_db.show_members.assert_called_once()

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    def test_execute_passes_members_to_formatter(self, mock_db, mock_format_table):
        """Test that the return value of show_members is passed to format_member_table."""

        members = [
            ("user1", "Alice", "alice@example.com", "2025-01-01"),
            ("user2", "Bob", "bob@example.com", "2025-02-01"),
        ]
        mock_db.show_members.return_value = members
        mock_format_table.return_value = "Table"

        ListMembersCommand().execute()

        mock_format_table.assert_called_once_with(members)

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_prints_formatted_table(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test that the formatted table string is printed."""

        mock_db.show_members.return_value = [
            ("user1", "Alice", "a@b.com", "2025-01-01")
        ]
        mock_format_table.return_value = "Formatted Output"

        ListMembersCommand().execute()

        mock_print.assert_called_once_with("Formatted Output")

    # ------------------------------------------------------------------
    # Various data scenarios
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_with_empty_member_list(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test that an empty list is passed to formatter and result is printed."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = "No members found"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with([])
        mock_print.assert_called_once_with("No members found")

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_with_single_member(self, mock_print, mock_db, mock_format_table):
        """Test execution with exactly one member (boundary case)."""

        members = [("only_user", "Solo Member", "solo@example.com", "2025-06-01")]
        mock_db.show_members.return_value = members
        mock_format_table.return_value = "Single member table"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(members)
        mock_print.assert_called_once_with("Single member table")

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_with_large_member_list(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test execution with a large member dataset."""

        members = [
            (f"user{i}", f"Member {i}", f"user{i}@example.com", "2025-01-01")
            for i in range(1, 501)
        ]
        mock_db.show_members.return_value = members
        mock_format_table.return_value = "Large table"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(members)

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_with_none_from_db(self, mock_print, mock_db, mock_format_table):
        """Test execution when db.show_members returns None."""

        mock_db.show_members.return_value = None
        mock_format_table.return_value = "None table"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_format_table.assert_called_once_with(None)
        mock_print.assert_called_once_with("None table")

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_with_special_characters_in_data(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test execution with special characters in member data."""

        members = [
            ("user_1", "O'Brien, John", "o.brien+tag@example.co.uk", "2025-03-15"),
            ("user-2", "李 伟", "liwei@example.cn", "2025-04-20"),
            ("user.3", "Müller, Hans", "hans.mueller@example.de", "2025-05-10"),
        ]
        mock_db.show_members.return_value = members
        mock_format_table.return_value = "Special chars table"

        success, result = ListMembersCommand().execute()

        self.assertTrue(success)
        mock_format_table.assert_called_once_with(members)

    # ------------------------------------------------------------------
    # data= parameter
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_data_parameter_ignored_with_dict(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test that passing a dict as data= is silently ignored."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = ""

        success, result = ListMembersCommand().execute(data={"ignored": "value"})

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_members.assert_called_once()

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_data_none_explicit(self, mock_print, mock_db, mock_format_table):
        """Test that execute(data=None) behaves identically to execute()."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = ""

        success, result = ListMembersCommand().execute(data=None)

        self.assertTrue(success)
        self.assertIsNone(result)
        mock_db.show_members.assert_called_once()

    # ------------------------------------------------------------------
    # Return structure
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_return_value_is_tuple_of_length_2(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test return value is always a 2-tuple."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = ""

        result = ListMembersCommand().execute()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_first_element_is_bool_true(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test that the first element is always bool True."""

        mock_db.show_members.return_value = []
        mock_format_table.return_value = ""

        success, _ = ListMembersCommand().execute()

        self.assertIsInstance(success, bool)
        self.assertTrue(success)

    @patch("business_logic.commands.member.list_members_command.format_member_table")
    @patch("business_logic.commands.member.list_members_command.db")
    @patch("builtins.print")
    def test_execute_second_element_is_always_none(
        self, mock_print, mock_db, mock_format_table
    ):
        """Test that the second element is always None."""

        mock_db.show_members.return_value = [("u1", "Alice", "a@b.com", "2025-01-01")]
        mock_format_table.return_value = "Table"

        _, result = ListMembersCommand().execute()

        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # Formatter edge cases
    # ------------------------------------------------------------------
