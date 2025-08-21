from business_logic import (
    ListMembersCommand,
    AddMembersCommand,
    UpdateMembersEmailCommand,
    UpdateMembersPasswordCommand,
    DeleteMembersCommand,
    ListRoomCommand,
    SearchRoomCommand,
    BookRoomCommand,
    CancelBookRoomCommand,
)
from presentation import Option
from prompt_toolkit import prompt

member_options = {
    "A": Option("View All Members", ListMembersCommand(), success_message=""),
    "B": Option("Add New Member", AddMembersCommand(), success_message=""),
    "C": Option("Update Member Email", UpdateMembersEmailCommand(), success_message=""),
    "D": Option("Update Member Password", UpdateMembersPasswordCommand(), success_message=""),
    "E": Option("Delete A Member", DeleteMembersCommand()),
}

room_options = {
    "A": Option("View All Rooms", ListRoomCommand(), success_message=""),
    "B": Option("Search A Room", SearchRoomCommand()),
    "C": Option("Book A Room", BookRoomCommand()),
    "D": Option("Cancel Booking", CancelBookRoomCommand()),
}

menu_options = {
    "A": ("Member Management", member_options),
    "B": ("Room Management", room_options),
}


def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("🏟️  SPORTS COMPLEX BOOKING SYSTEM")
        print("=" * 50)
        print("Main Menu:")
        for key, (menu_name, _) in menu_options.items():
            print(f"  {key}: {menu_name}")
        print("  Q: Quit")
        print("-" * 50)

        choice = prompt("Select an option: ").upper()

        if choice in menu_options:
            menu_name, sub_options = menu_options[choice]
            sub_menu(menu_name, sub_options)
        elif choice == "Q":
            print("Thank you for using Sports Complex Booking System!")
            break
        else:
            print("❌ Invalid option. Please try again.")


def sub_menu(menu_name: str, options: dict):
    while True:
        print(f"\n" + "=" * 50)
        print(f"📋 {menu_name}")
        print("=" * 50)
        for key, option in options.items():
            print(f"  {key}: {option.name}")
        print("  X: Back to Main Menu")
        print("-" * 50)

        choice = prompt("Select an option: ").upper()

        if choice in options:
            try:
                print(f"\n🔄 Executing: {options[choice].name}")
                options[choice].choose()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
        elif choice == "X":
            break
        else:
            print("❌ Invalid option. Please try again.")
            input("Press Enter to continue...")
