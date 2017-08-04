from scrapex import *
import re
import logging


s = Scraper()
def main():
    item = []
    first_url = 'https://www.rosewholesale.com/cheapest/plaid-trim-wool-blend-coat-1668763.html'
    res = s.load(first_url)
    _handle = first_url.split('/')[-1].replace('.html','')
    _title  = res.x('//header[@class="goods_header"]/div/h1/text()').split(' - ')[0].strip()
    _body   = res.node('//div[@class="g_description"]').html()
    _vendor = "rosewholesale"
    categories = res.q('//div[@id="mainWrap"]/div[contains(@class,"path")]/a')
    _type   = categories[2].x('text()').trim()
    _tags   = res.x('//meta[@name="keyword"]/@content').trim()
    _published = True
    _grams = re.findall('(\d+.\d+)kg',_body)[0]

    print _grams
    price = res.x('//i[contains(@class,"marketPrice")]/span[@id="unit_price2"]/text()').trim()
    old_price = res.x('//i[contains(@class,"costPrice")]/strong[@class="my_shop_price"]/text()').trim()
    cut_price = res.x('//i[contains(@class,"cutPrice")]/span/text()').trim()
    cut_time = res.q('//div[contains(@class,"cutTime")]/span//text()').join(' ').trim()
    colors = [str(row.x('@title')) for row in res.q('//ul[@id="js_property_color"]/li[contains(@class,"item")]/a')]
    # sizes = res.q('//ul[@id="js_property_size"]/li[@class="item"]/a/@title').join().trim()
    sizes = [str(row.x('text()')) for row in res.q('//ul[@id="js_property_size"]/li[contains(@class,"item")]/a')]
    qty   = res.q('//li[contains(@class,"pr")]/input/@value').join().trim()
    desciption = res.q('//div[@classimage_small_urls="xxkkk2"]//text()').join('\n').replace('Product Description:').trim()
    image_big_url = res.x('//div[@id="js_jqzoom"]/img[@class="myImgs"]/@src').trim()
    image_small_urls = [row.x('@src') for row in res.q('//ul[@class="slider"]/li[contains(@class,"thumbnail_list")]/a/img')]
    _sku = res.x('//p[@class="sku"]/span/text()').trim()
    
    _total = max([len(colors), len(sizes), len(image_small_urls)])
    print _total
    # logging.debug(price)
    # logging.debug(old_price)
    # logging.debug(cut_price)
    # logging.debug(cut_time)
    # logging.debug(colors)
    # logging.debug(sizes)
    # logging.debug(qty)
    # logging.debug(desciption)
    # logging.debug(image_big_url)
    # logging.debug(image_small_url)
    # logging.debug(sku)
    for idx in range(0, _total):
        item = []
        item.append("Handle")
        item.append(_handle)
        item.append("Title")
        if idx==0: item.append(_title) 
        else: item.append("")
        item.append("Body(HTML)")
        if idx==0: item.append(_body) 
        else: item.append("")
        item.append("Vendor")
        if idx==0: item.append(_vendor) 
        else: item.append("")
        item.append("Type")
        if idx==0: item.append(_type) 
        else: item.append("")
        item.append("Tags")
        if idx==0: item.append(_tags) 
        else: item.append("")
        item.append("Published")
        if idx==0: item.append(_published) 
        else: item.append("")
        item.append("Variant SKU")
        if idx==0: item.append(_sku) 
        else: item.append("")
        item.append("Variant Grams")
        if idx==0: item.append(_grams) 
        else: item.append("")
        item.append("Variant Inventory Qty")
        if idx==0: item.append(qty) 
        else: item.append(0)
        item.append("Variant Inventory Tracker")
        item.append("")
        item.append("Variant Inventory Policy")
        item.append("deny")
        item.append("Variant Fulfillment Service")
        item.append("manual")
        item.append("Variant Price")
        item.append(price) 
        item.append("Variant Compare At Price")
        if idx==0:
            if old_price != "":
                item.append(old_price)
            else:
                item.append(0)
        else:
            item.append(0)
        item.append("Variant Requires Shipping")
        item.append("")
        item.append("Variant Taxable")
        item.append("")
        item.append("Variant Barcode")
        item.append("")
        item.append("Image Src")
        if idx==0:
            item.append(image_big_url)
        else:
            item.append("")
        item.append("Image Alt Text")
        if idx==0:
            item.append(_title)
        else:
            item.append("")
        item.append("Variant Image")
        try:
            item.append(image_small_urls[idx])
        except:
            item.append("")
        ind = 0
        item.append("Option1 Name")
        if idx<len(colors):
            item.append("Color")
        else:
            item.append("")
        item.append("Option1 Value")
        try:
            item.append(colors[idx])
        except:
            item.append("")
        ind = 1
        item.append("Option2 Name")
        if idx < len(sizes):
            item.append("Size")
        else:
            item.append("")
        item.append("Option2 Value")
        try:
            item.append(sizes[idx])
        except:
            item.append("")
        item.append("Option3 Name")
        item.append("")
        item.append("Option3 Value")
        item.append("")
        # s.save(item, remove_existing_file=False)
        s.save(item)
    # product_type = 

if __name__ == '__main__':
    main()