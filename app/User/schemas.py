from typing import Annotated
from pydantic import BaseModel

from ..Booking.models import Booking


class User(BaseModel):
    username: str
    firstname: str | None = None
    lastname: str | None = None
    bookings: list[Booking] | None = None

class UserInDB(User):
    hashed_password: str

