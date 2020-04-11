# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from .model import FoodyItems, db_connect, create_foody_table
from scrapy.exceptions import DropItem


class FoodyPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_foody_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        fditem = FoodyItems(**item)
        if session.query(FoodyItems).filter_by(url=item['url'], avgscore=item['avgscore']).first() == None:
            try:
                session.add(fditem)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item
