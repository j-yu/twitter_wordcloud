import tweepy
import credentials
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
# from nltk.tokenize import TweetTokenizer
import models


# tokenizer = TweetTokenizer(reduce_len=True)

stop_words = set(stopwords.words('english'))


auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class TwitterInterface:

    db = models.DataBase()

    def __init__(self, screen_name=''):
        self.screen_name = screen_name

    def clean_text(self, tweet):
        tokens = word_tokenize(tweet)
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = stopwords.words('english')
        words = [w for w in words if w not in stop_words and
                 w not in ['https', 'http', 'amp']]

        return " ".join(words)

    def sentiment(self, tweet):
        blob = TextBlob(tweet)
        if blob.sentiment.polarity < 0:
            return "negative"
        elif blob.sentiment.polarity == 0:
            return "neutral"
        else:
            return "positive"

    def grab_texts(self):

        db = models.DataBase()
        db.delete()

        for status in tweepy.Cursor(api.user_timeline, screen_name=self.screen_name, tweet_mode='extended').items(20):
            try:
                tweet = {'text': status.retweeted_status.full_text, 'username': status.user.screen_name}
            except:
                tweet = {'text': status.full_text, 'username': status.user.screen_name}

            raw = tweet['text']
            clean = self.clean_text(raw)
            tweet['clean'] = clean

            sentiment = self.sentiment(clean)
            tweet['sentiment'] = sentiment

            db.create(tweet)

            r = self.db.read()
        return r
