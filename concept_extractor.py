import nltk
import string
import collections

def load_data(filename='data/TweetData.txt'):
    tweet_file = open(filename)
    tweets = []
    for i,tweet in enumerate(tweet_file):
        # Skip first header line
        if i == 0:
            continue
        # Remove the two first and the last column
        words = tweet.split(" ")[2:-1]
        # Only keep english tweets
        if words[-1] == 'en':
            tweets.append(words[:-1])
    return tweets

def preprocess_data(tweets):
    for i,tweet in enumerate(tweets):
        # Remove urls
        tweets[i] = [x for x in tweet if not 'http' in x]
        # Remove non-ascii characters
        for j,word in enumerate(tweets[i]):
            tweets[i][j] = "".join([c for c in word if c in string.printable])
        # Remove retweet headers
        if tweets[i][0] == 'RT':
            tweets[i] = tweets[i][2:]
        # Remove @ and capitalize word
        tweets[i] = [ x[1:].capitalize() if x.startswith('@') else x for x in tweets[i] ]
    return collections.Counter([ ' '.join(x) for x in tweets ])

tweets = preprocess_data(load_data())

for tweet in tweets.keys():
    print [tweet, tweets[tweet]]