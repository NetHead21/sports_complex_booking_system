from business_logic import Command
from business_logic.member_database_manager import db
from persistence.models import Member


class AddMembersCommand(Command):
    def execute(self, member: Member) -> tuple[bool, any]:
        db.create_new_member(member)
        print("Member Registered Successfully!")
        return True, None


if __name__ == "__main__":
    try:
        member_data = {
            "id": "prince_elle_07",
            "password": "HellImPrince07",
            "email": "princeelle@gmail.com",
        }

        member = Member(**member_data)

        # list_members = ListMembersCommand()
        # print(list_members.execute(member_booking))

        add_member = AddMembersCommand()
        add_member.execute(member)
    except Exception as e:
        print(e)
