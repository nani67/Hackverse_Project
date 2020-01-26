from bs4 import BeautifulSoup
import json, random, re, requests
import pyfacebook

class FacebookScrape(object):
    def __init__(self):
        self.app_id = '376395939967416'
        self.app_secret = '52edfbb8fb4f9c59a64613b81b5efc9a'
        self.app_token = '376395939967416|ewOGBPPoLg5F0pWHY3qkiaOKS1A'
        self.access_token = 'EAAFWVIJL8bgBAKksiJKDzXDTXZBzmZAfjpPwGL9sLvzgSy2I5OdngerWMbWESlFBQc2rlsLADLq7opHOViOSX4jJU0IQlHL8KZAguRVnlgwgdH7SVK9XQrFzuClK2ZCACxzvxzbwAfkYhdsUzDyaLI17nrgCmSL70NnvxzRGZBFgB3CtnIoTA'
        self.graph = pyfacebook.Api(long_term_token=self.access_token)
        self.username = ''

    def get_default(self):
        result = requests.get

    def get_posts(self, username):
        self.username = username
        feed = self.graph.get_posts(username=self.username, return_json=True)
        return feed


test = FacebookScrape()
x = test.get_posts('depression')
print(x)




