Business Logic - Commands
Booking Commands (Missing 1 of 4):
✅ book_room_command.py - HAS TEST (634 lines of tests)
✅ cancel_booking_command.py - HAS TEST (889 lines of tests)
✅ list_rooms_command.py - HAS TEST (734 lines of tests)
❌ search_rooms_command.py - NEEDS TEST
Member Commands (Missing all 5):
❌ add_member_command.py - NEEDS TEST
❌ delete_member_command.py - NEEDS TEST
❌ list_members_command.py - NEEDS TEST
❌ update_email_command.py - NEEDS TEST
❌ update_password_command.py - NEEDS TEST
System Commands:
❌ quit_command.py - NEEDS TEST (low priority)
Business Logic - Services
✅ booking_input_service.py - HAS TEST (538 lines of tests)
✅ member_input_service.py - HAS TEST (654 lines of tests)
Business Logic - Managers (Missing both):
❌ member_database_manager.py - NEEDS TEST
❌ room_database_manager.py - NEEDS TEST
Persistence Layer (Missing all 4):
❌ database.py - NEEDS TEST
❌ member_booking_database.py - NEEDS TEST
❌ room_booking_database.py - NEEDS TEST
❌ models.py - NEEDS TEST
Presentation Layer (Lower priority, but could test):
menu.py
options.py
table_formatter.py
user_input.py
utils.py