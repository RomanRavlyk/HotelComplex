from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.Amenity.models import HotelAmenityDB
    from app.Cottage.models import CottageDB

class HotelDB(SQLModel, table=True):
    __tablename__ = "hotel"
    id: int = Field(primary_key=True, default=None)
    hotel_name: str = Field(index=True, default=None)
    cottages: list["CottageDB"] | None = Relationship(back_populates="hotel")
    amenities: list["HotelAmenityDB"] | None = Relationship(back_populates="hotel")

