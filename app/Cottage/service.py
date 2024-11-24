from datetime import datetime
from app.Hotel.service import plus_hotel_stats, minus_hotel_stats
from fastapi import HTTPException
from sqlmodel import Session, select
from .schemas import CottageBase, CottageGive, GetCottage, Cottage
from .models import CottageDB
from ..Amenity.models import HotelAmenityDB
from app.Amenity.service import get_all_hotel_amenities
from ..Booking.models import Booking


def create_cottage_db(cottage: CottageBase, db: Session) -> CottageDB:
    check_cottage_db = db.exec(select(CottageDB).where(CottageDB.cottage_name == cottage.cottage_name)).first()

    if check_cottage_db:
        raise HTTPException(status_code = 409, detail="This cottage already exists")

    cottage_data = CottageDB.model_validate(cottage.model_dump())
    db.add(cottage_data)
    db.commit()
    db.refresh(cottage_data)

    plus_hotel_stats(db, cottage_data.hotel_id, 0.0, 30)
    db.refresh(cottage_data)

    return cottage_data

def get_cottage_db(cottage: GetCottage, db: Session) -> CottageDB:
    cottage_db = db.exec(select(CottageDB).where(CottageDB.cottage_name == cottage.cottage_name)).first()

    if not cottage_db:
        raise HTTPException(status_code = 404, detail="Cottage not found")

    return cottage_db

def get_cottages_db(db: Session, offset: int, limit: int) -> list[CottageDB]:
    cottages = db.exec(select(CottageDB).offset(offset).limit(limit)).all()

    if not cottages:
        raise HTTPException(status_code = 404, detail="Cottages not found")

    response = []
    for cottage in cottages:
        response.append(CottageDB.model_validate(cottage.model_dump()))

    return response

def change_cottage_in_db(cottage: CottageGive, db: Session) -> CottageDB:
    query = select(CottageDB).where(CottageDB.id == cottage.id)

    cottage_db = db.exec(query).first()

    if not cottage_db:
        raise HTTPException(status_code = 404, detail="Cottage not found")

    for key, value in cottage.model_dump().items():
        setattr(cottage_db, key, value)

    db.add(cottage_db)
    db.commit()
    db.refresh(cottage_db)

    return cottage_db

def delete_cottage_in_db(cottage: Cottage, db: Session) -> bool:
    query = select(CottageDB).where(CottageDB.id == cottage.id)
    cottage_db = db.exec(query).first()

    if not cottage_db:
        raise HTTPException(status_code = 404, detail="Cottage not found")

    db.delete(cottage_db)
    db.commit()

    minus_hotel_stats(db, cottage_db.hotel_id, cottage_db.cost_per_day, 10.0)

    return True

def get_available_amenities(cottage_id: int, db: Session) -> list[HotelAmenityDB]:
    cottage = db.exec(select(CottageDB).where(CottageDB.id == cottage_id)).first()

    if not cottage:
        raise HTTPException(status_code = 404, detail="Cottage not found")

    try:
        amenities = get_all_hotel_amenities(cottage.hotel_id, db)
    except HTTPException as e:
        raise e

    return amenities


def get_cottage_by_type_db(cottage_type: str, db: Session) -> list[CottageDB]:
    cottages = db.exec(select(CottageDB).where(CottageDB.cottage_type == cottage_type)).all()

    if not cottages:
        raise HTTPException(status_code=404, detail="No cottages found for this type")

    return cottages

def check_cottage_availability(
        cottage_id: int, requested_start_date: datetime, requested_end_date: datetime, db: Session
) -> bool:

    query = (
        select(Booking)
        .where(Booking.cottage_id == cottage_id)
        .where(
            (Booking.start_date <= requested_end_date) &
            (Booking.end_date >= requested_start_date)
        )
    )
    conflicting_bookings = db.exec(query).all()

    if not conflicting_bookings:
        return True

    return False

def get_available_periods_db(cottage_id: int, db: Session):
    bookings = db.exec(
        select(Booking).where(Booking.cottage_id == cottage_id).order_by(Booking.start_date)
    ).all()

    available_periods = []
    now = datetime.now()

    if bookings and bookings[0].start_date > now:
        available_periods.append({"start": now, "end": bookings[0].start_date})

    for i in range(len(bookings) - 1):
        if bookings[i].end_date < bookings[i + 1].start_date:
            available_periods.append(
                {"start": bookings[i].end_date, "end": bookings[i + 1].start_date}
            )

    if bookings and bookings[-1].end_date >= now:
        available_periods.append({"start": bookings[-1].end_date, "end": None})
    elif not bookings:
        available_periods.append({"start": now, "end": None})

    return available_periods

