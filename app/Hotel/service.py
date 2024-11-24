from fastapi import HTTPException
from sqlmodel import Session
from sqlmodel import select
from starlette import status
from .schemas import HotelBase, HotelGive, Hotel
from .models import HotelDB
from app.Amenity.models import CottageAmenityDB
from app.Hotel.models import HotelStatsDB
from app.Cottage.models import CottageDB

def create_hotel(hotel: HotelBase, db: Session) -> HotelDB:
    check_hotel_db = db.exec(select(HotelDB).where(HotelDB.hotel_name == hotel.hotel_name)).first()

    if check_hotel_db is not None:
        raise HTTPException(status_code=409, detail="This hotel already exists")

    hotel_data = HotelDB.model_validate(hotel.model_dump())

    db.add(hotel_data)
    db.commit()
    db.refresh(hotel_data)

    hotel_stats_data = HotelStatsDB(
        income=0.0,
        expenses=0.0,
        hotel_id=hotel_data.id
    )

    db.add(hotel_stats_data)
    db.commit()
    db.refresh(hotel_stats_data)

    db.refresh(hotel_data)

    return hotel_data


def get_hotel_db(hotel: HotelBase, db: Session) -> HotelDB:
    hotel_db = db.exec(select(HotelDB).where(HotelDB.hotel_name == hotel.hotel_name)).first()

    if hotel_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This hotel does not exist")

    return hotel_db

def get_all_hotels_in_db(db: Session, offset: int, limit: int) -> list[HotelDB]:
    hotels = db.exec(select(HotelDB)
        .offset(offset)
        .limit(limit)
    ).all()

    if not hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hotels found")

    response = []
    for hotel in hotels:
        response.append(HotelDB.model_validate(hotel.model_dump()))

    return response

def update_hotel_in_db(hotel: HotelGive, db: Session) -> HotelDB:
    query = select(HotelDB).where(
        HotelDB.id == hotel.id,
    )

    hotel_db = db.exec(query).first()

    if not hotel_db:
        raise HTTPException(status_code=404, detail="Hotel not found")

    for key, value in hotel.model_dump().items():
        setattr(hotel_db, key, value)

    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)

    return hotel_db

def delete_hotel_from_db(hotel: HotelGive, db: Session) -> True:
    query = select(HotelDB).where(
        HotelDB.id == hotel.id,
    )

    hotel_db = db.exec(query).first()

    if not hotel_db:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db.delete(hotel_db)
    db.commit()
    return True

def get_hotel_cottages(hotel: Hotel, db: Session) -> list[CottageDB]:
    query = select(CottageDB).where(CottageDB.hotel_id == hotel.id)

    cottages = db.exec(query).all()

    if not cottages:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cottages not found")

    response = []
    for cottage in cottages:
        response.append(CottageDB.model_validate(cottage.model_dump()))
    return response

def plus_hotel_stats(db: Session, hotel_id: int, income: float, expenses: float):
    hotel_stats = db.exec(select(HotelStatsDB).where(HotelStatsDB.hotel_id == hotel_id)).first()
    if hotel_stats:
        hotel_stats.income += income
        hotel_stats.expenses += expenses
        db.commit()
        db.refresh(hotel_stats)
        return hotel_stats
    else:
        raise Exception("Hotel not found")


def minus_hotel_stats(db: Session, hotel_id: int, income: float, expenses: float):
    hotel_stats = db.exec(select(HotelStatsDB).where(HotelStatsDB.hotel_id == hotel_id)).first()

    if hotel_stats:
        hotel_stats.income -= income
        hotel_stats.expenses -= expenses
        db.commit()
        db.refresh(hotel_stats)
        return hotel_stats
    else:
        raise Exception("Hotel not found")

def get_hotel_stats(hotel_id: int, db: Session) -> HotelStatsDB:
    stats = db.exec(select(HotelStatsDB).where(HotelStatsDB.hotel_id == hotel_id)).first()

    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel stats not found")

    return stats