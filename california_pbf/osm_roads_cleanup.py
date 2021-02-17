# Python3 script creates table osm_streets from osmr_temp
import psycopg2

print("connecting to postgreSQL database")
# Connect to PostGIS
conn = psycopg2.connect("dbname='[your database name]' user='[your user name]' host='localhost' password='[your password]'") 
cur = conn.cursor()

print("extracting reference values from osm tags")
# drop table hwy_ref if it exists, then create it
cur.execute("drop table if exists hwy_ref")

cur.execute("""
create table hwy_ref (
locid serial,
osm_id character varying,
ref character varying
)
"""
)

# get data from other_tags
cur.execute("""
select
osm_id,
other_tags
from osmr_temp
"""
)

rows = cur.fetchall()

data = []

for row in rows:
  t = row[1]
  if t is not None:
    for i in t.split(','):
      if i.split('=>')[0] == '"ref"':
        ref = i.split('=>')[1].replace('"','')
        ref_row = (row[0], ref)
        data.append(ref_row)

cur.executemany("""
insert into hwy_ref (osm_id, ref) values(%s, %s)
""", data
)

conn.commit()

print("creating table osm_roads")
# drop table osm_roads if exists, then create from above
cur.execute("drop table if exists osm_roads")

cur.execute("""
create table osm_roads as select
osmr_temp.ogc_fid,
osmr_temp.osm_id,
osmr_temp.name,
osmr_temp.highway,
osmr_temp.z_order,
hwy_ref.ref,
osmr_temp.geom
from osmr_temp
left join hwy_ref
on osmr_temp.osm_id = hwy_ref.osm_id;
"""
)

conn.commit()

cur.execute("create index idx_osm_roads_geom on osm_roads using gist (geom)")

print("dropping temp tables and disconnecting from database")

cur.execute("drop table if exists osmr_temp")
cur.execute("drop table if exists hwy_ref")

conn.commit()
conn.close()

