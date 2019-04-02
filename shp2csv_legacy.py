# shp2csv.py converts shapefiles to CSVs with geometry expressed as WKT values

import ogr, csv, time, glob, zipfile

print(time.strftime('%X') + ' Begin running shp2csv.py')

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

def convert_your_csv(shapefile_name):
  #Open files
  shpfile = shapefile_name
  csvfile = shapefile_name.split('.')[0] + '.csv'
  csvfile = open(csvfile,'w')
  ds = ogr.Open(shpfile)
  lyr = ds.GetLayer()
  
  #Get field names
  dfn = lyr.GetLayerDefn()
  nfields = dfn.GetFieldCount()
  fields = []
  for i in range(nfields):
    fields.append(dfn.GetFieldDefn(i).GetName())
  fields.append('WKT')
  
  # set up csv and add header
  csvwriter = csv.DictWriter(csvfile, fieldnames=fields, lineterminator='\n')
  csvwriter.writeheader()
  
  # Write attributes and wkt out to csv
  for feat in lyr:
    attributes = feat.items()
    geom = feat.GetGeometryRef()
    attributes['WKT'] = geom.ExportToWkt()
    csvwriter.writerow(attributes)
  
  #clean up
  del csvwriter,lyr,ds
  csvfile.close()

for file in roads_shp:
  print(time.strftime('%X') + ' Converting ' + file + ' to csv')
  convert_your_csv(file)

print(time.strftime('%X') + ' End running shp2csv.py')




