#! /usr/bin/python3
import tweepy
import feedparser
import csv
import time
import datetime
import random
import sys
import re
import os
import urllib.request

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")


def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def getCreds():
    credList = []
    with open(str('{}//mycreds.csv'.format(pwdDir())), 'r') as credsRaw:
        credsData = csv.reader(credsRaw, delimiter=",")
        for item in credsData:
            credList.append(item)
        return credList


#### TWITTER API INTERFACE, ADD YOUR KEYS AND TOKENS
def tweetPoster(tweetString):
    print("Tweeting -------------- TWEETING")
    print(tweetString)

    # Consumer keys and access tokens, used for OAuth
    creds = getCreds()
    consumer_key = creds[0][0]
    consumer_secret = creds[0][1]
    access_token = creds[0][2]
    access_token_secret = creds[0][3]

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    # Sample method, used to update a status
    # api.update_status(status = tweetString)
    geos = [[37.427621,-122.161944], [37.793372,-122.39711], [37.334308,-121.890445], [38.897691,-77.036488],
            [38.889804,-77.009185], [40.762374,-73.973912],[37.3323,-121.8897], [37.22215,-121.98388], [37.79457,-122.400264],
            [47.603017,-122.33872]]
    cords = random.choice(geos)
    latitude = cords[0]
    longitude = cords[1]
    api.update_status(status=tweetString, lat=latitude, long=longitude)
    print("Tweet Posted")




#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = re.sub('[^A-Za-z0-9]+', '', str(dataString))
    return dataString

#### TWEET PROCESSING
def twitterTweetBot():
    print("starting post")
    tweetRssLog = []
    #### CHANGE THE NUMBER OF TWEETS TO POST PER CYCLE
    tweetNumbToPost = 1
    with open(str('{}/tweetBotLogger.csv'.format(pwdDir())), 'r') as tweetLog:
        tweetLogFile = csv.reader(tweetLog, delimiter=',', quotechar='"')
        for eachRow in tweetLogFile:
            tweetRssLog.append(eachRow)
        # print(tweetRssLog)
    

    tweetDict = {"http://feeds.feedburner.com/TechCrunchIT": "#tech",
                    "http://feeds.feedburner.com/TechCrunch/startups": "#startup",
                    "http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml": "#tech",
                    "https://www.wired.com/feed/category/security/latest/rss": "#security",
                    "https://www.wired.com/feed/rss": "#tech #news",
                    "https://www.wired.com/feed/category/science/latest/rss": "#science",
                    "https://www.wired.com/feed/category/business/latest/rss": "#tech #business",
                    "https://krebsonsecurity.com/feed/": "#security #data",
                    "https://www.hackread.com/sec/":"#security #data #hacking",
                    "https://www.hackread.com/sec/malware/":"#security #malware",
                    "https://www.hackread.com/latest-cyber-crime/":"#security #hacking #cybercrime",
                    "https://www.hackread.com/latest-cyber-crime/phishing-scam/":"#security #phishing #cybercrime",
                    "https://www.hackread.com/how-to/": "#lifehack #tech #howto",
                    "https://www.hackerone.com/blog/category/Data%20and%20Analysis":"#data #analysis",
                    "https://www.hackread.com/cyber-events/cyber-attacks-cyber-events/":"#security #cyberattack #data",
                    "https://www.hackread.com/cyber-events/censorship/": "#censorship",
                    "https://www.hackread.com/surveillance/":"#surveillance",
                    "http://starbridgepartners.com/data-science-report/":"#data #DataScience #DataEngineering",
                    "https://www.smartdatacollective.com/feed/":"#data #DataScience #DataEngineering",
                    "https://insidebigdata.com/feed/":"#bigdata #data #DataScience #DataEngineering",
                    "https://simplystatistics.org/":"#data #statistics #DataScience #DataEngineering",
                    "https://101.datascience.community/":"#data #DataScience #DataEngineering",
                    "https://dataconomy.com/":"#data #DataScience #DataEngineering",
                    "https://www.hackread.com/surveillance/drones/":"#drone #security #surveillance",
                    "https://www.hackread.com/surveillance/nsa/": "#nsa #security #surveillance",
                    "https://www.hackread.com/surveillance/privacy/":"#privacy #security #surveillance"
                    }

    feedRow = (random.choice(list(tweetDict.items())))
    print(feedRow)
    RssFeedURL = feedRow[0]
    RssFeedHashTag = feedRow[1]
    tweetLimitCount = 0
    getRss = feedparser.parse(RssFeedURL)
    for feed in getRss.entries:
        rssFeedTitle = feed.title
        rssFeedLinkURL = feed.link
        rssSerialNumber = charcterCleaner(feed.link)[8:48]
        if rssSerialNumber not in tweetRssLog:
            # print (rssSerialNumber)
            if tweetLimitCount < tweetNumbToPost:
                passString = rssFeedTitle + " " + tiny_url(rssFeedLinkURL) + " " + RssFeedHashTag
                tweetPoster(passString)
                tweetLimitCount += 1
                with open(str('{}/tweetBotLogger.csv'.format(pwdDir())), 'a') as tweetLog:
                    tweetLogFile = csv.writer(tweetLog, delimiter=',', quotechar='"')
                    tweetLogFile.writerow([rssSerialNumber])
            else:
                None


if __name__ == "__main__":
    twitterTweetBot()

    # #### CHANGE THE START AND END HOUR FOR EXAMPLE
    # #### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
    # #### HOUR CLOCK
    # startTime = 5  # Start at 5 am
    # endTime = 21  # end at 9pm

    # randomNumber = random.randint(0, 55)
    # print (randomNumber)
    # if randomNumber <= 38:
    #     sleepTime = randomNumber * 30
    #     currentHour = datetime.datetime.now().hour
    #     print("Current Hour: {}".format(currentHour))
    #     if currentHour >= startTime and currentHour <= endTime:
    #         time.sleep(sleepTime)
    #         twitterTweetBot()
    #     else:
    #         sys.exit()
    #         None
    # else:
    #     sys.exit()
    #     None

