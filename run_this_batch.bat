:: process.bat is a CMD batch file that geoprocesses your GeoFabrik downloads in this folder
:: updated 2020-01-01 in response to pip no longer updating Python 2.x in the OSGeo4W shell

:: Run this in a CMD shell, in the folder these scripts are running
python extract_roads.py

:: Convert this CMD to an OSGEO4W shell:
call C:\OSGeo4W64\bin\o4w_env.bat
python shp2csv.py

:: Open a new CMD to this folder to use the Unidecode library
C:\Python27\python convert_utf8.py

:: Go back to the CMD window you made into an OSGeo4W shell
python csv2postgres.py

:: Set env in OSGeo4W shell to run Python 3 to use psychopg2 library
py3_env
python merge_join.py

python make_sqlite_db.py
