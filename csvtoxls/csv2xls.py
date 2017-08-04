import xlwt, csv, os

csv_folder = "Output/"

book = xlwt.Workbook()
for fil in os.listdir(csv_folder):
    sheet = book.add_sheet(fil[:-4])
    with open(csv_folder + fil) as filname:
        reader = csv.reader(filname)
        i = 0
        for row in reader:
            for j, each in enumerate(row):
                sheet.write(i, j, each.decode('utf-8'))
            i += 1

book.save("Output.xls")