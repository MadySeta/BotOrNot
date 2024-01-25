from json import JSONDecodeError
import json
import os
import requests 
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from utils import compute


makePredictionMSURL = "https://makepredictionms.azurewebsites.net"
InfoProcessorMSURL = "https://infoprocessorms.azurewebsites.net"

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
   
@app.route('/user', methods=['POST'])
def user():
   infoProcessor_endpoint = "/extract-user-features"
   predictionUser_endpoint = "/predictionUser"
   name = request.form.get('name')

   if name:
       try:
            params = {"username": name}
            url = InfoProcessorMSURL + infoProcessor_endpoint
            infoResponse = requests.get(url, params=params)
            if infoResponse.status_code == 200:
                extracted_user_features = infoResponse.json()
                
                prediction_url = makePredictionMSURL + predictionUser_endpoint
                predictionResult = requests.get(prediction_url, json=extracted_user_features)
                res = predictionResult.json()
                prediction = res['prediction']
                trust_human = res['trust_human']
                trust_bot = res['trust_bot']
                return render_template('user.html', 
                                    name = name, 
                                    prediction = prediction, 
                                    trust_human = trust_human, 
                                    trust_bot = trust_bot)
            else : 
                return render_template('error.html', name = name)   

       except json.JSONDecodeError as e:
            return render_template('error.html', name = name)   
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/follower', methods=['POST'])
def follower():
   infoProcessor_endpoint = "/extract-followers-features"
   predictionUserFollowers_endpoint = "/predictionUserFollowers"
   name = request.form.get('name')

   if name:
        try:
            params = {"username": name}
            url = InfoProcessorMSURL + infoProcessor_endpoint
            infoResponse = requests.get(url, params=params)
            extracted_user_followers_features = infoResponse.json()

            prediction_url = makePredictionMSURL + predictionUserFollowers_endpoint
            predictionResult = requests.get(prediction_url, json=extracted_user_followers_features)
            
            res = predictionResult.json()

            predictions = res['all_predictions']
            humanprobabilities = res['all_human_probabilities']
            botprobabilities = res['all_bot_probabilities']

            botRatio = compute.BotRatio(predictions)
            botpercentage, humanpercentage = compute.FollowersBotHumanPercentage(humanprobabilities, botprobabilities)

            return render_template('follower.html', 
                                   name = name, 
                                   botRatio = round(botRatio,4), 
                                   botpercentage = round(botpercentage,4),
                                   humanpercentage = round(humanpercentage,4))
        except json.JSONDecodeError as e:
            return render_template('error.html', name = name) 
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)
