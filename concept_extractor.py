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
    hashtags = collections.Counter()
    unique_tweets = collections.Counter()
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

        # Remove #words at the end of the tweet and remove # in the remaining tweet
        end_sentence = len(tweets[i])-1
        for j, word in reversed(list(enumerate(tweets[i]))):
            end_sentence = j
            if word.startswith('#'):
                hashtags.update([tweets[i][j][1:]])
            else:
                break
        
        # Remove hashtag character in tweet text
        tweet_text = ' '.join(tweets[i][:end_sentence + 1]).replace('#', '')
        unique_tweets.update([tweet_text])
        
    return (unique_tweets, hashtags)

tweets, hashtags = preprocess_data(load_data())

for tweet in tweets.keys():
     print [tweet, tweets[tweet]]

# for hashtag in hashtags.keys():
#     print [hashtag, hashtags[hashtag]]