from fastapi import Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from starlette import status

from .schemas import HotelAmenityCreate, HotelAmenityUpdate, HotelAmenityResponse, HotelAmenityFull, CottageAmenityCreate, CottageAmenityUpdate, CottageAmenityResponse
from sqlmodel import select, Session

from ..Hotel.schemas import Hotel
from ..database import get_session
from app.Hotel.models import HotelDB
from app.Amenity.models import HotelAmenityDB
# from app.Amenity.models import CottageAmenityDB
# from ..Cottage.models import Cottage

def create_hotel_amenity(amenity: HotelAmenityCreate, hotel_id: int, db: Session) -> HotelAmenityDB: #good

    query= select(HotelAmenityDB).where(HotelAmenityDB.amenity_name == amenity.amenity_name)

    check_amenity_db = db.exec(query).first()

    if check_amenity_db is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This amenity already exists")

    amenity_data = amenity.model_dump()
    amenity_data['hotel_id'] = hotel_id
    amenity_db = HotelAmenityDB(**amenity_data)

    db.add(amenity_db)
    db.commit()
    db.refresh(amenity_db)
    return amenity_db


def get_all_hotel_amenities(hotel_id: int, db: Session = Depends(get_session), offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[HotelAmenityDB]:
    query_set = (
        select(HotelAmenityDB)
        .where(HotelAmenityDB.hotel_id == hotel_id)
        .offset(offset)
        .limit(limit)
    )

    hotel_amenities = db.exec(query_set).all()

    if not hotel_amenities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This hotel has no amenity")

    # response_list = []
    # for amenity in hotel_amenities:
    #     response_list.append(HotelAmenityResponse.model_validate(amenity))

    return hotel_amenities


def get_hotel_amenity_by_id(amenity_id: int, hotel_id: int, db: Session) -> HotelAmenityDB:
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel_id,
    )

    hotel_amenity = db.exec(query).first()

    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Hotel Amenity Not Found")

    return hotel_amenity


def change_hotel_amenity_in_db(amenity: HotelAmenityFull, hotel_id: Hotel, db: Session) -> HotelAmenityDB:
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity.id,
        HotelAmenityDB.hotel_id == hotel_id.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    for key, value in amenity.model_dump().items():
        setattr(hotel_amenity, key, value)


    db.add(hotel_amenity)
    db.commit()
    db.refresh(hotel_amenity)

    return hotel_amenity


def delete_hotel_amenity(amenity_id: int, hotel: Hotel, db: Session):
    query = select(HotelAmenityDB).where(
        HotelAmenityDB.id == amenity_id,
        HotelAmenityDB.hotel_id == hotel.id,
    )

    hotel_amenity = db.exec(query).first()


    if not hotel_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(hotel_amenity)
    db.commit()
    return True
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