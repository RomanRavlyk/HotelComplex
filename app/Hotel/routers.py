from typing import Annotated

from fastapi.exceptions import HTTPException
from app.Amenity.schemas import HotelAmenityUpdate, HotelAmenityFull
from fastapi import APIRouter
from fastapi.params import Depends, Body, Query

from sqlmodel import Session
from starlette.responses import JSONResponse

from app.Amenity.service import (change_hotel_amenity_in_db, delete_hotel_amenity,
                                 create_hotel_amenity, get_all_hotel_amenities, get_hotel_amenity_by_id)
from app.Hotel.schemas import HotelBase, HotelResponse, HotelGive, Hotel
from app.Hotel.service import (
    create_hotel,
    get_hotel_db,
    get_all_hotels_in_db,
    update_hotel_in_db,
    delete_hotel_from_db,
)

from .models import HotelDB
from ..Amenity.models import HotelAmenityDB
from ..database import get_session
from ..Amenity.schemas import HotelAmenityCreate, HotelAmenityResponse
router = APIRouter(tags=["hotel"])

@router.post("/create_hotel/", response_model=HotelResponse) #good
async def create_hotel_request(hotel_db: HotelBase, session: Session = Depends(get_session)):
    try:
        hotel = create_hotel(hotel_db, session)
        hotel_data = hotel.model_dump()
        return HotelResponse.model_validate(hotel_data)
    except HTTPException as e:
        return {"message": str(e)}

@router.get("/get_hotel/", response_model=HotelResponse)
async def get_hotel(hotel_in: Annotated[HotelBase, Query()], session: Session = Depends(get_session)):
    try:
        hotel = get_hotel_db(hotel_in, session)
        hotel_data = hotel.model_dump()
        return HotelResponse.model_validate(hotel_data)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/hotels/", response_model=list[HotelResponse])
async def get_hotels(db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    try:
        hotels: list[HotelDB] = get_all_hotels_in_db(db, offset=offset, limit=limit)
        return hotels
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.put("/update_hotel/", response_model=HotelResponse)
async def update_hotel(hotel: HotelGive, db: Session = Depends(get_session)):
    try:
        updated_hotel = update_hotel_in_db(hotel, db)
        hotel_data = updated_hotel.model_dump()
        return HotelResponse.model_validate(hotel_data)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.delete("/delete_hotel/", response_model=HotelResponse)
async def delete_hotel(hotel: HotelGive, db: Session = Depends(get_session)):
    try:
        response: bool = delete_hotel_from_db(hotel, db)
        if response:
            return JSONResponse({"message": "Hotel deleted"})
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.post("/create_hotel_amenity/", response_model=HotelAmenityResponse) #good
async def add_new_hotel_amenity(amenity: HotelAmenityCreate, session: Session = Depends(get_session)):
    try:
        new_amenity = create_hotel_amenity(amenity, amenity.hotel_id, session)
        return new_amenity
    except ValueError as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_hotel_amenities/", response_model=list[HotelAmenityResponse])
async def get_amenities_in_hotel(hotel_id: Annotated[int, Query()], db: Session = Depends(get_session),
                                 offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    try:
        amenities: list[HotelAmenityDB] = get_all_hotel_amenities(hotel_id, db, offset=offset, limit=limit)
        response = [HotelAmenityResponse.model_validate(amenity) for amenity in amenities]
        return response
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_amenity_by_id/", response_model=HotelAmenityResponse)
async def get_by_id_amenity(amenity_id: int, hotel_id: int, db: Session = Depends(get_session)):
    try:
        amenity = get_hotel_amenity_by_id(amenity_id, hotel_id, db)
        return amenity
    except ValueError as e:
        return JSONResponse({"message": str(e)})

@router.put("/change_hotel_amenity", response_model=HotelAmenityResponse)
async def change_hotel_amenity(amenity: HotelAmenityFull, hotel_id: Hotel, db: Session = Depends(get_session)):
    try:
        amenity = change_hotel_amenity_in_db(amenity, hotel_id, db)
        return amenity
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.delete("/delete_amenity/")
async def delete_amenity(amenity_id: Annotated[int, Body()], hotel: Hotel, db: Session = Depends(get_session)):
    try:
        response: bool = delete_hotel_amenity(amenity_id, hotel, db)
        if response:
            return JSONResponse({"message": "Amenity deleted"})
    except HTTPException as e:
        return JSONResponse({"message": str(e)})
