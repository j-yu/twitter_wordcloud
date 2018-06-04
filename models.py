import pymysql
import credentials


class DataBase:

    conn = pymysql.connect(host=credentials.host, unix_socket=credentials.unix_socket,
                           user=credentials.user, passwd=credentials.passwd, db=credentials.db)
    cur = conn.cursor()
    conn.set_charset('utf8mb4')
    cur.execute("SET NAMES utf8mb4;")
    cur.execute("SET CHARACTER SET utf8mb4;")
    cur.execute("SET character_set_connection=utf8mb4;")

    def create(self, tweet):
        self.cur.execute("INSERT IGNORE INTO twitter.tweets (tweets, username, sentiment, clean) VALUES (%s, %s, %s, %s);",
                         (tweet['text'], tweet['username'], tweet['sentiment'], tweet['clean']))

        self.conn.commit()
        return

    @classmethod
    def read(cls):
        cls.cur.execute("SELECT * from twitter.tweets;")
        tweets = [{'text': row[1], 'username': row[2], 'sentiment': row[3], 'clean': row[4]} for row in cls.cur.fetchall()]
        return tweets

    def update(self):
        pass

    def delete(self):

        self.cur.execute("DELETE from twitter.tweets;")
        self.conn.commit()
        return





