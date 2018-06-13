#importing libraries needed
import tweepy
import json
from paralleldots import set_api_key, get_api_key
import nltk
from nltk.corpus import *
nltk.download('stopwords')
from collections import Counter

# authentication keys
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""
oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_secret)
api = tweepy.API(oauth)

# displaying menu
def display_menu():
    global flag
    message = str
    while flag==True:
        print("MENU")
        print("1. Retrieve tweets")
        print("2. Count the followers")
        print("3. Determine the sentiment")
        print("4. Location, Language and Time Zone")
        print("5. Compare tweets")
        print("6. Analyse the top usage")
        print("7. Tweet a message")
        print("8. Exit")
        option = int(input("What do you wanna do?"))
        if option==1:
            Get_Search()
            display_menu()
        elif option==2:
            fcount()
            display_menu()
        elif option == 3:
            sentiment_analysis()
            display_menu()
        elif option == 4:
            location()
            display_menu()
        elif option == 5:
            compare()
            display_menu()
        elif option == 6:
            top_usage()
            display_menu()
        elif option==7:
            tweet_status(new=message)
            display_menu()
        elif option==8:
            print("See u again, Tata")
            flag = False
        else:
            print("Enter a valid value!")
            display_menu()

# putting on the hashtag
def query():
    global tweets
    tweet_input = input("For which hashtag do you want to see the tweets? (Do not include #)")
    tweet_input = "#" + tweet_input
    tweets = api.search(q=tweet_input)

#forming the status object
def Get_Search():
    query()
    status = tweets[0]
    json_str = json.dumps(status._json,indent=4,sort_keys=True)
    print(json_str)

# counting followers
def fcount():
    query()
    print("UserName      Follower Count")
    for tweet in tweets:
        print(tweet.user.name+"     "+str(tweet.user.followers_count))

# determining the sentiment
def sentiment_analysis():
    flagpos = 0
    flagneu = 0
    flagneg = 0
    query()
    from paralleldots import similarity, taxonomy, sentiment, emotion, abuse
    set_api_key("")
    get_api_key()
    for tweet in tweets:
        text = tweet.text
        sentiment_value = sentiment(text)
        values1 = sentiment_value['sentiment']
        if values1 == "positive":
            flagpos = flagpos + 1
        elif values1 == "negative":
            flagneg = flagneg + 1
        else:
            flagneu = flagneu + 1
    if flagneu > flagneg and flagneu > flagpos:
        print("Sentiment: Neutral")
    elif flagneg > flagneu and flagneg > flagpos:
        print("Sentiment: Negative")
    else:
        print("Sentiment: Positive")

# determines the location, language and time zone
def location():
    global time_zone1,loca,lang
    query()
    location = {}
    language = {}
    time_zone = {}
    for tweet in tweets:
        loca = tweet.user.location
        lang = tweet.user.lang
        time_zone1 = tweet.user.time_zone
        if loca in location:
            location[loca] += 1
        else:
            location[loca] = 1
        if lang in language:
            language[lang] += 1
        else:
            language[lang] = 1
        if time_zone1 in time_zone:
            time_zone[time_zone1] += 1
        else:
            time_zone[time_zone1] = 1
    if time_zone==None or time_zone=="" or time_zone[time_zone1]==1:
        del time_zone[None]
        del time_zone[""]
        del time_zone[:][1]
    if location== None or location== "" or location[loca]==1:
        del location[None]
        del location[""]
        del location[:][1]
    if language== None or language=="":
        del language[None]
        del language[""]
    print("Language:")
    print(language)
    print("Location:")
    print(location)
    print("Time Zone:")
    print(time_zone)

# compare tweets
def compare():
    flagword = 0
    flagword1 = 0
    # for narendra modi
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word=word.upper()
            if word == "AMERICA" or word == "US" or word=="USA" or word=="UNITED STATES OF AMERICA":
                flagword = flagword + 1
    print("USA BY NARENDRA MODI: "+ str(flagword))

    # for donald trump
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word = word.upper()
            if word == "INDIA":
                flagword1 = flagword1 + 1
    print("INDIA BY DONALD TRUMP: " + str(flagword1))

# analysing top usage
def top_usage():
    global count
    stop_words = set(stopwords.words('english'))
    x = [x.upper() for x in stop_words]
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet1 = re.split(r"\s", cur_tweet)
        cur_tweet = [w for w in cur_tweet1 if not w in stop_words]
        cur_tweet=[]
        for w in cur_tweet1:
            if w not in stop_words:
                cur_tweet.append(w)
                count = Counter(cur_tweet).most_common(10)
        print(count)

#  updates status
def tweet_status(new):
    message = input("What is the status that you want to set?")
    api.update_status(message)

print("Twitter Bot")
display_menu()
