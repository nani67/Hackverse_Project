import re
from os.path import join

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


def scrape():
    # instagram_handle = InstagramScrape('xxx', 'xxx')
    # twitter_handle = TwitterTarget('ChaotiqueEdge')
    reddit_handle = RedditTarget()
    mental_illnesses = ['depression']

    # instagram_handle.scrape(mental_illnesses)
    # twitter_handle.scrape(mental_illnesses)
    reddit_handle.scrape(mental_illnesses)

# scrape()

def read_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_instagram_json(file):
    data = read_json_file(file)
    key = list(data.keys())[0]
    return data[key]


def get_twitter_json(file):
    data = read_json_file(file)
    return data


def get_reddit_json(file):
    data = read_json_file(file)
    return data


def get_top_5_texts(lst):
    all_recorded_users = []
    texts = {}
    use_id = True

    # print(lst)

    try:
        val = lst[0]['id']
    except KeyError as ke:
        use_id = False

    if use_id is True:
        all_recorded_users_double_counted = list(map(lambda x: x['id'], lst))

        for user in all_recorded_users_double_counted:
            if user not in all_recorded_users:
                all_recorded_users.append(user)

        for user in all_recorded_users:
            filtered = list(filter(lambda x: x['id'] == user, lst))
            top_5 = list(filter(lambda x: len(x['text']) != 0, filtered))
            top_5 = list(map(lambda x: x['text'], top_5))

            if len(top_5) > 5:
                top_5 = top_5[0:5]

            texts[user] = top_5
    else:
        all_recorded_users_double_counted = list(map(lambda x: x['author'], lst))

        for user in all_recorded_users_double_counted:
            if user not in all_recorded_users:
                all_recorded_users.append(user)

        for user in all_recorded_users:
            filtered = list(filter(lambda x: x['author'] == user, lst))
            top_5 = list(filter(lambda x: len(x['text']) != 0 or len(x['title']) != 0, filtered))
            top_5 = list(map(lambda x: x['text'], top_5))

            if len(top_5) > 5:
                top_5 = top_5[0:5]

            texts[user] = top_5

    return texts


def clean_tweet(tweet):
    return ' '.join(re.sub("(@(\w+))|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|((http|https|ftp)://[a-zA-Z0-9\\./]+)|(#(\w+))"," ", tweet).split())

instagram_depression = get_top_5_texts(get_instagram_json('instagram_depression.json'))
for user in list(instagram_depression.keys()):
    instagram_depression[user] = list(map(lambda x: tokenize.sent_tokenize(x), instagram_depression[user]))

# instagram_anxiety = get_top_5_texts(get_instagram_json('instagram_anxiety.json'))
# instagram_stress = get_top_5_texts(get_instagram_json('instagram_stress.json'))

twitter_depression = get_top_5_texts(get_twitter_json('twitter_depression.json'))
for user in list(twitter_depression.keys()):
    twitter_depression[user] = twitter_depression[user][0]
    twitter_depression[user] = list(map(lambda x: clean_tweet(x), twitter_depression[user]))
    twitter_depression[user] = list(map(lambda x: tokenize.sent_tokenize(x), twitter_depression[user]))
# twitter_anxiety = get_top_5_texts(get_twitter_json('twitter_anxiety.json'))
# twitter_stress = get_top_5_texts(get_twitter_json('twitter_stress.json'))

reddit_depression = get_top_5_texts(get_reddit_json('reddit_depression.json'))
for user in list(reddit_depression.keys()):
    reddit_depression[user] = list(map(lambda x: tokenize.sent_tokenize(x), reddit_depression[user]))
# reddit_anxiety = get_top_5_texts(get_reddit_json('reddit_anxiety.json'))
# reddit_stress = get_top_5_texts(get_reddit_json('reddit_stress.json'))

def get_sentiment_percentage(sentiments):
    results = {}
    for user in list(sentiments.keys()):
        summary = {'positive': 0, 'negative': 0, 'neutral': 0}
        total = len(sentiments[user])
        for sentiment in sentiments[user]:
            for sentence in sentiment:
                sentence = clean_tweet(sentence)
                ss = sid.polarity_scores(sentence)
                print("sentence: ", sentence)
                print("ss: ", ss)
                if ss['compound'] == 0:
                    summary['neutral'] = summary['neutral'] + 1
                elif ss['compound'] < 0:
                    summary['negative'] = summary['negative'] + 1
                else:
                    summary['positive'] = summary['positive'] + 1
        results[user] = summary
    return results


print(get_sentiment_percentage(instagram_depression))
print(get_sentiment_percentage(twitter_depression))
print(get_sentiment_percentage(reddit_depression))

# Instagram => Check caption, picture and extract both for processing
# Twitter => Check twitter posts