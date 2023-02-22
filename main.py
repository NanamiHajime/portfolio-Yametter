import twitter_access
import streamlit as st

#ツイッターの情報
list_timeline=twitter_access.get_timeline_id_array()[0]
#ネガティブなツイートの数
timeline_stress=twitter_access.get_timeline_id_array()[1]

if __name__ == '__main__':
    #app.run(debug=True)
    #プロキシ環境
    st.title("Yametter")
    st.write("--------------------------")
    for tweet in list_timeline:
        if tweet["polarity"]=="NEGATIVE":
            st.write(tweet["polarity"])
        st.write("username:",tweet["user_name"])
        st.write("user id:",tweet["user_id"])
        st.write(tweet["text"])
        st.write("tweet time:",tweet["tweet_time"])
        st.write("fav:",tweet["favorite"])
        st.write("retweet:",tweet["retweet"])
        st.write("--------------------------")