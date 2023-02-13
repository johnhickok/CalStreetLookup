:: process.bat is a CMD batch file that geoprocesses your GeoFabrik downloads in this folder
:: updated 2020-01-01 in response to pip no longer updating Python 2.x in the OSGeo4W shell

:: Run this in a CMD shell, in the folder these scripts are running
python extract_roads.py

:: Convert this CMD to an OSGEO4W Shell:
call C:\OSGeo4W64\bin\o4w_env.bat

:: Set the OSGeo4W Shell env to run Python 3
call py3_env

python shp2csv.py
python convert_utf8.py
:: (You might need to run convert_utf8_py2.py with Python 2.7)
python csv2postgres.py
python merge_join.py
python make_sqlite_db.py
