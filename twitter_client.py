import tweepy
import string
from nltk import word_tokenize
from nltk.corpus import stopwords

# register and create your Twitter application at apps.twitter.com
consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'
access_token = 'your access token'
access_token_secret = 'your access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class TwitterInterface:

    def __init__(self, screen_name=''):
        self.screen_name = screen_name

    def clean_text(self, tweet):
        tokens = word_tokenize(tweet['text'])
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = stopwords.words('english')
        words = [w for w in words if w not in stop_words and w not in ['https', 'http', 'amp']]

        return " ".join(words)

    def grab_texts(self):
        tweets = []
        # untruncated text of retweets are accessible only with tweet_mode extended and within status.retweeted_status
        for status in tweepy.Cursor(api.user_timeline, screen_name=self.screen_name, tweet_mode='extended').items(50):

            try:
                text = {'text': status.retweeted_status.full_text}
            except:
                text = {'text': status.full_text}

            cleaned = self.clean_text(text)

            tweets.append({'text': cleaned})

        return tweets
