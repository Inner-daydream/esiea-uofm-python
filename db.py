import sqlite3 as sql

def init(database_name):
    conn = sql.connect(database_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id TEXT PRIMARY KEY, title TEXT, timestamp INTEGER, nsfw INTEGER)''')
    conn.commit()
