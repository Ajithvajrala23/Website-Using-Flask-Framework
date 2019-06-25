"""
Routes and views for the flask application.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from FlaskWebProject2 import app
import os
import requests
import operator
import re
#import nltk
from flask import Flask, render_template, request, send_file
from collections import Counter
#from bs4 import BeautifulSoup
#from textblob import TextBlob
import numpy as np
#from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
#import base64

analyser = SentimentIntensityAnalyzer()

stops = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
    't', 'can', 'will', 'just', 'don', 'should', 'now', 'id', 'var',
    'function', 'js', 'd', 'script', '\'script', 'fjs', 'document', 'r',
    'b', 'g', 'e', '\'s', 'c', 'f', 'h', 'l', 'k'
]


def calculate_sentimet(comment):
    score = analyser.polarity_scores(comment)
    negative = score['neg']
    positive = score['pos']
    neutral = score['neu']

    return positive,neutral,  negative


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Details'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About Me',
        year=datetime.now().year,
        message='I am Libra'
    )

@app.route('/projects')
def projects():
    """Renders the about page."""
    return render_template(
        'projects.html',
        title='Projects',
        year=datetime.now().year,
        message='My Notable works are'
    )

@app.route("/text")
def text():
    return render_template('text.html')

@app.route("/process", methods =['POST'])
def process():

    comment = request.form['comment']
    positive, neutral,  negative = calculate_sentimet(comment)
    pie_labels = ['Positive' ,'Neutral',  'Negative']
    pie_values = [positive*100, neutral*100, negative*100]
    colors = ['green', 'orange', 'red']

    return render_template('sentiment.html', comment = comment,
                           positive = positive, neutral = neutral,
                           negative= negative,
                           max=17000,
                           set=zip(pie_values, pie_labels, colors))


@app.route('/me', methods=['GET', 'POST'])
def me():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('me.html', errors=errors)
        if r:
            # text processing
            print(r)
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            #nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)
            # save the results

            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )
            print(results)
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )

            except:
                errors.append("Unable to add item to database.")

    return render_template('me.html', errors=errors, results=results)

