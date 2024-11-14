from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated
from ..Amenity.models import HotelAmenity


class Hotel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, default=None)
    amenities: list[HotelAmenity] = Relationship(back_populates="hotel")