from scrapex import *
import csv
import os
import os.path

s = Scraper(
    use_cache=False,
    retries = 3,
    timeout = 300
)

class Meeyshop(object):
    start_url = 'https://www.meetyshop.com/'
    
    def parse(self):
        with open('item.csv','rb') as item_file:
            pno = csv.reader(item_file)
            pno_list = list(item_reader)
            
        for row in pno_list:
            each_url = 'https://www.meetyshop.com/shop?searchText=' + row
            doc = s.load(each_url)
            image_url = 'https://www.meetyshop.com' + doc.x('//div[@class="product"]/div[@class="image"]/a/img/@src).trim()

            extension = image_url.split('.')[-1]
            dir ='image'

            try:
                os.stat(dir)
            except:
                os.mkdir(dir)
            filename = response.meta['id'] + '.' + extension
            with open(dir + "/" + filename, 'wb') as f:
                f.write(response.body)
            
            
            
    
if __name__ == '__main__':
    scraper = Meeyshop()
    scraper.parse()