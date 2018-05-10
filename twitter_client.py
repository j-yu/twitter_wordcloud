import tweepy
import re
from nltk import pos_tag, word_tokenize

# register and create your Twitter application at apps.twitter.com
consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'
access_token = 'your access token'
access_token_secret = 'your access token'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class TwitterInterface:

    def __init__(self, screen_name=''):
        self.screen_name = screen_name

    def clean_and_find_nouns(self, sent_string):
        x = " ".join(re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t\n])|(\w+:\S+)', " ", sent_string['text']).split())
        nouns = [word for word, pos in pos_tag(word_tokenize(x)) if
                 pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS']
        return " ".join(nouns) + " "

    def grab_texts(self):
        tweets = []
        # untruncated text of retweets are accessible only with tweet_mode extended and within status.retweeted_status
        for status in tweepy.Cursor(api.user_timeline, screen_name=self.screen_name, tweet_mode='extended').items(50):

            try:
                text = {'text': status.retweeted_status.full_text}
            except:
                text = {'text': status.full_text}

            text['text'] = self.clean_and_find_nouns(text)

            tweets.append(text)

        return tweets


client = TwitterInterface()
