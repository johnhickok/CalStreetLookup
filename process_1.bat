:: process_1.bat is a Windows batch file and extracts CSV's from OpenStreetMap shapefles
:: 
:: Before running this Windows batch file,
:: 1. Download these files from geofabrik:
::    a. norcal-latest-free.shp.zip
::    b. socal-latest-free.shp.zip
:: 2. Create folders norcal and socal for these archives and put them in the right folders
:: 3. In each folder, extract the road files (same file names in each folder):
::    a. gis_osm_roads_free_1.cpg
::    b. gis_osm_roads_free_1.dbf
::    c. gis_osm_roads_free_1.prj
::    d. gis_osm_roads_free_1.shp
::    e. gis_osm_roads_free_1.shx

:: Make this cmd shell run OSGeo4W commands
call C:\OSGeo4W64\bin\o4w_env.bat

:: Convert osm_roads_free_1.shp to roads_wkt.csv
echo %time%

call C:\OSGeo4W64\bin\ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=postgres" -s_srs EPSG:4326 -t_srs EPSG:4326 osm_roads_norcal.csv -overwrite --config PG_USE_COPY YES

echo %time%

call C:\OSGeo4W64\bin\ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=postgres" -s_srs EPSG:4326 -t_srs EPSG:4326 osm_roads_socal.csv -overwrite --config PG_USE_COPY YES

echo %time%

:: To remove non-utf8 chars from the above CSVs run convert_utf8.py (Python script) in a new window
