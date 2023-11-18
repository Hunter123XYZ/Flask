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

class Todo(db.Model):
    #primary_key means a unique identifier (ex: patient number)
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/')
def index(): 
    if request.method == 'POST':
        return "Hello!"
    else: 
        return render_template('index.html')
    
# @app.route('/', methods=['POST', 'GET'])
# def predict()
    

@app.route('/<name>')
def name(name):
    return f"Hi {name}"

if __name__ == "__main__":
    app.run(debug=True)