from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(DATABASE_URL, echo=True)

def init_test_db():
    SQLModel.metadata.create_all(test_engine)

def drop_test_db():
    SQLModel.metadata.drop_all(test_engine)

def get_test_session() -> Session:
    with Session(test_engine) as session:
        yield session