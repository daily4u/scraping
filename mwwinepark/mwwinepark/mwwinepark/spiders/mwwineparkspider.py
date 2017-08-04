# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from mwwinepark.items import MwwineparkItem

class MwwineparkspiderSpider(scrapy.Spider):
    name = 'mwwineparkspider'
    allowed_domains = ['www.mwwinepark.com']
    start_urls = ['https://www.mwwinepark.com/search/result_size/96']
    parent_url = 'https://www.mwwinepark.com'
    def start_requests(self):
        yield Request(url=self.start_urls[0],callback=self.parse, dont_filter=True)
    def parse(self, response):
        items_detail_url = response.xpath("//div[@id='product-list']/div[contains(@class,'items')]")
        for items_url in items_detail_url:
            item_detail_url = items_url.xpath(".//a[@class='product-link']/@href").extract_first()
            item_detail_req  = Request(url=self.parent_url + item_detail_url, callback=self.parse_detail, dont_filter=True)
            yield item_detail_req
            
        
        curr_url = response.url
        next_url = self.parent_url + response.xpath("//ul[@class='pagination pull-right']/li[last()]/a/@href").extract_first()
        print next_url
        if (next_url != curr_url):
            next_req = Request(url=next_url,callback=self.parse, dont_filter=True)
            yield next_req
    
    def parse_detail(self, response):
        item_name     =  response.xpath("//div[@id='product-detail']/h1[@class='product-name']/text()").extract_first()
        item_id       =  response.xpath("//div[@id='product-detail']/h1[@class='product-name']/@data-itemid").extract_first()   
        product_id    =  response.xpath("//div[@id='product-detail']/h1[@class='product-name']/@data-product-id").extract_first()   
        brand_id      =  response.xpath("//div[@id='product-detail']/h1[@class='product-name']/@data-brandid").extract_first()   
        sku           =  response.xpath("//div[@id='product-detail']/h1[@class='product-name']/@data-sku").extract_first()   
        description   =  response.xpath("//div[@id='product-detail']//div[@class='product-description']/text()").extract_first()   
        item_category = ''
        item_variental = ''
        item_country = ''
        item_region = ''
        brand = ''
        alcohol = ''
        appellation = ''
        for row in response.xpath("//div[@id='product-detail']//table[@class='table']/tr"):
            label = row.xpath("td[1]//text()").extract_first().strip()
            print label
            if label=="Category":
                item_category =  row.xpath("td[2]//text()").extract_first()   
            elif (label=="Varietal" or label=="Varietals"):
                item_variental =  ','.join(row.xpath("td[2]//ul/li/a/text()").extract())
                print "-----------"
            elif label=="Country":
                item_country =  row.xpath("td[2]//text()").extract_first()   
            elif label=="Region":
                item_region =  row.xpath("td[2]//text()").extract_first()   
            elif label=="Brand":
                brand =  row.xpath("td[2]//text()").extract_first()   
            elif label=="Alcohol/vol":
                alcohol =  row.xpath("td[2]//text()").extract_first()   
            elif label=="Appellation":
                appellation =  row.xpath("td[2]//text()").extract_first()   
            # item_category =  response.xpath("//div[@id='product-detail']//table[@class='table']/tr[1]/td[2]//text()").extract_first()   
            # item_variental=  response.xpath("//div[@id='product-detail']//table[@class='table']/tr[2]/td[2]//text()").extract_first()      
            # item_country  =  response.xpath("//div[@id='product-detail']//table[@class='table']/tr[3]/td[2]//text()").extract_first()      
            # item_region   =  response.xpath("//div[@id='product-detail']//table[@class='table']/tr[4]/td[2]//text()").extract_first()      
            # brand         =  response.xpath("//div[@id='product-detail']//table[@class='table']/tr[5]/td[2]//text()").extract_first()   
        
        price         =  response.xpath("//div[@id='product-detail']//div[@class='prices']/div[@class='price currency']/text()").extract_first()      
        disc_price    =  response.xpath("//div[@id='product-detail']//div[@class='prices']/span[@class='case-discount-price']/text()").extract_first()      
        unit          =  response.xpath("//div[@id='product-detail']//p[contains(@class,'size-container')]/text()").extract_first()      
        image         =  'https:'+response.xpath("//div[@id='product-detail']//div[@class='product-image']/img/@data-src").extract_first()
        good_item = MwwineparkItem()
        good_item['item_name']       =  item_name
        good_item['item_id']         =  item_id
        good_item['product_id']      =  product_id
        good_item['brand_id']        =  brand_id
        good_item['sku']             =  sku
        good_item['item_category']   =  item_category
        good_item['item_variental']  =  item_variental
        good_item['item_country']    =  item_country
        good_item['item_region']     =  item_region
        good_item['brand']           =  brand
        good_item['price']           =  price
        good_item['disc_price']      =  disc_price
        good_item['unit']            =  unit
        good_item['image']           =  image
        good_item['alcohol']         =  alcohol
        good_item['appellation']     =  appellation
        good_item['description']     =  description
        yield good_item