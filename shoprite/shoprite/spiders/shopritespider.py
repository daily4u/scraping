# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from shoprite.items import ShopriteItem, ProductItem
import re
import json, csv
import time
import sys
import requests
import os
import os.path
import base64

class ShopritespiderSpider(scrapy.Spider):
    name = 'shopritespider'
    allowed_domains = ['shop.shoprite.com']
    # start_urls = ['https://shop.shoprite.com/store/4487590#/']
    parent_url = 'https://shop.shoprite.com/store/4487590#/'
    
    def start_requests(self):
        print "---------------1-----------"
        req = Request(url=self.parent_url, callback=self.parse, dont_filter=True)
        yield req
    
    def parse(self, response):
        print "----------------2------------"
        configuration = re.search("var configuration = ([^;]+);", response.text, re.M|re.S).group(1)
        configuration = json.loads(configuration)
        entry_url = configuration['EntryUrl']
        user_id = configuration['CurrentUser']['UserId']
        token = configuration['Token']
        headers = {
            'Accept':'application/vnd.mywebgrocer.shop-entry+json',
            'Authorization':token,
            'X-Requested-With':'XMLHttpRequest'
        }

        # ajax_req = self.set_proxies(url=entry_url, callback=self.parse_entry, headers=headers)
        ajax_req = Request(url=entry_url, callback=self.parse_entry, dont_filter=True, headers=headers)
        ajax_req.meta['user_id'] = user_id
        ajax_req.meta['token'] = token
        yield ajax_req

    def parse_entry(self, response):
        print "-------------3---------------"
        queries = json.loads(response.text)
        categories_url = queries['Links'][10]['Uri']
        special_url = queries['Links'][18]['Uri']

        headers = response.request.headers
        user_id = response.meta['user_id']
        token = response.meta['token']
        
        print categories_url
        print special_url
        print headers

        # product id parse
        # categories_req = Request(url=categories_url, callback=self.parse_categories, dont_filter=False, headers=headers)
        # yield categories_req    

        # special_req = Request(url=special_url, callback=self.parse_categories, dont_filter=False, headers=headers)
        # yield special_req    

        # parse sku
        myfile = open("product.csv", "rb")
        idlist = csv.reader(myfile)
        # print len(idlist)
        print "-------------------------Begin--------------------------------"
        for ind, row in enumerate(idlist):
            pid = row[0]
            pname = row[1]
            skip = 0
            take = 20
            userid = user_id
            sku_url = 'https://shop.shoprite.com/api/product/v5/products/category/'+str(pid)+'/store/4487590' + "?skip="+str(skip)+"&take="+str(take)+"&userId="+str(userid)
            # product_req = self.set_proxies(url=sku_url, callback=self.parse_product, headers=headers)
            product_req = Request(url=sku_url, callback=self.parse_product, dont_filter=True, headers=headers)
            
            product_req.meta['user_id'] = user_id
            product_req.meta['token'] = token
            yield product_req            
            


    def parse_categories(self, response):
        headers = response.request.headers        
        print ("----------------------------------------------------------------")
        json_data = json.loads(response.text)

        for json_dat in json_data:
            Id =  json_dat['Id']
            Name = json_dat['Name']
            links = json_dat['Links']
            if len(links) == 1:
                item = ShopriteItem()
                item['Id'] = str(Id)
                item['Name'] = Name
                yield item
            elif len(links) == 2:
                subUri = links[0]['Uri']
                # sub_req = self.set_proxies(url=subUri, callback=self.parse_categories,  headers=headers)
                sub_req = Request(url=subUri, callback=self.parse_categories, dont_filter=True, headers=headers)
                yield sub_req

    def parse_product(self, response):
        print("-----------------Product------------------")
        headers = response.request.headers
        product_list = json.loads(response.text)
        pages = product_list['Pages']
        total_quantity = product_list['TotalQuantity']
        item_count = product_list['ItemCount']
        # if (len(pages) == 1):
        product_items = product_list['Items']
        for product_item in product_items:
            item = ProductItem()

            item['Sku'] = product_item['Sku']
            item['Id'] = product_item['Id']
            item['Name'] = product_item['Name']
            item['ItemKey'] = product_item['ItemKey']
            item['Description'] = product_item['Description']
            item['Brand'] = product_item['Brand']
            item['Category'] = product_item['Category']
            item['RegularPrice'] = product_item['RegularPrice']
            item['CurrentPrice'] = product_item['CurrentPrice']
            item['CurrentUnitPrice'] = product_item['CurrentUnitPrice']
            try:
                item['SalesValid'] = product_item['Sale']['DateText']
                item['SalesMinQty'] = product_item['Sale']['LimitText']
                item['SalesDesc1'] = product_item['Sale']['Description1']
                item['SalesDesc2'] = product_item['Sale']['Description1']
            except:
                item['SalesValid'] = ''
                item['SalesMinQty'] = ''
                item['SalesDesc1'] = ''
                item['SalesDesc2'] = ''
                
            labels = ''
            try:
                for desc in product_item['Labels']:
                    labels = labels + desc['Title'] + "\n" + desc['Description'] + "\n"
            except:
                pass

            item['Labels'] = labels
            image_url = product_item['ImageLinks'][1]['Uri'].replace('http:', 'https:')
            # item['Images'] = 'image/%s.%s' % ( product_item['Id'], image_url.split('.')[-1])
            item['Images'] = product_item['ImageLinks'][1]['Uri'].replace('http:', 'https:')

            # print product_item['Links'][2]['Uri']
            # token =  response.meta['token']
            # requests_headers = {
            #         'Accept':'application/vnd.mywebgrocer.shop-entry+json',
            #         'Authorization':token,
            #         'X-Requested-With':'XMLHttpRequest'
            #     }
            # nut_res = requests.get(product_item['Links'][2]['Uri'], headers=requests_headers).json()
            # item['Nutritions'] = nut_res

            # nut_req = self.set_proxies(product_item['Links'][2]['Uri'], callback=self.download_html, headers=headers)
            nut_req = Request(product_item['Links'][2]['Uri'], callback=self.download_html,dont_filter=True, headers=headers)
            nut_req.meta['id'] = product_item['Id']
            yield nut_req

            item['Nutritions'] = 'html/%s.html' % product_item['Id']
            yield item

            # download_req = self.set_proxies(url=image_url, callback=self.download_image)
            # download_req = Request(url=image_url, callback=self.download_image, dont_filter=True)
            # download_req.meta['id'] = product_item['Id']
            # yield download_req

        try:
            try:
                next_url = product_list['PageLinks'][4]['Uri']
            except:
                rel = product_list['PageLinks'][3]['Rel']
                if (rel=='next'):
                    next_url = product_list['PageLinks'][3]['Uri']
            print "---------------------------- Next Page ---------------------------------------"
            print next_url
            # req = self.set_proxies(url=next_url, callback=self.parse_product,  headers=headers)
            req = Request(url=next_url, callback=self.parse_product, dont_filter=True, headers=headers)
            yield req
        except:
            print "---------------------------- End Page -----------------------------------------"
            return

    def download_html(self, response):
        print '----------------------HTML BEGIN-----------------------------------'
        body_text = json.loads(response.body)
        # print body_text
        if body_text == None:
            return
        html_text = '<html><body>%s</body></html>' % body_text

        extension = response.url.split('.')[-1]

        dir ='html'
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)
        filename = response.meta['id'] + '.html'
        with open(dir + "/" + filename, 'wb') as f:
            f.write(html_text)
        print '----------------------HTML END--------------------------------------'

    def download_image(self, response):
        print '---------------------------IMAGE BEGIN--------------------------------------'
        extension = response.url.split('.')[-1]

        dir ='image'
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)
        filename = response.meta['id'] + '.' + extension
        with open(dir + "/" + filename, 'wb') as f:
            f.write(response.body)

        print '---------------------------IMAGE END--------------------------------------'

