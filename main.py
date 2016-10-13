#curl -i http://127.0.0.1:5000/keywords-in-tweets-app/api/v0.1/tasks
# http://127.0.0.1:5000/keywords-in-tweets-app/api/v0.1/charts

#the tutorial for pie chart http://www.pygal.org
# https://pythonprogramming.net/pygal-tutorial/


from celery_tasks import count_keywords
from flask import Flask,jsonify, json, render_template
import pygal
import os
import swiftclient

config = {'user':os.environ['OS_USERNAME'],
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
conn = swiftclient.Connection(auth_version=3, **config)


app = Flask(__name__)

#counter = count_keywords('05cb5036-2170-401b-947d-68f9191b21c6')
#counter = count_keywords('my_tweet_test')
counter = {}
filepath = 'tweets'

#create drirctory to save the downloaded tweets files
if not os.path.isdir(filepath):
   os.makedirs(filepath)

#this is the container name in openstack cloud
bucket_name = "tweets"


#download all tweets  
for data in conn.get_container(bucket_name)[1]:
    obj_tuple = conn.get_object(bucket_name, data)
    with open((filepath+'/'+ os.format(data['name'])), 'w') as my_tweet:
         my_tweet.write(obj_tuple[1]) 
         #read all tweets contents and save the frequncy of keywords in counter verible
         #for filename in os.listdir(filepath):
         counter.update (count_keywords(filepath+'/'+ os.format(data['name'])))
         #delete the object file
         os.remove(filepath+'/'+ os.format(data['name']))


@app.route('/keywords-in-tweets-app/api/v0.1/tasks',methods=['GET'])
def get_tasks():
       with open('results.json', 'w') as outfile:
              json.dump(counter, outfile)
       return jsonify(counter)  #will return the json

@app.route('/keywords-in-tweets-app/api/v0.1/charts', methods=['GET'] )
def keywords_charts():
     try:
        pie_chart = pygal.Pie(height=450)
	pie_chart.title = 'Frequency of Selected Swedish Pronouns in Tweeter Datasets'
        for k, i in counter.items():
            pie_chart.add(k,i)
	
        return pie_chart.render()
     except Exception, e:
	return(str(e))
   

if(__name__ == '__main__'):
    app.run(host='0.0.0.0',debug=True)
