# make_sqlite_db.py creates sqlite database streetz.db from file streetz.csv
# More help on importing csv files into sqlite can be found at:
# http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# jhickok2011@gmail.com 2016-07-28

# Import modules, create sqlite database file and table
import csv, sqlite3, time

print(time.strftime('%X') + ' Begin make_sqlite_db.py')

c = sqlite3.connect('.\\streetz.db')
c.execute("CREATE TABLE streetz (st_name text, community text, state text, zip text, st_count integer);")

# Iterate values from streetz.csv, insert values into table streetz
reader = csv.reader(open('streetz.csv', 'r'), delimiter='|')
for row in reader:
    to_db = [row[0], row[1], row[2], row[3], row[4]]
    c.execute("INSERT INTO streetz (st_name, community, state, zip, st_count) VALUES (?, ?, ?, ?, ?);", to_db)
c.commit()

# Create index
c.execute("CREATE INDEX streetz_index on streetz (st_name, zip);")

print(time.strftime('%X') + ' End make_sqlite_db.py')


