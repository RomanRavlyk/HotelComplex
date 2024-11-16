from fastapi.exceptions import HTTPException

from fastapi import APIRouter
from fastapi.params import Depends

from sqlmodel import Session
from starlette.responses import JSONResponse

from app.Hotel.schemas import HotelBase, HotelResponse, HotelGive
from app.Hotel.service import create_hotel, add_hotel_amenity
from ..database import get_session
from ..Amenity.schemas import HotelAmenityCreate, HotelAmenityResponse
router = APIRouter()

@router.post("/create_hotel/", response_model=HotelResponse) #good
async def create_hotel_request(hotel: HotelBase, session: Session = Depends(get_session)):
    try:
        hotel = create_hotel(hotel, session)
        hotel_data = hotel.model_dump()
        return HotelResponse.model_validate(hotel_data)
    except HTTPException as e:
        return {"message": str(e)}

@router.post("/create_hotel_amenity/", response_model=HotelAmenityResponse) #good
async def add_new_hotel_amenity(amenity: HotelAmenityCreate, session: Session = Depends(get_session)):
    try:
        new_amenity = add_hotel_amenity(amenity, session)
        return new_amenity
    except ValueError as e:
        return JSONResponse({"message": str(e)})

