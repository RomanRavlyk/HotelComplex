from sqlmodel import SQLModel, Field, Relationship

from app.Hotel.models import Hotel


class HotelAmenity(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    amenity_name: str = Field(default=None, index=True)
    amenity_cost: float = Field(default=None, nullable=True)
    hotel_id: int = Field(foreign_key='hotel.id')
    hotel: Hotel | None = Relationship(back_populates="amenity")



# class CottageAmenity(SQLModel, table=True):
#     id: int = Field(primary_key=True, default=None)
#     amenity_name: str = Field(default=None, index=True)
#     amenity_cost: float = Field(default=None, nullable=True)
#     cottage_id: int = Field(foreign_key='cottage.id')
#     hotel: Cottage | None = Relationship(back_populates="amenity")