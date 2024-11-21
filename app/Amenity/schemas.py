from pydantic import BaseModel, Field

class AmenityBase(BaseModel):
    amenity_name: str
    amenity_cost: float = Field(ge=0, description="Cost of the amenity must be non-negative")

class HotelAmenityCreate(AmenityBase):
    hotel_id: int

class HotelAmenityUpdate(BaseModel):
    amenity_name: str | None = None
    amenity_cost: float | None = None

class HotelAmenityFull(BaseModel):
    id: int
    amenity_name: str
    amenity_cost: float

class HotelAmenityResponse(BaseModel):
    id: int
    amenity_name: str
    amenity_cost: float

    class Config:
        from_attributes = True

class CottageAmenityCreate(AmenityBase):
    cottage_id: int

class CottageAmenityUpdate(BaseModel):
    amenity_name: str | None = None
    amenity_cost: float | None = None

class CottageAmenityResponse(BaseModel):
    id: int
    amenity_name: str
    amenity_cost: float

    class Config:
        from_attributes = True