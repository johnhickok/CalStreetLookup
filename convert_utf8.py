#!/usr/bin/python
# -*- coding: utf-8 -*-
# jhickok 2018-12-26

# Geoprocessing with GDAL and PostGIS require clean UTF-8 values
# convert_utf8.py (Python 2.x) inputs

# roads_wkt_norcal.csv
# roads_wkt_socal.csv

# and outputs

# osm_roads_norcal.csv
# osm_roads_socal.csv

# Also removes characters unneeded and incompatible with sqlite

import csv, os, zipfile, subprocess
from unidecode import unidecode
import time

print(time.strftime('%X') + ' Begin running convert_utf8.py')

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

# input roads_wkt_norcal.csv, export osm_roads_norcal.csv
outfile_csv = open('osm_roads_norcal.csv', 'w')
outfile_csv.write('WKT,osm_id,code,fclass,name,ref,oneway,maxspeed,layer,bridge,tunnel\n')

with open('roads_wkt_norcal.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
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
        new_row = ''
        new_row += '"' + row['WKT'] + '",'
        new_row += '"' + row['osm_id'] + '",'
        new_row += row['code'] +  ','
        new_row += row['fclass'] + ','
        new_row += name + ','
        new_row += row['ref'] + ','
        new_row += row['oneway'] + ','
        new_row += row['maxspeed'] + ','
        new_row += row['layer'] + ','
        new_row += row['bridge'] + ','
        new_row += row['tunnel'] + '\n'		
        outfile_csv.write(new_row)

# input roads_wkt_socal.csv, export osm_roads_socal.csv
outfile_csv = open('osm_roads_socal.csv', 'w')
outfile_csv.write('WKT,osm_id,code,fclass,name,ref,oneway,maxspeed,layer,bridge,tunnel\n')

with open('roads_wkt_socal.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
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
        new_row = ''
        new_row += '"' + row['WKT'] + '",'
        new_row += '"' + row['osm_id'] + '",'
        new_row += row['code'] +  ','
        new_row += row['fclass'] + ','
        new_row += name + ','
        new_row += row['ref'] + ','
        new_row += row['oneway'] + ','
        new_row += row['maxspeed'] + ','
        new_row += row['layer'] + ','
        new_row += row['bridge'] + ','
        new_row += row['tunnel'] + '\n'		
        outfile_csv.write(new_row)

outfile_csv.close()

print(time.strftime('%X') + ' End running convert_utf8.py')

