import praw
import numpy as np
import pandas as pd
from praw.models import MoreComments
from textblob import TextBlob



reddit_read_only = praw.Reddit(client_id="BaKNw2tt2llud_6yjW5ePQ",         # your client id
                               client_secret="p4YqpO0wtHYP47U2C02WkgRHRMAQLw",      # your client secret
                               user_agent="PythonScraping")        # your user agent
 
# Authorized instance
reddit_authorized = praw.Reddit(client_id="BaKNw2tt2llud_6yjW5ePQ",         # your client id
                                client_secret="p4YqpO0wtHYP47U2C02WkgRHRMAQLw",      # your client secret
                                user_agent="PythonScraping",        # your user agent
                                username="CreepCrawler123",        # your reddit username
                                password="") 

subreddit = reddit_read_only.subreddit("todayilearned")

print("Display name:", subreddit.display_name)
# Display the title of the Subreddit
print("Title:", subreddit.title)
 
# # Display the description of the Subreddit
# print("Description:", subreddit.description)
time = time_filter = "month"
posts = subreddit.top(time)

posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": []
              }

for post in posts:
        # Title of each post
    posts_dict["Title"].append(post.title)
     
    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)
     
    # Unique ID of each post
    posts_dict["ID"].append(post.id)
     
    # The score of a post
    posts_dict["Score"].append(post.score)
     
    # Total number of comments inside the post
    posts_dict["Total Comments"].append(post.num_comments)
     
    # URL of each post like actual url not url within post
    posts_dict["Post URL"].append("https://www.reddit.com" + post.permalink)
    
top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv("Top_Posts.csv", index=True)

counter =0
post_comments = []
url = ""

for i in posts_dict["Post URL"]:
    url = i
    submission = reddit_read_only.submission(url=url)
    
    for comment in submission.comments:
        if type(comment) == MoreComments:
            continue
        post_comments.append(comment.body)
    
    counter += 1
    if counter == 1:
        break
    
comments_df = pd.DataFrame(post_comments, columns=['top comments'])

# Save the DataFrame to 
comments_df.to_csv("Top5Comments.csv", index=False)


