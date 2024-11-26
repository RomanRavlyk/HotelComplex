from http.client import HTTPException

from fastapi import APIRouter, Depends, Body
from typing import Annotated
from sqlmodel import Session
from starlette.responses import JSONResponse
from app.Cottage.service import check_cottage_availability, get_available_periods_db
from app.Booking.service import create_user_booking, get_user_bookings_db, change_user_booking_db, delete_booking_db, \
    get_user_booking_by_id_db
from app.Booking.schemas import BookingSchema, AvailabilityRequest, BookingResponse, BookingChange
from app.database import get_session

router = APIRouter(tags=['Booking'], prefix='/booking')

@router.post("/create_booking/", response_model=BookingResponse)
async def create_booking(booking: BookingSchema, db: Annotated[Session, Depends(get_session)]):
    try:
        booking = create_user_booking(booking, db)
        return booking
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_user_bookings/", response_model=list[BookingResponse])
async def get_user_bookings(user_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        bookings = get_user_bookings_db(user_id, db)
        return bookings
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_booking_by_id/", response_model=BookingResponse)
async def get_user_booking_by_id(user_id: int, booking_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        booking = get_user_booking_by_id_db(user_id, booking_id, db)
        return booking
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.post("/check_availability/")
async def check_availability(
    cottage_id: Annotated[int, Body()],
    dates: AvailabilityRequest,
    session: Session = Depends(get_session)
):
    is_available = check_cottage_availability(
        cottage_id, dates.start_date, dates.end_date, session
    )
    if is_available:
        return {"cottage_id": cottage_id, "available": True}
    else:
        return {"cottage_id": cottage_id, "available": False}


@router.post("/get_available_periods/")
async def get_available_periods(cottage_id: int, db: Session = Depends(get_session)):
    periods = get_available_periods_db(cottage_id, db)

    if not periods:
        return {"message": "No available periods", "cottage_id": cottage_id}

    return {"cottage_id": cottage_id, "available_periods": periods}

@router.put("/update_user_booking/", response_model=BookingResponse)
async def change_user_booking(booking: BookingChange, db: Session = Depends(get_session)):
    try:
        changed_booking = change_user_booking_db(booking, db)
        return changed_booking
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.delete("/delete_user_booking/")
async def delete_user_booking(user_id: int, booking_id: int, db: Session = Depends(get_session)):
    try:
        response = delete_booking_db(user_id, booking_id, db)
        if response:
            return JSONResponse({"message": "Successfully deleted"})
    except HTTPException as e:
        return JSONResponse({"message": str(e)})