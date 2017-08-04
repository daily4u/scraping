# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DepartItem(scrapy.Item):
    # define the fields for your item here like:
    depart_title = scrapy.Field()
    depart_path = scrapy.Field()
    depart_sub_title = scrapy.Field()
    depart_sub_path = scrapy.Field()
    depart_no = scrapy.Field()
    depart_sub_no = scrapy.Field()

class GoodItem(scrapy.Item):
    Brand = scrapy.Field()
    Category = scrapy.Field()
    Brand_No = scrapy.Field()
    Category_No = scrapy.Field()
    Id = scrapy.Field()
    Name = scrapy.Field()
    Size = scrapy.Field()
    Unit = scrapy.Field()
    Price = scrapy.Field()
    SourceImage = scrapy.Field()
    TargetImage = scrapy.Field()
    TrackingParam = scrapy.Field()

class ImageItem(scrapy.Item):
    Ids  = scrapy.Field()
    Dirs = scrapy.Field()
    image_urls  = scrapy.Field()