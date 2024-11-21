from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, Field, select
from .database import create_db_and_tables, get_session
from contextlib import asynccontextmanager
from app.Hotel.routers import router as hotel_router
from fastapi.middleware.cors import CORSMiddleware
from app.Cottage.routers import router as cottage_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    create_db_and_tables()
    yield
    print("Application shutdown")
app = FastAPI(lifespan=lifespan)

app.include_router(hotel_router)
app.include_router(cottage_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DataBase Manual test
class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    item_name: str = Field(index=True, default=None)

@app.post('/create_item/')
def create_item(item: Item, db: Session = Depends(get_session)):
    db_item = Item.model_validate(item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/items/', response_model=list[Item])
def read_items(db: Session = Depends(get_session)):
    items = db.exec(select(Item)).all()
    return items

@app.delete('/delete_item/{item_id}')
def read_items(item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    db.delete(item)
    db.commit()
    return True

