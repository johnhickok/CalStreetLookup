# CalStreetLookup

Mispelled street names are a major cause of geocoding errors. This is especially true if your addresses are acquired over a phone call. These tools create a list of street names in California with their corresponding ZIP Codes and postal cities. This repository also includes scripts for creating a SQLite database for looking up street spellings by ZIP Code, city, or parts of street names.

It is assumed you already installed and are at least familiar with <a href="https://qgis.org/en/site/">QGIS</a> (OSGeo4W installation) and PostGIS. It is also helpful if you have a working knowledge of OGR, Python and Spatial SQL. If you need some training using PostGIS, start with the <a href="https://postgis.net/workshops/postgis-intro">official postgis documentation</a>. Boundless no longer hosts free tutorials, but does offer a few <a href="https://learn.boundlessgeo.com/series/postgis">courses for a fee</a>. For your convenience, please visit the <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a> page.

You will need some data:
<ul>
  <li>OpenStreetMap (OSM) data is available from <a href="https://www.geofabrik.de/">geofabrik</a>. Note our example uses California shapefile downloads, which Geofabrik split into north and south.</li>
  <li>USA ZIP Codes data are available from Esri (<a href="http://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24">download here</a>).</li>
</ul>

Some steps to take are listed below.
<ul>
    <li>Using PGAdmin, create a database in Postgres and make it spatially enabled. Boundless <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/createdb.html">provides a few tips</a>. Examples used herein use a database named <b>calstreets</b>.</li>
</ul>

<pre>
CREATE EXTENSION postgis;
</pre>

<ul>
  <li>Use the <a href="http://docs.qgis.org/2.18/en/docs/user_manual/plugins/plugins_db_manager.html">QGIS DB Manager</a> or the <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/pgshapeloader.html">PostGIS Shapefile Import/Export Manager</a> to load the Esri ZIP Code polygons into your database. The sample text below is provided if you prefer to use ogr2ogr:</li>
 </ul>

<pre>
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=<i><b>your login</b></i> password=<i><b>your password</b></i>" -s_srs EPSG:4326 -t_srs EPSG:4326 zip_poly.gdb -sql "SELECT ZIP_CODE, PO_NAME, STATE FROM zip_poly AS USA_ZIP_POLY" -overwrite -progress --config PG_USE_COPY YES -nlt MULTIPOLYGON
</pre>

<ul>
  <li>To access your postgress database from the command line without a password prompt, edit the pgpass.conf file in your Windows Users directory. (See formatting below.) More information about this file is in the <a href="https://www.postgresql.org/docs/current/static/libpq-pgpass.html">postgres documentation.</a></li>
</ul>

<pre>
<b><i>hostname:port:database:username:password</i></b>
</pre>

<p>
More details are remarked in the Windows batch files and the scripts called. Please also visit the <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a> for more info.
<ul>
  <li><b>process_1.bat</b> extracts CSVs from norcal and socal shapefiles.</li>
  <li><b>process_2.bat</b> uses Python and the <a href="http://initd.org/psycopg/docs/index.html">psycopg2</a> library to geoprocess your data in PostGIS.</li>
</ul>  

John Hickok, 2018-12-26
