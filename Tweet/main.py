import tweepy
import pandas as pd
import os
 
# consumer keys and access tokens, used for OAuth
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# creation of the actual interface, using authentication
api = tweepy.API(auth, wait_on_rate_limit=True)

data = []

for tweet in tweepy.Cursor(api.search, q="#NicolasMaduro", count=100,
                           lang="es",
                           since="2019-02-01").items():
    item = [tweet.created_at, tweet.user.name, tweet.text, tweet.retweet_count, tweet.favorite_count]
    print(tweet.created_at, tweet.user.name, tweet.text, tweet.retweet_count, tweet.favorite_count)
    data.append(item)

df = pd.DataFrame(data, columns=['timestamp', 'author', 'text', 'rts', 'favs'])
df.to_csv('nico.csv', line_terminator='\n', index=False)