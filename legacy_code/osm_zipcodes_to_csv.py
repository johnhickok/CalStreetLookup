# Python3 script spatially joins osm_roads and usa zip codes into streetz.csv
import psycopg2

print("Connect to postgreSQL")
# Connect to PostGIS
conn = psycopg2.connect("dbname=<your db name> user=<your user> host=<your host> password=<your password>") 
cur = conn.cursor()

# Spatially join ZIP Code polygons with OSM streets
# You will want to query the zip code polygons for the region you want to speed this query
psql_extract = (
"""
select * from
(select
roads.name as st_name,
zip.po_name as community,
zip.state,
zip.zip_code as zip,
count(roads.name) as st_count
from (select po_name, state, zip_code, geom from usa_zip_poly where state = 'CA') as zip
join (select * from osm_roads where osm_roads.name > '') as roads
on st_intersects(zip.geom, roads.geom)
group by roads.name, zip.zip_code, zip.po_name, zip.state
order by roads.name) as geo_derive
where geo_derive.st_name >= '0'
"""
)

print("Exporting to csv.")

# Set up output file streetz.csv
output_csv = open('streetz.csv', 'w')

cur.execute(psql_extract)
row = cur.fetchall()
for i in row:
  output_csv.write(i[0] + '|' + i[1] + '|' + str(i[2]) + '|' + str(i[3]) + '|' + str(i[4]) + '\n')

output_csv.close()
