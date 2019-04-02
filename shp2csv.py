# shp2csv.py converts shapefiles to CSVs with geometry expressed as WKT values

import zipfile, glob, os, time

print(time.strftime('%X') + ' Begin running shp2csv.py')

# Get a list of the zipped shapefiles from GeoFabrik
zip_list = []
roads_shp = []

for i in glob.glob('*.zip'):
  if 'latest-free.shp' in i:
    zip_list.append(i)

for archive in zip_list:
  region = archive.split('-')[0]
  archive_open = zipfile.ZipFile(archive)
  for file in zipfile.ZipFile.namelist(archive_open):
    if 'roads' in file and '.shp' in file:
      roads_shp.append(region + '_' + file)
  archive_open.close()

# Create and run ogr2ogr expressions on the command line
for filename in roads_shp:
  file_prefix = filename.split('.')[0]
  ogrstring = 'ogr2ogr -f CSV '
  ogrstring += file_prefix
  ogrstring += '.csv '
  ogrstring += filename
  ogrstring += ' -lco GEOMETRY=AS_WKT'
  print (time.strftime('%X') + ' converting ' + filename + '...')
  os.system(ogrstring)

print(time.strftime('%X') + ' End running shp2csv.py')




