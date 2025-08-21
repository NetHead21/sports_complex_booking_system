from .command import Command
from .member_database_manager import db
from .member_input_service import MemberInputService


class AddMembersCommand(Command):
    """Command responsible for adding new members to the database."""

    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the add member command.

        Single responsibility: Execute the database operation for adding a member.
        Input collection and member creation are delegated to MemberInputService.
        """
        try:
            # Delegate input collection and member creation to service
            member = MemberInputService.collect_new_member_data()

            if member is None:
                return False, "Member creation cancelled or failed"

            # Focus solely on database execution
            db.create_new_member(member)
            print(f"✅ Member '{member.id}' registered successfully!")
            return True, None

        except Exception as e:
            print(f"❌ Database Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    # Test the command
    add_member = AddMembersCommand()
    success, result = add_member.execute()
    print(f"Command result: Success={success}, Result={result}")
