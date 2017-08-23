# CalStreetLookup

These tools extract a list of street names in California, spatially joined to ZIP Codes. This is to be a rewrite from earlier projects, but with better documentation.

If you need some training using PostGIS, take this <a href="http://workshops.boundlessgeo.com/postgis-intro/">online workshop</a>, provided by Boundless.

You will need some data:
OpenStreetMap (OSM) data is available from geofabrik.
USA ZIP Codes data is available from Esri.

Some steps to take are listed below. The following steps are listed to teach you more about PostGIS while minimizing the abount of programming you'll need to do.

Use ArcGIS, QGIS, or any other desktop GIS software to create a statewide shapefile of your ZIP Codes
Create another shapefile with just a few selected streets from OSM.

<pre>
CREATE TABLE public.roads
(
  gid SERIAL PRIMARY KEY,
  name character varying(150),
  geom geometry(LineString,4326)
)
;
</pre>


For your selected roads shapefile, remove all fields but the street name.
Use PGAdmin to create the database for your joins.
Use PGshapeloader to load the above shapefiles into your database.
Alter your roads table geometry type from Multilinestring to Linestring.
Copy and save your SQL that created your spatial index for your roads table.
Drop your roads table spatial index.
Truncate your roads table.

Use desktop GIS to save your entire OSM roads shapefile to CSV with WKT values for the geometry.
Use the Python script xxx.py in this repository to convert your roads CSV to SQL insert statements.
Run the insert statements to load values into your roads table.
Run the SQL to replace the roads spatial index
Vacuum analyze your database (recommended for Posgress.
