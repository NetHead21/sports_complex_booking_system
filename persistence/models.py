from datetime import date, time

from pydantic import BaseModel


class Member(BaseModel):
    id: str
    password: str
    email: str


class SearchRoom(BaseModel):
    room_type: str
    book_date: date
    book_time: time


class Booking(BaseModel):
    room_id: str
    book_date: date
    book_time: time
    user: str


if __name__ == "__main__":
    member = Member(id="shalow21", password="HelloWorld21", email="shalow21@gmail.com")
    print(member)
