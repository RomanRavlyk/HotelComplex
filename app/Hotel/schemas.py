from pydantic import BaseModel
from typing import Annotated, Optional
# from ..Cottage.schemas import Cottage
# from ..Amenity.schemas import AmenityBase, HotelAmenityResponse
from fastapi import Depends

from ..Amenity.schemas import HotelAmenityUpdate


class HotelBase(BaseModel):
    hotel_name: str
    # hotel_amenities: list[HotelAmenityUpdate] | None = None

class HotelGive(BaseModel):
    id: int
    hotel_name: str
    # hotel_amenities: list[HotelAmenityUpdate] | None = None

class HotelResponse(BaseModel):
    id: int
    hotel_name: str
    # hotel_amenities: list[HotelAmenityUpdate] | None = None



