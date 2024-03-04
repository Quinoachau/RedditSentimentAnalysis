import praw
import re
import numpy as np
import pandas as pd
from praw.models import MoreComments
from textblob import TextBlob


posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": []
              }

post_comments = []
pcomments = []
ncomments = []
neutral = []



class RedditClient(object):
    
    def __init__(self):
        self.reddit_read_only = praw.Reddit(client_id="BaKNw2tt2llud_6yjW5ePQ",         
                                            client_secret="p4YqpO0wtHYP47U2C02WkgRHRMAQLw",      
                                            user_agent="PythonScraping")        
        self.subreddit = self.reddit_read_only.subreddit("todayilearned")
        
        
        
    def setSubreddit(self,s):
        self.subreddit = self.reddit_read_only.subreddit(s)
        
    def getSubreddit(self):
        return self.subreddit
    
    def getRedditReadOnly(self):
        return self.reddit_read_only
    
    def getPosts(self):
        return self.subreddit.top('day')
    
    def populate(self):
        posts = self.getPosts()
        global posts_dict
        counter = 0
        for post in posts:
            posts_dict["Title"].append(post.title)
            posts_dict["Post Text"].append(post.selftext)
            posts_dict["ID"].append(post.id)
            posts_dict["Score"].append(post.score)
            posts_dict["Total Comments"].append(post.num_comments)
            posts_dict["Post URL"].append("https://www.reddit.com" + post.permalink)
            counter +=1
            if counter == 10:
                break
        
        top_posts = pd.DataFrame(posts_dict)
        top_posts.to_csv("Top_Posts.csv", index=True)  
        
    def getComments(self):
        global posts_dict
        for post_url in posts_dict["Post URL"]:
            submission = self.reddit_read_only.submission(url=post_url)
                
            for comment in submission.comments:
                if type(comment) == MoreComments:
                    continue
                post_comments.append(comment.body)
                    
        comments_df = pd.DataFrame(post_comments, columns=['top comments'])
        comments_df.to_csv("TopComments.csv", index=False)
        
    def cleanComments(self, comment):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())
        
    def get_comment_sentiment(self, comment):
        analysis = TextBlob(self.cleanComments(comment))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
        
def main():
    api = RedditClient()
    api.setSubreddit('csgo')
    api.populate()
    api.getComments()
    for comment in post_comments:
        if api.get_comment_sentiment(comment) == 'positive':
            pcomments.append(comment)
        elif api.get_comment_sentiment(comment) == 'negative':
            ncomments.append(comment)
        else:
            neutral.append (comment)
    print("Positive comments percentage: {:.2f} %".format(100*len(pcomments)/len(post_comments)))
    print("Negative comments percentage: {:.2f} %".format(100*len(ncomments)/len(post_comments)))
    print("Neutral comments percentage: {:.2f} %".format(100*len(neutral)/len(post_comments)))
    
    print("\n\nPositive comments:")
    for comment in pcomments[:1]:
        print(comment)
        
    print("\n\nNegative comments:")
    for comment in ncomments[:1]:
        print(comment)
    
            
            
    
    
    
    
if __name__ == "__main__":
    # calling main function
    main()
    

