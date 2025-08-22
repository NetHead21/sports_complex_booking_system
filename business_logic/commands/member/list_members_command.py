from mysql.connector.cursor_cext import CMySQLCursor

from business_logic.base.command import Command
from business_logic.member_database_manager import db
from presentation.table_formatter import format_member_table


class ListMembersCommand(Command):
    def __init__(self, order_by: str = "member_since") -> None:
        self.order_by = order_by

    def execute(self, data=None) -> tuple[bool, None]:
        members = db.show_members()  # This already returns a list, not a cursor

        # Format and print the table
        formatted_table = format_member_table(members)
        print(formatted_table)

        # Return None as result since we already printed the formatted table
        return True, None
