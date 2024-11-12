from datetime import date, time

from pydantic import BaseModel


class Member(BaseModel):
    id: str
    password: str
    email: str


class SearchRoom(BaseModel):
    room_type: str
    date: date
    time: time


class Booking(BaseModel):
    room_id: str
    date: date
    time: time
    user: str


if __name__ == "__main__":
    user = {
        "id": "NetHead21",
        "password": "$@@v3dr@21",
        "email": "junivensaavedra@gmail.com",
    }

    member1 = Member(**user)

    print(member1.id)
    print(member1.password)
    print(member1.email)
    #
    # book1 = Booking(room_id="AR", date="2024-11-20", time="13:00:00", user=member1.id)
    #
    # print(book1)
