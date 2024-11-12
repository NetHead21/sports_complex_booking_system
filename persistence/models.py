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
