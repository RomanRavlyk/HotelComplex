from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, List
# from ..Amenity.models import HotelAmenityDB
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.Amenity.models import HotelAmenityDB


class HotelDB(SQLModel, table=True):
    __tablename__ = "hotel"
    id: int = Field(primary_key=True, default=None)
    hotel_name: str = Field(index=True, default=None)
    amenities: list["HotelAmenityDB"] | None = Relationship(back_populates="hotel")

