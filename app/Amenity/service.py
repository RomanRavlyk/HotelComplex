from fastapi import Query, HTTPException, Depends
from typing import Annotated

from starlette import status

from .schemas import HotelAmenityCreate, HotelAmenityFull, CottageAmenityResponse, HotelAmenityResponse
from sqlmodel import select, Session
from app.Hotel.service import plus_hotel_stats, minus_hotel_stats
from ..Cottage.models import CottageDB
from ..Hotel.schemas import Hotel
from ..database import get_session
from app.Hotel.models import HotelDB
from app.Amenity.models import HotelAmenityDB, CottageAmenityDB

def create_hotel_amenity(amenity: HotelAmenityCreate, hotel_id: int, db: Session) -> HotelAmenityDB: #good

    query= select(HotelAmenityDB).where(HotelAmenityDB.amenity_name == amenity.amenity_name)

    check_amenity_db = db.exec(query).first()

    if check_amenity_db is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This amenity already exists")

    amenity_data = amenity.model_dump()
    amenity_data['hotel_id'] = hotel_id
    amenity_db = HotelAmenityDB(**amenity_data)

    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return amenity_db


def get_all_hotel_amenities(hotel_id: int, db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[HotelAmenityDB]:
    query_set = (
        select(HotelAmenityDB)
        .where(HotelAmenityDB.hotel_id == hotel_id)
        .offset(offset)
        .limit(limit)
    )

    hotel_amenities = db.exec(query_set).all()

    if not hotel_amenities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This hotel has no amenity")

    # response_list = []
    # for amenity in hotel_amenities:
    #     response_list.append(HotelAmenityResponse.model_validate(amenity))

    return hotel_amenities


def get_hotel_amenity_by_id(amenity_id: int, hotel_id: int, db: Session) -> HotelAmenityDB:
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel_id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Hotel Amenity Not Found")

    return hotel_amenity


def change_hotel_amenity_in_db(amenity: HotelAmenityFull, hotel_id: Hotel, db: Session) -> HotelAmenityDB:
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity.id,
        HotelAmenityDB.hotel_id == hotel_id.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    for key, value in amenity.model_dump().items():
        setattr(hotel_amenity, key, value)


    db.add(hotel_amenity)
    db.commit()
    db.refresh(hotel_amenity)

    update_cottage_amenities(hotel_amenity.id, hotel_amenity, db)

    return hotel_amenity


def delete_hotel_amenity(amenity_id: int, hotel: Hotel, db: Session):
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(hotel_amenity)
    db.commit()

    delete_amenity_in_all_cottages(amenity_id, hotel.id, db)

    return True

def add_amenity_to_cottage_db(cottage_id: int, amenity_id: int, db: Session):
    amenity_db = db.exec(select(CottageAmenityDB).where((CottageAmenityDB.id == amenity_id) & (CottageAmenityDB.cottage_id == cottage_id))).first()
    if amenity_db:
        raise HTTPException(status_code=409, detail="This amenity already exists")

    cottage = db.exec(select(CottageDB).where(CottageDB.id == cottage_id)).first()
    if not cottage:
        raise HTTPException(status_code=404, detail="Cottage not found")

    hotel = db.exec(select(HotelDB).where(HotelDB.id == cottage.hotel_id)).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    amenities = get_all_hotel_amenities(hotel.id, db)

    selected_amenity = None
    for amenity in amenities:
        if amenity.id == amenity_id:
            selected_amenity = amenity
            break

    if not selected_amenity:
        raise HTTPException(status_code=404, detail="Amenity not available for this hotel")

    new_cottage_amenity = CottageAmenityDB(
        id=selected_amenity.id,
        amenity_name=selected_amenity.amenity_name,
        amenity_cost=selected_amenity.amenity_cost,
        cottage_id=cottage_id,
        cottage=cottage,
        plus_children=selected_amenity.plus_children,
        plus_adults=selected_amenity.plus_adults
    )

    db.add(new_cottage_amenity)
    db.commit()
    db.refresh(new_cottage_amenity)

    cottage.childs += new_cottage_amenity.plus_children
    cottage.adults += new_cottage_amenity.plus_adults
    db.commit()

    plus_hotel_stats(db, hotel.id, new_cottage_amenity.amenity_cost, 0.0)
    db.refresh(new_cottage_amenity)
    return new_cottage_amenity

def get_cottage_amenities_db(cottage_id: int, db: Session):
    cottage_amenities = db.exec(select(CottageAmenityDB).where(CottageAmenityDB.cottage_id == cottage_id)).all()
    amenities_cottage = []
    for amenity in cottage_amenities:
        amenities_cottage.append(CottageAmenityResponse.model_validate(amenity))

    cottage = db.exec(select(CottageDB).where(CottageDB.id == cottage_id)).first()
    if not cottage:
        raise HTTPException(status_code=404, detail="Cottage not found")

    hotel_amenities_query = (
        select(HotelAmenityDB)
        .where(HotelAmenityDB.hotel_id == cottage.hotel_id)
    )
    hotel_amenities = db.exec(hotel_amenities_query).all()
    amenities_hotel = [
        HotelAmenityResponse.model_validate(amenity) for amenity in hotel_amenities
    ]

    return {"cottage_amenities": amenities_cottage, "hotel_amenities": amenities_hotel}



def get_cottage_amenity_by_id_db(cottage_id: int, amenity_id: int, db: Session = Depends(get_session)) -> CottageAmenityDB:
    query = select(CottageAmenityDB).where(
        CottageAmenityDB.id == amenity_id,
        CottageAmenityDB.cottage_id == cottage_id,
    )

    cottage_amenity = db.exec(query).first()

    if not cottage_amenity:
        raise HTTPException(status_code=404, detail="Cottage Amenity Not Found")

    return cottage_amenity


def update_cottage_amenities(amenity_id: int, updated_data: HotelAmenityDB, db: Session):
    cottage_amenities = db.exec(
        select(CottageAmenityDB).where(CottageAmenityDB.id == amenity_id)
    ).all()

    for cottage_amenity in cottage_amenities:
        for key, value in updated_data.model_dump().items():
            if hasattr(cottage_amenity, key):
                setattr(cottage_amenity, key, value)
                plus_hotel_stats(db, cottage_amenity.hotel_id, value, 0.0)


    db.commit()

def delete_cottage_amenity(amenity_id: int, cottage_id: int, db: Session) -> bool:
    query = select(CottageAmenityDB).where(
        CottageAmenityDB.id == amenity_id,
        CottageAmenityDB.cottage_id == cottage_id,
    )

    cottage_amenity = db.exec(query).first()

    if not cottage_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    cottage = db.exec(select(CottageDB).where(CottageDB.id == cottage_id)).first()

    cottage.childs -= cottage_amenity.plus_children
    cottage.adults -= cottage_amenity.plus_adults

    db.delete(cottage_amenity)
    db.commit()
    minus_hotel_stats(db, cottage_amenity.hotel_id, cottage_amenity.amenity_cost, 0.0)
    return True

def delete_amenity_in_all_cottages(amenity_id: int, hotel_id: int, db: Session):
    cottages = db.exec(select(CottageDB).where(CottageDB.hotel_id == hotel_id)).all()

    if not cottages:
        return None

    for cottage in cottages:
        cottage_amenities = db.exec(
            select(CottageAmenityDB)
            .where(CottageAmenityDB.id == amenity_id)
            .where(CottageAmenityDB.cottage_id == cottage.id)
        ).all()

        for amenity in cottage_amenities:
            cottage.childs -= amenity.plus_children
            cottage.adults -= amenity.plus_adults

            db.delete(amenity)

        db.add(cottage)

    db.commit()

