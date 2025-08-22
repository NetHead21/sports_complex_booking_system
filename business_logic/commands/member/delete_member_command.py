from business_logic.base.command import Command
from business_logic.member_database_manager import db
from business_logic.services.member_input_service import MemberInputService


class DeleteMembersCommand(Command):
    """Command responsible for deleting members from the database."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the delete member command.

        Single responsibility: Execute the database operation for deleting a member.
        Input collection and confirmation are delegated to MemberInputService.
        """
        try:
            # Delegate input collection and confirmation to service
            member_id = MemberInputService.collect_member_id_for_deletion()

            if member_id is None:
                return False, "Member deletion cancelled or failed"

            # Focus solely on database execution
            success = db.delete_member(member_id)

            # Display appropriate message using service utility
            if success:
                MemberInputService.display_operation_result(
                    "Member Deletion", member_id, True
                )
                return True, None
            else:
                MemberInputService.display_operation_result(
                    "Member Deletion", member_id, False, "Member not found"
                )
                return False, f"Member '{member_id}' does not exist"

        except Exception as e:
            print(f"❌ Database Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    # Test the command
    delete_member = DeleteMembersCommand()
    success, result = delete_member.execute()
    print(f"Command result: Success={success}, Result={result}")
