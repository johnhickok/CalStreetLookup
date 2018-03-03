# CalStreetLookup

These tools extract a list of street names in California, spatially joined to ZIP Codes. If you need some training using PostGIS, take this <a href="http://workshops.boundlessgeo.com/postgis-intro/">online workshop</a>, provided by Boundless.

You will need some data:
<ul>
  <li>OpenStreetMap (OSM) data is available from <a href="https://www.geofabrik.de/">geofabrik</a>.</li>
  <li>USA ZIP Codes data is available from Esri (<a href="http://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24">download here</a>).</li>
</ul>

Some steps to take are listed below.
<ul>
    <li>Using PGAdmin, create a database in Postgres and make it spatially enabled. Boundless <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/createdb.html">provides a few tips</a>. Examples used in processes.bat use a database named <b>calstreets</b>.</li>
</ul>

<pre>
CREATE EXTENSION postgis;
</pre>

<ul>
  <li>Use the <a href="http://docs.qgis.org/2.18/en/docs/user_manual/plugins/plugins_db_manager.html">QGIS DB Manager</a> or the <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/pgshapeloader.html">PostGIS Shapefile Import/Export Manager</a> to load the Esri ZIP Code polygons into your database. The sample text below is provided if you prefer to use ogr2ogr:</li>
 </ul>

<pre>
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=<i><b>your login</b></i> password=<i><b>your password</b></i>" -s_srs EPSG:4326 -t_srs EPSG:4326 zip_poly.gdb -sql "SELECT ZIP_CODE, PO_NAME, STATE FROM zip_poly AS USA_ZIP_POLY" -overwrite -progress --config PG_USE_COPY YES
</pre>

<ul>
  <li>To access your postgress database from the command line without a password prompt, edit the pgpass.conf file in your Windows Users directory. (See formatting below.) More information about this file is in the <a href="https://www.postgresql.org/docs/current/static/libpq-pgpass.html">postgres documentation.</a></li>
</ul>

<pre>
<b><i>hostname:port:database:username:password</i></b>
</pre>

<ul>
  <li>The rest of the steps are remarked in the file <i>processes.bat</i>.</li>
</ul>  

John Hickok, 2018-02-05
