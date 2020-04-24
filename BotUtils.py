import praw, re
from functools import reduce

def get_all_comments(reddit, username):
    redditor = reddit.redditor(username)
    params = {
        'after': '',
        'count': 100
    }
    comments = {}
    recent_comments = [comment for comment in redditor.comments.new(limit=100,params=params)]
    count = 0
    while len(recent_comments) > 0:
        params['after'] = f"t1_{recent_comments[-1].id}"
        params['count'] = len(comments)
        for comment in recent_comments:
            comments[comment.id] = comment
        recent_comments = [comment for comment in redditor.comments.new(limit=100,params=params)]
    return comments


def get_all_submissions(reddit, username):
    redditor = reddit.redditor(username)
    params = {
        'after': '',
        'count': 100
    }
    submissions = {}
    recent_submissions = [submission for submission in redditor.submissions.new()]
    while len(recent_submissions) > 0:
        params['after'] = f"t3_{recent_submissions[-1].id}"
        params['count'] = len(submissions)
        for submission in recent_submissions:
            submissions[submission.id] = submission
        recent_submissions = [submission for submission in redditor.submissions.new(params=params)]
    return submissions

def pretty_decimal(num):
    return f"{int(num)}.{int(num * 10) % 10}{int(num * 100) % 10}"
