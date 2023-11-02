import sqlite3

# Open connection to database file
connection = sqlite3.connect('database.db')

# Open SQL schema and create the tables
# ex. 'programs' table
with open('schema.sql') as f:
    connection.executescript(f.read())

# Add programs to 'programs' table
cur = connection.cursor()
cur.execute("INSERT INTO programs (title, content) VALUES (?, ?)",
            ('Serial Monitor to CSV', 'This program converts Serial Monitor from the ESP32s into CSV-readable format.')
            )
            
connection.commit()
connection.close()