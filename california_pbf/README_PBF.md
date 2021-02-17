<b>Loading OpenStreetMap streets (*.pbf) into PostgreSQL</b>

Note these steps are for streets covering California

1. Visit the <a href="https://download.geofabrik.de/north-america/us/california.html">Geofabrik Download Server</a> for California and download 
california-latest.osm.pbf. Move this large file into the same folder 
in which you want to run these scripts.

2. Open the OSGeo4W Shell, and navigate to the folder you just copied your 
pbf file into, then copy/paste the following:
<pre>
ogr2ogr -f PostgreSQL PG:"host=localhost user=postgres password=postgres dbname=cal_streets" california-latest.osm.pbf -sql "select osm_id, name, highway, z_order, other_tags from lines where highway is not null" -nln osmr_temp -lco GEOMETRY_NAME=geom
</pre>

This will create a temporary table (osmr_temp) with most of what you need.

3. In the OSGeo4W Shell, enter the command below to enable Python.
<pre>
py3_env
</pre>

4. In the OSGeo4W Shell, run the Python script below. This searches the other_tags field for freeway references, then populates a field ref which contains freeway numbers. This field is valuable for identifying state, federal, and interstate highways.
<pre>
python osm_roads_cleanup.py
</pre>

5. Run the Python script below to spatially join OSM roads with <href="https://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24">USA ZIP Code polygons</a> from Esri. Script extracts data to streetz.csv.
<pre>
python osm_zipcodes_to_csv.py
</pre>

6. Run the Python script below to create sqlite database streetz.db, import streetz.csv and create an index.
<pre>
python make_sqlite_db.py
</pre>

7. Finally, you can run streetzip.py (Python 3) to query your sqlite database.
