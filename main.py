#curl -i http://127.0.0.1:5000/keywords-in-tweets-app/api/v0.1/tasks
# http://127.0.0.1:5000/keywords-in-tweets-app/api/v0.1/charts

#the tutorial for pie chart http://www.pygal.org
# https://pythonprogramming.net/pygal-tutorial/


from celery_tasks import count_keywords
from flask import Flask,jsonify, json, render_template
import pygal

app = Flask(__name__)

counter = count_keywords('05cb5036-2170-401b-947d-68f9191b21c6')



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
    app.run(debug = True)
