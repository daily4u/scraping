# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class FetchquickPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    
    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.meta['filename']
        dirname = request.meta['dirname']
        image_guid_extension = (request.url.split('.')[-1]).split('?')[0]
        return '%s/%s' % (dirname, image_guid + '.' + image_guid_extension)

    def get_media_requests(self, item, info):
        for ind, image in enumerate(item['image_urls']):
            if (ind==0): continue
            print "--------" + image +  "-----------"
            req = Request(image)
            req.meta['dirname'] =  item['Dirs'][ind]
            req.meta['filename'] =  image.split('=')[-1]
            yield req