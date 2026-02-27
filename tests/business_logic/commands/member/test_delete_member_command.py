"""
Comprehensive test suite for DeleteMembersCommand module.

Coverage:
    - Successful deletion (happy path)
    - User cancellation (service returns None)
    - Member not found (db.delete_member returns False/falsy)
    - Exact success print / display_operation_result args
    - Exact failure display_operation_result args
    - Exception from input service
    - Exception from database
    - Multiple exception types all yield (False, str(e))
    - data= parameter is always ignored
    - execute(data=None) explicit default
    - Return tuple structure
    - Multiple sequential calls on the same instance (statelessness)
    - Edge-case member ID values
"""

import unittest
from unittest.mock import patch, call

from business_logic.commands.member.delete_member_command import DeleteMembersCommand


class TestDeleteMembersCommandExecute(unittest.TestCase):
    """Test cases for DeleteMembersCommand.execute."""

    # ------------------------------------------------------------------
    # Happy-path
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_success(self, mock_input_service, mock_db):
        """Test successful member deletion returns (True, None)."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        command = DeleteMembersCommand()
        success, error = command.execute()

        self.assertTrue(success)
        self.assertIsNone(error)

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_success_calls_service_once(self, mock_input_service, mock_db):
        """Test that collect_member_id_for_deletion is called exactly once on success."""
