# This Python 2.x script assumes 
# - you downloaded california-latest-free.shp.zip # from Geofabrik.
# (http://download.geofabrik.de/north-america/us/california-latest-free.shp.zip)
# - You used the OSGEO4W installation of QGIS

import os, zipfile, subprocess

#Set the current working folder
thisfolder = os.getcwd()

# Extracts only the roads shapefile
geofabrik = zipfile.ZipFile("california-latest-free.shp.zip")
geofabrik.extract("gis_osm_roads_free_1.cpg")
geofabrik.extract("gis_osm_roads_free_1.dbf")
geofabrik.extract("gis_osm_roads_free_1.prj")
geofabrik.extract("gis_osm_roads_free_1.shp")
geofabrik.extract("gis_osm_roads_free_1.shx")

geofabrik.close()

# rename the shapefile to prep for geoprocessing
os.rename('gis.osm_roads_free_1.cpg', 'osm_roads_free_1.cpg')
os.rename('gis.osm_roads_free_1.dbf', 'osm_roads_free_1.dbf')
os.rename('gis.osm_roads_free_1.prj', 'osm_roads_free_1.prj')
os.rename('gis.osm_roads_free_1.shp', 'osm_roads_free_1.shp')
os.rename('gis.osm_roads_free_1.shx', 'osm_roads_free_1.shx')
