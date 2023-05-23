import sqlite3 as sql
import pandas as pd
import os

class Database(object):
    def __init__(self,database_name):
        os.mkdir('data') if not os.path.exists('data') else None
        self.conn = sql.connect(database_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS submissions
                    (id TEXT PRIMARY KEY, title TEXT, timestamp INTEGER, nsfw INTEGER, author TEXT, locked INTEGER, upvote_ratio REAL, score INTEGER, num_comments INTEGER)''')
        self.conn.commit()

    def insert_submission(self, id, title, timestamp, nsfw, author, locked, upvote_ratio, score, num_comments):
        self.cur.execute('''INSERT OR IGNORE INTO submissions VALUES (?,?,?,?,?,?,?,?,?)''', 
                        (id, title, timestamp, nsfw, author, locked, upvote_ratio, score, num_comments))
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def export_csv(self, path):
        df = pd.read_sql_query("select * from submissions", self.conn)
        df.to_csv(path, index=False)

        