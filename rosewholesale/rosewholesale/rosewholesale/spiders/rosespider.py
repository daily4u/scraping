# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import Request


class RosespiderSpider(scrapy.Spider):
    name = 'rosespider'
    allowed_domains = ['www.rosewholesale.com']
    start_urls = ['http://www.rosewholesale.com/']
    
    first_url = 'https://www.rosewholesale.com/cheapest/striped-open-back-cover-ups-1931460.html'
    
    def start_requests(self):
        yield scrapy.Request(self.first_url, callback=self.parse,  dont_filter=True)
# Handle	Title	Body (HTML)	
# Vendor	
# Type	
# Tags	
# Published	
# Option1 Name	
# Option1 Value	
# Option2 Name	Option2 Value	Option3 Name	Option3 Value	Variant SKU	Variant Grams	Variant Inventory Tracker	Variant Inventory Qty	Variant Inventory Policy	Variant Fulfillment Service	Variant Price	Variant Compare At Price	Variant Requires Shipping	Variant Taxable	Variant Barcode	Image Src	Image Alt Text	Variant Image

    def parse(self, response):
        logging.debug("++++++++++++++++++++++")
        url = response.url
        categories = '/'.join(response.xpath('//div[@id="mainWrap"]/div[contains(@class,"path")]/a/text()').extract()).strip()
        logging.debug(categories)
        title = response.xpath('//header[@class="goods_header"]/div/h1/text()').extract_first()
        logging.debug(title)

        