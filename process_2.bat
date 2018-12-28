:: process_2.bat is a Windows batch file that calls Python scripts to geoprocess data in PostGIS

echo %time% Begin script
echo %time% Run convert_utf8.py to remove non-utf-8 characters

:: Removes non-utf8 characters. Requires unidecode, see https://pypi.org/project/Unidecode/
python convert_utf8.py

call C:\OSGeo4W64\bin\o4w_env.bat

echo %time% Finished converting to an OSGEO4w shell

echo %time% Loading osm_roads_norcal.csv into PostGIS

call C:\OSGeo4W64\bin\ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=[your password]" -s_srs EPSG:4326 -t_srs EPSG:4326 osm_roads_norcal.csv -overwrite --config PG_USE_COPY YES

echo %time% Loading osm_roads_socal.csv into PostGIS

call C:\OSGeo4W64\bin\ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=calstreets user=postgres password=[your password]" -s_srs EPSG:4326 -t_srs EPSG:4326 osm_roads_socal.csv -overwrite --config PG_USE_COPY YES

echo %time% Running merge_join.py for geoprocessing in PostGIS

python merge_join.py

echo %time% Running make_sqlite_db.py to load streetz.csv into SQLite database streetz.db

python make_sqlite_db.py

echo %time% End script
