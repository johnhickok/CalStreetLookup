:: process.bat is a CMD batch file that geoprocesses your GeoFabrik downloads in this folder

python extract_roads.py

:: Convert this CMD to an OSGEO4W shell:
call C:\OSGeo4W64\bin\o4w_env.bat

python shp2csv.py
python convert_utf8.py
python csv2postgres.py
python merge_join.py
python make_sqlite_db.py
