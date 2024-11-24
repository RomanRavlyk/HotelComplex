from datetime import datetime, timezone
from sqlmodel import Session, select
from starlette.exceptions import HTTPException
from app.Hotel.service import plus_hotel_stats, minus_hotel_stats
from app.Booking.models import Booking
from app.Booking.schemas import BookingSchema
from app.Cottage.models import CottageDB


def is_low_season(date: datetime) -> bool:
    return date.month in [11, 3]

def create_user_booking(booking: BookingSchema, db: Session):
    booking = Booking(**booking.model_dump())

    if booking.end_date < booking.start_date:
        raise HTTPException(status_code=404, detail="End date cannot be earlier than start date")

    if booking.start_date < datetime.now(timezone.utc) or booking.end_date < datetime.now(
            timezone.utc):
        raise HTTPException(status_code=404, detail="Booking dates cannot be in the past")

    cottage = db.exec(select(CottageDB).where(CottageDB.id == booking.cottage_id)).first()

    if cottage is None:
        raise HTTPException(status_code=404, detail="Cottage not found")

    if is_low_season(booking.start_date) or is_low_season(booking.end_date):
        discounted_cost = cottage.calculate_discounted_cost(booking.start_date, booking.end_date)
        booking.cottage_cost = discounted_cost
    else:
        booking.cottage_cost = cottage.cost_per_day

    check_booking = db.exec(select(Booking).where(Booking.user_id == booking.user_id,
                                                  Booking.cottage_id == booking.cottage_id,
                                                  Booking.start_date == booking.start_date,
                                                  Booking.end_date == booking.end_date)).first()

    if check_booking:
        raise HTTPException(status_code=409, detail="This booking already exists")

    db.add(booking)
    db.commit()
    db.refresh(booking)
    plus_hotel_stats(db, cottage.hotel_id, booking.cottage_cost, 5.0)
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

    cottage=db.exec(select(CottageDB).where(CottageDB.id == get_booking.cottage_id,))

    db.delete(get_booking)
    db.commit()

    minus_hotel_stats(db, cottage.hotel_id, get_booking.cottage_cost, 15.0)

    return True