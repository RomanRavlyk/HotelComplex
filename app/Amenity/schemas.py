from pydantic import BaseModel, Field

class AmenityBase(BaseModel):
    amenity_name: str
    amenity_cost: float = Field(ge=0, description="Cost of the amenity must be non-negative")
    plus_adults: int
    plus_children: int

class HotelAmenityCreate(AmenityBase):
    hotel_id: int

class HotelAmenityUpdate(BaseModel):
    amenity_name: str | None = None
    amenity_cost: float | None = Field(ge=0, description="Cost of the amenity must be non-negative")
    plus_adults: int
    plus_children: int

class HotelAmenityFull(BaseModel):
    id: int
    amenity_name: str
    amenity_cost: float
    plus_adults: int
    plus_children: int

class HotelAmenityResponse(BaseModel):
    id: int
    hotel_id: int
    amenity_name: str
    amenity_cost: float
    plus_adults: int
    plus_children: int

    class Config:
        from_attributes = True

class CottageAmenityCreate(AmenityBase):
    cottage_id: int

class CottageAmenityUpdate(BaseModel):
    amenity_name: str | None = None
    amenity_cost: float | None = Field(ge=0, description="Cost of the amenity must be non-negative")
    plus_adults: int
    plus_children: int

class CottageAmenityResponse(BaseModel):
    id: int
    cottage_id: int
    amenity_name: str
    amenity_cost: float
    plus_adults: int
    plus_children: int

    class Config:
        from_attributes = True