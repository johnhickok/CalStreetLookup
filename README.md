# CalStreetLookup
<p>
Mispelled street names are a major cause of geocoding errors. This is especially true if your addresses are acquired over a phone call. These tools create a list of street names in California with their corresponding ZIP Codes and postal cities.
</p>
<p>
It is assumed you already installed and have a working knowledge of <a href="https://qgis.org/en/site/">QGIS</a> (OSGeo4W installation), <a href="https://postgis.net/">PostGIS</a>, <a href="https://www.gdal.org/">GDAL</a>, and <a href="https://www.python.org/">Python</a>. For your convenience, the <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a> includes some details on how to set up PostGIS for running these scripts.
</p>
<p>
<b>You will need some data:</b>
<ul>
  <li>OpenStreetMap (OSM) data is available from <a href="https://www.geofabrik.de/">geofabrik</a>. Note our example uses California shapefile downloads, which Geofabrik split into north and south. These scripts can work with other USA regional shapefile downloads from GeoFabrik.</li>
  <li>USA ZIP Codes data are available from Esri (<a href="http://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24">download here</a>).</li>
</ul>

<b>Some more needed steps are listed below:</b>
<ul>
    <li><b>Create a geospatial database:</b> Using PGAdmin, create a database in Postgres and make it spatially enabled. Boundless <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/createdb.html">provides a few tips</a>, or you can visit the <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a>. Examples used herein use a database named <b>calstreets</b>.
<pre>
CREATE EXTENSION postgis;
</pre>  
</li>
<li><b>Load Esri's USA ZIP Code polygons into your database:</b> Use the <a href="http://docs.qgis.org/2.18/en/docs/user_manual/plugins/plugins_db_manager.html">QGIS DB Manager</a> or the <a href="https://connect.boundlessgeo.com/docs/suite/4.8/dataadmin/pgGettingStarted/pgshapeloader.html">PostGIS Shapefile Import/Export Manager</a> to load the Esri ZIP Code polygons into your database. The sample text below is provided if you prefer to use ogr2ogr in the OSGEO4W Shell. The <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a> includes a few more details.
<pre>
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=<i><b>your user name</b></i> password=<i><b>your password</b></i>" -s_srs EPSG:4326 -t_srs EPSG:4326 zip_poly.gdb -sql "SELECT ZIP_CODE, PO_NAME, STATE FROM zip_poly AS USA_ZIP_POLY" -overwrite -progress --config PG_USE_COPY YES -nlt MULTIPOLYGON
</pre> 
</li>
<li><b>Install the Unidecode Python Library:</b> Open the OSGeo4W Shell and enter the text below. Again, the <a href="https://github.com/johnhickok/CalStreetLookup/wiki">wiki</a> includes a few more details.
<pre>
python -m pip install Unidecode
</pre>
</li> 
<li><b>Make Some Edits:</b> When you create databases in or install Postgres, you will use passwords and database names of your choosing. You will need to edit your copies of <b><i>csv2postgres.py</i></b> and <b><i>merge_join.py</i></b> with your database names and passwords. In addition, the geospatial SQL in <b><i>merge_join.py</i></b> narrows the USA ZIP Codes table to California to speed up your spatial join. Please update this expression if you are working with other regions.
</li>
</ul>  

John Hickok, 2019-01-18
</p>
