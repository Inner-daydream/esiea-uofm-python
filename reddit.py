# oauth login to reddit api
from config import RedditConfig
import praw
import time


reddit = praw.Reddit(
    client_id=RedditConfig.CLIENT_ID,
    client_secret=RedditConfig.CLIENT_SECRET,
    user_agent=RedditConfig.USER_AGENT
)

def get_popular_subreddits(limit):
    """Returns a list of popular subreddits."""
    subreddits = []
    for sub in reddit.subreddits.popular(limit=int(limit)):
        subreddits.append(sub)
    return subreddits

# reddit submissions within timeframe from the api
def submissions_within_timeframe(start, end, submission_limit,subreddit):
    """Returns a list of submissions within the timeframe from the api."""
    submissions = []
    for submission in subreddit.new(limit=int(submission_limit)):
        if int(start) <= submission.created_utc <= int(end):
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
                                    submission.num_comments,
                                    time.time(),
                                    submission.is_original_content,
                                    submission.is_self
        )
        
def collect_data(subreddit_limit=50, submission_limit=None, threshold=86400, database=None):
    popular_subreddits = get_popular_subreddits(subreddit_limit)
    for sub in popular_subreddits:
        print(f"Collecting data from r/{sub.display_name}")
        now =  time.time() 
        yesterday = now - threshold # epoch time
        submissions = submissions_within_timeframe(start=yesterday, 
                                                   end=now, 
                                                   submission_limit=submission_limit, 
                                                   subreddit=sub)
        store_submissions(submissions, database)


def update_score(database, threshold):
    """Updates the score of all submissions in the database."""
    submissions = database.get_submissions(threshold)
    ids = [f"t3_{submission[0]}" for submission in submissions]
    submissions = reddit.info(fullnames=ids)
    for submission in submissions:
        database.update_submission(score=submission.score, update_time=time.time(), id=submission.id)

    return submissions

