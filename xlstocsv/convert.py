import csv
from os import sys
from scrapex import *

def csv_from_excel(excel_file):
    with open(excel_file, 'rb') as f:
        file_content = f.read()
    s = Scraper(
        use_cache=False,
    )
    html_doc = '<html><body>%s</body></html>' % str(file_content)
    # print html_doc
    doc = Doc(html=html_doc)
    headers = doc.q('//table/tr/th')
    # print headers
    print "-----------------------------"
    bodies = doc.q('//table/tr')
    # print bodies
    for ind, row in enumerate(bodies):
        if ind == 0: continue
        # print row
        contents = row.q('td')
        # print contents
        item = []
        # return
        for idx, col in enumerate(contents):
            header = headers[idx].x('text()').trim()
            content =  col.x('text()').trim()
            item.append(header)
            item.append(content)
        s.save(item)

if __name__ == "__main__":
    csv_from_excel(sys.argv[1])