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
    QuitCommand,
)
from presentation import Option, get_options_choice

member_options = {
    "A": Option("View All Members", ListMembersCommand(), success_message=""),
    "B": Option("Add New Member", AddMembersCommand(), success_message=""),
    "C": Option("Update Member Email", UpdateMembersEmailCommand(), success_message=""),
    "D": Option("Update Member Password", UpdateMembersPasswordCommand(), success_message=""),
    "E": Option("Delete A Member", DeleteMembersCommand(), success_message=""),
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
    "Q": ("Quit", {"Q": Option("Quit Application", QuitCommand(), success_message="")}),
}


def main_menu():
    """
    Display and handle the main menu navigation for the sports booking system.
    
    This function provides the main entry point for user interaction, displaying
    the available menu categories (Member Management, Room Management) and handling
    user navigation choices. It uses the get_options_choice utility for robust
    input validation and follows the Command pattern consistently for all actions.
    
    Menu Structure:
        - A: Member Management (leads to member_options submenu)
        - B: Room Management (leads to room_options submenu)  
        - Q: Quit (executes QuitCommand to terminate application)
    
    The function automatically handles invalid input by re-prompting the user
    until a valid choice is made using the get_options_choice utility.
    All menu actions follow the Command pattern for architectural consistency.
    """
    while True:
        print("\n" + "=" * 50)
        print("🏟️  SPORTS COMPLEX BOOKING SYSTEM")
        print("=" * 50)
        print("Main Menu:")
        for key, (menu_name, _) in menu_options.items():
            print(f"  {key}: {menu_name}")
        print("-" * 50)

        # Create choices dictionary for get_options_choice
        main_choices = {
            key: (menu_name, sub_options) for key, (menu_name, sub_options) in menu_options.items()
        }
        
        # Use get_options_choice for automatic validation
        choice_result = get_options_choice(main_choices)
        menu_name, sub_options = choice_result
        sub_menu(menu_name, sub_options)


def sub_menu(menu_name: str, options: dict):
    """
    Display and handle submenu navigation for specific menu categories.
    
    This function manages the display and interaction for submenu items within
    a specific category (like Member Management or Room Management). It uses
    the get_options_choice utility for input validation and handles command
    execution with proper error handling.
    
    Args:
        menu_name (str): The name of the submenu category to display in the header.
        options (dict): Dictionary of menu options where keys are choice letters
                       and values are Option objects containing commands to execute.
    
    Menu Behavior:
        - Displays all available options for the category
        - X: Back to Main Menu (returns to parent menu)
        - Executes selected commands and handles any errors gracefully
        - Uses get_options_choice for automatic input validation
        - Waits for user confirmation before returning to menu
    
    Error Handling:
        - Catches and displays any exceptions during command execution
        - Prompts user to continue after errors or successful operations
    """
    while True:
        print(f"\n" + "=" * 50)
        print(f"📋 {menu_name}")
        print("=" * 50)
        for key, option in options.items():
            print(f"  {key}: {option.name}")
        print("  X: Back to Main Menu")
        print("-" * 50)

        # Create choices dictionary including back option
        submenu_choices = {
            **options,
            "X": Option("Back to Main Menu", None)
        }
        
        # Use get_options_choice for automatic validation
        selected_option = get_options_choice(submenu_choices)
        
        if selected_option.name == "Back to Main Menu":
            break
        else:
            try:
                print(f"\n🔄 Executing: {selected_option.name}")
                selected_option.choose()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
