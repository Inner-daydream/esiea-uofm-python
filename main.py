import reddit
from db import Database
import signal, sys
from functools import partial
# handle sigint
def signal_handler(database, sig, frame):
    # cleanup here
    database.close()
    sys.exit(0)

def main():
    if __name__=='__main__':
        # init database
        database = Database('reddit.db')
        # Register signal handler
        signal.signal(signal.SIGINT, partial(signal_handler, database))

        reddit.query_popular_nsfw(popular_limit=10, 
                                  submission_limit=20, 
                                  database=database)

main()