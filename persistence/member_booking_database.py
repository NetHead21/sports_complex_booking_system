import mysql
from mysql.connector.cursor_cext import CMySQLCursor

from persistence import DatabaseManager, Member


class MemberBookingDatabase:
    def __init__(self):
        self.db = DatabaseManager()

    def create_new_member(self, member: Member) -> None:
        """
        Create a new member and insert it into member table.

        :param member: Member Class Object
        :return: None
        """

        try:
            query = """
                call insert_new_member(%s, %s, %s);
            """
            self.db.execute(query, member.id, member.password, member.email)
            self.db.connection.commit()
            print("Member Registered Successfully!")
        except mysql.connector.Error as err:
            print(err)

    def delete_member(self, member_id: str) -> None:
        """
        Deleting a member from the members table

        :param member_id: str, the member_id or username to be deleted
        :return: None
        """

        try:
            query = """
                call delete_member(%s);
            """
            self.db.execute(query, member_id)
            self.db.connection.commit()
        except mysql.connector.Error:
            print(f"Member with ID {member_id} does not exist.")

    def update_member_password(self, member_id: str, password: str) -> None:
        """
        Update Member Password

        :param member_id: int
        :param password: str
        :return: None
        """

        try:
            query = """
                call update_member_password(%s, %s);
            """
            self.db.execute(query, member_id, password)
            self.db.connection.commit()
        except mysql.connector.Error:
            print(f"Member with ID {member_id} does not exist.")

    def update_member_email(self, member_id: str, email: str) -> None:
        """
        Update Member Email

        :param member_id: int
        :param email: str
        :return: None
        """

        try:
            query = """
                call update_member_email(%s, %s);
            """
            self.db.execute(query, member_id, email)
            self.db.connection.commit()
        except mysql.connector.Error:
            print(f"Member with ID {member_id} does not exist.")

    def show_members(self) -> CMySQLCursor:
        """
        Show all member records from the member table
        :return: MySQLCursor Select Results
        """

        query = """
            select
                id,
                email,
                payment_due
            from members
            order by member_since desc;
        """

        try:
            results = self.db.execute(query)
            return results.fetchall()
        except mysql.connector.Error as err:
            print(err)

    # table = PrettyTable()
    # field_names: list[str] = [
    #     "Id",
    #     "Email",
    #     "Payment_Due"
    # ]
    #
    # table.field_names = field_names
    #
    #
    # for result in results:
    #     table.add_row(list(result))
    #
    # table.align = "l"
    # print(table)


if __name__ == "__main__":
    member_booking = MemberBookingDatabase()
    # print(member_booking.show_members())

    # Insert new member to members table
    # member_data = {
    #     "id": "shalow21",
    #     "password": "hello_world_21",
    #     "email": "shalow21@gmail.com"
    # }
    # member_booking.create_new_member(Member(**member_data))

    # Delete a member from members table
    # member_id = "philip.l"
    # member_booking.delete_member(member_id)

    # Update Member Password
    # member_id = "shalow21"
    # new_password = "HelloWorld21"
    # member_booking.update_member_password(member_id, new_password)

    # Update Member Email
    # member_id = "shalow21"
    # new_email = "shalow21@hotmail.com"
    # member_booking.update_member_email(member_id, new_email)
