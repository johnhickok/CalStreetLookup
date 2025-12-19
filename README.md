<b>Using PostGIS to Create a Street Name Lookup Table</b>

Mispelled street names are a major cause for geocoding errors. This script creates an up-to-date table you can use for looking up all the streets in a given ZIP Code, listed alphabetically. We can thank the contributors of <a href="https://wiki.openstreetmap.org">Open Street Map</a> and <a href="https://www.esri.com">Esri</a> for the data we're using. Let's not forget to thank <a href="https://www.geofabrik.de">Geofabrik</a> for making it easy to download Open Street Map data! Note these steps are for streets covering California. It is assumed the user of these scripts is familiar with QGIS, GDAL, Python, PostgreSQL, and PostGIS.

Begin with downloading some data.

1. Visit the <a href="https://download.geofabrik.de/north-america/us/california.html">Geofabrik Download Server</a> for California and download a file california-latest.osm.pbf. Move this large file into the same folder in which you want to run these scripts.

2. Copy/paste the following ogr2ogr expression into a text editor and replace your PostgreSQL host, user name, database name, and password. Open the OSGeo4W Shell, navigate to the folder you copied your pbf file into, then copy/paste your personalized ogr2ogr expression from your text editor into the shell.
<pre>
ogr2ogr -f PostgreSQL PG:"host=localhost user=[your user name] password=[your password] dbname=[your database name]" california-latest.osm.pbf -sql "select osm_id, name, highway, z_order, other_tags from lines where highway is not null" -nln osmr_temp -lco GEOMETRY_NAME=geom
</pre>

This will create a temporary table (osmr_temp) in your PostgreSQL database with most of what you need.

3. Before running the script below in the OSGeo4W Shell, you will need to edit your copy of this Python script with your PostgreSQL host, user name, database name, and password. This script searches the other_tags field for freeway references, then populates a field ref which contains freeway numbers. This field is valuable for identifying state, federal, and interstate highways. The osmr_temp table is replaced with a new table osm_roads which can be used for spatial joining in the SQL steps further below or for general mapping.
<pre>
python osm_roads_hwy_ref.py
</pre>

4. Download <a href="https://www.arcgis.com/home/item.html?id=5f31109b46d541da86119bd4cf213848">United States ZIP Code Boundaries</a> from Esri. In the past, Esri made this available as a general public download. Today, Esri places this layer under its Living Atlas umbrella. Use desktop GIS software to download a local copy of this GIS data (filtered for California) and upload this layer as a table into the same PostgreSQL database as your osm_roads table. Name this new table ca_zip_poly.

5. The following SQL creates a table with spatially joined values from your osm_roads and ca_zip_poly tables to include California ZIP Codes, Street names, and Post Office names used to guestimate city names. The following code can be run using <a href="https://www.postgresql.org/docs/current/app-psql.html">psql</a> (available in the OSGEO4W Shell), <a href="https://www.pgadmin.org/">pgAdmin4</a>, or other database management tools.
<pre>
create table cal_street_lookup as
select
ca_zip_poly.zip_code as zip,
roads.name as street,
ca_zip_poly.po_name as city,
count(roads.name) as streetcount
from ca_zip_poly
join (select name, geom from osm_roads where name > '0') as roads
on st_intersects(ca_zip_poly.geom, roads.geom)
group by roads.name, ca_zip_poly.zip_code, ca_zip_poly.po_name
order by ca_zip_poly.zip_code, roads.name
;
</pre>

6. Run cleanup_cal_street_lookup.sql to clean up some buggy data that might be from OpenStreetMap in your cal_street_lookup table.


<b>Extras</b>

The following Python script can be run in the OSGEO4W Shell, taking user input and querying your table cal_street_lookup. The code retrieves pre geoprocessed street names, U.S. postal cities, and ZIP Codes and displays the results in a text file via the Python webbrowser module.

<pre>
python street_lookup.py
</pre>

The script below is the same as above, except using PostGIS geospatial queries direcly from your osm_roads and ca_zip_poly tables with their geometries. Comparing these two scripts can help decide if the computational expense will work for you.

<pre>
python street_lookup_geo.py
</pre>

All sample code in this repository is provided as is without warranty of any kind, either express or implied, including any implied warranties of fitness for a particular purpose, merchantability, or non-infringement.
