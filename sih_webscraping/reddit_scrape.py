import praw, json

mental_illnesses = ['depression', 'anxiety', 'stress']

class RedditTarget(object):

    def __init__(self):
        self.client_id = 'nOU50agIaLiB_A'
        self.secret = 'VSW6KfIBnCyh2nJ0eMyLE52mY6s'
        self.user_agent = 'sih_test'
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.secret,
                                  user_agent=self.user_agent)

    def search_subreddit(self, term, params=20):
        return self.reddit.subreddit(term).top(limit=params)

    def get_posts_info(self, term):
        results = []
        search_result = self.search_subreddit(term)

        for seek in search_result:

            author = 'anonymous'
            title = seek.title
            text = seek.selftext
            comments = seek.comments.list()

            if seek.author is not None:
                author = seek.author.name

            result = {'author': author,
                      'title': title,
                      'text': text}
            results.append(result)

        return results

    def scrape(self, mental_illnesses):
        reddit_results = {}

        for mental_illness in mental_illnesses:

            reddit_search = self.get_posts_info(mental_illness)
            reddit_results[mental_illness] = reddit_search

            filename = 'reddit_' + mental_illness + '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(reddit_results[mental_illness], f)
