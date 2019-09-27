import csv
import json
#превращаем csv в json
csvfile = open('lp2019.csv', 'r')
jsonfile = open('lp2019.json', 'w', encoding='utf-8')

fieldnames = ("MNN","TorgName","ReleaseForm","Count","Price","Barcode")
reader = csv.DictReader(csvfile, fieldnames,delimiter = ';')
for row in reader:
    json.dump(row, jsonfile,ensure_ascii=False)
    jsonfile.write('\n')
