from typing import Annotated
from fastapi import Depends, APIRouter, Query

from sqlmodel import Session
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from .models import CottageDB
from .schemas import CottageResponse, CottageBase, GetCottage, CottageGive, Cottage
from ..Amenity.models import HotelAmenityDB
from ..Amenity.schemas import CottageAmenityResponse
from ..database import get_session
from .service import (create_cottage_db, get_cottage_db,
                      get_cottages_db, change_cottage_in_db,
                      delete_cottage_in_db, get_available_amenities)
from app.Amenity.service import (add_amenity_to_cottage_db, get_cottage_amenities_db,
                                 get_cottage_amenity_by_id_db, delete_cottage_amenity
                                 )

router = APIRouter(prefix="/cottage", tags=["cottage"])

@router.post("/create_cottage/", response_model=CottageResponse)
def create_cottage(cottage: CottageBase, session: Session = Depends(get_session)):
    try:
        cottage = create_cottage_db(cottage, session)
        cottage_data = cottage.model_dump()
        return CottageResponse.model_validate(cottage_data)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_cottage/", response_model=CottageResponse)
def get_cottage(cottage: Annotated[GetCottage, Query()], session: Session = Depends(get_session)):
    try:
        cottage = get_cottage_db(cottage, session)
        cottage_data = cottage.model_dump()
        return CottageResponse.model_validate(cottage_data)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})



@router.get("/get_cottages/", response_model=list[CottageResponse])
def get_cottages(db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    try:
        cottages: list[CottageDB] = get_cottages_db(db, offset, limit)
        return cottages
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.put("/change_cottage/", response_model=CottageResponse)
async def change_cottage(cottage: CottageGive, session: Annotated[Session, Depends(get_session)]):
    try:
        updated_cottage = change_cottage_in_db(cottage, session)
        cottage_data = cottage.model_dump()
        return CottageResponse.model_validate(cottage_data)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.delete("/delete_cottage/")
async def delete_cottage(cottage: Cottage, session: Annotated[Session, Depends(get_session)]):
        try:
            response = delete_cottage_in_db(cottage, session)
            if response:
                return JSONResponse({"message": "Cottage successfully deleted"})
        except HTTPException as e:
            return JSONResponse({"message": str(e)})

@router.get("/get_available_amenities/", response_model=list[HotelAmenityDB])
async def get_available_cottage_available_amenities(cottage_id: Annotated[int, Query()], session: Session = Depends(get_session)):
    try:
        amenities = get_available_amenities(cottage_id, session)
        return amenities
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.post("/add_amenity_to_cottage/", response_model=CottageAmenityResponse)
async def add_amenity_to_cottage(cottage_id: int, amenity_id: int, db: Session = Depends(get_session)):
    try:
        new_amenity = add_amenity_to_cottage_db(cottage_id, amenity_id, db)
        return CottageAmenityResponse.model_validate(new_amenity)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/cottage_amenities/", response_model=list[CottageAmenityResponse])
async def get_cottage_amenities(cottage_id: Annotated[int, Query()], db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    try:
        amenities = get_cottage_amenities_db(cottage_id, db, offset, limit)
        return amenities
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.get("/get_cottage_amenity/", response_model=CottageAmenityResponse)
async def get_cottage_amenity_by_id(cottage_id: int, amenity_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        amenity = get_cottage_amenity_by_id_db(cottage_id, cottage_id, db)
        return CottageAmenityResponse.model_validate(amenity)
    except HTTPException as e:
        return JSONResponse({"message": str(e)})

@router.delete("/delete_cottage_amenity/")
async def change_cottage_amenity(amenity_id: int, cottage_id: int, db: Annotated[Session, Depends(get_session)]):
    try:
        response = delete_cottage_amenity(cottage_id, amenity_id, db)
        if response:
            return JSONResponse({"message": "Cottage amenity successfully deleted"})
    except HTTPException as e:
        return JSONResponse({"message": str(e)})