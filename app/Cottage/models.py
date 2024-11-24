from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.Amenity.models import CottageAmenityDB
    from app.Hotel.models import HotelDB

def is_low_season(date: datetime) -> bool:
    return date.month in [11, 3]

class CottageDB(SQLModel, table=True):
    __tablename__ = "cottage"
    id: int = Field(default=None, primary_key=True)
    cottage_name: str = Field(index=True, default=None)
    cottage_type: str = Field(index=False, default=None)
    cost_per_day: float = Field(default=None)
    hotel_id: int = Field(foreign_key='hotel.id')
    hotel: "HotelDB" = Relationship(back_populates="cottages")
    amenities: list["CottageAmenityDB"] = Relationship(back_populates="cottage")
    adults: int = Field(default=None)
    childs: int = Field(default=None)

    def calculate_discounted_cost(self, start_date: datetime, end_date: datetime) -> float:
        cottage_cost = self.cost_per_day
        if is_low_season(start_date) or is_low_season(end_date):
            cottage_cost *= 0.8
        return cottage_cost

