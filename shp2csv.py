# shp2csv.py converts shapefiles to CSVs with geometry expressed as WKT values

import ogr, csv, sys, os, time

thisfolder = os.getcwd()

print(time.strftime('%X') + ' Begin running shp2csv.py')

# shpfile=r'C:\Temp\test.shp' #sys.argv[1]
# csvfile=r'C:\Temp\test.csv' #sys.argv[2]

shpfile = 'norcal_gis_osm_roads_free_1.shp'
csvfile = 'roads_wkt_norcal.csv'

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

norcal = ['norcal_gis_osm_roads_free_1.shp','roads_wkt_norcal.csv']
socal = ['norcal_gis_osm_roads_free_1.shp','roads_wkt_socal.csv']

print(time.strftime('%X') + ' Converting norcal_gis_osm_roads_free_1.shp to roads_wkt_norcal.csv')

convert_your_csv(norcal)

print(time.strftime('%X') + ' Converting socal_gis_osm_roads_free_1.shp to roads_wkt_socal.csv')

convert_your_csv(socal)

print(time.strftime('%X') + ' End running shp2csv.py')




