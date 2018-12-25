# This Python 2.x script extracts road shapefiles from northern and southern 
# California Open Street Map files downloaded from Geofabrik

import os, zipfile, subprocess

#Set the current working folder
thisfolder = os.getcwd()

# Extract roads shapefile from norcal
open_zip = zipfile.ZipFile("norcal-latest-free.shp.zip")

file_list = zipfile.ZipFile.namelist(open_zip)

road_list = []

# select the items in the archive including 'roads' in the name
for i in file_list:
  if 'roads' in i:
    road_list.append(i)

for j in road_list:
  open_zip.extract(j)
  os.rename(j, 'norcal_' + j)


# Extract roads shapefile from socal
open_zip = zipfile.ZipFile("socal-latest-free.shp.zip")

# get a list of all the files in the archive
file_list = zipfile.ZipFile.namelist(open_zip)

road_list = []

# select the items including 'roads' in the name
for i in file_list:
  if 'roads' in i:
    road_list.append(i)

for j in road_list:
  open_zip.extract(j)
  os.rename(j, 'socal_' + j)
