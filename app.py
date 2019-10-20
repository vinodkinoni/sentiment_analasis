from flask import Flask, render_template, flash, request, url_for, redirect, session
import re
import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


IMAGE_FOLDER = os.path.join('static', 'img_pool')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

def calculate_sentimet(comment):
    score = analyser.polarity_scores(comment)
    negative = score['neg']
    positive = score['pos']
    neutral = score['neu']
    return positive,neutral,  negative


#########################Code for Sentiment Analysis
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict', methods = ['POST', "GET"])
def predict():
    if request.method=='POST':
        text = request.form['message']
        print(text)
        positive, neutral, negative = calculate_sentimet(text)
        target_key = 1
        if negative > positive:
            sentiment = 'Negative'
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Sad_Emoji.png')
        else:
            sentiment = 'Positive'
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Smiling_Emoji.png')
        print(text, sentiment)
        target_key = 1
    return render_template('home.html', target_key = target_key,text=text, sentiment=sentiment, image=img_filename)


if __name__ == "__main__":
    app.run()
