from mysql.connector.cursor_cext import CMySQLCursor

from business_logic import Command
from business_logic.member_database_manager import db


class ListMembersCommand(Command):
    def __init__(self, order_by: str = "member_since") -> None:
        self.order_by = order_by

    def execute(self, data=None) -> tuple[bool, CMySQLCursor]:
        return True, db.show_members()
