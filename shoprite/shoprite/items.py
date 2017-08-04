# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopriteItem(scrapy.Item):
    # define the fields for your item here like:
    Id = scrapy.Field()
    Name = scrapy.Field()

class ProductItem(scrapy.Item):
    Sku = scrapy.Field()
    Id = scrapy.Field()
    Name = scrapy.Field()
    ItemKey = scrapy.Field()
    Category = scrapy.Field()
    Description = scrapy.Field()
    Brand = scrapy.Field()
    Category = scrapy.Field()
    RegularPrice = scrapy.Field()
    CurrentUnitPrice = scrapy.Field()
    CurrentPrice = scrapy.Field()
    ItemType = scrapy.Field()
    Size = scrapy.Field()
    SalesValid = scrapy.Field()
    SalesMinQty = scrapy.Field()
    SalesDesc1 = scrapy.Field()
    SalesDesc2 = scrapy.Field()
    Labels = scrapy.Field()
    Images = scrapy.Field()
    Nutritions = scrapy.Field()


