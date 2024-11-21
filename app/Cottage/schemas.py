from pydantic import BaseModel

class CottageBase(BaseModel):
    cottage_name: str
    hotel_id: int
    cost_per_day: float

class CottageGive(BaseModel):
    id: int
    cottage_name: str
    hotel_id: int
    cost_per_day: float

class CottageResponse(BaseModel):
    id: int
    cottage_name: str
    hotel_id: int
    cost_per_day: float

class GetCottage(BaseModel):
    cottage_name: str

class Cottage(BaseModel):
    id: int