import pandas as pd
import tweepy

# Put your tweepy credentials here
CONSUMER_KEY = "your_CONSUMER_KEY" 
CONSUMER_SECRET = "your_CONSUMER_SECRET"
ACCESS_TOKEN = "your_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "your_ACCESS_TOKEN_SECRET"

# Create tweepy API object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# Scraping Racism tweets with 'Nigga' keyword in them

# Initializing a dataframe
columns=['Racism']
df = pd.DataFrame(columns=columns)

query = 'Nigga' # The keyword to ve searched for 

max_tweets = 1000 # Maximum number of tweets

# Until argument in tweepy.Cursor() specifies the date till which you want to scrape tweets
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query,Until="2015-01-01" ,tweet_mode="extended").items(max_tweets)]

count = 0

# Extract text from the scraped tweets
for j in range(len(searched_tweets)):
    try:
        # Check if it is a re-tweet because re-tweets are extracted differently 
        if searched_tweets[j].retweeted_status:
            res = searched_tweets[j].retweeted_status.full_text
            count+=1
    except:
        res = searched_tweets[j].full_text
    df = df.append({'Racism' : res } , ignore_index=True)

print(count,len(searched_tweets))

# Save tweets in a csv
df.to_csv("Racism.csv")
