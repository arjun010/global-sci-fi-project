import praw
import csv
import unicodedata

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

# print topics_dict.keys()
writer = csv.writer(open('data.csv','wb'))
writer.writerow(topics_dict.keys())
for i in range(0,100):
    postData = []
    for key in topics_dict.keys():
        val = topics_dict[key][i]
        # print type(val)
        if type(val) is unicode:
            val = unicodedata.normalize('NFKD', val).encode('ascii','ignore')
            # val = val.encode('utf-8')        
        postData.append(val)
    # print postData
    # print len(postData)
    writer.writerow(postData)