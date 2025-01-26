from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///ecommerce.db', echo=True)
session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)

