from business_logic import Command
from business_logic.member_database_manager import db


class DeleteMembersCommand(Command):
    def execute(self, member_id: str) -> tuple[bool, any]:
        db.delete_member(member_id)
        return True, None



if __name__ == '__main__':

    try:
        member_id = "shalow21"
        delete_member = DeleteMembersCommand()
        delete_member.execute(member_id)
    except Exception as e:
        print(e)