from fastapi import Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from .schemas import HotelAmenityCreate, HotelAmenityUpdate, HotelAmenityResponse, CottageAmenityCreate, CottageAmenityUpdate, CottageAmenityResponse
from sqlmodel import select
from app.main import SessionDep
from app.Hotel.models import Hotel
from app.Amenity.models import HotelAmenityDB, CottageAmenityDB
from ..Cottage.models import Cottage

#todo create a logic for check unique of amenity in hotel_update function and cottage_update function
#todo create abstract classes for all same functions to avoid code duplication

def create_hotel_amenity(amenity: HotelAmenityCreate, db: SessionDep):
    amenity_db = HotelAmenityDB.model_validate(amenity)
    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return {"message": "Hotel amenity successfully created", "amenity":
        HotelAmenityResponse.model_validate(amenity_db)
    }


def get_hotel_amenity(hotel: Hotel, db: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[HotelAmenityResponse]: #should return list of HotelAmenityResponse
    query_set = (
        select(HotelAmenityDB)
        .where(HotelAmenityDB.hotel_id == hotel.id)
        .offset(offset)
        .limit(limit)
    )

    hotel_amenities = db.exec(query_set).all()

    response_list = []
    for amenity in hotel_amenities:
        response_list.append(HotelAmenityResponse.model_validate(amenity))

    return response_list


def get_hotel_amenity_by_id(db: SessionDep, amenity_id: int, hotel: Hotel) -> HotelAmenityResponse: #should return HotelAmenityResponse
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Hotel Amenity Not Found")

    return HotelAmenityResponse.model_validate(hotel_amenity)


def change_hotel_amenity(db: SessionDep, amenity_id: int, amenity: HotelAmenityUpdate, hotel: Hotel) -> HotelAmenityResponse: #should return HotelAmenityResponse
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    data_for_update = amenity.model_dump(exclude_unset=True)

    hotel_amenity.update(**data_for_update)

    db.add(hotel_amenity)
    db.commit()
    db.refresh(hotel_amenity)

    return HotelAmenityResponse.model_validate(hotel_amenity)


def delete_hotel_amenity(db: SessionDep, amenity_id: int, hotel: Hotel):
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(hotel_amenity)
    db.commit()
    return {"message": "Successfully deleted hotel amenity"}

def create_cottage_amenity(amenity: CottageAmenityCreate, db: SessionDep):
    amenity_db = CottageAmenityDB.model_validate(amenity)
    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return {"message": "Cottage amenity successfully created", "amenity":
        CottageAmenityResponse.model_validate(amenity_db)
    }


def get_cottage_amenity(cottage: Cottage, db: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[CottageAmenityResponse]: #should return list of HotelAmenityResponse
    query_set = (
        select(CottageAmenityDB)
        .where(CottageAmenityDB.cottage_id == cottage.id)
        .offset(offset)
        .limit(limit)
    )

    cottage_amenities = db.exec(query_set).all()

    response_list = []
    for amenity in cottage_amenities:
        response_list.append(CottageAmenityResponse.model_validate(amenity))

    return response_list


def get_cottage_amenity_by_id(db: SessionDep, amenity_id: int, cottage: Cottage) -> CottageAmenityResponse: #should return HotelAmenityResponse
    query = select(CottageAmenityDB).where(
        CottageAmenityDB.id == amenity_id,
        CottageAmenityDB.cottage_id == cottage.id,
    )

    cottage_amenity = db.exec(query).first()

    if not cottage_amenity:
        raise HTTPException(status_code=404, detail="Cottage Amenity Not Found")

    return CottageAmenityResponse.model_validate(cottage_amenity)


def change_cottage_amenity(db: SessionDep, amenity_id: int, amenity: CottageAmenityUpdate, cottage: Cottage) -> CottageAmenityResponse: #should return HotelAmenityResponse
    query = select(CottageAmenityDB).where(
        CottageAmenityDB.id == amenity_id,
        CottageAmenityDB.cottage_id == cottage.id,
    )

    cottage_amenity = db.exec(query).first()


    if not cottage_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    data_for_update = amenity.model_dump(exclude_unset=True)

    cottage_amenity.update(**data_for_update)

    db.add(cottage_amenity)
    db.commit()
    db.refresh(cottage_amenity)

    return CottageAmenityResponse.model_validate(cottage_amenity)


def delete_cottage_amenity(db: SessionDep, amenity_id: int, cottage: Cottage):
    query = select(CottageAmenityDB).where(
        CottageAmenityDB.id == amenity_id,
        CottageAmenityDB.cottage_id == cottage.id,
    )

    cottage_amenity = db.exec(query).first()

    if not cottage_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(cottage_amenity)
    db.commit()
    return {"message": "Successfully deleted cottage amenity"}