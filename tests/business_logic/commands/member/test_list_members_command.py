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
