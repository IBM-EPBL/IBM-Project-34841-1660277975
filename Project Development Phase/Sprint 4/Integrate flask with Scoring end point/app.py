#import Flask
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import json
import pickle
model = pickle.load(open('university.pkl','rb'))

API_KEY = "w7wZ3NDUKJjLg9ulwEFwDCKCnOurNNLrzp3gZ-SNrbGO"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print(mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def basic():
    if request.method == 'POST':
        gre = request.form['gre']
        toefl = request.form['toefl']
        universityNumber = request.form['universityNumber']
        sop = request.form['sop']
        lor = request.form['lor']
        cgpa = request.form['cgpa']
        research = request.form['research']

        y_pred = [[gre, toefl, universityNumber, sop, lor, cgpa, research]]
        """
        print(y_pred)
        prediction_value = model.predict(y_pred)
        print(prediction_value)
        """
        payload_scoring = {"input_data": [
            {"field": [["GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR ", "CGPA", "Research"]],
             "values": y_pred}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/67f91885-c382-4d94-9b23-60bbc3f65a47/predictions?version=2022-11-18',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        predictions = response_scoring.json()
        print(predictions)
        output = predictions['predictions'][0]['values'][0][0]
        print(output)

        if output == 'Yes':
            return render_template('chance.html')
        if output == 'No':
            return render_template('Nochance.html')
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)