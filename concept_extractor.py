from nltk import pos_tag
import string
import collections
from nltk.tokenize import TweetTokenizer
from nltk.text import TextCollection
import math
import re
import operator


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
    VALID_CHARACTERS = string.ascii_letters + string.digits + '-.,;:!?' + "'"
    for i,tweet in enumerate(tweets):

        # Remove urls and quotemarks
        tweets[i] = [x.replace('"','') for x in tweet if not 'http' in x]

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
                hashtags.update([tweets[i][j][1:].lower()])
            else:
                break
        
        # Remove '#' and '...' at the end
        tmp = tweets[i][:end_sentence + 1]
        if tmp[-1].endswith('...'):
            tmp = tmp[:len(tmp)-1]

        # Remove invalid characters / keep valid characters
        for i, word in enumerate(tmp):
            tmp[i] = ''.join([x for x in word if x in VALID_CHARACTERS])
        
        # Remove hashtag character in tweet text
        tweet_text = ' '.join(tmp).replace('#', '')
        unique_tweets.update([tweet_text])

    return (unique_tweets, hashtags)

def extract_chunks(tweets):
    # Extract chunks out of tweets

    VALID_CONTEXTS = [
        re.compile("(  NN)+"), 
        re.compile("(  NN)+( NNS)"), 
        re.compile("( NNP)+"), 
        re.compile("( NNP)+(NNPS)")
        # re.compile(" JJ(S|R)(  NN)+"), 
        # re.compile(" JJ(S|R)(  NN)+( NNS)"), 
        # re.compile(" JJ(S|R)( NNP)+"), 
        # re.compile(" JJ(S|R)( NNP)+(NNPS)"),
        # re.compile("  JJ(  NN)+"), 
        # re.compile("  JJ(  NN)+( NNS)"), 
        # re.compile("  JJ( NNP)+"), 
        # re.compile("  JJ( NNP)+(NNPS)")
    ]

    tokenizer = TweetTokenizer()
    chunks = collections.Counter()

    # Tokenize and pos-tag tweet
    postagged_tweets = [ (pos_tag(tokenizer.tokenize(x)), occurences) for x, occurences in tweets.items() ]
    for tweet in postagged_tweets:
        tags = tweet[0]

        # Create tagged POS sequence
        tag_string = ''.join([x[1].rjust(4, ' ') for x in tags])

        # Extract chunks
        for regex in VALID_CONTEXTS:
            for match in regex.finditer(tag_string):
                # Map POS to text and save chunks
                chunk = tags[int(match.start() / 4) : int(match.end() / 4)]
                chunk_string = [' '.join([tag[0].lower() for tag in chunk])]
                for _ in range(tweet[1]):
                    chunks.update(chunk_string)
            
    return chunks

tweets, hashtags = preprocess_data(load_data())
chunks = extract_chunks(tweets)

for hashtag, times in hashtags.items():
    for _ in range(int(times*0.25)):
        chunks.update(hashtags)

# Reduce single word significance
for chunk in chunks:
    chunk_expression = re.compile(r'(\s+|^){}(\s+|$)'.format(chunk))
    for other_chunk in chunks:
        if chunk == other_chunk:
            continue
        elif chunk_expression.search(other_chunk) != None:
            chunks[chunk] -= chunks[other_chunk]

print chunks.most_common(10)