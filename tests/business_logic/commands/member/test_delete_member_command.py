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

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        DeleteMembersCommand().execute()

        mock_input_service.collect_member_id_for_deletion.assert_called_once()

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_success_passes_member_id_to_db(self, mock_input_service, mock_db):
        """Test that the member ID from the service is forwarded to db.delete_member."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        DeleteMembersCommand().execute()

        mock_db.delete_member.assert_called_once_with("user123")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_success_calls_display_with_correct_args(
        self, mock_input_service, mock_db
    ):
        """Test display_operation_result is called with correct args on success."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        DeleteMembersCommand().execute()

        mock_input_service.display_operation_result.assert_called_once_with(
            "Member Deletion", "user123", True
        )

    # ------------------------------------------------------------------
    # Cancellation
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_cancelled_returns_false(self, mock_input_service, mock_db):
        """Test that cancellation returns False."""

        mock_input_service.collect_member_id_for_deletion.return_value = None

        success, _ = DeleteMembersCommand().execute()

        self.assertFalse(success)

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_cancelled_exact_error_message(self, mock_input_service, mock_db):
        """Test the exact cancellation error string."""

        mock_input_service.collect_member_id_for_deletion.return_value = None
        _, error = DeleteMembersCommand().execute()

        self.assertEqual(error, "Member deletion cancelled or failed")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_cancelled_db_never_called(self, mock_input_service, mock_db):
        """Test that db.delete_member is never reached when service returns None."""

        mock_input_service.collect_member_id_for_deletion.return_value = None

        DeleteMembersCommand().execute()

        mock_db.delete_member.assert_not_called()

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_cancelled_display_never_called(self, mock_input_service, mock_db):
        """Test that display_operation_result is never called when cancelled."""

        mock_input_service.collect_member_id_for_deletion.return_value = None

        DeleteMembersCommand().execute()

        mock_input_service.display_operation_result.assert_not_called()

    # ------------------------------------------------------------------
    # Member not found (db returns falsy)
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_member_not_found_returns_false(self, mock_input_service, mock_db):
        """Test that a falsy db result returns (False, ...)."""

        mock_input_service.collect_member_id_for_deletion.return_value = "ghost_user"
        mock_db.delete_member.return_value = False

        success, _ = DeleteMembersCommand().execute()

        self.assertFalse(success)

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_member_not_found_exact_error_message(
        self, mock_input_service, mock_db
    ):
        """Test the exact 'does not exist' error message."""

        mock_input_service.collect_member_id_for_deletion.return_value = "ghost_user"
        mock_db.delete_member.return_value = False

        _, error = DeleteMembersCommand().execute()

        self.assertEqual(error, "Member 'ghost_user' does not exist")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_member_not_found_calls_display_with_failure_args(
        self, mock_input_service, mock_db
    ):
        """Test display_operation_result is called with failure args when member not found."""

        mock_input_service.collect_member_id_for_deletion.return_value = "ghost_user"
        mock_db.delete_member.return_value = False

        DeleteMembersCommand().execute()

        mock_input_service.display_operation_result.assert_called_once_with(
            "Member Deletion", "ghost_user", False, "Member not found"
        )

    # ------------------------------------------------------------------
    # Exception handling
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_input_service(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when input service raises an error."""
