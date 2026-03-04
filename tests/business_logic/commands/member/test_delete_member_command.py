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

        mock_input_service.collect_member_id_for_deletion.side_effect = Exception(
            "Input service error"
        )

        success, error = DeleteMembersCommand().execute()

        self.assertFalse(success)
        self.assertEqual(error, "Input service error")
        mock_db.delete_member.assert_not_called()

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_input_service_prints_error(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the exact error print is emitted when input service raises."""

        mock_input_service.collect_member_id_for_deletion.side_effect = Exception(
            "Input service error"
        )

        DeleteMembersCommand().execute()

        mock_print.assert_called_once_with("❌ Database Error: Input service error")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_database(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test exception handling when database raises an error."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.side_effect = Exception("Database connection error")

        success, error = DeleteMembersCommand().execute()

        self.assertFalse(success)
        self.assertEqual(error, "Database connection error")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_exception_in_database_prints_error(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the exact error print is emitted when database raises."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.side_effect = Exception("Database connection error")

        DeleteMembersCommand().execute()

        mock_print.assert_called_once_with(
            "❌ Database Error: Database connection error"
        )

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_various_exception_types_return_false_and_str_e(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that all exception types are caught and return (False, str(e))."""

        exceptions = [
            ValueError("Invalid value"),
            RuntimeError("Runtime failure"),
            ConnectionError("Connection refused"),
            TypeError("Type mismatch"),
            PermissionError("Access denied"),
        ]

        command = DeleteMembersCommand()

        for exc in exceptions:
            with self.subTest(exception_type=type(exc).__name__):
                mock_input_service.collect_member_id_for_deletion.side_effect = exc
                mock_db.reset_mock()
                mock_print.reset_mock()

                success, error = command.execute()

                self.assertFalse(success)
                self.assertEqual(error, str(exc))
                self.assertIsInstance(error, str)
                mock_db.delete_member.assert_not_called()
                mock_print.assert_called_once_with(f"❌ Database Error: {exc}")

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    @patch("builtins.print")
    def test_execute_error_second_element_is_exact_str_of_exception(
        self, mock_print, mock_input_service, mock_db
    ):
        """Test that the returned error is exactly str(exception)."""

        exc = Exception("exact error message")
        mock_input_service.collect_member_id_for_deletion.side_effect = exc

        _, error = DeleteMembersCommand().execute()

        self.assertEqual(error, str(exc))
        self.assertEqual(error, "exact error message")

    # ------------------------------------------------------------------
    # data= parameter
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_data_parameter_ignored_with_dict(
        self, mock_input_service, mock_db
    ):
        """Test that passing a dict as data= is silently ignored."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        success, error = DeleteMembersCommand().execute(data={"ignored": "value"})

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_input_service.collect_member_id_for_deletion.assert_called_once()

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_data_none_explicit(self, mock_input_service, mock_db):
        """Test that execute(data=None) behaves identically to execute()."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        success, error = DeleteMembersCommand().execute(data=None)

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_db.delete_member.assert_called_once_with("user123")

    # ------------------------------------------------------------------
    # Return structure
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_return_value_is_tuple_of_length_2(
        self, mock_input_service, mock_db
    ):
        """Test return value is always a 2-tuple."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        result = DeleteMembersCommand().execute()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_first_element_is_bool(self, mock_input_service, mock_db):
        """Test that the first element of the return tuple is always a bool."""

        for return_val, service_val in [(True, "user123"), (False, None)]:
            with self.subTest(return_val=return_val):
                mock_input_service.collect_member_id_for_deletion.return_value = (
                    service_val
                )
                mock_db.delete_member.return_value = return_val

                result = DeleteMembersCommand().execute()

                self.assertIsInstance(result[0], bool)

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_success_second_element_is_none(self, mock_input_service, mock_db):
        """Test that a successful delete always returns None as the second element."""

        mock_input_service.collect_member_id_for_deletion.return_value = "user123"
        mock_db.delete_member.return_value = True

        _, result = DeleteMembersCommand().execute()

        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # Statelessness / sequential calls
    # ------------------------------------------------------------------

    @patch("business_logic.commands.member.delete_member_command.db")
    @patch("business_logic.commands.member.delete_member_command.MemberInputService")
    def test_execute_multiple_sequential_calls_same_instance(
        self, mock_input_service, mock_db
    ):
        """Test stateless behavior: same instance handles multiple calls correctly."""

        command = DeleteMembersCommand()

        # First call — success
        mock_input_service.collect_member_id_for_deletion.return_value = "alice"
        mock_db.delete_member.return_value = True
        success_a, error_a = command.execute()

        self.assertTrue(success_a)
        self.assertIsNone(error_a)

        mock_db.reset_mock()
        mock_input_service.reset_mock()

        # Second call — different member
        mock_input_service.collect_member_id_for_deletion.return_value = "bob"
        mock_db.delete_member.return_value = True
        success_b, error_b = command.execute()

        self.assertTrue(success_b)
        self.assertIsNone(error_b)
        mock_db.delete_member.assert_called_once_with("bob")

        mock_db.reset_mock()
        mock_input_service.reset_mock()

        # Third call — cancelled
        mock_input_service.collect_member_id_for_deletion.return_value = None
        success_c, error_c = command.execute()
        self.assertFalse(success_c)
        self.assertEqual(error_c, "Member deletion cancelled or failed")
        mock_db.delete_member.assert_not_called()

    # ------------------------------------------------------------------
    # Edge-case member IDs
    # ------------------------------------------------------------------
