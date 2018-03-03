# streetzip.py queries sqlite database streetz.db and appends a list of zipcodes
# and street names into streetlist.txt. The streetz.db file contains an indexed list
# of street names and zipcodes extracted from OpenStreetMap data for California.

import webbrowser, sqlite3

# Ask for user input in the CMD Console
print """
This program asks you for the ZIP Code, street name, and the city.
You can enter all or part of any of these categories.
Blank entries retun everything.
"""
user_zip = raw_input( "Enter Zip Code:  " )
user_street = raw_input( "Enter Part of Street Name:  " )
user_city = raw_input( "Enter Part of City:  " )
print ""

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
streetlist_file.write("Data per OpenStreetMap!\n")
streetlist_file.write("Your search: Street = '" + user_street_display + "', City = '" + 
user_city_display + "', ZIP Code = '" + user_zip_display + "'\n\n")
streetlist_file.write("STREET, CITY, STATE + ZIP\n")

# parse a query search string qsearch and iterate database output into streetlist.txt
c = sqlite3.connect('streetz.db')
qsrch = ("SELECT [st_name], [community], [zip], [st_count] FROM streetz WHERE zip like '%" + 
user_zip + "%' AND st_name like '%" + user_street + "%' AND community like '%" + user_city + 
"%' ORDER BY [st_name], [zip]")
for row in c.execute(qsrch):
  streetlist_file.write(str(row[0]) + ", " + str(row[1]) + ", CA " + str(row[2]) + "\n")

streetlist_file.close()

# Display streetlist.txt
webbrowser.open("streetlist.txt")
