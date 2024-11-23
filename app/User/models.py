import uuid
from datetime import datetime, timezone
from typing import Optional
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.Booking.models import Booking

class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str = Field(nullable=False)
    bookings: list["Booking"] = Relationship(back_populates="user")

class SessionDB(SQLModel, table=True):
    __tablename__ = "sessions"

    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))