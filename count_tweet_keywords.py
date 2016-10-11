#the idea of source has been taked from http://socialmedia-class.org/twittertutorial.html

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# use the file saved from the container at SSC
#tweets_filename = '05cb5036-2170-401b-947d-68f9191b21c6'
tweets_filename = 'my_tweet_test'
tweets_file = open(tweets_filename, "r")
#from collections import defaultdict


#filterKeywords = [' han ', ' hon ', ' den ', ' det ', ' denna ', ' denne ', ' hen ']
filterKeywords = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
wordcount={}
count = 0


for line in tweets_file:
    try:
        # Read in one line of the file, convert it into a json object 
        #tweet = json.loads(line.strip())
        tweet = json.loads(line)
            #if any([i for i in filterKeywords if i in tweet["text"]]):
        for word in filterKeywords:
            if (word in tweet["text"].split() and ('RT' not in tweet["text"].split())):  #ignore RT retweet (tweet["retweeted"] == False)):
              print('Tweet found filtered by  ' + word )
              print tweet['text']
              count+=1
              if word not in wordcount:
                    wordcount[word] = 1
              else:
                    wordcount[word] += 1
    except:
        # read in a line is not in JSON format (sometimes error occured)
     continue

print('Number of Word matched  ' + str(count))
for k,v in wordcount.items():
    print k, v
