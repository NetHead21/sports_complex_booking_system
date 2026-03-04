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
