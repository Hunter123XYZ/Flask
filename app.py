from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

model = pickle.load(open('model.pkl', 'rb'))
test=pd.read_csv("test_data.csv")
x_test=test.drop('prognosis',axis=1)

class Patients(db.Model):
    #primary_key means a unique identifier (ex: patient number)

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    diagnosis = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id
    
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/input',methods=['POST','GET'])
def input():
    title = "Input"
    # return render_template('input.html', title = title)
    if request.method=="POST":
        col=x_test.columns
        patient_name = request.form['name']
        s1 = request.form['s1']
        s2 = request.form['s2']
        s3 = request.form['s3']

        #make it combine the symptoms (look at Disease.py for formatting)
        inputt = [s1, s2, s3]

        b=[0]*132
        for x in range(0,132):
            for y in inputt:
                if(col[x]==y):
                    b[x]=1
        b=np.array(b)
        b=b.reshape(1,132)
        prediction = model.predict(b)
        prediction=prediction[0]

        new_patient = Patients(name=patient_name, diagnosis = prediction)

        #add to database 
        try: 
            db.session.add(new_patient)
            db.session.commit()
            patients = Patients.query.order_by(Patients.date_created)
            return redirect("results.html", patients = patients)
        except:
            return "There was an error identifying your disease...Please try again"
        
    # return render_template('index.html', pred="The probable diagnosis says it could be {}".format(prediction))
    else:
        return render_template("input.html", title = "Input")

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/<name>')
def name(name):
    return f"Hi {name}"

if __name__ == "__main__":
    app.run(debug=True)