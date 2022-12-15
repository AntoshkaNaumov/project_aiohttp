from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from errors import NotFound


Base = declarative_base()


class OwnerModel(Base):

    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    ads = relationship('AdvertisementModel', backref='owner')


class AdvertisementModel(Base):

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.today)
    owner_id = Column(Integer, ForeignKey('owners.id'))
