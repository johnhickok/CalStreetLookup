# merge_join is a Python script that runs geoprocessing tasks in PostGIS

import zipfile, glob, psycopg2
import time

print(time.strftime('%X') + ' Begin running merge_join.py')

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

# Connect to PostGIS
connection = psycopg2.connect("dbname=calstreets user=postgres password=postgres") 
cursor = connection.cursor()

# drop table osm_roads if it exists
cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", ('osm_roads',))

if cursor.fetchone()[0]:
  cursor.execute("DROP TABLE OSM_ROADS")
  cursor.execute("commit")

# merge tables loaded
psql_merge = "CREATE TABLE OSM_STAGING AS "

i = 1
len_list = len(roads_shp)

for file in roads_shp:
  tablename = file.split('.')[0] + '_utf8'
  if i < len_list:
    psql_merge += "(select * from " + tablename + ")"
    psql_merge += " union "
    i += 1
  else:
    psql_merge += "select * from " + tablename

print(time.strftime('%X') + ' Merging tables')

cursor.execute(psql_merge)
cursor.execute("commit")

print(time.strftime('%X') + ' Create table osm_roads with unique osm_id values')

# Creates table osm_ca with unique records based on the OpenStreetMap ID
psql_ca_unique = (
"""
CREATE TABLE OSM_ROADS AS SELECT DISTINCT ON (OSM_STAGING.OSM_ID) 
OSM_STAGING.OGC_FID,
OSM_STAGING.OSM_ID,
OSM_STAGING.CODE,
OSM_STAGING.FCLASS,
OSM_STAGING.NAME,
OSM_STAGING.REF,
OSM_STAGING.ONEWAY,
OSM_STAGING.MAXSPEED,
OSM_STAGING.LAYER,
OSM_STAGING.BRIDGE,
OSM_STAGING.TUNNEL,
OSM_STAGING.WKB_GEOMETRY
FROM OSM_STAGING
"""
)
cursor.execute(psql_ca_unique)
cursor.execute("commit")

print(time.strftime('%X') + ' Cleaning up Postgres database')

# Drop interim tables, plus some Postgres cleanup
for file in roads_shp:
  pgsql_drop = "drop table " + file.split('.')[0] + '_utf8'
  cursor.execute(pgsql_drop)
  cursor.execute("commit")

cursor.execute('DROP TABLE OSM_STAGING')
cursor.execute("commit")
cursor.execute("VACUUM ANALYZE")


print(time.strftime('%X') + ' Create spatial index for osm_roads')

# Create spatial index
psql_spatial_index = (
"""
CREATE INDEX osm_roads_wkb_geometry_geom_idx ON osm_roads USING gist (wkb_geometry)
"""
)

cursor.execute(psql_spatial_index)
cursor.execute("commit")

print(time.strftime('%X') + ' Spatially join ZIP Code polygons with osm_roads')

# Spatially join ZIP Code polygons with OSM streets
# You will want to query the zip code polygons for the region you want to speed this query
psql_extract = (
"""
SELECT * from
(SELECT
roads.name AS st_name,
zip.PO_NAME AS community,
zip.STATE,
zip.ZIP_CODE AS zip,
COUNT(roads.name) as st_count
FROM (SELECT PO_NAME, STATE, ZIP_CODE, wkb_geometry FROM usa_zip_poly where STATE = 'CA') AS zip
JOIN (SELECT * FROM osm_roads WHERE osm_roads.name > '') as roads
ON ST_intersects(zip.wkb_geometry, roads.wkb_geometry)
GROUP BY roads.name, zip.ZIP_CODE, zip.PO_NAME, zip.STATE
ORDER BY roads.name) as geo_derive
WHERE geo_derive.st_name >= '0'
"""
)

print(time.strftime('%X') + ' Output file streetz.csv')

# Set up output file streetz.csv
output_csv = open('streetz.csv', 'w')

cursor.execute(psql_extract)
row = cursor.fetchall()
for i in row:
  output_csv.write(i[0] + '|' + i[1] + '|' + str(i[2]) + '|' + str(i[3]) + '|' + str(i[4]) + '\n')

print(time.strftime('%X') + ' End running merge_join.py')

output_csv.close()

