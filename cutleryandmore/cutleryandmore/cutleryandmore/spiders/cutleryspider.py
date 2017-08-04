# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from time import sleep
from cutleryandmore.items import CutleryandmoreItem


class CutleryspiderSpider(scrapy.Spider):
    name = 'cutleryspider'
    allowed_domains = ['www.cutleryandmore.com']
    start_urls = ['http://www.cutleryandmore.com/kitchen-knives-cutlery-list']
    parent_url = 'http://www.cutleryandmore.com'

    def parse(self, response):
        tr_xpath = response.xpath('//table[@class="product_table"]')
        for ind, row in enumerate(tr_xpath):
            url = row.xpath('.//td[@class="product_name"]/a/@href').extract_first()
            req = Request(url=self.parent_url + url, callback=self.parse_detail, dont_filter=True)
            yield req
    
    def parse_detail(self, response):
        item = CutleryandmoreItem()
        product_id = response.url.split('-')[-1]
        item['product_id'] = product_id
        item_name = response.xpath('//td[@class="PV_ItemName"]/text()').extract_first()
        item['item_name'] = item_name
        item_brand = response.xpath('//td[@class="breadcrumbs"]//a[1]/text()').extract_first()
        item['item_brand'] = item_brand
        item_category = response.xpath('//td[@class="breadcrumbs"]//a[2]/text()').extract_first()
        item['item_category'] = item_category
        item_subcategory = response.xpath('//td[@class="breadcrumbs"]//a[3]/text()').extract_first()
        item['item_subcategory'] = item_subcategory
        item_img_url = response.xpath('//img[@id="PV_Image"]/@src').extract_first()
        item['item_img_url'] = item_img_url
        # item_description = ' '.join(response.xpath('//td[@class="PV_Description"]//text()').extract()).strip()
        # item['item_description'] = item_description
        item_id = response.xpath('//td[@class="PV_Description"]//text()').extract()[-1].replace("Item:","").strip()
        item['item_id'] = item_id
        item_contains = ','.join(response.xpath('//table[@class="PV_SetContentsTable"]//td[@class="PV_SetContents"]//text()').extract()).strip()
        item['item_contains'] = item_contains
        price_details = response.xpath('//tr[contains(@id,"TopRow")]')
        
        for row in price_details:
            item_bug = row.xpath('./td[@class="PV_TableNewBug"]//text()').extract_first()
            item['item_bug'] = item_bug
            item_type = row.xpath('./td[@class="PV_TableName"]//text()').extract_first()
            item['item_type'] = item_type
            item_old_price = row.xpath('./td[@class="PV_TableMSRP"]//text()').extract_first()
            item['item_old_price'] = item_old_price
            item_new_price = row.xpath('./td[@class="PV_TablePrice"]//text()').extract_first()
            item['item_new_price'] = item_new_price
            print "------------------------------------"
            yield item
            # return

