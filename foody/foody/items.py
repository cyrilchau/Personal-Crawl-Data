# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    coverurl = scrapy.Field()
    category = scrapy.Field()
    avgscore = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    timeopen = scrapy.Field()
    pricerange = scrapy.Field()


class ItemImage(scrapy.Item):
    url = scrapy.Field()
    imgurl = scrapy.Field()


class ItemComments(scrapy.Item):
    url = scrapy.Field()
    user = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()

