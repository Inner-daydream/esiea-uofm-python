# oauth login to reddit api
from config import RedditConfig
import praw
from datetime import datetime
import time
import pprint


reddit = praw.Reddit(
    client_id=RedditConfig.CLIENT_ID,
    client_secret=RedditConfig.CLIENT_SECRET,
    user_agent=RedditConfig.USER_AGENT
)

def get_popular_subreddits(limit):
    """Returns a list of popular subreddits."""
    subreddits = []
    for sub in reddit.subreddits.popular(limit=limit):
        subreddits.append(sub)
    return subreddits

# def query_popular_nsfw(popular_limit, submission_limit, database):
#     popular_subs = reddit.subreddits.popular(limit=popular_limit)
#     for sub in popular_subs:
#         for submission in sub.new(limit=submission_limit):
#             database.insert_submission(submission.id, submission.title, submission.created_utc, submission.over_18)

# reddit submissions within timeframe from the api
def submissions_within_timeframe(start, end, submission_limit,subreddit):
    """Returns a list of submissions within the timeframe from the api."""
    submissions = []
    for submission in subreddit.new(limit=submission_limit):
        if start <= submission.created_utc <= end:
            submissions.append(submission)
    return submissions

def store_submissions(submissions, database):
    """Stores submissions in the database."""
    for submission in submissions:
        try:
            author = submission.author.name
        except AttributeError:
            author = '[deleted]'
        database.insert_submission(submission.id, 
                                    submission.title, 
                                    submission.created_utc, 
                                    submission.over_18,
                                    author,
                                    submission.locked,
                                    submission.upvote_ratio,
                                    submission.score,
                                    submission.num_comments)
        
def collect_data(subreddit_limit=50, submission_limit=None, database=None):
    print("Starting a job.")
    popular_subreddits = get_popular_subreddits(subreddit_limit)
    for sub in popular_subreddits:
        print(f"Collecting data from r/{sub.display_name}")
        now =  time.time() 
        yesterday = now - 86400 # 86400 seconds in a day
        submissions = submissions_within_timeframe(start=yesterday, 
                                                   end=now, 
                                                   submission_limit=submission_limit, 
                                                   subreddit=sub)
        store_submissions(submissions, database)

