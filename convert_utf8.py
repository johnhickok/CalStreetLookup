#!/usr/bin/python
# -*- coding: utf-8 -*-
# jhickok 2016-04-01

# convert_utf8.py inputs roads_wkt.csv and outputs roads_wkt_utf8.sql. This process
# 1. Extracts only records that have non null street name values
# 2. Of the above, only the WKT and name fields are extracted (see https://pypi.python.org/pypi/Unidecode)
# 3. Transliterates special characters with UTF-8 characters
# 4. Removes other characters unneeded and incompatible with sqlite

import csv, os, zipfile, subprocess
from unidecode import unidecode

# function for replacing or removing non-UTF8 characters
# (GDAL scripts need this.)
def remove_non_ascii(text):
  try:
    finalval = unidecode(unicode(text, encoding = "utf-8"))
  except UnicodeDecodeError:
    finalval = ''
    for i in text:
      try:
        i.decode('utf-8')
        finalval += i
      except UnicodeError:
        print ('Found a non-decodable character')
  return finalval

infile_csv = open('roads_wkt.csv', 'r')
outfile_csv = open('osm_roads_ca.csv', 'w')

outfile_csv.write('WKT,STNAME\n')

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
            new_row = '"' + row['WKT'] + '",' + name + '\n'
            outfile_csv.write(new_row)

infile_csv.close()
outfile_csv.close()

