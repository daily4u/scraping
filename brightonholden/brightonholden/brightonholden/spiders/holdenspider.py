# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class HoldenspiderSpider(scrapy.Spider):
    name = 'holdenspider'
    allowed_domains = ['www.brightonholden.com.au']
    start_urls = ['http://www.brightonholden.com.au/VehicleSearchResults?search=new&search=demo']
    # http://bayfordvolkswagen.com.au/stock
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)
    def parse(self, response):
        items = response.xpath('section[@class="vehicleListWrapper"]/article')
        for row in items:
            vehicle_name_contain = row.xpath('div[@class="vehicleName"]/a')
            url = vehicle_name_contain.xpath('@href')
            req = Request(url=url, callback=self.parse_detail, dont_filter=True)
            yield req
            # vin_code = vehicle_name_contain.xpath('@data-vin')
            # condition = vehicle_name_contain.xpath('span[contain(@class,"condition category highlight")]/text()').extract_first()
            # year = vehicle_name_contain.xpath('span[contain(@class,"year")]/text()').extract_first()
            # make = vehicle_name_contain.xpath('span[contain(@class,"make")]/text()').extract_first()
            # model = vehicle_name_contain.xpath('span[contain(@class,"model")]/text()').extract_first()
            # trim  = vehicle_name_contain.xpath('span[contain(@class,"trim")]/text()').extract_first()

        # button[@class="cblt-button loadMore"]
    def parse_detail(self, response):
        item_cond = response.xpath("//span[@itemprop='itemCondition']/text()").extract_first()
        item_release = response.xpath("//span[@itemprop='releaseDate']/text()").extract_first()
        item_manufacturer = response.xpath("//span[@itemprop='manufacturer']/text()").extract_first()
        item_model = response.xpath("//span[@itemprop='model']/text()").extract_first()
        item_trim = response.xpath("//span[@itemprop='trim']/text()").extract_first()