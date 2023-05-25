import os
class RedditConfig:
    """Contains the configuration for the Reddit API."""
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    USER_AGENT = os.environ.get('USER_AGENT') or 'uofm reddit api project'


class AppConfig:
    """Contains the configuration for the application."""
    COLLECT_DATA = os.environ.get('COLLECT') or True
    UPDATE_SCORE = os.environ.get('UPDATE') or True
    EXPORT_CSV = os.environ.get('EXPORT') or False
    SCORE_UPDATE_THRESHOLD = os.environ.get('SCORE_UPDATE_THRESHOLD') or 60 * 60 * 24 # 24 hours
    COLLECTION_THRESHOLD = os.environ.get('COLLECTION_THRESHOLD') or 60 * 60 * 24 # 24 hours
    SUBMISSION_LIMIT = os.environ.get('SUBMISSION_LIMIT') or None
    SUBREDDIT_LIMIT = os.environ.get('SUBREDDIT_LIMIT') or 50
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'data/reddit.db'
    CSV_PATH = os.environ.get('CSV_PATH') or 'data/reddit.csv'
    JOB_FREQUENCY = os.environ.get('JOB_FREQUENCY') or 2 # 2 hours
    POLLING_RATE = os.environ.get('POLLING_RATE') or 60
    RUN_ONCE = os.environ.get('RUN_ONCE') or False
    



