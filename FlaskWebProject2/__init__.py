"""
The flask application package.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
import re
nltk.download('punkt')
import operator

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stops = stopwords.words('english')

app = Flask(__name__)

import FlaskWebProject2.views