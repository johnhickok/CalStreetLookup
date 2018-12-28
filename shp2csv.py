# shp2csv.py converts shapefiles to CSVs with geometry expressed as WKT values

import ogr, csv, sys, os, time

thisfolder = os.getcwd()

print(time.strftime('%X') + ' Begin running shp2csv.py')

def convert_your_csv(files):
  #Open files
  shpfile = files[0]
  csvfile = files[1]
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

# List files to be converted, then feed them into the function
norcal = ['norcal_gis_osm_roads_free_1.shp','roads_wkt_norcal.csv']
socal = ['socal_gis_osm_roads_free_1.shp','roads_wkt_socal.csv']

print(time.strftime('%X') + ' Converting ' + norcal[0] + ' to ' + norcal[1])

convert_your_csv(norcal)

print(time.strftime('%X') + ' Converting ' + socal[0] + ' to ' + socal[1])

convert_your_csv(socal)

print(time.strftime('%X') + ' End running shp2csv.py')




