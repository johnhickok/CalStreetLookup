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

# Creates a table osm_ca with OSM_ID as a primary key
psql_ca_unique_create = (
"""
CREATE TABLE PUBLIC.OSM_ROADS
(
  OSM_ID CHARACTER VARYING PRIMARY KEY,
  CODE CHARACTER VARYING,
  FCLASS CHARACTER VARYING,
  NAME CHARACTER VARYING,
  REF CHARACTER VARYING,
  ONEWAY CHARACTER VARYING,
  MAXSPEED CHARACTER VARYING,
  LAYER CHARACTER VARYING,
  BRIDGE CHARACTER VARYING,
  TUNNEL CHARACTER VARYING,
  WKB_GEOMETRY GEOMETRY(GEOMETRY,4326)
)
"""
)
cursor.execute(psql_ca_unique_create)
cursor.execute("commit")

# Append osm_ca with values from staging
psql_ca_unique = (
"""
INSERT INTO PUBLIC.OSM_ROADS (
OSM_ID, 
CODE, 
FCLASS, 
NAME, 
REF, 
ONEWAY, 
MAXSPEED, 
LAYER, 
BRIDGE, 
TUNNEL, 
WKB_GEOMETRY)
SELECT DISTINCT ON (OSM_STAGING.OSM_ID)
OSM_ID, 
CODE, 
FCLASS, 
NAME, 
REF, 
ONEWAY, 
MAXSPEED, 
LAYER, 
BRIDGE, 
TUNNEL, 
WKB_GEOMETRY
FROM OSM_STAGING;
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
CREATE INDEX OSM_ROADS_WKB_GEOMETRY_GEOM_IDX ON OSM_ROADS USING GIST (WKB_GEOMETRY)
"""
)

cursor.execute(psql_spatial_index)
cursor.execute("commit")

print(time.strftime('%X') + ' Spatially joining ZIP Code polygons with osm_roads')

# Spatially join ZIP Code polygons with OSM streets
# You will want to query the zip code polygons for the region you want to speed this query
psql_extract = (
"""
SELECT * FROM
(SELECT
ROADS.NAME AS ST_NAME,
ZIP.PO_NAME AS COMMUNITY,
ZIP.STATE,
ZIP.ZIP_CODE AS ZIP,
COUNT(ROADS.NAME) AS ST_COUNT
FROM (SELECT PO_NAME, STATE, ZIP_CODE, WKB_GEOMETRY FROM USA_ZIP_POLY WHERE STATE = 'CA') AS ZIP
JOIN (SELECT * FROM OSM_ROADS WHERE OSM_ROADS.NAME > '') AS ROADS
ON ST_INTERSECTS(ZIP.WKB_GEOMETRY, ROADS.WKB_GEOMETRY)
GROUP BY ROADS.NAME, ZIP.ZIP_CODE, ZIP.PO_NAME, ZIP.STATE
ORDER BY ROADS.NAME) AS GEO_DERIVE
WHERE GEO_DERIVE.ST_NAME >= '0'
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

