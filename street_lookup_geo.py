# street_lookup_geo.py queries a PostgreSQL database and appends a list of zipcodes
# and street names into streetlist.txt. Geospatial data used is OpenStreetMap Roads
# and Esri USA ZIP Code polygons.
# John Hickok 2025

import webbrowser, psycopg2, os

# clear the screen
os.system('cls')

# set up a cursor for postgres database
conn = psycopg2.connect(
  host='localhost',
  dbname='<your database name>', 
  user='<your database user name>', 
  password='<your database password>'
  )
cur = conn.cursor()

# Ask for user input in the CMD Console
print ("""
This program asks you for the ZIP Code, (no street name, city).
You can enter all or part of any of these categories.
Blank entries return everything.
"""
)

user_zip = input( "Enter Zip Code:  " )
user_street = input( "Enter Part of Street Name:  " )
user_city = input( "Enter Part of City:  " )
print ("")

# Create variables to display search terms back to the user
if user_zip == "":
    user_zip_display = "Any"
else:
    user_zip_display = user_zip

if user_street == "":
    user_street_display = "Any"
else:
    user_street_display = user_street

if user_city == "":
    user_city_display = "Any"
else:
    user_city_display = user_city


# Open streetlist.txt and add user search terms and field headers
streetlist_file = open("streetlist.txt", "w")
streetlist_file.write("Data per OpenStreetMap + Esri\n")
streetlist_file.write("Your search: Street = '" + user_street_display + "', City = '" + 
user_city_display + "', ZIP Code = '" + user_zip_display + "'\n\n")
streetlist_file.write("STREET, CITY, STATE + ZIP\n")

# parse a query search string qsearch and iterate database output into streetlist.txt

qsrch = ("""
select distinct
o.name,
z.po_name as city,
'CA' as st,
z.zip_code
from (select * from usa_zip_poly where state like 'CA') z
join osm_roads o
on st_intersects(z.geom, o.geom)
where z.zip_code like '%user_zip%'
and o.name ilike '%user_street%'
and z.po_name ilike '%user_city%'
order by o.name, z.po_name
limit 10000
"""
)

qsrch = qsrch.replace('user_zip', user_zip)
qsrch = qsrch.replace('user_street', user_street)
qsrch = qsrch.replace('user_city', user_city)

cur.execute(qsrch)

for row in cur.fetchall():
  streetlist_file.write(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + " " + str(row[3]) + "\n")

conn.close()
streetlist_file.close()

# Display streetlist.txt
webbrowser.open("streetlist.txt")

