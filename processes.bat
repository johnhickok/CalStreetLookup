:: processes.bat extracts openstreetmap replaces PostGIS table osm_roads_ca in database calstreets
:: It is assumed database calstreets already has nationwide zipdodes from Esri
:: http://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24
:: sample code: ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=postgres" -s_srs EPSG:4326 -t_srs EPSG:4326 zip_poly.gdb -sql "SELECT ZIP_CODE, PO_NAME, STATE FROM zip_poly AS USA_ZIP_POLY" -overwrite -progress --config PG_USE_COPY YES

:: Extract gis.osm_roads_free_1.shp from california-latest-free.shp.zip; 
:: rename to osm_roads_free_1.shp
python extract_roads.py

:: Make this cmd shell run OSGeo4W commands
call C:\OSGeo4W64\bin\o4w_env.bat

:: Convert osm_roads_free_1.shp to roads_wkt.csv
call C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt.csv osm_roads_free_1.shp -lco GEOMETRY=AS_WKT

:: Remove non-utf8 chars from roads_wkt.csv; output osm_roads_ca.csv
python convert_utf8.py

:: Replace PostGIS table osm_roads_ca with osm_roads_ca.csv
call C:\OSGeo4W64\bin\ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=postgres" -s_srs EPSG:4326 -t_srs EPSG:4326 osm_roads_ca.csv -overwrite --config PG_USE_COPY YES

:: Vacuum analyize osm_roads_ca
psql -h localhost -p 5432 -U postgres -d calstreets -q -c "VACUUM ANALYZE osm_roads_ca;"

:: Spatially join roads and ZIP Codes, then export streetz.csv
psql -h localhost -p 5432 -U postgres -d calstreets -q -o streetz.csv -A -t -f street_zip_summary.sql

:: Create sqlite database streetz.db
python make_sqlite_db.py

:: Double-click streetzip.py and follow the prompts to get a list of streets.
