import re
from os.path import join
import urllib.request

from instagram_infiltrate import InstagramScrape
from twitter_infiltrate import TwitterTarget
from reddit_scrape import RedditTarget
import json

import nltk

from nltk import tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier

sid = SentimentIntensityAnalyzer()

import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = r"C:\Users\kendrik\Pictures\sih_instagram\\"


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Fetch the service account key JSON file contents
cred = credentials.Certificate('stressbuster.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = firestore.client()

doc_ref = ref.collection(u'web-data-obtaining').document()

users_ref = ref.collection(u'web-data-obtaining')
docs = users_ref.stream()

risk_to_index = {'Low risk': 0, 'Medium risk': 1, 'High risk': 2}
index_to_risk = {0: 'Low risk', 1: 'Medium risk', 2: 'High risk'}

def read_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def get_instagram_json(file):
    data = read_json_file(file)
    return data


def get_twitter_json(file):
    data = read_json_file(file)
    return data


def get_reddit_json(file):
    data = read_json_file(file)
    return data

def clean_tweet(tweet):
    return ' '.join(re.sub("(@(\w+))|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|((http|https|ftp)://[a-zA-Z0-9\\./]+)|(#(\w+))"," ", tweet).split())

def determine_risk(summarized_percentages):
    if summarized_percentages['negative'] <= 0.19:
        return 'Low risk'
    elif 0.2 <= summarized_percentages['negative'] <= 0.34:
        return 'Medium risk'
    else:
        return 'High risk'

def process_img(im):
    width = im.shape[1]
    height = im.shape[0]
    im = im.transpose(2,0,1).reshape(3,-1)

    brg = np.amax(im,axis=0)
    brg[brg==0] = 1
    denom = np.sqrt((im[0]-im[1])**2-(im[0]-im[2])*(im[1]-im[2]))
    # hue = np.arccos(0.5*(2*im[0]-im[1]-im[2])/denom)
    sat = (brg - np.amin(im,axis=0))/brg

    return width, height, np.mean(brg), np.mean(sat)

class Account(object):
    def __init__(self):
        self.instagram_username = "kendrikwah"
        self.instagram_password = ''
        self.instagram_account = None
        self.twitter_username = ''
        self.twitter_account = None
        self.instagram_filename = ''
        self.twitter_filename = ''
        self.extracted_instagram_count = 0
        self.extracted_twitter_count = 0

    def log_into_instagram(self, username, password):
        self.instagram_username = username
        self.instagram_password = password
        self.instagram_account = InstagramScrape(self.instagram_username, self.instagram_password)

    def log_into_twitter(self, username):
        self.twitter_username = username
        self.twitter_account = TwitterTarget(self.twitter_username)

    def extract_from_instagram(self):
        instagram_results = self.instagram_account.get_self_feed()
        self.instagram_filename = 'instagram_' + self.instagram_username + '.json'
        return instagram_results

    def extract_from_instagram_offline(self):
        self.instagram_account.save_self_scraped_information()

    def extract_from_twitter(self):
        twitter_results = self.twitter_account.scrape_self()
        self.twitter_filename = 'twitter_' + self.twitter_username + '.json'
        return twitter_results

    def extract_from_twitter_offline(self):
        self.twitter_account.save_self_scraped_information()

    def analyze_instagram_feed(self, filename):
        # self.extract_from_instagram_offline()
        extracted_json = get_instagram_json(filename)
        summary_text = {'negative': 0, 'positive': 0, 'neutral': 0}
        summary_media = {'negative': 0, 'not negative': 0}
        existing_text = []
        existing_media = []
        text_risk = None
        media_risk = None

        for post in extracted_json:
            text = post['text']
            media = post['url']
            tokenized_text = tokenize.sent_tokenize(text)

            for txt in tokenized_text:
                txt = txt.lower()
                if txt not in existing_text:
                    if txt is not None:
                        txt = txt.lower()
                        ss = sid.polarity_scores(txt)
                        if ss['compound'] < 0:
                            summary_text['negative'] = summary_text['negative'] + 1
                        elif ss['compound'] == 0:
                            summary_text['neutral'] = summary_text['neutral'] + 1
                        else:
                            summary_text['positive'] = summary_text['positive'] + 1

                        existing_text.append(txt)

            if media not in existing_media:
                if media is not None:
                    online_url = media.split("/")[6].split("?")
                    img_url = online_url[0]
                    save_path = path + img_url
                    urllib.request.urlretrieve(media, save_path)
                    img = Image.open(save_path)
                    attempt_text = pytesseract.image_to_string(img)

                    if len(attempt_text) > 0:
                        ss = sid.polarity_scores(attempt_text)
                        if ss['compound'] < 0:
                            summary_text['negative'] = summary_text['negative'] + 1
                        elif ss['compound'] == 0:
                            summary_text['neutral'] = summary_text['neutral'] + 1
                        else:
                            summary_text['positive'] = summary_text['positive'] + 1

                        existing_text.append(attempt_text)

                    im = np.array(img)
                    processing_result = process_img(im)
                    if processing_result[2] <= 55:
                        summary_media['negative'] = summary_media['negative'] + 1
                    else:
                        summary_media['not negative'] = summary_media['not negative'] + 1
                    existing_media.append(media)

        total = 0
        for base in list(summary_text.keys()):
            total += summary_text[base]

        img_total = 0
        for base in list(summary_media.keys()):
            img_total += summary_media[base]

        if total != 0:
            for base in list(summary_text.keys()):
                summary_text[base] = round(summary_text[base]/total, 2)
            text_risk = determine_risk(summary_text)

        if img_total != 0:
            for base in list(summary_media.keys()):
                summary_media[base] = round(summary_media[base]/img_total, 2)
            media_risk = determine_risk(summary_media)

        if not text_risk and media_risk:
            overall_risk = media_risk
        elif not media_risk and text_risk:
            overall_risk = text_risk
        else:
            risk_index = (risk_to_index[text_risk] + risk_to_index[media_risk])/2
            overall_risk = index_to_risk[round(risk_index)]

        data = {u'instagram_username': self.instagram_username,
                u'filename': filename,
                u'extracted_instagram_content': extracted_json,
                u'existing_instagram_feeds': existing_text,
                u'existing_instagram_media': existing_media,
                u'existing_text_count': summary_text,
                u'existing_media_count': summary_media,
                u'text_risk': text_risk,
                u'media_risk': media_risk,
                u'overall_risk': overall_risk}

        doc_ref.set(data)
        for key in list(data.keys()):
            print(key, ':', data[key])

    def analyze_twitter_feed(self, filename):
        self.extract_from_twitter_offline()
        extracted_json = get_twitter_json(filename)
        summary_text = {'negative': 0, 'positive': 0, 'neutral': 0}
        summary_media = {'negative': 0, 'not_negative': 0}
        existing_text = []
        existing_media = []
        text_risk = None
        media_risk = None

        for post in extracted_json:
            text = post['text']
            media = post['media']

            if text not in existing_text:
                if text is not None:
                    text = clean_tweet(text)
                    text = text.lower()
                    ss = sid.polarity_scores(text)
                    if ss['compound'] < 0:
                        summary_text['negative'] = summary_text['negative'] + 1
                    elif ss['compound'] == 0:
                        summary_text['neutral'] = summary_text['neutral'] + 1
                    else:
                        summary_text['positive'] = summary_text['positive'] + 1

                    existing_text.append(text)

            if media not in existing_media:
                if media is not None:
                    online_url = media.split("/")[4]
                    img_url = online_url[0]
                    save_path = path + img_url
                    urllib.request.urlretrieve(media, save_path)
                    img = Image.open(save_path)
                    attempt_text = pytesseract.image_to_string(img)
                    if attempt_text != '' or attempt_text is not None:
                        ss = sid.polarity_scores(attempt_text)
                        if ss['compound'] < 0:
                            summary_text['negative'] = summary_text['negative'] + 1
                        elif ss['compound'] == 0:
                            summary_text['neutral'] = summary_text['neutral'] + 1
                        else:
                            summary_text['positive'] = summary_text['positive'] + 1

                        existing_text.append(attempt_text)

                    im = np.array(img)
                    processing_result = process_img(im)
                    if processing_result[2] <= 55:
                        summary_media['negative'] = summary_media['negative'] + 1
                    else:
                        summary_media['not_negative'] = summary_media['not_negative'] + 1

                    existing_media.append(media)

        total = 0
        for base in list(summary_text.keys()):
            total += summary_text[base]

        img_total = 0
        for base in list(summary_media.keys()):
            img_total += summary_media[base]

        if total != 0:
            for base in list(summary_text.keys()):
                summary_text[base] = round(summary_text[base]/total, 2)
            text_risk = determine_risk(summary_text)

        if img_total != 0:
            for base in list(summary_media.keys()):
                summary_media[base] = round(summary_media[base]/img_total, 2)
            media_risk = determine_risk(summary_media)

        if not text_risk and media_risk:
            overall_risk = media_risk
        elif not media_risk and text_risk:
            overall_risk = text_risk
        else:
            risk_index = (risk_to_index[text_risk] + risk_to_index[media_risk])/2
            overall_risk = index_to_risk[round(risk_index)]

        data = {u'twitter_username': self.twitter_username,
                u'filename': filename,
                u'extracted_twitter_content': extracted_json,
                u'existing_twitter_texts': existing_text,
                u'existing_twitter_media': existing_media,
                u'existing_text_count': summary_text,
                u'existing_media_count': summary_media,
                u'text_risk': text_risk,
                u'media_risk': media_risk,
                u'overall_risk': overall_risk}

        doc_ref.set(data)
        for key in list(data.keys()):
            print(key, ':', data[key])


acc = Account()
# acc.log_into_instagram("xxxxxxxx", "xxxxxxxx")
# acc.extract_from_instagram_offline()
extracted_instagram = acc.analyze_instagram_feed("instagram_kendrikwah.json")

print("\n")

acc.log_into_twitter("depressingmsgs")
# acc.extract_from_twitter_offline()
extracted_twitter = acc.analyze_twitter_feed('twitter_depressingmsgs.json')

#
#    Pipeline will work like this:
# 1) Get credentials of users (username and password for Instagram, username for Twitter)
# 2) After doing extraction, use analyze_instagram_feed() and analyze_twitter_feed() (use offline methods if you wish to extract via json instead)
#    These analyze methods will have the NLP and image-to-string codes inside.