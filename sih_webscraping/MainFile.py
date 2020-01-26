from urllib.request import urlopen
from urllib.parse import urlencode
import json
import requests
from bs4 import BeautifulSoup

# access_token='719197117.4bf1d80.c7af0e7fa9a6492283c8ca52ed8393cf'
# client_id='4bf1d80dc15b4d368eb57efe2dd8e367'
# client_secret='1150b494eaa843e58e884a601821fbb4'

import numpy
import nltk
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets

from nltk import tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.classify import SklearnClassifier
# sid = SentimentIntensityAnalyzer()
#
# test_sentence = 'I love Fortnite so much! It is the best game ever!'
# tricky_sentence = 'Sentiment analysis has never been good.'
# paragraph = "It was one of the worst movies I've seen, despite good reviews.\nUnbelievably good acting!! Great direction. VERY poor production. \nThe movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"
# new_sentence = "The plot was good, but the characters are uncompelling and the dialog is not great."
#
# lines_list = []
# test_sentences = [tricky_sentence]
# test_test = tokenize.sent_tokenize(test_sentence)
# print(test_test)
# lines_list = tokenize.sent_tokenize(paragraph)
# print(lines_list)
# test_sentences.extend(test_test)
# test_sentences.extend(lines_list)
# test_sentences.append(new_sentence)
#
# tldr = {'positive': 0,
#         'neutral': 0,
#         'negative': 0}
#
# for sentence in test_sentences:
#     ss = sid.polarity_scores(sentence)
#     print(sentence, ':', ss['compound'])
#     if ss['compound'] == 0.0:
#         tldr['neutral'] += 1
#     elif ss['compound'] > 0.0:
#         tldr['positive'] += 1
#     else:
#         tldr['negative'] += 1
#
# print(tldr)

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import urllib.request
import numpy as np

url = "https://www.cam.ac.uk/sites/www.cam.ac.uk/files/styles/content-885x432/public/news/research/news/depress.jpg?itok=ctfouPZ3"
split_url = url.split('/')
img_name = split_url[-1].split('?')[0]
path = r"C:\Users\kendrik\Pictures\Saved Pictures" + "\\" + img_name

urllib.request.urlretrieve(url, path)

im = np.array(Image.open(r"C:\Users\kendrik\Pictures\Saved Pictures\depress.jpg"))

def process_img(im):
    width = im.shape[1]
    height = im.shape[0]
    im = im.transpose(2,0,1).reshape(3,-1)

    brg = np.amax(im,axis=0)
    brg[brg==0] = 1
    denom = np.sqrt((im[0]-im[1])**2-(im[0]-im[2])*(im[1]-im[2]))
    denom[denom==0] = 1
    hue = np.arccos(0.5*(2*im[0]-im[1]-im[2])/denom)
    sat = (brg - np.amin(im,axis=0))/brg

    return width, height, np.mean(brg), np.mean(sat), np.mean(hue)

# text = pytesseract.image_to_string(im, lang='eng')

# print(type(text))
# print(len(text))
result = process_img(im)
print(result)
