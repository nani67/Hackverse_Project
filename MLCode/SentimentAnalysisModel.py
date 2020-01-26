import numpy as np
import pandas as pd
import re
import nltk

data_source_url = "https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv"
airline_tweets = pd.read_csv(data_source_url)

print(airline_tweets.head())

features = airline_tweets.iloc[:, 10].values
labels = airline_tweets.iloc[:, 1].values

print(features)
print(labels)


processed_features = []

for sentence in range(0, len(features)):
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)

    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)

    # Converting to Lowercase
    processed_feature = processed_feature.lower()

    processed_features.append(processed_feature)

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()

from sklearn.model_selection import train_test_split
X_train, X_Test, Y_Train, Y_Test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)

from sklearn.ensemble import RandomForestClassifier

text_classifier_rf = RandomForestClassifier(n_estimators=2000, random_state=0)
text_classifier_rf.fit(X_train, Y_Train)

from sklearn.metrics import accuracy_score
predictions = text_classifier_rf.predict(X_Test)
print(accuracy_score(Y_Test, predictions))

import pickle

filename = 'finalized_model.dat'
pickle.dump(text_classifier_rf, open(filename, 'wb'))


# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.predict(data)
# print(result)
