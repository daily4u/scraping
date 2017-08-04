# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LkdsItem(scrapy.Item):
    # define the fields for your item here like:
    slug = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    betaId = scrapy.Field()
    street1 = scrapy.Field()
    street2 = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    postalCode = scrapy.Field()
    size = scrapy.Field()
    industry = scrapy.Field()
    description = scrapy.Field()
    company_type = scrapy.Field()
    employees = scrapy.Field()
    specialties = scrapy.Field()
    logo_url = scrapy.Field()
    showcase = scrapy.Field()
    founded_year = scrapy.Field()
    website = scrapy.Field()
    related_orgs = scrapy.Field()
    affiliated_orgs = scrapy.Field()



