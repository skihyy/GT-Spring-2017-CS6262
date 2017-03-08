# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrowserSimulatorItem(scrapy.Item):
    # define the fields for your item here like:
    raw_data = scrapy.Field()
    url = scrapy.Field()
    header = scrapy.Field()
    body = scrapy.Field()
    redirect = scrapy.Field()
    links = scrapy.Field()
    pass
