# merge_join is a Python script that runs geoprocessing tasks in PostGIS

import psycopg2
import time

connection = psycopg2.connect("dbname=calstreets user=postgres password=[your password]") 
cursor = connection.cursor()

# Begin running script after importing libraries
print(time.strftime('%X') + ' Begin running merge_join.py')
print(time.strftime('%X') + ' Merge Northern and Southern California tables together')

# Merge Northern and Southern California tables together
psql_merge_ca = (
"""
CREATE TABLE OSM_CA_STAGING AS 
(SELECT * FROM OSM_ROADS_NORCAL)
UNION
(SELECT * FROM OSM_ROADS_SOCAL)
"""
)

cursor.execute(psql_merge_ca)
cursor.execute("commit")

print(time.strftime('%X') + ' Create table osm_ca_roads with unique osm_id values')

# Creates table osm_ca with unique records based on the OpenStreetMap ID
psql_ca_unique = (
"""
CREATE TABLE OSM_CA_ROADS AS SELECT DISTINCT ON (OSM_CA_STAGING.OSM_ID) 
OSM_CA_STAGING.OGC_FID,
OSM_CA_STAGING.OSM_ID,
OSM_CA_STAGING.CODE,
OSM_CA_STAGING.FCLASS,
OSM_CA_STAGING.NAME,
OSM_CA_STAGING.REF,
OSM_CA_STAGING.ONEWAY,
OSM_CA_STAGING.MAXSPEED,
OSM_CA_STAGING.LAYER,
OSM_CA_STAGING.BRIDGE,
OSM_CA_STAGING.TUNNEL,
OSM_CA_STAGING.WKB_GEOMETRY
FROM OSM_CA_STAGING
"""
)
cursor.execute(psql_ca_unique)
cursor.execute("commit")

print(time.strftime('%X') + ' Cleanup')

# Drops interim tables, plus some Postgres cleanup
pgsql_drop = ("DROP TABLE OSM_ROADS_NORCAL, OSM_ROADS_SOCAL, OSM_CA_STAGING")
cursor.execute(pgsql_drop)
cursor.execute("commit")
cursor.execute("VACUUM ANALYZE")


print(time.strftime('%X') + ' Create spatial index for California streets table')

# Create spatial index
psql_spatial_index = (
"""
CREATE INDEX osm_ca_roads_wkb_geometry_geom_idx ON osm_ca_roads USING gist (wkb_geometry)
"""
)

cursor.execute(psql_spatial_index)
cursor.execute("commit")


print(time.strftime('%X') + ' Spatially join ZIP Code polygons with OSM streets')

# Spatially join ZIP Code polygons with OSM streets
psql_extract_ca = (
"""
SELECT 
roads.name AS st_name,
zip.PO_NAME AS community,
zip.ZIP_CODE AS zip,
COUNT(roads.name) as st_count
FROM (SELECT PO_NAME, ZIP_CODE, wkb_geometry FROM usa_zip_poly where STATE = 'CA') AS zip
join (SELECT * FROM osm_ca_roads WHERE osm_ca_roads.name > '') as roads
ON ST_intersects(zip.wkb_geometry, roads.wkb_geometry)
GROUP BY roads.name, zip.ZIP_CODE, zip.PO_NAME
ORDER BY roads.name
"""
)


print(time.strftime('%X') + ' Output file streetz.csv')

# Set up output file streetz.csv
output_csv = open('streetz.csv', 'w')

cursor.execute(psql_extract_ca)
row = cursor.fetchall()
for i in row:
  output_csv.write(i[0] + '|' + i[1] + '|' + str(i[2]) + '|' + str(i[3]) + '\n')

print(time.strftime('%X') + ' Finish merge_join.py')

output_csv.close()

