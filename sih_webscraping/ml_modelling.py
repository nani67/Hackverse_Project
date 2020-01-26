import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from math import log, sqrt
import pandas as pd
import numpy as np
import re

tweets = pd.read_csv('sentiment140.csv', encoding = "ISO-8859-1")
tweets.head(20)

