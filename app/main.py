from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, Field, select
from typing import Annotated
from .database import engine, create_db_and_tables

async def lifespan(app: FastAPI):
    print("Application startup")
    create_db_and_tables()
    yield

    print("Application shutdown")
app = FastAPI(lifespan=lifespan)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

# DataBase Manual test
class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    item_name: str = Field(index=True, default=None)

@app.post('/create_item/')
def create_item(db: SessionDep, item: Item):
    db_item = Item.model_validate(item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/items/', response_model=list[Item])
def read_items(db: SessionDep):
    items = db.exec(select(Item)).all()
    return items

