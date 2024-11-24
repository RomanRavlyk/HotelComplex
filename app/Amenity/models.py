from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.Hotel.models import HotelDB
    from app.Cottage.models import CottageDB

class AmenityBase(SQLModel):
    amenity_name: str = Field(default=None, index=True)
    amenity_cost: float = Field(default=None, nullable=True)
    plus_adults: int = Field(default=None, nullable=True)
    plus_children: int = Field(default=None, nullable=True)

class HotelAmenityDB(AmenityBase, table=True):
    __tablename__ = "hotel_amenity"
    id: int = Field(primary_key=True, default=None)
    hotel_id: int = Field(foreign_key='hotel.id')
    hotel: "HotelDB" = Relationship(back_populates="amenities")


class CottageAmenityDB(AmenityBase, table=True):
    __tablename__ = "cottage_amenity"
    id: int = Field(primary_key=True, default=None)
    cottage_id: int = Field(foreign_key='cottage.id')
    cottage: "CottageDB" = Relationship(back_populates="amenities")