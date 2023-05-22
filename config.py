import os
class RedditConfig:
    """Contains the configuration for the Reddit API."""
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    USER_AGENT = os.environ.get('USER_AGENT') or 'uofm reddit api project'
