import reddit
from db import Database
import signal, sys
from functools import partial
import schedule, time
# handle sigint
def signal_handler(database, sig, frame):
    # cleanup here
    print('Exiting...')
    database.close()
    sys.exit(0)

def main():
    if __name__=='__main__':
        # init database
        database = Database('data/reddit.db')
        print('Database initialized.')
        # Register signal handler
        signal.signal(signal.SIGINT, partial(signal_handler, database))
        # run immediatly at launch
        reddit.collect_data(database=database)
        # Collect data every 5 minutes
        schedule.every(2).hours.do(reddit.collect_data, 50, None, database)
    while True:
        schedule.run_pending()
        time.sleep(60)
        
main()