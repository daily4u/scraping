# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyhammerItem(scrapy.Item):
    # define the fields for your item here like:
    # service_name = scrapy.Field()
    # name = scrapy.Field()
    # street = scrapy.Field()
    # postal = scrapy.Field()
    # locality = scrapy.Field()
    # country = scrapy.Field()
    url = scrapy.Field()
    iswp = scrapy.Field()
    wp_version = scrapy.Field()
