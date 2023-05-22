# oauth login to reddit api
from config import RedditConfig
import praw


reddit = praw.Reddit(
    client_id=RedditConfig.CLIENT_ID,
    client_secret=RedditConfig.CLIENT_SECRET,
    user_agent=RedditConfig.USER_AGENT
)

def query_popular_nsfw(popular_limit, submission_limit, database):
    popular_subs = reddit.subreddits.popular(limit=popular_limit)
    for sub in popular_subs:
        for submission in sub.new(limit=submission_limit):
            database.insert_submission(submission.id, submission.title, submission.created_utc, submission.over_18)


