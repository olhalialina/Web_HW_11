from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25))
    last_name = Column(String(30), nullable=False, index=True)
    email = Column(String, unique=True)
    phone_number = Column(String(25))
    born_date = Column(Date)
    description = Column(String(250))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())