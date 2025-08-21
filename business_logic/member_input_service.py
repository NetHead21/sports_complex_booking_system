"""
Member service for handling member-related operations and input collection.
"""
from persistence.models import Member
from presentation.user_input import get_user_input
from typing import Optional, Tuple


class MemberInputService:
    """Service for collecting and validating member input data."""
    
    @staticmethod
    def collect_new_member_data() -> Optional[Member]:
        """
        Collect member information from user input and create a Member object.
        
        Returns:
            Member object if successful, None if cancelled or invalid
        """
        try:
            print("\n📝 Adding New Member")
            print("-" * 30)
            
            # Collect member information from user
            member_id = get_user_input("Enter member username", required=True)
            password = get_user_input("Enter password", required=True)
            email = get_user_input("Enter email", required=True)
            
            # Create and validate Member object using Pydantic
            member = Member(id=member_id, password=password, email=email)
            return member
            
        except ValueError as e:
            print(f"❌ Validation Error: {e}")
            return None
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    @staticmethod
    def collect_member_email_update_data() -> Optional[Tuple[str, str]]:
        """
        Collect data for updating a member's email.
        
        Returns:
            Tuple of (member_id, new_email) if successful, None if cancelled
        """
        try:
            print("\n📧 Updating Member Email")
            print("-" * 30)
            
            member_id = get_user_input("Enter member username", required=True)
            new_email = get_user_input("Enter new email address", required=True)
            
            # Basic email validation (you could enhance this with regex)
            if "@" not in new_email or "." not in new_email:
                print("❌ Invalid email format")
                return None
            
            return member_id, new_email
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting email data: {e}")
            return None
    
    @staticmethod
    def collect_member_password_update_data() -> Optional[Tuple[str, str]]:
        """
        Collect data for updating a member's password.
        
        Returns:
            Tuple of (member_id, new_password) if successful, None if cancelled
        """
        try:
            print("\n� Updating Member Password")
            print("-" * 30)
            
            member_id = get_user_input("Enter member username", required=True)
            new_password = get_user_input("Enter new password", required=True)
            
            # Basic password validation
            if len(new_password) < 6:
                print("❌ Password must be at least 6 characters long")
                return None
            
            # Confirm password
            confirm_password = get_user_input("Confirm new password", required=True)
            
            if new_password != confirm_password:
                print("❌ Passwords do not match")
                return None
            
            return member_id, new_password
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error collecting password data: {e}")
            return None
    
    @staticmethod
    def collect_member_id_for_deletion() -> Optional[str]:
        """
        Collect member ID for deletion with confirmation.
        
        Returns:
            Member ID if successful, None if cancelled
        """
        try:
            print("\n🗑️ Delete Member")
            print("-" * 30)
            print("⚠️ WARNING: This action cannot be undone!")
            
            member_id = get_user_input("Enter member username to delete", required=True)
            
            # Show warning and ask for confirmation
            print(f"\n⚠️ You are about to delete member: '{member_id}'")
            print("This will:")
            print("  • Remove the member from the database")
            print("  • Cancel any existing bookings")
            print("  • This action is IRREVERSIBLE")
            
            confirm = get_user_input("Type 'DELETE' to confirm deletion", required=True)
            
            if confirm == "DELETE":
                return member_id
            else:
                print("❌ Deletion cancelled - confirmation text does not match")
                return None
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    @staticmethod
    def collect_member_id_for_lookup() -> Optional[str]:
        """
        Collect member ID for general lookup operations.
        
        Returns:
            Member ID if provided, None if cancelled
        """
        try:
            print("\n🔍 Member Lookup")
            print("-" * 30)
            
            member_id = get_user_input("Enter member username", required=True)
            return member_id
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    @staticmethod
    def display_operation_result(operation: str, member_id: str, success: bool, error_msg: str = None):
        """
        Display the result of a member operation with consistent formatting.
        
        Args:
            operation: Name of the operation (e.g., "Email Update", "Password Update")
            member_id: ID of the member involved
            success: Whether the operation was successful
            error_msg: Error message if operation failed
        """
        if success:
            print(f"✅ {operation} successful for member '{member_id}'!")
        else:
            if error_msg:
                print(f"❌ {operation} failed for member '{member_id}': {error_msg}")
            else:
                print(f"❌ {operation} failed for member '{member_id}'")
    
    @staticmethod
    def validate_member_data(member_id: str, email: str = None, password: str = None) -> Tuple[bool, str]:
        """
        Validate member data before database operations.
        
        Args:
            member_id: Member username
            email: Email to validate (optional)
            password: Password to validate (optional)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate member ID
        if not member_id or len(member_id.strip()) == 0:
            return False, "Member ID cannot be empty"
        
        if len(member_id) < 3:
            return False, "Member ID must be at least 3 characters long"
        
        # Validate email if provided
        if email is not None:
            if "@" not in email or "." not in email:
                return False, "Invalid email format"
            
            if len(email) < 5:
                return False, "Email too short"
        
        # Validate password if provided
        if password is not None:
            if len(password) < 6:
                return False, "Password must be at least 6 characters long"
            
            if password.isspace():
                return False, "Password cannot contain only whitespace"
        
        return True, ""
