:: process_1.bat is a Windows batch file and extracts CSV's from OpenStreetMap shapefles
:: 
:: Before running this Windows batch file,
:: 1. Download these files from geofabrik:
::    a. norcal-latest-free.shp.zip
::    b. socal-latest-free.shp.zip

echo %time% Begin script
echo %time% Run extract_roads.py to extract and rename norcal and socal roads shapefiles

python extract_roads.py

call C:\OSGeo4W64\bin\o4w_env.bat

echo %time% Finished converting to an OSGEO4w shell

echo %time% Converting norcal_gis_osm_roads_free_1.shp to roads_wkt_norcal.csv

call C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt_norcal.csv norcal_gis_osm_roads_free_1.shp -lco GEOMETRY=AS_WKT

:: SoCal: convert socal_gis_osm_roads_free_1.shp to roads_wkt_socal.csv

echo %time% Converting socal_gis_osm_roads_free_1.shp to roads_wkt_socal.csv

call C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt_socal.csv socal_gis_osm_roads_free_1.shp -lco GEOMETRY=AS_WKT

echo %time% End script. Run process_2.bat in a new window.

:: To remove non-utf8 chars from the above CSVs run convert_utf8.py (Python script) in a new window
