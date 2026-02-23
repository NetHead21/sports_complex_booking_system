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
