from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated
from ..Amenity.models import HotelAmenityDB


class Hotel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, default=None)
    amenities: list[HotelAmenityDB] = Relationship(back_populates="hotel")