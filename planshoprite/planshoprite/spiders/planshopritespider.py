# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from planshoprite.items import PlanshopriteItem

class PlanshopritespiderSpider(scrapy.Spider):
    name = 'planshopritespider'
    allowed_domains = ['plan.shoprite.com']
    # start_urls = ['http://plan.shoprite.com/']
    parent_url = 'http://plan.shoprite.com/Stores?f=Ogs&mobile=0'
    base_location_url = 'http://plan.shoprite.com/Stores/Get?Country=United States&Region=%s&StoreType=Ogs&StoresPageSize=undefined&IsShortList=undefined'
    base_zipcode_url = 'http://plan.shoprite.com/Stores/Get?PostalCode=%s&Radius=20&Units=Miles&StoreType=Ogs&StoresPageSize=undefined&IsShortList=undefined'
    base_url = 'http://plan.shoprite.com/Stores/Get?PostalCode=07675'

    def __init__(self, location=None, zipcode=None, *args, **kwargs):
        super(PlanshopritespiderSpider, self).__init__(*args, **kwargs)
        if (location == None) and (zipcode == None):
           self.base_url =  self.base_url
        elif (location != None):
            self.base_url = self.base_location_url % location
        elif (zipcode != None):
            self.base_url = self.base_zipcode_url % zipcode

    def start_requests(self):
        print '---------_START_-----------'
        yield Request(url=self.parent_url, callback=self.parse, dont_filter=True)        
    
    def parse(self, response):
        print '---------_PARSE_-----------'
        req = Request(url=self.base_url, callback=self.parse_item, dont_filter=True)
        yield req
    
    def parse_item(self, response):
        print '-------_PARSE_ITEM_--------'
        print response.text
        storelists = response.xpath('//div[@id="StoreList"]//div[@class="store-item store-item-none"]')
        for storelist in storelists:
            item = PlanshopriteItem()
            store_id = ''.join(storelist.xpath('.//@data-id').extract()).strip()
            store_lat = ''.join(storelist.xpath('.//@data-lat').extract()).strip()
            store_lng = ''.join(storelist.xpath('.//@data-lng').extract()).strip()
            # store_service_url = storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StorePharmacy-780"]/div[@class="storelist-info-text"]/h4/text()').extract()
            # print store_service_url
            # return
            store_detail_id = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/a[1]/@data-clientanalyticslabel').extract()).strip()
            store_detail_name = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/h4//text()').extract()).strip()
            store_detail_address1 = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/p[1]//text()').extract()).strip()
            store_detail_address2 = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/p[2]//text()').extract()).strip()

            store_detail_map = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/p[@class="storelist-phone-directions"]/a/@href').extract()).strip()
            store_detail_phone = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/p[@class="storelist-phone-directions"]/span[1]/text()').extract()).strip().replace('Phone: ','')
            store_detail_fax = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/p[@class="storelist-fax"]//text()').extract()).strip().replace('Fax: ', '')

            store_detail_view_circular = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/a[1]/@data-outboundhref').extract()).strip()
            store_detail_order_ready = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/a[2]/@data-outboundhref').extract()).strip()
            store_detail_online_shopping = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/a[3]/@data-outboundhref').extract()).strip()
            store_detail_ogs_delivery_info = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreDetails-'+store_id+'"]/div[@class="storelist-info-text"]/a[4]/@href').extract()).strip()
            
            store_service_url = ''.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreServices-'+store_id+'"]/div[@id="StoreServicesContainer"]/h4[1]/a/@href').extract()).strip()
            store_service_name = ' '.join(' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreServices-'+store_id+'"]/div[@id="StoreServicesContainer"]/h4[1]//text()').extract()).strip().split())
            store_service_hours = ' '.join(' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreServices-'+store_id+'"]/div[@id="StoreServicesContainer"]/span/text()').extract()).strip().split())
            store_service_services = ' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StoreServices-'+store_id+'"]/div[@id="StoreServicesContainer"]/ul/li/text()').extract()).strip().replace(' ', ',')
            
            
            store_pharmacy_title = ' '.join(' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StorePharmacy-'+store_id+'"]/div[@class="storelist-info-text"]/h4/text()').extract()).strip().split())
            store_pharmacy_address1 = ' '.join(' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StorePharmacy-'+store_id+'"]/div[@class="storelist-info-text"]/p[1]/text()').extract()).strip().split())
            store_pharmacy_address2 = ' '.join(' '.join(storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StorePharmacy-'+store_id+'"]/div[@class="storelist-info-text"]/p[2]/text()').extract()).strip().split())
            
            store_pharmacy_lists = storelist.xpath('.//div[@class="storelist-inner-tab"]/div[@id="StorePharmacy-'+store_id+'"]/div[@class="storelist-info-text"]/p')
            
            store_pharmacy_phone=''
            store_pharmacy_fax=''
            store_pharmacy_phar=''
            store_pharmacy_hours =''
            
            for store_pharmacy in store_pharmacy_lists:
                keytext = ' '.join(store_pharmacy.xpath('.//text()').extract()).strip()
                if "Phone: " in keytext:
                    store_pharmacy_phone = ' '.join(keytext.split()).replace("Phone: ", "")
                elif "Fax: " in keytext:
                    store_pharmacy_fax = ' '.join(keytext.split()).replace("Fax: ", "")
                elif "Pharmacist: " in keytext:
                    store_pharmacy_phar = ' '.join(keytext.split()).replace("Pharmacist: ", "")
                elif "Hours: " in keytext:
                    store_pharmacy_hours = ' '.join(keytext.split()).replace("Hours: ", "")

            item['Store_ID'] = store_id
            item['Store_Address1'] = store_detail_address1
            item['Store_Address2'] = store_detail_address2
            item['Store_Phone'] = store_detail_phone
            item['Store_Fax'] = store_detail_fax

            item['Store_Driving_Directions'] = store_detail_map
            item['Store_View_Circular'] = store_detail_view_circular
            item['Store_Order_Ready'] = store_detail_order_ready
            item['Store_Online_Shopping'] = store_detail_online_shopping
            item['Store_OGS_Delivery_Info'] = store_detail_ogs_delivery_info
            item['Store_Latitude'] = store_lat
            item['Store_Longitude'] = store_lng
            
            item['Service_ID'] = store_detail_id
            item['Service_Name'] = store_service_name
            item['Service_URL'] = store_service_url
            item['Service_Hours'] = store_service_hours
            item['Service_Services'] = store_service_services

            item['Pharmacy_Name'] = store_pharmacy_title
            item['Pharmacy_Address1'] = store_pharmacy_address1
            item['Pharmacy_Address2'] = store_pharmacy_address2
            item['Pharmacy_Phone'] = store_pharmacy_phone
            item['Pharmacy_Fax'] = store_pharmacy_fax
            item['Pharmacy_Pharmacist'] = store_pharmacy_phar
            item['Pharmacy_Hours'] = store_pharmacy_hours
            yield item
