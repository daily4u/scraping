# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from wholefoodsmarket.items import DepartItem, GoodItem, ImageItem

import numpy as np
import json, csv

import sys

class WholefoodspiderSpider(scrapy.Spider):
    name = 'wholefoodspider'
    allowed_domains = ['delivery.wholefoodsmarket.com']
    start_urls = ['https://delivery.wholefoodsmarket.com/']
    
    # https://delivery.wholefoodsmarket.com/v3/retailers/3/containers
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_login, dont_filter=True)
    
    def parse_login(self, response):
        print '-------login--------'
        # Get authentication token
        authenticity_token = response.xpath('//meta[@name="csrf-token"]/@content').extract()
        yield scrapy.FormRequest(
            url='https://delivery.wholefoodsmarket.com/accounts/login',
            formdata={
                'user[email]':'rise.henrik@mail.ru',
                'user[password]':'dnflgmlakd888',
                'authenticity_token': authenticity_token
            },
            callback=self.parse
        )
        print authenticity_token
        
    def parse(self, response):
        print ("---------after login---------")
        ########################################################################
        # Get Depart Number And Export to depart.csv
        ########################################################################
        # depart_url = 'https://delivery.wholefoodsmarket.com/v3/retailers/3/containers'
        # depart_req = Request(url=depart_url, callback=self.parse_depart, dont_filter=True)
        # yield depart_req
        
        ########################################################################
        # After Getting Depart Number, Open depart.csv And Get Item Information
        ########################################################################
        depart_file = open("depart.csv", "rb")
        depart_list = csv.reader(depart_file)
        for row in depart_list:
            depart_no = row[1]
            depart_sub_no = row[0]
            depart_title = row[-1]
            depart_sub_title = row[2]

            goods_url = 'https://delivery.wholefoodsmarket.com/v3/retailers/3/module_data/aisle_%s_%s?aisle_id=%s&department_id=%s&source=web&tracking.items_per_row=7&per=100' % (depart_no,depart_sub_no,depart_no,depart_sub_no)
            print goods_url
            goods_req = Request(url=goods_url, callback=self.parse_goods, dont_filter=True)
            goods_req.meta['depart_no'] = depart_no
            goods_req.meta['depart_sub_no'] = depart_sub_no
            goods_req.meta['depart_title'] = depart_title
            goods_req.meta['depart_sub_title'] = depart_sub_title

            yield goods_req
            # return

        #########################################################################
        # After All getting items, open item.csv and download image file
        #########################################################################
        # with open('item.csv', 'rb') as f:
        #     reader = csv.reader(f)
        #     items_list = list(reader)        
        # image_lists = np.array(items_list)
        # image_item = ImageItem()
        # # Current source image url column index of item.csv file is 4
        # image_item['Ids'] = image_lists[:,9]
        # image_item['Dirs'] = image_lists[:,6]
        # image_item['image_urls'] = image_lists[:,8]
        # yield image_item

    ######################Parse depart number#########################
    def parse_depart(self, response):
        print '-------GETTING DEPARTMENT---------'
        depart_containers = json.loads(response.body)['containers']
        for row in depart_containers:
            depart_title = row['title']
            depart_path = row['path']
            depart_no = depart_path.split('/')[-1]
            for col in row['containers']:
                depart_item = DepartItem()
                depart_sub_title = col['title']
                depart_sub_path = col['path']
                depart_sub_no = depart_sub_path.split('/')[-1]
                depart_item['depart_title'] = depart_title
                depart_item['depart_path'] = depart_path
                depart_item['depart_no'] = depart_no
                depart_item['depart_sub_title'] = depart_sub_title
                depart_item['depart_sub_path'] = depart_sub_path
                depart_item['depart_sub_no'] = depart_sub_no
                yield depart_item
    
    ####################Parse goods#############################
    def parse_goods(self, response):
        print '----------Begin Page-----------'
        items = json.loads(response.body)['module_data']['items']
        item_brand = response.meta['depart_title']
        item_brand_no = response.meta['depart_no']
        item_category = response.meta['depart_sub_title']
        item_category_no = response.meta['depart_sub_no']

        for item in items:
            good_item = GoodItem()
            good_item['Brand'] = item_brand
            good_item['Brand_No'] = item_brand_no
            good_item['Category'] = item_category
            good_item['Category_No'] = item_category_no
            good_item['Id'] = item['legacy_id']
            good_item['Name'] = item['name']
            good_item['Size'] = item['size']
            good_item['Unit'] = item['unit']
            good_item['Price'] = item['pricing']['price']
            try:
                source_image_url = item['image']['responsive']['template']
                source_image_default = item['image']['responsive']['defaults']
                source_image_url = source_image_url.replace('{width}',str(source_image_default['width']))
                source_image_url = source_image_url.replace('{fill}', source_image_default['fill'])
                source_image_url = source_image_url.replace('{format}', source_image_default['format'])
            except:
                source_image_url = item['image']['url']
            good_item['SourceImage'] = source_image_url
            good_item['TargetImage'] = 'images/' + str(item['legacy_id']) + '.' + source_image_default['format']
            good_item['TrackingParam'] = item['tracking_params']['item_card_impression_id']
            yield good_item

        print '----------End Page-----------'    
        try:
            pagenation = json.loads(response.body)['module_data']['pagination']
            next_page = pagenation['next_page']
            per_page = pagenation['per_page']

            next_goods_url = 'https://delivery.wholefoodsmarket.com/v3/retailers/3/module_data/aisle_%s_%s?aisle_id=%s&department_id=%s&source=web&tracking.items_per_row=7&page=%s&per=%s' % (item_brand_no,item_category_no,item_brand_no,item_category_no,next_page, per_page)
            next_goods_req = Request(url=next_goods_url, callback=self.parse_goods, dont_filter=True)
            
            next_goods_req.meta['depart_no'] = item_brand_no
            next_goods_req.meta['depart_sub_no'] = item_category_no
            next_goods_req.meta['depart_title'] = item_brand
            next_goods_req.meta['depart_sub_title'] = item_category

            yield next_goods_req
        except:
            return
