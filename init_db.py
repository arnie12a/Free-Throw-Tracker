import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO freethrowlog (sessionDate, ftMade, ftAttempted, locationName) VALUES (?, ?, ?, ?)",
            ('11/12/2023', 23, 25, 'Madison')
            )

cur.execute("INSERT INTO freethrowlog (sessionDate, ftMade, ftAttempted, locationName) VALUES (?, ?, ?, ?)",
            ('12/22/2023', 12, 15, "South Barrington")
            )

connection.commit()
connection.close()