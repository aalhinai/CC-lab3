## the idea based on the toturial https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps


# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

from celery import Celery

filterKeywords = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
wordcount={}

#create a celery application instance that connects to the default RabbitMQ service
app = Celery('tasks', backend='amqp', broker='amqp://')

#the job of this celery task function is to count the frequncy of the keywords
#in each json format file that has been passed to it and rutren the results
#as dictionary list 
@app.task
def count_keywords(tweets_filename):
        #global counter
        tweets_file = open(tweets_filename, "r")
	for line in tweets_file:
	    try:
		# Read in one line of the file, convert it into a json object 
		tweet = json.loads(line.strip())
		for keyword in filterKeywords:
                    if tweet.has_key("retweeted_status") or ('RT' in tweet["text"].split()) :   #ignore retweeted tweet
                          continue
	            else:
                         for word in tweet["text"].split():
                           if keyword == word.lower(): 
			      if keyword not in wordcount:
			         wordcount[keyword] = 1
			      else:
			        wordcount[keyword] += 1
                           else:
                              continue
	    except:
		# read in a line is not in JSON format (sometimes error occured)
	     continue

	return wordcount
