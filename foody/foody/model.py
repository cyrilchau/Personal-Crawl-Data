from sqlalchemy import create_engine, Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from scrapy.utils.project import get_project_settings

settings=get_project_settings()
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

class FoodyItems(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "tbl_items"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
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
