# extract_roads.py is a Python script that iterates through your GeoFabrik
# zip archives in this folder, extracts just the shapefiles representing roads,
# then renames the files for regions you downloaded.

import zipfile, glob, os

# Get a list of the zipped shapefiles from GeoFabrik

zip_list = []

for i in glob.glob('*.zip'):
  if 'latest-free.shp' in i:
    zip_list.append(i)

# Extract roads shapefiles and rename according to regions
for archive in zip_list:
  region = archive.split('-')[0]
  roads_shp = []
  archive_open = zipfile.ZipFile(archive)
  for file in zipfile.ZipFile.namelist(archive_open):
    if 'roads' in file:
      archive_open.extract(file)
      os.rename(file, region + '_' + file)
  archive_open.close()
