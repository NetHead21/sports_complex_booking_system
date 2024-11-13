from business_logic import Command
from business_logic.member_database_manager import db


class UpdateMembersPasswordCommand(Command):
    def execute(self, member_data: dict) -> tuple[bool, any]:
        db.update_member_password(member_data['member_id'], member_data['password'])
        return True, None



if __name__ == '__main__':

    try:
        data: dict[str, str] = {
            "member_id": "prince_elle_07",
            "password": "helloWorld07"
        }
        update_member = UpdateMembersPasswordCommand()
        update_member.execute(data)
        
    except Exception as e:
        print(e)