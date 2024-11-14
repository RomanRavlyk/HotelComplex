from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated
from ..Amenity.models import CottageAmenity


class Cottage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, default=None)
    cost_per_day: float = Field(default=None)
    amenities: list[CottageAmenity] = Relationship(back_populates="cottage")