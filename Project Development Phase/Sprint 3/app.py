#import Flask
from flask import Flask, render_template, request
import pyrebase
import pickle
model = pickle.load(open('university.pkl','rb'))

config = {
  "apiKey": "AIzaSyBLcGYGA82pCAHW4xKjgDYv_bsnEJEgo1E",
  "authDomain": "universityadmitpredictor.firebaseapp.com",
  "projectId": "universityadmitpredictor",
  "storageBucket": "universityadmitpredictor.appspot.com",
  "messagingSenderId": "938493164189",
  "databaseURL": "https://console.firebase.google.com/u/0/project/universityadmitpredictor/database/universityadmitpredictor-default-rtdb/data/~2F",
}


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def homepage():
    if request.method == 'POST':
        unsuccessful = 'Please check your credentials'

        email = request.form['name']
        password = request.form['pass']

        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html')
        except:
            auth.create_user_with_email_and_password(email,password)
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html')


    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])    
    if request.method == 'POST':
        gre = request.form['gre']
        toefl = request.form['toefl']
        universityNumber = request.form['universityNumber']
        sop = request.form['sop']
        lor = request.form['lor']
        cgpa = request.form['cgpa']
        research = request.form['research']

        y_pred = [[gre, toefl, universityNumber, sop, lor, cgpa, research]]
        print(y_pred)
        prediction_value = model.predict(y_pred)
        print(prediction_value)
        if prediction_value == 'Yes':
            return render_template('chance.html')
        if prediction_value == 'No':
            return render_template('Nochance.html')
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)