# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from brewersassociation.items import BrewersassociationItem
class BrewerspiderSpider(scrapy.Spider):
    name = 'brewerspider'
    allowed_domains = ['www.brewersassociation.org']
    start_urls = ['https://www.brewersassociation.org/directories/breweries/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)
    
    def parse(self, response):
        formdata ={
            'action':'get_breweries',
            '_id':'Canada',
            'search_by':'country'
        }
        yield FormRequest(
            url='https://www.brewersassociation.org/wp-admin/admin-ajax.php',
            formdata=formdata,
            callback=self.parse_form
        )
    def parse_form(self, response):
        # print response.body
        brewery_lists = response.xpath("//div[@class='brewery']/ul[@class='vcard simple']")
        # print brewery_lists
        for row in brewery_lists:
            name        = row.xpath("li[@class='name']/text()").extract_first()
            address     = row.xpath("li[@class='address']/text()").extract_first()
            country     = row.xpath("li[3]/text()").extract_first()
            try:
                telephone = row.xpath("li[@class='telephone']/text()").extract_first().replace("Phone: ","")
            except:
                telephone = ''
            url         = row.xpath("li[@class='url']/a/@href").extract_first()
            item = BrewersassociationItem()
            item['name'] = name
            item['address'] = address
            item['country'] = country
            item['telephone'] = telephone
            item['url'] = url
            yield item
