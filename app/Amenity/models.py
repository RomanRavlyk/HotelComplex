from sqlmodel import SQLModel, Field, Relationship

from app.Hotel.models import Hotel
from ..Cottage.models import Cottage

class AmenityBase(SQLModel):
    amenity_name: str = Field(default=None, index=True)
    amenity_cost: float = Field(default=None, nullable=True)

class HotelAmenityDB(AmenityBase, table=True):
    id: int = Field(primary_key=True, default=None)
    hotel_id: int = Field(foreign_key='hotel.id')
    hotel: Hotel | None = Relationship(back_populates="amenity")

class CottageAmenityDB(AmenityBase, table=True):
    id: int = Field(primary_key=True, default=None)
    cottage_id: int = Field(foreign_key='cottage.id')
    cottage: Cottage | None = Relationship(back_populates="amenity")