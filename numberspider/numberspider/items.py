# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NumberspiderItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    extraNumberDrawn = scrapy.Field()
    numberDrawn = scrapy.Field()
    numbersDrawn = scrapy.Field()
    # pass
