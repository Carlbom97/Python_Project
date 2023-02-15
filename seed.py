import sqlite3
import csv

conn = sqlite3.connect("Allsvenskan.db")
cur = conn.cursor()

file = open("teams.csv")
data = csv.reader(file)
header = None
for row in data:
    if not header:
        header = row
        continue
    cur.execute("INSERT INTO teams (Team_Name, Coach) VALUES (?,?)", tuple(row))

file = open("players.csv")
data = csv.reader(file)
header = None
for row in data:
    if not header:
        header = row
        continue
    cur.execute("INSERT INTO players (Name, Team) VALUES (?,?)", tuple(row))

file.close()
conn.commit()
conn.close()
