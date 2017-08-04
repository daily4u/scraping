# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MartialartsclubsItem(scrapy.Item):
    # define the fields for your item here like:
    Martial_Art = scrapy.Field()
    Style = scrapy.Field()
    County = scrapy.Field()
    Town = scrapy.Field()
    Venue = scrapy.Field()
    Contact_Name = scrapy.Field()
    Email = scrapy.Field()
    Telephone = scrapy.Field()
    Website = scrapy.Field()
    Description = scrapy.Field()