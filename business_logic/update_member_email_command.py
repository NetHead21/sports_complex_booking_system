from business_logic import Command
from business_logic.member_database_manager import db


class UpdateMembersEmailCommand(Command):
    def execute(self, member_data: dict) -> tuple[bool, any]:
        db.update_member_email(member_data["member_id"], member_data["email"])
        return True, None


if __name__ == "__main__":
    try:
        data: dict[str, str] = {
            "member_id": "prince_elle_07",
            "email": "prince_elle@hotmail.com",
        }
        update_member = UpdateMembersEmailCommand()
        update_member.execute(data)

    except Exception as e:
        print(e)
