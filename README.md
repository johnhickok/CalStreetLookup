<b>Loading OpenStreetMap streets (*.pbf) into PostgreSQL</b>

Note these steps are for streets covering California. It is assumed the user of these scripts is familiar with QGIS/GDAL, Python, and PostgreSQL/PostGIS.

Begin with downloading some data.

1. Visit the <a href="https://download.geofabrik.de/north-america/us/california.html">Geofabrik Download Server</a> for California and download 
<i>california-latest.osm.pbf</i>. Move this large file into the same folder in which you want to run these scripts.

2. Copy/paste the following ogr2ogr expression into a text editor and replace your PostgreSQL user name, database name, and password. Open the OSGeo4W Shell, navigate to the folder you copied your pbf file into, then copy/paste your personalized ogr2ogr expression from your text editor into the shell.
<pre>
ogr2ogr -f PostgreSQL PG:"host=localhost user=[your user name] password=[your password] dbname=[your database name]" california-latest.osm.pbf -sql "select osm_id, name, highway, z_order, other_tags from lines where highway is not null" -nln osmr_temp -lco GEOMETRY_NAME=geom
</pre>

This will create a temporary table (osmr_temp) in your PostgreSQL database with most of what you need.

3. In the OSGeo4W Shell, run the Python script below. This searches the <i>other_tags</i> field for freeway references, then populates a field <i>ref</i> which contains freeway numbers. This field is valuable for identifying state, federal, and interstate highways. The osmr_temp table is replaced with a new table osm_roads which can be used for spatial joining in the steps below or for general mapping.
<pre>
python osm_roads_cleanup.py
</pre>

4. Download <a href="https://www.arcgis.com/home/item.html?id=91379236cdca4fd88f3682283f63953e#overview">United States ZIP Code Boundaries</a> from Esri. In the past, Esri made this available as a public download. Today, Esri places this layer under the Living Atlas umbrella. Use desktop GIS software to download a local copy of this GIS data (filtered for California) and upload this layer as a table into the same database as your <i>osm_roads</i> table. Name this new table usa_zip_poly. If you can create an ogr2ogr expression for this step, kudos! It can be done.

5. In the OSGeo4W Shell, run the Python script below to spatially join your <i>osm_roads</i> and <i>usa_zip_poly</i> tables. The script extracts data to the file streetz.csv, which can be used for uploading into other databases.
<pre>
python osm_zipcodes_to_csv.py
</pre>

6. If you wanto to use a local SQLITE database for quick and simple street name lookups. open the OSGeo4W Shell, run the Python script below. This script will create a sqlite database streetz.db, import streetz.csv, and create an index.
<pre>
python csv2sqlite.py
</pre>

7. Finally, you can run street_lookup.py (Python 3) to query your sqlite database.
