:: process_2.bat is a Windows batch file that calls Python scripts to geoprocess data in PostGIS

:: Removes non-utf8 characters. Requires unidecode, see
:: https://pypi.org/project/Unidecode/
python convert_utf8.py

:: Make this an OSGEO Window
call C:\OSGeo4W64\bin\o4w_env.bat

:: Python script does the geoprocessing in PostGIS
python merge_join.py

:: Create sqlite database streetz.db
python make_sqlite_db.py

