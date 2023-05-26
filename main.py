import reddit
from db import Database
import signal, sys
from functools import partial
import schedule, time
from config import AppConfig
import frontend

# handle sigint
def signal_handler(database, sig, frame):
    shutdown(database)

def shutdown(database):
    print('\nExiting...')
    database.close()
    sys.exit(0)

def routine(database):
    print('Running routine...')
    if AppConfig.UPDATE_SCORE:
        print('->Updating scores...')
        reddit.update_score(database, int(time.time() - AppConfig.SCORE_UPDATE_THRESHOLD))
    if AppConfig.COLLECT_DATA:
        print('->Collecting data...')
        reddit.collect_data(AppConfig.SUBREDDIT_LIMIT, AppConfig.SUBMISSION_LIMIT, AppConfig.COLLECTION_THRESHOLD, database)
    if AppConfig.EXPORT_CSV:
        print('->Exporting to csv...')
        Database.export_csv(database,AppConfig.CSV_PATH)

def main():
    if __name__=='__main__':
        # init database
        database = Database(AppConfig.DATABASE_PATH)
        print('Database initialized.')
        # Register signal handler
        signal.signal(signal.SIGINT, partial(signal_handler, database))
        # run frontend
        frontend.run(port=8080)
        # run immediatly at launch
        routine(database)
        if (AppConfig.RUN_ONCE):
            shutdown(database)
        schedule.every(AppConfig.JOB_FREQUENCY).hours.do(routine, database)
        while True:
            schedule.run_pending()
            time.sleep(AppConfig.POLLING_RATE)
        
main()