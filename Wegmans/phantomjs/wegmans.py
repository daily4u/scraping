# -*- coding: utf-8 -*-

from scrapex import *
import json
import requests
import re
from time import sleep
import urllib

# from selenium import webdriver
parent_url = 'https://www.wegmans.com'
start_url = 'https://www.wegmans.com/products.html'
category_base_url = "https://sp1004f27d.guided.ss-omtrdc.net/?do=prod-search;storeNumber=%s;q1=%s;x1=cat.category;q2=%s;x2=cat.department;sp_c=18;sp_n=1;callback=angular.callbacks._0"                
store_number = 25

s = Scraper(
    use_cache = False,
    retries = 3,
    timeout = 300,
)

class WegmanScraper(object):
    # def __init__(self):
    #     # self.driver = webdriver.PhantomJS()

    def parse(self):
        doc = s.load(start_url)
        subscription_key = re.search("Wegmans\.subscriptionKey \= \"(.*?)\";",s.load_html(start_url), re.M|re.S|re.I).group(1)

        products = doc.q('//ul[@class="child-nav-columns"]/li')
        for idx,row in enumerate(products):
            if (idx<6): continue
            product_name = row.x('a/text()').trim()
            product_url  = row.x('a/@href').trim()
            print product_name + '===================> Processing'

            product_url_name = product_url.split('/')[-1].replace('.html', '')
            ajax_request_url = '%s/_jcr_content.department.%s.json' % (product_url.replace('.html', ''),  product_url_name)
            print ajax_request_url
            try:
                product_child_res = s.load_json(ajax_request_url)
                # print product_child_res

                for col in product_child_res:
                    product_child_name  =  col['name']
                    product_child_url   =  col['linkUrl']
                    product_child_count =  col['count']
                    print "+++" + product_child_name + "===================> Processing"
                    print "+++" + product_child_count + "===================> Processing"
                    category_request_url = category_base_url % (store_number, urllib.quote_plus(product_child_name) , urllib.quote_plus(product_name))
                    headers = {
                        "Accept":"application/json, text/plain, */*",
                        "Content-Type":"application/json",
                        "Ocp-Apim-Subscription-Key":str(subscription_key)
                    }
                    while(True):
                        print "."
                        product_category_res = json.loads(re.search("angular\.callbacks\._0\( (.*) \)", s.load_html(category_request_url) ,re.M|re.S|re.I).group(1))
                        data = []
                        for item in product_category_res['results']:
                            data.append({"Sku":item['sku'],"Quantity":1})
                        params = json.dumps({"LineItems":data,"StoreNumber":str(store_number)})
                        prices = requests.post('https://wegapi.azure-api.net/pricing/carttotal/false?api-version=1.0',data=params, headers=headers).json()
                        price = {}
                        for item in prices['InvalidItems']:
                            sku = item['Sku']
                            price.update({sku:{'Aisle':item['Aisle'], 'Price':item['Price'], 'ExtendedPrice':item['ExtendedPrice'], 'Valid':'F'}})
                        for item in prices['LineItems']:
                            sku = item['Sku']
                            price.update({sku:{'Aisle':item['Aisle'], 'Price':item['Price'], 'ExtendedPrice':item['ExtendedPrice'], 'Valid':'T'}})
                        
                        for ind, item in enumerate(product_category_res['results']):

                            product_item = []
                            product_item.append('AverageOverallRating')
                            product_item.append(item['averageOverallRating'])
                            product_item.append('AverageWeight')
                            product_item.append(item['averageWeight'])
                            product_item.append('Brand')
                            product_item.append(item['brand'])
                            product_item.append('Category')
                            product_item.append(item['category'])
                            product_item.append('Department')
                            product_item.append(item['department'])
                            product_item.append('Name')
                            product_item.append(item['name'])
                            product_item.append('Popular')
                            product_item.append(item['popular'])
                            product_item.append('ProductLine')
                            product_item.append(item['productLine'])
                            product_item.append('Sku')
                            product_item.append(item['sku'])
                            product_item.append('SoldByQuantity')
                            product_item.append(item['soldByQuantity'])
                            product_item.append('SoldByUom')
                            product_item.append(item['soldByUom'])
                            product_item.append('SoldByUomAw')
                            product_item.append(item['soldByUomAw'])
                            product_item.append('Subcategory')
                            product_item.append(item['subcategory'])
                            product_item.append('TotalReviewCount')
                            product_item.append(item['totalReviewCount'])

                            product_item.append('Aisle')
                            product_item.append(price[int(item['sku'])]['Aisle'])
                            product_item.append('ExtendedPrice')
                            product_item.append(price[int(item['sku'])]['ExtendedPrice'])
                            product_item.append('Price')
                            product_item.append(price[int(item['sku'])]['Price'])
                            product_item.append('Valid')
                            product_item.append(price[int(item['sku'])]['Valid'])

                            product_item.append('Details')
                            product_item.append(item['details'])
                            product_item.append('Url')
                            product_item.append(item['url'])
                            product_item.append('ImageUrl')
                            product_item.append(item['imageUrl'])

                            s.save(product_item, 'product.csv')

                        if (product_category_res['pagination']['next'] == ""):
                            break
                        print product_category_res['pagination']['next']
                        category_request_url = 'https://sp1004f27d.guided.ss-omtrdc.net/' + product_category_res['pagination']['next']

                    print "+++" + product_child_name + "===================> OK"
            except:
                category_simple_base_url = 'https://sp1004f27d.guided.ss-omtrdc.net/?do=prod-search;storeNumber=%s;q1=%s;x1=cat.department;sp_c=18;sp_n=1;callback=angular.callbacks._0'
                category_request_url = category_simple_base_url % (store_number , urllib.quote_plus(product_name))
                headers = {
                    "Accept":"application/json, text/plain, */*",
                    "Content-Type":"application/json",
                    "Ocp-Apim-Subscription-Key":str(subscription_key)
                }
                while(True):
                    print "---------Exception Processing-------"
                    product_category_res = json.loads(re.search("angular\.callbacks\._0\( (.*) \)", s.load_html(category_request_url) ,re.M|re.S|re.I).group(1))
                    data = []
                    for item in product_category_res['results']:
                        data.append({"Sku":item['sku'],"Quantity":1})
                    params = json.dumps({"LineItems":data,"StoreNumber":str(store_number)})
                    prices = requests.post('https://wegapi.azure-api.net/pricing/carttotal/false?api-version=1.0',data=params, headers=headers).json()
                    price = {}
                    for item in prices['InvalidItems']:
                        sku = item['Sku']
                        price.update({sku:{'Aisle':item['Aisle'], 'Price':item['Price'], 'ExtendedPrice':item['ExtendedPrice'], 'Valid':'F'}})
                    for item in prices['LineItems']:
                        sku = item['Sku']
                        price.update({sku:{'Aisle':item['Aisle'], 'Price':item['Price'], 'ExtendedPrice':item['ExtendedPrice'], 'Valid':'T'}})
                    
                    for ind, item in enumerate(product_category_res['results']):

                        product_item = []
                        product_item.append('AverageOverallRating')
                        product_item.append(item['averageOverallRating'])
                        product_item.append('AverageWeight')
                        product_item.append(item['averageWeight'])
                        product_item.append('Brand')
                        product_item.append(item['brand'])
                        product_item.append('Category')
                        product_item.append(item['category'])
                        product_item.append('Department')
                        product_item.append(item['department'])
                        product_item.append('Name')
                        product_item.append(item['name'])
                        product_item.append('Popular')
                        product_item.append(item['popular'])
                        product_item.append('ProductLine')
                        product_item.append(item['productLine'])
                        product_item.append('Sku')
                        product_item.append(item['sku'])
                        product_item.append('SoldByQuantity')
                        product_item.append(item['soldByQuantity'])
                        product_item.append('SoldByUom')
                        product_item.append(item['soldByUom'])
                        product_item.append('SoldByUomAw')
                        product_item.append(item['soldByUomAw'])
                        product_item.append('Subcategory')
                        product_item.append(item['subcategory'])
                        product_item.append('TotalReviewCount')
                        product_item.append(item['totalReviewCount'])

                        product_item.append('Aisle')
                        product_item.append(price[int(item['sku'])]['Aisle'])
                        product_item.append('ExtendedPrice')
                        product_item.append(price[int(item['sku'])]['ExtendedPrice'])
                        product_item.append('Price')
                        product_item.append(price[int(item['sku'])]['Price'])
                        product_item.append('Valid')
                        product_item.append(price[int(item['sku'])]['Valid'])

                        product_item.append('Details')
                        product_item.append(item['details'])
                        product_item.append('Url')
                        product_item.append(item['url'])
                        product_item.append('ImageUrl')
                        product_item.append(item['imageUrl'])

                        s.save(product_item, 'product1.csv')

                    if (product_category_res['pagination']['next'] == ""):
                        break
                    print product_category_res['pagination']['next']
                    category_request_url = 'https://sp1004f27d.guided.ss-omtrdc.net/' + product_category_res['pagination']['next']
            print '#################END###################'


if __name__ == '__main__':
    scraper = WegmanScraper()
    scraper.parse()