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
    stats: "HotelStatsDB" = Relationship(back_populates="hotel", sa_relationship_kwargs={"uselist": False})


class HotelStatsDB(SQLModel, table=True):
    __tablename__ = 'hotel_stats'

    id: int = Field(default=None, primary_key=True)
    income: float = Field(default=0.0)
    expenses: float = Field(default=0.0)
    hotel_id: int = Field(foreign_key="hotel.id")
    hotel: HotelDB = Relationship(back_populates="stats")