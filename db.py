import sqlite3 as sql

class Database(object):
    def __init__(self,database_name):
        self.conn = sql.connect(database_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS submissions
                    (id TEXT PRIMARY KEY, title TEXT, timestamp INTEGER, nsfw INTEGER)''')
        self.conn.commit()

    def insert_submission(self, id, title, timestamp, nsfw):
        self.cur.execute('''INSERT INTO submissions VALUES (?, ?, ?, ?)''', (id, title, timestamp, nsfw))
        self.conn.commit()

    def close(self):
        self.conn.close()