from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine("sqlite:///ecommerce.db", echo=True)
Session = sessionmaker(bind=engine)

async def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)