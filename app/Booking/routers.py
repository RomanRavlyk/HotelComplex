from http.client import HTTPException

from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session
from starlette.responses import JSONResponse

from app.Booking.service import create_user_booking, get_user_bookings_db, change_user_booking_db, delete_booking_db, \
    get_user_booking_by_id_db
from app.Booking.schemas import BookingSchema
from app.database import get_session

router = APIRouter(tags=['Booking'], prefix='/booking')

@router.post("/create_booking/", response_model=BookingSchema)
async def create_booking(booking: BookingSchema, db: Annotated[Session, Depends(get_session)]):
    try:
        booking = create_user_booking(booking, db)
        return booking
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_user_bookings/", response_model=list[BookingSchema])
async def get_user_bookings(user_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        bookings = get_user_bookings_db(user_id, db)
        return bookings
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_booking_by_id/", response_model=BookingSchema)
async def get_user_booking_by_id(user_id: int, booking_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        booking = get_user_booking_by_id_db(user_id, booking_id, db)
        return booking
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.put("/update_user_booking/", response_model=BookingSchema)
async def change_user_booking(booking: BookingSchema, db: Session = Depends(get_session)):
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