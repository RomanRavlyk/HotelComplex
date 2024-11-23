from fastapi import FastAPI
from .database import create_db_and_tables
from contextlib import asynccontextmanager
from app.Hotel.routers import router as hotel_router
from fastapi.middleware.cors import CORSMiddleware
from app.Cottage.routers import router as cottage_router
from app.User.routers import router as user_router
from app.Booking.routers import router as booking_router
from app.middleware.loginmiddleware import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    create_db_and_tables()
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(hotel_router)
app.include_router(cottage_router)
app.include_router(user_router)

app.include_router(booking_router)

app.add_middleware(SessionMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
