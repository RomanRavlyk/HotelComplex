from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # from app.Cottage.models import CottageDB
    from app.User.models import UserDB

class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='users.id')
    user: "UserDB" = Relationship(back_populates="bookings")
    cottage_id: int = Field(foreign_key='cottage.id')
    cottage_cost: float = Field(default=None)
    start_date: datetime = Field()
    end_date: datetime = Field()
