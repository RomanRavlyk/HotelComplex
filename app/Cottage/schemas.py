from pydantic import BaseModel

from ..Amenity.schemas import AmenityBase


class Cottage(BaseModel):
    cottage_name: str
    cost_per_day: float
    amenities: list[AmenityBase]