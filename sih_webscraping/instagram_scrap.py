import json
import codecs
import datetime
import os.path
import logging
import sys

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    username = sys.argv[1]
    password = sys.argv[2]
    settings_file_path = 'test_credentials.json'

    print('Client version: {0!s}'.format(client_version))
    device_id = None
    try:
        settings_file = settings_file_path
        if not os.path.isfile(settings_file):
            print('Unable to find file: {0!s}'.format(settings_file))
            api = Client(
                username, password,
                on_login=lambda x: onlogin_callback(x, settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))
            device_id = cached_settings.get('device_id')
            api = Client(
                username, password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        api = Client(
            username, password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    cookie_expiry = api.cookie_jar.auth_expires
    print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    rank_token = Client.generate_uuid()
    tag_results = []
    resultsForTimeline = api.feed_timeline()
    resultsForLikedFeeds = api.feed_liked()
    apple = json.dumps([resultsForTimeline], indent=100)
    mango = json.dumps([resultsForLikedFeeds], indent=100)
    y = json.loads(apple)
    z = json.loads(mango)

    stringList = []

    for s in y:
        for e in s['feed_items']:
            try:
                stringList.append(e['media_or_ad']['caption']['text'])
            except:
                print('')

    captionDetails = []
    userLikedFeeds = []

    for d in z:
        for f in d['items']:
            captionDetails.append(f['caption'])

    for x in captionDetails:
        try:
            userLikedFeeds.append(x['text'])
        except:
            userLikedFeeds.append('')

    userFeeds = stringList

    print(userFeeds)
    print('\n\n\n')
    print(userLikedFeeds)
    
    # Writing to file to view
    
    file1 = open("me.txt", "w")
    # choose between apple orange and mango
    # Apple  = User's Feed
    # Orange = Specified user post
    # Mango  = User's Likes
    data = json.loads(apple)
    file1.writelines(json.dumps(data, indent=4, sort_keys=True))
    file1.close()

