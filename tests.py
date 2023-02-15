import sqlite3
from db import call_db

query = """UPDATE players SET Team = 'AIK' WHERE id = 100"""

conn = sqlite3.connect("Allsvenskan.db")
cur = conn.cursor()
cur.execute(query)
res = cur.fetchall()
conn.commit()

cur.close()
conn.close()