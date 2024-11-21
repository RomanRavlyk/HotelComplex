from fastapi import HTTPException
from sqlmodel import Session, select
from .schemas import CottageBase, CottageGive, GetCottage, Cottage
from .models import CottageDB
from ..Amenity.models import HotelAmenityDB
from app.Amenity.service import get_all_hotel_amenities

def create_cottage_db(cottage: CottageBase, db: Session) -> CottageDB:
    check_cottage_db = db.exec(select(CottageDB).where(CottageDB.cottage_name == cottage.cottage_name)).first()

    if check_cottage_db:
        raise HTTPException(status_code = 409, detail="This cottage already exists")

    cottage_data = CottageDB.model_validate(cottage.model_dump())
    db.add(cottage_data)
    db.commit()
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