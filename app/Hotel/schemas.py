from pydantic import BaseModel
class HotelBase(BaseModel):
    hotel_name: str


class HotelGive(BaseModel):
    id: int
    hotel_name: str


class HotelResponse(BaseModel):
    id: int
    hotel_name: str

class Hotel(BaseModel):
    id: int

class HotelStatsResponse(BaseModel):
    hotel_id: int
    income: float
    expenses: float
