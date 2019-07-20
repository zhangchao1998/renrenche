# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrencheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    mileage = scrapy.Field()
    register_time = scrapy.Field()
    address = scrapy.Field()
    standard = scrapy.Field()
    gearbox = scrapy.Field()
    transfer_record = scrapy.Field()
    car_link = scrapy.Field()
