from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from app.Amenity.models import CottageAmenityDB
    from app.Hotel.models import HotelDB

class CottageDB(SQLModel, table=True):
    __tablename__ = "cottage"
    id: int = Field(default=None, primary_key=True)
    cottage_name: str = Field(index=True, default=None)
    cost_per_day: float = Field(default=None)
    hotel_id: int = Field(foreign_key='hotel.id')
    hotel: "HotelDB" = Relationship(back_populates="cottages")
    amenities: list["CottageAmenityDB"] = Relationship(back_populates="cottage")