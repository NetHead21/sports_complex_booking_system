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

        query = """
            class insert_new_member(%s, %s, %s)
        """
        self.db.execute(query, member.id, member.password, member.email)
        self.db.connection.commit()

    def delete_member(self, member_id: int) -> None:
        """
        Deleting a member from the members table

        :param member_id: int
        :return: None
        """

        try:
            query = """
                call delete_member(%s)
            """
            self.db.execute(query, (member_id,))
            self.db.connection.commit()
        except Exception:
            print(f"Member with ID {member_id} does not exist.")

    def update_member_password(self, member_id: int, password: str) -> None:
        """
        Update Member Password

        :param member_id: int
        :param password: str
        :return: None
        """

        query = """
            call update_member_password(%s, %s)
        """
        self.db.execute(query, (member_id, password))
        self.db.connection.commit()

    def update_member_email(self, member_id: int, email: str) -> None:
        """
        Update Member Email

        :param member_id: int
        :param email: str
        :return: None
        """

        query = """
            call update_member_email(%s, %s)
        """
        self.db.execute(query, (member_id, email))
        self.db.connection.commit()



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
