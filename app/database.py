
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./dep_data.db"
engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind= engine,
                            autoflush=False,
                            autocommit = False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    