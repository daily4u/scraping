# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MwwineparkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name =  scrapy.Field()
    item_id =  scrapy.Field()
    product_id =  scrapy.Field()
    brand_id =  scrapy.Field()
    sku =  scrapy.Field()
    item_category =  scrapy.Field()
    item_variental =  scrapy.Field()
    item_country =  scrapy.Field()
    item_region =  scrapy.Field()
    brand =  scrapy.Field()
    price =  scrapy.Field()
    disc_price =  scrapy.Field()
    unit =  scrapy.Field()
    image =  scrapy.Field()
    alcohol =  scrapy.Field()
    appellation =  scrapy.Field()
    description =  scrapy.Field()

class ImageItem(scrapy.Item):
    Ids = scrapy.Field()
    Dirs = scrapy.Field()
    image_urls = scrapy.Field()
