import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd=os.getenv('PASSWORD'),
    database='sports_booking'
)


cursor = conn.cursor()

# create new member
# user = {
#     "id": "PrinceElle",
#     "password": "HelloWorld21",
#     "email": "princesaavedragmail.com"
# }
#
# member1 = Member(**user)
#
# query = f"""
#     call insert_new_member(%s, %s, %s)
# """
#
# cursor.execute(query, (member1.id, member1.password, member1.email))
# conn.commit()




# # Show bookings
# query = """
#     select
#         room_id,
#         room_type,
#         datetime_of_booking,
#         member_id,
#         payment_status
#     from member_bookings
# """
#
# cursor.execute(query)
# results = cursor.fetchall()
#
#
# table = PrettyTable()
# field_names: list[str] = [
#     "Room_ID",
#     "Room_Type",
#     "Date and Time",
#     "Booked_By",
#     "Status"
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


# Deleting a member
# member_id = "marvin1"
# query = f"""
#     call delete_member(%s)
# """
# cursor.execute(query, (member_id))
# conn.commit()

#
# Update Member Password
# member_id = "noah51"
# new_password = "Hello_World21"
#
# query = f"""
#     call update_member_password(%s, %s)
# """
# cursor.execute(query, (member_id, new_password))
# conn.commit()


# Update Member Email
# member_id = "noah51"
# new_email = "noah51@gmail.com"
#
# query = f"""
#     call update_member_email(%s, %s)
# """
# cursor.execute(query, (member_id, new_email))
# conn.commit()



# Search Room
# room_type = "Archery Range"
# date = "2017-12-26"
# time = "13:00:00"
#
# query = """
#     call search_room(%s, %s, %s)
# """
#
# cursor.execute(query, (room_type, date, time))
# results = cursor.fetchall()
#
# if results:
#     table = PrettyTable()
#     field_names: list[str] = [
#         "Id",
#         "Room_Type",
#         "Price"
#     ]
#
#     table.field_names = field_names
#
#
#     for result in results:
#         table.add_row(list(result))
#
#     table.align = "l"
#     print(table)
# else:
#     print("No results found, try another date and time.")


# Book a Room
# room_id = "AR"
# date = "2017-12-26"
# time = "13:00:00"
# user = "noah51"

# room_id = "AR"
# date = "2024-11-13"
# time = "13:00:00"
# user = "nethead21"
#
# query = f"""
#     call make_booking(%s, %s, %s, %s)
# """
#
# try:
#     cursor.execute(query, (room_id, date, time, user))
#     conn.commit()
#     print("Room booked successfully")
# except mysql.connector.Error as err:
#     print(err)


# Cancel Booking
# book_id = 17
# message = ""
#
# query1 = f"""
#     call cancel_booking({book_id}, @message);
# """
#
# query2 = """
#     select @message;
# """
#
# try:
#     cursor.execute(query1)
#     cursor.execute(query2)
#     message = cursor.fetchone()
#     print(message)
#     conn.commit()
# except mysql.connector.Error as err:
#     print(err)


#
# # Show members
# query = """
#     select
#         id,
#         email,
#         payment_due
#     from members
#     order by member_since desc;
# """
#
# cursor.execute(query)
# results = cursor.fetchall()
#
#
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



