from pydantic import BaseModel, Field

class CottageBase(BaseModel):
    cottage_name: str
    hotel_id: int
    cost_per_day: float
    cottage_type: str
    adults: int = Field(default=None)
    childs: int = Field(default=None)

class CottageGive(BaseModel):
    id: int
    cottage_name: str
    hotel_id: int
    cost_per_day: float
    cottage_type: str
    adults: int = Field(default=None)
    childs: int = Field(default=None)


class CottageResponse(BaseModel):
    id: int
    cottage_name: str
    hotel_id: int
    cost_per_day: float
    cottage_type: str
    adults: int = Field(default=None)
    childs: int = Field(default=None)

class GetCottage(BaseModel):
    cottage_name: str

class Cottage(BaseModel):
    id: int