# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlanshopriteItem(scrapy.Item):
    # define the fields for your item here like:
    Store_ID = scrapy.Field()
    Store_Address1 = scrapy.Field()
    Store_Address2 = scrapy.Field()
    Store_Phone = scrapy.Field()
    Store_Fax = scrapy.Field()
    Store_Driving_Directions = scrapy.Field()
    Store_View_Circular = scrapy.Field()
    Store_Order_Ready = scrapy.Field()
    Store_Online_Shopping = scrapy.Field()
    Store_OGS_Delivery_Info = scrapy.Field()
    Store_Latitude = scrapy.Field()
    Store_Longitude = scrapy.Field()
    
    Service_ID = scrapy.Field()
    Service_Name = scrapy.Field()
    Service_URL = scrapy.Field()
    Service_Hours = scrapy.Field()
    Service_Services = scrapy.Field()

    Pharmacy_Name = scrapy.Field()
    Pharmacy_Address1 = scrapy.Field()
    Pharmacy_Address2 = scrapy.Field()
    Pharmacy_Phone = scrapy.Field()
    Pharmacy_Fax = scrapy.Field()
    Pharmacy_Pharmacist = scrapy.Field()
    Pharmacy_Hours = scrapy.Field()

