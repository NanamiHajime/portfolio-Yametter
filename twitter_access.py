import tweepy
# from ..AUTH import twitter_AUTH_leg
from datetime import timedelta
import pickle
from sklearn.feature_extraction import DictVectorizer
import collections
from sklearn.model_selection import train_test_split
from model import model_make

search_word="love"


API_KEY = ""
API_SECRET = ""

BEARER_TOKEN = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

negative_tweet = 0
#モデルを作る
model=model_make.model_make()

# Twitter APIの認証
def auth_twitter():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


api = auth_twitter()

# 受け取ったjson型のタイムライン情報から辞書型にする
def get_timeline_id_array():
    stress_count=0
    list_timeline = []
    tweets = tweepy.Cursor(api.search_tweets, q=search_word, \
                            include_entities=True, \
                            tweet_mode="extended", \
                            lang="en").items(20)
                            
    # status:ツイートごとの情報
    for i, status in enumerate(tweets):
        tweet_text=status.full_text
        list_timeline.append(
            {
                "user_id": status.user.screen_name,  # ユーザーID
                "tweet_id": status.id,  # ツイートid
                # 投稿した時間(UTCから日本時間に修正)
                "tweet_time": status.created_at+timedelta(hours=+9),
                "text": status.full_text,  # ツイート内容
                "user_name": status.user.name,  # ユーザーの名前
                "retweet": status.retweet_count,  # リツイート数
                "favorite": status.favorite_count,  # ツイート数
                "polarity": model_make.model_suiron(tweet_text)
            })
        #もし極性がnegativeならカウントをプラスする
        if list_timeline[i]["polarity"]=="NEGATIVE":
            stress_count=stress_count+1
    return list_timeline, stress_count


def url_maker():
    list_timeline_id = get_timeline_id_array()[0]
    list_timeline_url = []
    for i, tweet_data in enumerate(list_timeline_id):
        tweet_url = f'https://twitter.com/{tweet_data["user_id"]}/status/{tweet_data["tweet_id"]}'
        list_timeline_url.append(tweet_url)
    return list_timeline_url
