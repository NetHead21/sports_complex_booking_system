from .command import Command
from .member_database_manager import db
from .member_input_service import MemberInputService


class UpdateMembersEmailCommand(Command):
    """Command responsible for updating member email addresses in the database."""
    
    def execute(self, data=None) -> tuple[bool, any]:
        """
        Execute the update member email command.
        
        Single responsibility: Execute the database operation for updating member email.
        Input collection and validation are delegated to MemberInputService.
        """
        try:
            # Delegate input collection to service
            email_data = MemberInputService.collect_member_email_update_data()
            
            if email_data is None:
                return False, "Email update cancelled or failed"
            
            member_id, new_email = email_data
            
            # Focus solely on database execution
            success = db.update_member_email(member_id, new_email)
            
            # Display appropriate message using service utility
            if success:
                MemberInputService.display_operation_result("Email Update", member_id, True)
                return True, None
            else:
                MemberInputService.display_operation_result("Email Update", member_id, False, "Member not found")
                return False, f"Member '{member_id}' does not exist"
            
        except Exception as e:
            print(f"❌ Database Error: {e}")
            return False, str(e)


if __name__ == "__main__":
    # Test the command
    update_email = UpdateMembersEmailCommand()
    success, result = update_email.execute()
    print(f"Command result: Success={success}, Result={result}")
