from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.get('DATABASE')))


def create_foody_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class tbFoodyItems(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "tbl_items"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    coverurl = Column('coverurl', String)
    url = Column('url', String, unique=True)
    category = Column('category', String, nullable=True)
    avgscore = Column('avgscore', Float, nullable=False)
    address = Column('address', String, nullable=True)
    district = Column('district', String, nullable=True)
    city = Column('city', String, nullable=True)
    latitude = Column('latitude', Float, nullable=True)
    longitude = Column('longitude', Float, nullable=True)
    timeopen = Column('timeopen', String, nullable=True)
    pricerange = Column('pricerange', String, nullable=True)

    img = relationship('tbItemImage', backref='tbl_items', lazy='dynamic')
    cmt = relationship('tbItemComments', backref='tbl_items', lazy='dynamic')


class tbItemImage(DeclarativeBase):
    __tablename__ = "tbl_item_img"
    id = Column(Integer, primary_key=True)
    imgurl = Column('imgurl', String)
    url = Column('url', String)
    item_id = Column(Integer, ForeignKey('tbl_items.id', ondelete='CASCADE'),
                     nullable=False)


class tbItemComments(DeclarativeBase):
    __tablename__ = "tbl_item_comment"
    id = Column(Integer, primary_key=True)
    url = Column('url', String)
    user = Column('user', String, nullable=False)
    date = Column('date', DateTime, nullable=False)
    content = Column('content', Text, nullable=False)
    item_id = Column(Integer, ForeignKey(
        'tbl_items.id', ondelete='CASCADE'), nullable=False)
