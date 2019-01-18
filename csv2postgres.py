# csv2postgres.py loads geospatial CSVs into PostGIS

import zipfile, glob, os
import time

print(time.strftime('%X') + ' Begin running csv2postgres.py')

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

# Build ogr2ogr strings to load into postgres
introstring = 'ogr2ogr -f "PostgreSQL" PG:"'
hostname = 'host=localhost '
portname = 'port=5432 '
dbname = ' dbname=calstreets '
username = 'user=[your user name] '
passwordname = 'password=[your password]" '
projections = '-s_srs EPSG:4326 -t_srs EPSG:4326 '
endstring = '-overwrite --config PG_USE_COPY YES '
sqlstring = '-sql "select osm_id,code,fclass,name,ref,oneway,maxspeed,layer,bridge,tunnel from '

for file in roads_shp:
  utf8_csf_filename = file.split('.')[0] + '_utf8.csv'
  utf8_tablename = file.split('.')[0] + '_utf8'

  ogrstring = ""
  ogrstring += introstring
  ogrstring += hostname
  ogrstring += portname
  ogrstring += dbname
  ogrstring += username
  ogrstring += passwordname
  ogrstring += projections
  ogrstring += utf8_csf_filename + ' '
  ogrstring += sqlstring
  ogrstring += utf8_tablename + '"'
  
  print(time.strftime('%X') + ' Loading ' + utf8_csf_filename + ' to Postgres database')

  os.system(ogrstring)

print(time.strftime('%X') + ' End running csv2postgres.py')
