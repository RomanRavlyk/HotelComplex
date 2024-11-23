import uuid
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from sqlmodel import select, Session

from .models import SessionDB, UserDB
from app.auth.utils import hash_password


SESSION_TIMEOUT = timedelta(minutes=30)

def create_session(db: Session, user_id: str):
    session_id = str(uuid.uuid4())
    new_session = SessionDB(session_id=session_id, user_id=user_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_session_db(db: Session, session_id: str) -> SessionDB:
    query: SessionDB = db.exec(select(SessionDB).where(SessionDB.session_id == session_id)).first()
    return query

async def delete_session(db: Session, session_id: str):
    session = get_session_db(db, session_id)
    if session:
        db.delete(session)
        db.commit()

def create_user(db: Session, username: str, password: str):
    hashed_pw = hash_password(password)
    new_user = UserDB(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    query = select(UserDB).where(UserDB.username == username)
    result = db.exec(query).first()
    return result

def update_session_activity(db: Session, session_id: str):
    session = get_session_db(db, session_id)
    if session:
        session.last_activity_at = datetime.now(timezone.utc)
        db.commit()


def is_session_active(session: SessionDB) -> bool:
    if session.last_activity_at.tzinfo is None:
        session.last_activity_at = session.last_activity_at.replace(tzinfo=timezone.utc)

    return datetime.now(timezone.utc) - session.last_activity_at < SESSION_TIMEOUT


async def is_logged_in(session_id , db: Session):

    if not session_id:
        raise HTTPException(status_code=401, detail="Not logged in. Session ID not found.")

    session = get_session_db(db, session_id)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session.")

    if session.created_at.tzinfo is None:
        session.created_at = session.created_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - session.created_at > SESSION_TIMEOUT:
        raise HTTPException(status_code=401, detail="Session expired.")

    return session