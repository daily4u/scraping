# encoding=utf8
import sys
# from grab import Grab
# import logging
from grab.spider import Spider, Task

import json
import re
import urllib
import csv

reload(sys)
sys.setdefaultencoding('utf8')

class InstagramSpider(Spider):

    initial_urls = ['http://qpublic9.qpublic.net/hi_hawaii_display.php?KEY=730070680000&show_history=1&',]
    # initial_urls = ['https://www.instagram.com/beautifuldestinations/',]
    def prepare(self):
        print "Prepare part"
        self.fieldnames1 = ["ID","Owner Name","Mailing Address","Location Address","Property Class","Neighborhood Code","Legal Information","Today's Date","Parcel Number","Project Name","Parcel Map","Land Area (acres)","Land Area (approximate sq ft)"]
        self.fieldnames2 = ["ID","Year","Property Class","Market Land Value","Dedicated Use Value","Land Exemption","Net Taxable Land Value","Market Building Value","Assessed Building Value","Building Exemption","Net Taxable Building Value","Total Taxable Value"]
        self.fieldnames3 = [""]
        self.fieldnames4 = ["ID","Property Class","Square Footage","Acreage","Agricultural Usage"]
        self.fieldnames5 = ["ID","Building Number","Year Built","Effective Year Built","Square Feet","Total Room Count","Full Baths","Half Baths","Bedrooms","Framing","Exterior Wall","Roof Material","Heating/AC","Fireplace","Grade","Sketch"]
        self.fieldnames6 = ["ID","Description","Quantity","Year Built","Area","Gross Building Value"]
        self.fieldnames7 = ["ID","Date","Permit Number","Reason","Permit Amount"]
        self.fieldnames8 = ["ID","Permit Date","Permit Type","Permit Number","Permit Reason","Permit Description","Estimated Cost","Inspection Date","Inspection Status"]
        self.fieldnames9 = ["ID","Sale Date","Sale Amount","Instrument #","Instrument Type","Instrument Description","Date of Recording","Land Court Document Number","Cert #","Book/Page","Conveyance Tax","Document Type"]
        self.fieldnames10 = ["ID","Tax Period","Description","Original Due Date","Taxes Assessment","Tax Credits","Net Tax","Penalty","Interest","Other","Amount Due"]
        self.fieldnames11 = ["ID","Year","Tax","Payments and Credits","Penalty","Interest","Other","Amount Due"]
        self.fieldnames12 = ["ID","Building Number","Year Built","Effective Year Built","Square Feet","Total Room Count","Full Baths","Half Baths","Bedrooms","Framing","Exterior Wall","Roof Material","Heating/AC","Fireplace","Grade","Sketch"]
        
        self.result_file1 = csv.DictWriter(open('Owner and Parcel Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames1)
        self.result_file2 = csv.DictWriter(open('Assessment Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames2)
        self.result_file3 = csv.DictWriter(open('Appeal Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames3)
        self.result_file4 = csv.DictWriter(open('Land Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames4)
        self.result_file5 = csv.DictWriter(open('Residential Improvement Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames5)
        self.result_file6 = csv.DictWriter(open('Other Building and Yard Improvements.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames6)
        self.result_file7 = csv.DictWriter(open('Permit Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames7)
        self.result_file8 = csv.DictWriter(open('Dept of Public Works Bldg Division Permit and Inspections Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames8)
        self.result_file9 = csv.DictWriter(open('Sales Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames9)
        self.result_file10 = csv.DictWriter(open('Current Tax Bill Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames10)
        self.result_file11 = csv.DictWriter(open('Historical Tax Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames11)
        self.result_file12 = csv.DictWriter(open('Residential Improvement Information.csv', 'wb'), delimiter=',',fieldnames=self.fieldnames12)
        
        self.result_file1.writeheader()
        self.result_file2.writeheader()
        self.result_file3.writeheader()
        self.result_file4.writeheader()
        self.result_file5.writeheader()
        self.result_file6.writeheader()
        self.result_file7.writeheader()
        self.result_file8.writeheader()
        self.result_file9.writeheader()
        self.result_file10.writeheader()
        self.result_file11.writeheader()
        self.result_file12.writeheader()


    def task_initial(self, grab, task):
        print "Initial Part"
        table1 = grab.doc.select('//table[@class="table_class"]')[2]
        item = {"ID":"730070680000"}
        for row in table1.select('tr/td[@class="owner_header"]'):
            if row.text().strip() == "Parcel Map":
                item[row.text().strip()] = row.select('following-sibling::td[1]/a[1]/@href').text().strip() + "," + row.select('following-sibling::td[1]/a[2]/@href').text().strip()
            else:
                item[row.text().strip()] = row.select('following-sibling::td[1]//text()').text().strip()
        self.result_file1.writerow(item)
        print item 
        table2 = grab.doc.select('//table[@class="table_class"]')[3]
        for ind, row in enumerate(table2.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames2[idx+1]] = col.text().replace('$','').replace(',','').strip()
            print item
            self.result_file2.writerow(item)
        table4 = grab.doc.select('//table[@class="table_class"]')[5]
        for ind, row in enumerate(table4.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames4[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file4.writerow(item)

        table5 = grab.doc.select('//table[@class="table_class"]')[6]
        for ind, row in enumerate(table5.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames5[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file5.writerow(item)

        table6 = grab.doc.select('//table[@class="table_class"]')[7]
        for ind, row in enumerate(table6.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames6[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file6.writerow(item)

        table7 = grab.doc.select('//table[@class="table_class"]')[8]
        for ind, row in enumerate(table7.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames7[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file7.writerow(item)

        table8 = grab.doc.select('//table[@class="table_class"]')[9]
        for ind, row in enumerate(table8.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames8[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file8.writerow(item)

        table9 = grab.doc.select('//table[@class="table_class"]')[10]
        for ind, row in enumerate(table9.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames9[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file9.writerow(item)

        table10 = grab.doc.select('//table[@class="table_class"]')[11]
        for ind, row in enumerate(table10.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames10[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file10.writerow(item)

        table11 = grab.doc.select('//table[@class="table_class"]')[12]
        for ind, row in enumerate(table11.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                item[self.fieldnames11[idx+1]] = col.text().replace('$','').replace(',','').strip()
            print item
            self.result_file11.writerow(item)

        table12 = grab.doc.select('//table[@class="table_class"]')[6]
        for ind, row in enumerate(table12.select('tr')):
            item = {"ID":"730070680000"}
            if ind<2: continue
            for idx, col in enumerate(row.select('td[@class="sales_value"]')):
                if idx == len(row.select('td[@class="sales_value"]'))-1:
                    item[self.fieldnames12[idx+1]] = col.select('a/@href').text().strip()
                else:
                    item[self.fieldnames12[idx+1]] = col.text().replace(',','').strip()
            print item
            self.result_file12.writerow(item)
if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    bot = InstagramSpider(transport='threaded')
    bot.run()
