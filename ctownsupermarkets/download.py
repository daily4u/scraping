import urllib
import csv

def downloader(image_url, full_file_name):
    print image_url
    urllib.urlretrieve(image_url,full_file_name)
    # sleep(0.2)

with open('product_U41_196.csv', 'rb') as f:
    reader = csv.reader(f)
    items_list = list(reader)        

for ind, row in enumerate(items_list):
    if ind == 0: continue
    file_name = row[7]
    full_file_name = 'images/'+str(file_name) + '.jpg'
    image_url = row[-1]
    downloader(image_url, full_file_name)

    file_name = row[7] 
    full_file_name = 'images/'+str(file_name) + '_x.jpg'
    image_url = row[19]
    downloader(image_url, full_file_name)