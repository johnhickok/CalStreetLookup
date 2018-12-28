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

echo %time% Begin running shp2csv.py to convert shapefiles to CSV

python shp2csv.py


:: If you'd rather run ogr2ogr on the commad line, remark out the line above and unremark those lines below
:: echo %time% Converting norcal_gis_osm_roads_free_1.shp to roads_wkt_norcal.csv
:: call C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt_norcal.csv norcal_gis_osm_roads_free_1.shp -lco GEOMETRY=AS_WKT
:: echo %time% Converting socal_gis_osm_roads_free_1.shp to roads_wkt_socal.csv
:: call C:\OSGeo4W64\bin\ogr2ogr -f CSV roads_wkt_socal.csv socal_gis_osm_roads_free_1.shp -lco GEOMETRY=AS_WKT
:: echo %time% End script. Run process_2.bat in a new window.


echo %time% End converting shapefiles to CSV

