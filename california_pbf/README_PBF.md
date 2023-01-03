<b>Loading OpenStreetMap streets (*.pbf) into PostgreSQL</b>

Note these steps are for streets covering California. begin with downloading some data.

1. Visit the <a href="https://download.geofabrik.de/north-america/us/california.html">Geofabrik Download Server</a> for California and download 
<i>california-latest.osm.pbf</i>. Move this large file into the same folder in which you want to run these scripts.

2. Copy/paste the following ogr2ogr expression into a text editor and replace with your PostgreSQL user name, database name, and password. Open the OSGeo4W Shell, navigate to the folder you copied your pbf file into, then copy/paste your ogr2ogr expression into the shell.
<pre>
ogr2ogr -f PostgreSQL PG:"host=localhost user=[your user name] password=[your password] dbname=[your database name]" california-latest.osm.pbf -sql "select osm_id, name, highway, z_order, other_tags from lines where highway is not null" -nln osmr_temp -lco GEOMETRY_NAME=geom
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

5. Download <a href="https://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24">USA ZIP Code polygons</a> from Esri, and upload this file geodatabase into the same database as your <i>osm_roads</i> table. Name this new table <i>usa_zip_poly</i>.

6. Run the Python script below to spatially join your <i>osm_roads</i> and <i>usa_zip_poly</i> tables. The script extracts data to streetz.csv.
<pre>
python osm_zipcodes_to_csv.py
</pre>

6. Run the Python script below to create sqlite database streetz.db, import streetz.csv and create an index.
<pre>
python csv2sqlite.py
</pre>

7. Finally, you can run streetzip.py (Python 3) to query your sqlite database.
