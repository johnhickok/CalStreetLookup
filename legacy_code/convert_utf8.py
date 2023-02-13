#!/usr/bin/python
# -*- coding: utf-8 -*-
# jhickok 2020-01-05
# Small changes made to run on Python 3 in the OSGeo4W Shell

import csv, os, zipfile, glob
from unidecode import unidecode
import time

print(time.strftime('%X') + ' Begin running convert_utf8.py')

# Get a list of the zipped shapefiles from GeoFabrik
zip_list = []
roads_shp = []

for i in glob.glob('*.zip'):
  if 'latest-free.shp' in i:
    zip_list.append(i)

for archive in zip_list:
  region = archive.split('-')[0]
  archive_open = zipfile.ZipFile(archive)
  for file in zipfile.ZipFile.namelist(archive_open):
    if 'roads' in file and '.shp' in file:
      roads_shp.append(region + '_' + file)
  archive_open.close()

# function for replacing or removing non-UTF8 characters
# (GDAL scripts need this.)
def remove_non_ascii(text):
  try:
    finalval = unidecode(text)
  except UnicodeDecodeError:
    finalval = ''
    for i in text:
      try:
        i.decode('utf-8')
        finalval += i
      except UnicodeError:
        print ('Found a non-decodable character')
  return finalval

for file in roads_shp:
  in_csv_filename = file.split('.')[0] + '.csv'
  out_csv_filename = file.split('.')[0] + '_utf8.csv'
  
  print(time.strftime('%X') + ' Converting ' + in_csv_filename + ' to ' + out_csv_filename)
  
  out_csv = open(out_csv_filename, 'w')
  out_csv.write('WKT,osm_id,code,fclass,name,ref,oneway,maxspeed,layer,bridge,tunnel\n')

  with open(in_csv_filename, encoding="utf8") as csvfile:
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
      out_csv.write(new_row)

  out_csv.close()

print(time.strftime('%X') + ' End running convert_utf8.py')
