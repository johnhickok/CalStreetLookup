#!/usr/bin/python
# -*- coding: utf-8 -*-

# convert_utf8.py inputs roads_wkt.csv and outputs roads_wkt_utf8.sql. This process
# 1. Extracts only records that have non null street name values
# 2. Of the above, only the WKT and name fields are extracted (see https://pypi.python.org/pypi/Unidecode)
# 3. Transliterates special characters with UTF-8 characters
# 4. Removes other characters unneded and incompatible with sqlite

import csv
from unidecode import unidecode

# set up your unidecode function
def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

infile_csv = open('roads_wkt.csv', 'r')
outfile_csv = open('roads_wkt_utf8.sql', 'w')

#outfile_csv.write('WKT,name\n')

with open('roads_wkt.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row['name'] > '':
            name = remove_non_ascii(row['name'])
            name = name.replace('"','')
            name = name.replace("'","")
            name = name.replace(',',' ')
            name = name.replace('|','')
            name = name.replace('}','')
            name = name.replace('{','')
            name = name.replace(';','')
            name = name.replace('.','')
            name = name.replace('\\','')
            name = name.replace('\a','a')
            name = name.replace('\b','b')
            name = name.replace('\f','f')
            name = name.replace('\n','n')
            name = name.replace('\r','r')
            name = name.replace('\t','t')
            name = name.replace('\v','v')
            new_row = "INSERT INTO roads(name, geom) VALUES ('" + name + "',ST_GeomFromText('" + row['WKT'] + "',4326));\n"
            outfile_csv.write(new_row)

infile_csv.close()
outfile_csv.close()

