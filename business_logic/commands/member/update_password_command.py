from business_logic.base.command import Command
from business_logic.member_database_manager import db
from business_logic.services.member_input_service import MemberInputService


class UpdateMembersPasswordCommand(Command):
    """Command responsible for updating member passwords in the database."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the update member password command.

        Single responsibility: Execute the database operation for updating member password.
        Input collection and validation are delegated to MemberInputService.
        """
        try:
            # Delegate input collection to service
            password_data = MemberInputService.collect_member_password_update_data()

            if password_data is None:
                return False, "Password update cancelled or failed"

            member_id, new_password = password_data

            # Focus solely on database execution
            success = db.update_member_password(member_id, new_password)

            # Display appropriate message using service utility
            if success:
                MemberInputService.display_operation_result(
                    "Password Update", member_id, True
                )
                return True, None
            else:
                MemberInputService.display_operation_result(
                    "Password Update", member_id, False, "Member not found"
                )
                return False, f"Member '{member_id}' does not exist"

        except Exception as e:
            print(f"❌ Database Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    # Test the command
    update_password = UpdateMembersPasswordCommand()
    success, result = update_password.execute()
    print(f"Command result: Success={success}, Result={result}")
