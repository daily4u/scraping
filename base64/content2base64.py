# import  csv
# import base64

# with open("input.csv","r") as f:
#     reader = csv.reader(f)
#     contents = list(reader)
#     item = []
#     for row in contents:
#         item.append(row[0])
#         item.append(row[1])
#         item.append(base64.b64encode(bytes(row[0], 'utf-8'))
#         item.append(base64.b64encode(bytes(row[1], 'utf-8'))
    
# with open("output.csv","w") as f:
#     writer = csv.writer(f, delimiter=',')
#     for row in item:
#         writer.writerow(row)

import xlwt
import xlrd
import base64
workbook = xlrd.open_workbook('input.xls')
sheet = workbook.sheet_by_index(0)
i = 0
contents = []
while True:
    i += 1
    try:
        data = [sheet.cell_value(i, col) for col in range(sheet.ncols)]
        contents.append(data)
        print data
    except Exception:
        break
print contents
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')

for ind,rows in enumerate(contents):
    for index, value in enumerate(rows):
        sheet.write(ind, index, value)
        sheet.write(ind, len(rows) + index, base64.b64encode(value))

workbook.save('output.xls')