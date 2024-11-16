from fastapi import Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from starlette import status

from .schemas import HotelAmenityCreate, HotelAmenityUpdate, HotelAmenityResponse, CottageAmenityCreate, CottageAmenityUpdate, CottageAmenityResponse
from sqlmodel import select, Session
from ..database import get_session
from app.Hotel.models import HotelDB
from app.Amenity.models import HotelAmenityDB
# from app.Amenity.models import CottageAmenityDB
# from ..Cottage.models import Cottage

#todo create a logic for check unique of amenity in hotel_update function and cottage_update function
#todo create abstract classes for all same functions to avoid code duplication

def create_hotel_amenity(amenity: HotelAmenityCreate, hotel_id: int, db: Session) -> HotelAmenityDB: #good

    check_amenity_db = db.exec(select(HotelAmenityDB).where(HotelAmenityDB.amenity_name == amenity.amenity_name))

    if check_amenity_db is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This amenity already exists")

    amenity_data = amenity.model_dump()
    amenity_data['hotel_id'] = hotel_id
    amenity_db = HotelAmenityDB(**amenity_data)

    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return amenity_db


def get_hotel_amenity(hotel: HotelDB, db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100): #should return list of HotelAmenityResponse
    query_set = (
        select(HotelAmenityDB)
        .where(HotelAmenityDB.hotel_id == hotel.id)
        .offset(offset)
        .limit(limit)
    )

    hotel_amenities = db.exec(query_set).all()

    response_list = []
    for amenity in hotel_amenities:
        response_list.append(HotelAmenityResponse.model_validate(amenity))

    return response_list


def get_hotel_amenity_by_id(amenity_id: int, hotel: HotelDB, db: Session): #should return HotelAmenityResponse
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Hotel Amenity Not Found")

    return HotelAmenityResponse.model_validate(hotel_amenity)


def change_hotel_amenity(amenity_id: int, amenity: HotelAmenityUpdate, hotel: HotelDB, db: Session): #should return HotelAmenityResponse
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    data_for_update = amenity.model_dump(exclude_unset=True)

    hotel_amenity.update(**data_for_update)

    db.add(hotel_amenity)
    db.commit()
    db.refresh(hotel_amenity)

    return HotelAmenityResponse.model_validate(hotel_amenity)


def delete_hotel_amenity(amenity_id: int, hotel: HotelDB, db: Session):
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(hotel_amenity)
    db.commit()
    return {"message": "Successfully deleted hotel amenity"}
#
# # def create_cottage_amenity(amenity: CottageAmenityCreate, db: Session = Depends(get_session)):
# #     amenity_db = CottageAmenityDB.model_validate(amenity)
# #     db.add(amenity_db)
# #     db.commit()
# #     db.refresh(amenity_db)
# #     return {"message": "Cottage amenity successfully created", "amenity":
# #         CottageAmenityResponse.model_validate(amenity_db)
# #     }
# #
# #
# # def get_cottage_amenity(cottage: Cottage, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, db: Session = Depends(get_session)) -> list[CottageAmenityResponse]: #should return list of HotelAmenityResponse
# #     query_set = (
# #         select(CottageAmenityDB)
# #         .where(CottageAmenityDB.cottage_id == cottage.id)
# #         .offset(offset)
# #         .limit(limit)
# #     )
# #
# #     cottage_amenities = db.exec(query_set).all()
# #
# #     response_list = []
# #     for amenity in cottage_amenities:
# #         response_list.append(CottageAmenityResponse.model_validate(amenity))
# #
# #     return response_list
# #
# #
# # def get_cottage_amenity_by_id(amenity_id: int, cottage: Cottage, db: Session = Depends(get_session)) -> CottageAmenityResponse: #should return HotelAmenityResponse
# #     query = select(CottageAmenityDB).where(
# #         CottageAmenityDB.id == amenity_id,
# #         CottageAmenityDB.cottage_id == cottage.id,
# #     )
# #
# #     cottage_amenity = db.exec(query).first()
# #
# #     if not cottage_amenity:
# #         raise HTTPException(status_code=404, detail="Cottage Amenity Not Found")
# #
# #     return CottageAmenityResponse.model_validate(cottage_amenity)
# #
# #
# # def change_cottage_amenity(amenity_id: int, amenity: CottageAmenityUpdate, cottage: Cottage, db: Session = Depends(get_session)) -> CottageAmenityResponse: #should return HotelAmenityResponse
# #     query = select(CottageAmenityDB).where(
# #         CottageAmenityDB.id == amenity_id,
# #         CottageAmenityDB.cottage_id == cottage.id,
# #     )
# #
# #     cottage_amenity = db.exec(query).first()
# #
# #
# #     if not cottage_amenity:
# #         raise HTTPException(status_code=404, detail="Amenity not found")
# #
# #     data_for_update = amenity.model_dump(exclude_unset=True)
# #
# #     cottage_amenity.update(**data_for_update)
# #
# #     db.add(cottage_amenity)
# #     db.commit()
# #     db.refresh(cottage_amenity)
# #
# #     return CottageAmenityResponse.model_validate(cottage_amenity)
# #
# #
# # def delete_cottage_amenity(amenity_id: int, cottage: Cottage, db: Session = Depends(get_session)):
# #     query = select(CottageAmenityDB).where(
# #         CottageAmenityDB.id == amenity_id,
# #         CottageAmenityDB.cottage_id == cottage.id,
# #     )
# #
# #     cottage_amenity = db.exec(query).first()
# #
# #     if not cottage_amenity:
# #         raise HTTPException(status_code=404, detail="Amenity not found")
# #
# #     db.delete(cottage_amenity)
# #     db.commit()
# #     return {"message": "Successfully deleted cottage amenity"}