import re

import twitter, json
from twitter import TwitterError

class TwitterTarget(object):

    def __init__(self, your_username):
        self.consumer_API_key = "8mo1oe5PCYxRzXytj8lK9beaM"
        self.consumer_secret_API_key = "E7l6T7MYBCn05YGLA05tfVz9NKIfBNKJR79JjxALntnr6je113"
        self.access_token = "805220750042857472-n3zPdbfnjMLn1QpWV7igz42vG7Eqrvz"
        self.secret_access_token = "c19vA2yQQ0a0gYhMpcKzAehi6vKgJLUSZMFzVuYjEOchT"
        self.api = twitter.Api(consumer_key=self.consumer_API_key,
                               consumer_secret=self.consumer_secret_API_key,
                               access_token_key=self.access_token,
                               access_token_secret=self.secret_access_token,
                               tweet_mode='extended')
        self.target_username = your_username
        self.user = self.api.GetUser(screen_name=self.target_username)
        self.id = self.user.id
        self.name = self.user.name
        self.username = None
        self.search_result = {}
        self.results = []
        print("twitter scraper successfully initialized!")

    def get_own_id(self):
        return self.id

    def get_own_username(self):
        return self.target_username

    def get_own_name(self):
        return self.name

    def search_by_parameter(self, parameter):
        results = self.api.GetUsersSearch(term=parameter)
        for result in results:
            if result.id not in list(self.search_result.keys()):
                self.search_result[result.id] = ''
            self.search_result[result.id] = result.screen_name
        return self.search_result

    def get_feed_of_others(self, username):
        self.results = []

        try:
            timeline = self.api.GetUserTimeline(screen_name=username,
                                                count=100)
        except TwitterError as te:
            return te

        for status in timeline:
            id = status.id
            name = status.user.screen_name
            time = status.created_at
            text = status.full_text
            hashtags = status.hashtags
            media = status.media
            if status.media is not None:
                media = status.media[0].media_url

            if 'RT' in text:
                other_party = ""
                take_in = False
                count = 0
                for character in text:
                    if character == '@':
                        take_in = True
                        count = count + 1
                    elif character == ':':
                        text = text[count:]
                        name = other_party
                        break
                    elif take_in:
                        other_party = other_party + character
                        count = count + 1
                    elif not take_in:
                        count = count + 1
                        continue

            result = {"name": name,
                      "id": id,
                      "text": text,
                      "time": time,
                      "hashtags": hashtags,
                      "media": media}

            self.results.append(result)

    def get_results(self):
        return self.results

    def get_own_feed(self):
        self.get_feed_of_others(self.get_own_username())
        return self.get_results()

    def get_tweeters(self):
        return list(self.results.keys())

    def scrape(self, mental_illnesses):
        twitter_results = {}

        for mental_illness in mental_illnesses:
            twitter_results[mental_illness] = []

            print("currently handling Twitter information:")
            twitter_search = self.search_by_parameter(mental_illness)

            users = list(twitter_search.keys())
            for user in users:
                self.get_feed_of_others(twitter_search[user])

                if type(self.get_results()) is TwitterError or self.get_results() is []:
                    continue
                else:
                    last_5_posts = list(map(lambda x: x['text'], self.results))
                    last_5_media = list(map(lambda x: x['media'] if x['media'] is not None else x['media'], self.results))

                    search_result = {'id': user,
                                     'text': last_5_posts,
                                     'media': last_5_media}
                    twitter_results[mental_illness].append(search_result)

            filename = 'twitter_' + mental_illness + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(twitter_results[mental_illness], f)

            print("complete handling Twitter information.")

    def scrape_self(self):
        results = self.get_own_feed()
        return results

    def save_self_scraped_information(self):
        results = self.scrape_self()

        filename = 'twitter_' + self.target_username + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f)


# test = TwitterTarget('depressingmsgs')
# print(test.get_own_feed())

###############################################################################################################
# Use search_by_parameters to obtain 20 usernames. Only the same 20 will always be obtained.                  #
# For example, if I intend to look for depression, use test.search_by_parameter('depression') as shown below. #
###############################################################################################################
# search_depression = test.search_by_parameter('depression')
# print(search_depression)

######################################################################################################################
# Use set_target_by_username to obtain the last 200 posts of that username.                                          #
# Refer below for an example. It may be helpful to use the get_tweeters() method to see who made posts in that page. #
# Use get_results() method to get direct access to the results. It is a dictionary.                                  #
######################################################################################################################
# test.get_feed_of_others("BeyondBrokenDep")
# print(test.get_results())

# Do this:
# 1) search_by_parameters for mental illnesses
# 2) set_target_by_username for each username obtained by 1)
# 3) get the results and place it in a list
# 4) write to a .txt or .csv file
# 5) use set_target_by_username(your_own_username) to get your own feed.


