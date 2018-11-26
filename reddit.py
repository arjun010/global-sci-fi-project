import praw
import csv

reddit = praw.Reddit(client_id='BKgABmF31ARw4w', \
                     client_secret='MQfbvgznD05VRiU1O4CLE4QWo1E', \
                     user_agent='scifihw', \
                     username='asrinivasan40', \
                     password='Susheela1058')

subreddit = reddit.subreddit('shortscifistories')

top_subreddit = subreddit.top()

topics_dict = { "title":[], \
                "score":[], \
                "id":[], "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[]}
for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
