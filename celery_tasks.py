## the idea based on the toturial https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps


# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

from celery import Celery
#from flask import request, jsonify

filterKeywords = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
wordcount={}
#counter = 0
#count = 0



#create a celery application instance that connects to the default RabbitMQ service
app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task
def count_keywords(tweets_filename):
        #global counter
        tweets_file = open(tweets_filename, "r")
	for line in tweets_file:
	    try:
		# Read in one line of the file, convert it into a json object 
		tweet = json.loads(line)
		for word in filterKeywords:
		    if (word in tweet["text"].split() and ('RT' not in tweet["text"].split())):  #ignore RT retweet
		      #print('Tweet found filtered by  ' + word )
		      #print tweet['text']
		      #counter +=1
		      if word not in wordcount:
		            wordcount[word] = 1
		      else:
		            wordcount[word] += 1
	    except:
		# read in a line is not in JSON format (sometimes error occured)
	     continue

	return wordcount
        #return flask.jsonify(wordcount)
