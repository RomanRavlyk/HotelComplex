from fastapi import Body, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from .models import HotelAmenityDB, CottageAmenity, HotelAmenityUpdate, HotelAmenityResponse
from sqlmodel import select
from app.main import SessionDep
from app.Hotel.models import Hotel

def create_hotel_amenity(amenity: Annotated[HotelAmenityDB, Body()], hotel: Hotel, db: SessionDep):
    amenity_db = HotelAmenityDB.model_validate(amenity)
    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return JSONResponse(
        content={"message": "Successfully added hotel amenity"},
        status_code=200,
    )

def get_hotel_amenity(hotel: Hotel, db: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100): #should return list of HotelAmenityResponse
    hotel_amenities = db.exec(select(HotelAmenityDB).offset(offset).limit(limit)).all()
    return hotel_amenities

def get_hotel_amenity_by_id(db: SessionDep, amenity_id: int, hotel: Hotel): #should return HotelAmenityResponse
    hotel_amenity = db.get(HotelAmenityDB, amenity_id)
    return hotel_amenity

def change_hotel_amenity(db: SessionDep, amenity_id: int, amenity: HotelAmenityUpdate, hotel: Hotel): #should return HotelAmenityResponse
    hotel_amenity = db.get(HotelAmenityDB, amenity_id)
    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    data_for_update = amenity.model_dump(exclude_unset=True)
    hotel_amenity.sqlmodel_update(data_for_update)
    db.add(hotel_amenity)
    db.commit()
    db.refresh(hotel_amenity)
    return hotel_amenity

def delete_hotel_amenity(db: SessionDep, amenity_id: int, amenity, hotel: Hotel):
    hotel_amenity = db.get(HotelAmenityDB, amenity_id)
    if not hotel_amenity:
        return HTTPException(status_code=404, detail="Amenity not found")
    db.delete(hotel_amenity)
    db.commit()
    return JSONResponse(
        content={"message": "Successfully deleted hotel amenity"},
        status_code=200,
    )


                                                    #todo add logic for CottageAmenity