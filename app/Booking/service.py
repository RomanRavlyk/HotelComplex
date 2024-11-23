from datetime import datetime, timezone
from sqlmodel import Session, select
from starlette.exceptions import HTTPException

from app.Booking.models import Booking
from app.Booking.schemas import BookingSchema

def create_user_booking(booking: BookingSchema, db: Session):
    booking = Booking(**booking.model_dump())
    if booking.end_date < booking.start_date:
        raise HTTPException(status_code=404, detail="Invalid booking dates")
    if booking.start_date < datetime.now(timezone.utc) or booking.end_date < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Invalid booking dates")

    check_booking = db.exec(select(Booking).where(Booking.user_id == booking.user_id, Booking.cottage_id == booking.cottage_id,
                                                  Booking.start_date == booking.start_date,
                                                  Booking.end_date == booking.end_date)).first()

    if check_booking:
        raise HTTPException(status_code=409,detail="This booking already exists")

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_user_bookings_db(user_id: int, db: Session):
    bookings = db.exec(select(Booking).where(Booking.user_id == user_id)).all()

    if not bookings:
        raise HTTPException(status_code=404, detail="This user has no bookings")
    return bookings

def get_user_booking_by_id_db(user_id: int, booking_id: int, db: Session):
    booking = db.exec(select(Booking).where(Booking.user_id == user_id,
                                            Booking.id == booking_id)).first()

    if not booking:
        raise HTTPException(status_code=404, detail="This booking does not exist")

    return booking

def change_user_booking_db(booking: BookingSchema, db: Session):
    get_booking = db.exec(select(Booking).where(Booking.user_id == booking.user_id,)).first()
    if not get_booking:
        raise HTTPException(status_code=404, detail="This booking does not exist")

    for key, value in booking.model_dump().items():
        setattr(get_booking, key, value)

    if booking.end_date < booking.start_date:
        raise HTTPException(status_code=404, detail="Invalid booking dates")
    if booking.start_date < datetime.now() or booking.end_date < datetime.now():
        raise HTTPException(status_code=404, detail="Invalid booking dates")

    check_booking = db.exec(select(Booking).where(Booking.user_id == get_booking.user_id, Booking.cottage_id == get_booking.cottage_id,
                                                  Booking.start_date == booking.start_date,
                                                  Booking.end_date == booking.end_date)).first()

    if check_booking:
        raise HTTPException(status_code=409,detail="This booking already exists")

    db.add(get_booking)
    db.commit()
    db.refresh(get_booking)
    return booking

def delete_booking_db(user_id: int, booking_id: int, db: Session):
    get_booking = db.exec(select(Booking).where(Booking.user_id == user_id,
                                                Booking.id == booking_id)).first()
    if not get_booking:
        raise HTTPException(status_code=404, detail="This booking does not exist")

    db.delete(get_booking)
    db.commit()
    return True