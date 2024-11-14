from pydantic import BaseModel
from typing import Annotated


class AmenityBase(BaseModel):
    amenity_name: str
    cost: float

