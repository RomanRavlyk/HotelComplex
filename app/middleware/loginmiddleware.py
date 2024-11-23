from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
from starlette.responses import JSONResponse
from app.User.service import SESSION_TIMEOUT, is_logged_in
from sqlalchemy.orm import Session
from app.database import get_session

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth") or request.method == "GET":
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            return JSONResponse({"message": "Not logged in. Session ID not found."}, status_code=403)

        db: Session = next(get_session())
        session = await is_logged_in(session_id, db)

        if not session:
            return JSONResponse({"message": "Invalid session."}, status_code=401)

        if session.created_at.tzinfo is None:
            session.created_at = session.created_at.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) - session.created_at > SESSION_TIMEOUT:
            return JSONResponse({"message": "Session expired."}, status_code=401)
        request.state.session = session

        response = await call_next(request)
        return response
