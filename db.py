import sqlite3

def call_db(query: str, *args):
    conn = sqlite3.connect("Allsvenskan.db")
    cur = conn.cursor()
    res = cur.execute(query, args)
    data = res.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def update_db(query: str, *args):
    conn = sqlite3.connect("Allsvenskan.db")
    cur = conn.cursor()
    res = cur.execute(query, args)
    data = res.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def print_db(query: str, *args):
    conn = sqlite3.connect("Allsvenskan.db")
    cur = conn.cursor()
    cur.execute(query, args)
    res = cur.fetchall()

    for x in res:
        print(x)

    cur.close()
    conn.close()
    return res

def get_value(query: str, *args):
    conn = sqlite3.connect("Allsvenskan.db")
    cur = conn.cursor()
    cur.execute(query, args)
    res = cur.fetchone()
    value = res[0]
    cur.close()
    conn.close()
    return value

query = """CREATE TABLE IF NOT EXISTS
    Games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Home_Team VARCHAR(255) NOT NULL,
        Home_Team_id INT NOT NULL,
        Away_Team VARCHAR(255) NOT NULL,
        Away_Team_id INT NOT NULL,
        Home_Coach VARCHAR(255) NOT NULL,
        Away_Coach VARCHAR(255) NOT NULL,
        Home_Goals  INT NOT NULL,
        Away_Goals INT NOT NULL
    );
"""
call_db(query)

query = """CREATE TABLE IF NOT EXISTS
    Players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(255) NOT NULL,
        Team VARCHAR(255)
    );
"""

call_db(query)

query = """CREATE TABLE IF NOT EXISTS
    Teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Team_Name VARCHAR(255) NOT NULL,
        Coach VARCHAR(255)
    );
"""

call_db(query)

