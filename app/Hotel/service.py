from fastapi import HTTPException
from fastapi.params import Depends
from typing import Annotated
from sqlmodel import Session
from sqlmodel import SQLModel, select

from .schemas import HotelBase, HotelGive
from .models import HotelDB
from ..Amenity.models import HotelAmenityDB
from ..Amenity.schemas import HotelAmenityCreate
from  ..Amenity.service import create_hotel_amenity

def create_hotel(hotel: HotelBase, db: Session) -> HotelDB: #good
    check_hotel_db=db.exec(select(HotelDB).where(HotelDB.hotel_name == hotel.hotel_name)).first()

    if check_hotel_db is not None:
        raise HTTPException(status_code=409, detail="This hotel already exists")

    hotel_data = HotelDB.model_validate(hotel.model_dump())
    db.add(hotel_data)
    db.commit()
    db.refresh(hotel_data)

    return hotel_data

def add_hotel_amenity(amenity: HotelAmenityCreate, db: Session) -> HotelAmenityDB | HTTPException: #good
    try:
        new_hotel_amenity = create_hotel_amenity(amenity, amenity.hotel_id ,db)
        return new_hotel_amenity
    except HTTPException  as e:
        raise e
