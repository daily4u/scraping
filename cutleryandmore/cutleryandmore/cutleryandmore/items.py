# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CutleryandmoreItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    item_id = scrapy.Field()
    item_name   = scrapy.Field()
    item_brand  = scrapy.Field()
    item_category   = scrapy.Field()
    item_subcategory    = scrapy.Field()
    item_img_url    = scrapy.Field()
    # item_description    = scrapy.Field()
    item_contains   = scrapy.Field()
    item_bug    = scrapy.Field()
    item_type   = scrapy.Field()
    item_old_price  = scrapy.Field()
    item_new_price  = scrapy.Field()