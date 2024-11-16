from fastapi import HTTPException
from sqlmodel import Session
from sqlmodel import SQLModel, select
from starlette import status
from .schemas import HotelBase, HotelGive
from .models import HotelDB


def create_hotel(hotel: HotelBase, db: Session) -> HotelDB: #good
    check_hotel_db=db.exec(select(HotelDB).where(HotelDB.hotel_name == hotel.hotel_name)).first()

    if check_hotel_db is not None:
        raise HTTPException(status_code=409, detail="This hotel already exists")

    hotel_data = HotelDB.model_validate(hotel.model_dump())
    db.add(hotel_data)
    db.commit()
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

