from typing import Annotated

from fastapi import Depends, HTTPException, Request, APIRouter, Body
from fastapi.responses import JSONResponse

from .models import SessionDB
from .service import create_session, get_session_db, delete_session, get_user_by_username, create_user, update_session_activity, is_session_active, is_logged_in
from app.database import get_session
import os
from dotenv import load_dotenv
from sqlmodel import Session

from ..auth.utils import verify_password

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post("/register")
async def register(username: Annotated[str, Body()], password: Annotated[str, Body()], db: Session = Depends(get_session)):
    existing_user = get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    new_user = create_user(db, username, password)
    return {"message": "User registered successfully", "user": {"id": new_user.id, "username": new_user.username}}


@router.post("/login")
async def login(username: Annotated[str, Body()], password: Annotated[str, Body()], db: Session = Depends(get_session)):

    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    session = create_session(db, user.id)

    response = JSONResponse(content={"message": "Logged in"})
    response.set_cookie(key="session_id", value=session.session_id, httponly=True)
    return response


@router.get("/me")
async def get_user(request: Request, db: Session = Depends(get_session)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID not found")

    session: SessionDB = get_session_db(db, session_id)
    if not session or not is_session_active(session):
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    update_session_activity(db, session_id)

    return {"user_id": session.user_id}


@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_session)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID not found")
    await delete_session(db, session_id)
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="session_id")
    return response
