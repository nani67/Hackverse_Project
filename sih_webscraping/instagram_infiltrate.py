from instagram_private_api import Client, ClientCompatPatch, ClientError
import json

class InstagramScrape(object):

    def __init__(self, username, password):
        print("setting up instagram scraper...")
        self.username = username
        self.password = password
        self.api = Client(username=username, password=password)
        self.user_id = self.api.username_info(self.username)['user']['pk']
        print("instagram scraper successfully initialized!")

    def get_timeline(self):
        return self.api.feed_timeline()

    def get_self_feed(self):
        result = []
        feed = self.api.self_feed()['items']

        for entry in feed:
            if 'carousel_media_count' in list(entry.keys()):
                media = entry['carousel_media']
            else:
                media = [entry]
            carousel_parent_id = entry['id']

            if not entry['caption'] is None:
                text = entry['caption']['text']
            else:
                text = ''

            user_id = entry['caption']["user_id"]
            username = entry['user']['username']
            full_name = entry['user']['full_name']
            for medium in media:
                media_id = medium['id']
                images = medium['image_versions2']['candidates']
                for i in range(0, len(images)):
                    if not i % 2:
                        url = images[i]["url"]
                        image = {"carousel_parent_id": carousel_parent_id,
                                 "id": user_id,
                                 "username": username,
                                 "full_name": full_name,
                                 "media_id": media_id,
                                 "url": url,
                                 "text": text}

                        result.append(image)
        return result

    def get_own_stories(self):
        result = []
        tray = self.api.reels_tray()['tray'][0]
        user_id = tray['id']
        username = tray['user']['username']
        full_name = tray['user']['full_name']
        stories = tray['items']

        for story in stories:
            url = story['image_versions2']['candidates'][0]['url']
            entry = {"user_id": user_id,
                     "username": username,
                     "full_name": full_name,
                     "url": url}
            result.append(entry)

        return result

    def search_results(self, query):
        result = []
        search_results = self.api.search_users(query)['users']

        for user in search_results:
            pk = user['pk']
            username = user['username']
            full_name = user['full_name']
            info = {"id": pk,
                    "username": username,
                    "full_name": full_name}
            result.append(info)

        return result

    def get_user_feed(self, username, id):
        result = []

        try:
            feed = self.api.username_feed(username)['items']
        except ClientError as err:
            return err

        for entry in feed:
            if 'carousel_media_count' in list(entry.keys()):
                media = entry['carousel_media']
            else:
                media = [entry]
            carousel_parent_id = entry['id']

            if not entry['caption'] is None:
                text = entry['caption']['text']
            else:
                text = ''

            username = entry['user']['username']
            full_name = entry['user']['full_name']
            for medium in media:
                media_id = medium['id']
                images = medium['image_versions2']['candidates']
                for i in range(0, len(images)):
                    if not i % 2:
                        url = images[i]["url"]
                        image = {"carousel_parent_id": carousel_parent_id,
                                 "user_id": id,
                                 "username": username,
                                 "full_name": full_name,
                                 "media_id": media_id,
                                 "url": url,
                                 "text": text}
                        result.append(image)
        return result

    def gather_media_comments(self, media_id):
        results = []
        comments = self.api.media_comments(media_id)["comments"]

        for comment in comments:
            pk = comment['user']['pk']
            username = comment['user']['username']
            text = comment['text']
            result = {'pk': pk,
                      'username': username,
                      'media_id': media_id,
                      'comment_id': comment['pk'],
                      'text': text}
            results.append(result)

        return results

    def get_comment_replies(self, media_id, comment_id):
        results = []
        replies = self.api.comment_replies(media_id, comment_id)['child_comments']

        for reply in replies:
            id = reply['user_id']
            comment = reply['text']
            replier = reply['user']['username']
            replied_id = reply['user']['pk']
            result = {'id': id,
                      'comment': comment,
                      'from': replier,
                      'from_id': replied_id,
                      'media_id': media_id,
                      'comment_id': comment_id}
            results.append(result)

        return results

    def get_explore_results(self):
        return self.api.explore()

    def get_story_archive(self):
        return self.api.highlight_user_feed(self.user_id)

    def get_top_search(self):
        return self.api.top_search()

    def scrape_illnesses(self, mental_illnesses):
        instagram_results = {}

        for mental_illness in mental_illnesses:
            instagram_results[mental_illness] = []

            print("currently handling Instagram information:")
            ig_result = self.search_results(mental_illness)
            handle_feed_lst = {}

            for handle in ig_result:
                handle_feed_lst[handle['id']] = []
                handle_feed = self.get_user_feed(handle['username'], handle['id'])

                if type(handle_feed) is not ClientError:
                    handle_feed_lst[handle['id']].extend(handle_feed)

            users = list(handle_feed_lst.keys())
            carousel_ids = []

            for user in users:
                posts = handle_feed_lst[user]
                for post in posts:
                    print(post)
                    if post['carousel_parent_id'] in carousel_ids:
                        continue
                    else:
                        print(post['carousel_parent_id'])
                        carousel_ids.append(post['carousel_parent_id'])

                        search_result = {'id': user,
                                         'text': post['text'],
                                         'media': post['url']}
                        instagram_results[mental_illness].append(search_result)

            print(instagram_results[mental_illness])

        # return instagram_results
# filename = 'instagram_' + mental_illness + '.json'
# with open(filename, 'w', encoding='utf-8') as f:
#     json.dump(instagram_results, f)
#
# print("complete handling Instagram information.")

    def scrape_self(self):
        results = self.get_self_feed()
        return results

    def save_self_scraped_information(self):
        results = self.scrape_self()

        filename = 'instagram_' + self.username + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f)


# Do this:
# 1) Detect post.
# 2) Caption and picture.
# 3) Get the image out.
# 4) Process the image

# For user posts
# 1st run ==> Get last 50 posts if possible.
# 2nd run onwards ==> Get last 3 posts.
# Run weekly

# For user likes
# Get liked posts once every 4 hours.