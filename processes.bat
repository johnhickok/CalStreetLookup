:: This file spatially joins statewide OpenStreetMap (OSM) roads to Esri ZIP Code data.
:: This example assumes your database name is calstreets. Edit to suit your needs.

:: Convert OpenStreetMap roads shapefile to CSV with WKT values for geometry
C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt.csv gis.osm_roads_free_1.shp -lco GEOMETRY=AS_WKT
echo converted shp to csv >> log1.txt
echo %time% >> log1.txt

:: Python 2.x script removes non UTF8 characters and streets without names, creates
:: roads_wkt_utf8.sql, later used to reload your new data.
python convert_utf8.py
echo cleaned up csv >> log1.txt
echo %time% >> log1.txt

:: Removes old values from postgres roads table.
psql -h localhost -p 5432 -U postgres -d calstreets -q -c "TRUNCATE TABLE roads;"
echo truncated table >> log1.txt
echo %time% >> log1.txt

:: Drop your spatial index.
psql -h localhost -p 5432 -U postgres -d calstreets -q -c "DROP INDEX roads_geom_idx;"
echo dropped spatial index >> log1.txt
echo %time% >> log1.txt

:: Loads you new data into your roads table. This step takes a while.
psql -h localhost -p 5432 -U postgres -d calstreets -q -f roads_wkt_utf8.sql
echo loaded data >> log1.txt
echo %time% >> log1.txt

:: This step is important for cleaning your postgres database.
psql -h localhost -p 5432 -U postgres -d calstreets -q -c "VACUUM ANALYZE roads;"
echo vacuumed roads >> log1.txt
echo %time% >> log1.txt

:: Re creates your roads spatial index.
psql -h localhost -p 5432 -U postgres -d calstreets -q -c "CREATE INDEX roads_geom_idx ON roads USING gist(geom);"
echo created spatial index >> log1.txt
echo %time% >> log1.txt

:: This step spatially joins roads and ZIP Codes, then exports summary streetz.csv
psql -h localhost -p 5432 -U postgres -d calstreets -q -o streetz.csv -A -t -f street_zip_summary.sql
echo extracted csv >> log1.txt
echo %time% >> log1.txt
