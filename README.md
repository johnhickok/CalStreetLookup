# CalStreetLookup

These tools extract a list of street names in California, spatially joined to ZIP Codes. If you need some training using PostGIS, take this <a href="http://workshops.boundlessgeo.com/postgis-intro/">online workshop</a>, provided by Boundless.

You will need some data:
<ul>
  <li>OpenStreetMap (OSM) data is available from <a href="https://www.geofabrik.de/">geofabrik</a>.</li>
  <li>USA ZIP Codes data is available from Esri.</li>
</ul>

Some steps to take are listed below.
<ul>
  <li>Use ArcGIS, QGIS, or any other desktop GIS software to create a statewide shapefile of your ZIP Codes.</li>
    <li>Using PGAdmin, create a database in Postgres and make it spatially enabled. Boundless <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/createdb.html">provides a few tips</a>.</li>
</ul>

<pre>
CREATE EXTENSION postgis;
</pre>

<ul>
  <li>Use the <a href="http://docs.qgis.org/2.18/en/docs/user_manual/plugins/plugins_db_manager.html">QGIS DB Manager</a> or the <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/pgshapeloader.html">PostGIS Shapefile Import/Export Manager</a> to load this shapefile into your database.</li>
  <li>Create a new table for roads:</li>
</ul>

<pre>
CREATE TABLE public.roads
(
  gid SERIAL PRIMARY KEY,
  name character varying(150),
  geom geometry(LineString,4326)
);
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

John Hickok, 2017-06-30
