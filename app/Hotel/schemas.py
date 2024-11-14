from pydantic import BaseModel
from typing import Annotated
from ..Cottage.schemas import Cottage
from ..Amenity.schemas import AmenityBase
from fastapi import Depends



class HotelBase(BaseModel):
    hotel_name: str
    hotel_amenities: Annotated[list[AmenityBase], Depends()]
    hotel_cottages: Annotated[list[Cottage], Depends()]

