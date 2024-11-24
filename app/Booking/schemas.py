from datetime import datetime
from pydantic import BaseModel, field_validator


class BookingSchema(BaseModel):
    user_id: int
    cottage_id: int
    start_date: datetime
    end_date: datetime

class AvailabilityRequest(BaseModel):
    start_date: datetime
    end_date: datetime

class BookingResponse(BaseModel):
    user_id: int
    cottage_id: int
    start_date: datetime
    end_date: datetime
    cottage_cost: float