import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from math import log, sqrt
import pandas as pd
import numpy as np
import re
import jupyter

tweets = pd.read_csv('sentiment140.csv', encoding = "ISO-8859-1")
##tweets.head(20)

##print(tweets.head(20))


##tweets['0'].value_counts()


def split_data():
    train_index = []
    test_index = []
    for i in range(500):
        if np.random.uniform(0, 1) < 0.98:
            train_index = train_index + [i]
        else:
            test_index = test_index + [i]

    train_data = tweets.iloc[train_index]
    test_data = tweets.iloc[test_index]
    return [train_data, test_data]

split_result = split_data()
train_result = split_result[0]
test_result = split_result[1]
