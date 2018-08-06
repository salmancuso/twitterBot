import tweepy
import feedparser
import tinyurl
import csv
import time
import datetime
import random
import sys
import re
import os


def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def getCreds():
    credList = []
    with open(str(pwdDir())+str('/mycreds.csv'), 'r') as credsRaw:
        credsData = csv.reader(credsRaw, delimiter=",")
        for item in credsData:
            credList.append(item)
        return credList


#### TWITTER API INTERFACE, ADD YOUR KEYS AND TOKENS
def tweetPoster(tweetString):
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
    geos = [[37.427621, -122.161944], [37.793372, -122.39711], [37.334308, -121.890445], [38.897691, -77.036488],
            [38.889804, -77.009185], [40.762374, -73.973912]]
    cords = random.choice(geos)
    latitude = cords[0]
    longitude = cords[1]
    api.update_status(status=tweetString, lat=latitude, long=longitude)


#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = re.sub('[^A-Za-z0-9]+', '', str(dataString))
    return dataString

#### TWEET PROCESSING
def twitterTweetBot():
    tweetRssLog = []
    #### CHANGE THE NUMBER OF TWEETS TO POST PER CYCLE
    tweetNumbToPost = 1
    with open(str(pwdDir())+str('/tweetBotLogger.csv'), 'rb') as tweetLog:
        tweetLogFile = csv.reader(tweetLog, delimiter=',', quotechar='"')
        for eachRow in tweetLogFile:
            tweetRssLog.append(eachRow[0])

        tweetDict = {"http://feeds.feedburner.com/TechCrunchIT": "#tech",
                     "http://feeds.feedburner.com/TechCrunch/startups": "#startup",
                     "http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml": "#tech",
                     "https://www.wired.com/feed/category/security/latest/rss": "#security",
                     "https://www.wired.com/feed/rss": "#tech #news",
                     "https://www.wired.com/feed/category/science/latest/rss": "#science",
                     "https://www.wired.com/feed/category/business/latest/rss": "#tech #business",
                     "http://feeds.arstechnica.com/arstechnica/technology-lab": "#tech",
                     "http://feeds.arstechnica.com/arstechnica/business": "#tech #business",
                     "http://feeds.arstechnica.com/arstechnica/security": "#security #hacktivism",
                     "http://feeds.arstechnica.com/arstechnica/tech-policy": "#tech #law"}

    feedRow = (random.choice(list(tweetDict.items())))
    RssFeedURL = feedRow[0]
    RssFeedHashTag = feedRow[1]
    tweetLimitCount = 0
    getRss = feedparser.parse(RssFeedURL)
    for feed in getRss.entries:
        rssFeedTitle = feed.title
        rssFeedLinkURL = feed.link
        rssSerialNumber = charcterCleaner(feed.link)[8:48]
        if rssSerialNumber not in tweetRssLog:
            print rssSerialNumber
            if tweetLimitCount < tweetNumbToPost:
                passString = rssFeedTitle + " " + tinyurl.create_one(rssFeedLinkURL) + " " + RssFeedHashTag
                tweetPoster(passString)
                tweetLimitCount += 1
                with open(str(pwdDir())+str('/tweetBotLogger.csv'), 'a') as tweetLog:
                    tweetLogFile = csv.writer(tweetLog, delimiter=',', quotechar='"')
                    tweetLogFile.writerow([rssSerialNumber])
            else:
                None


if __name__ == "__main__":
    #### CHANGE THE START AND END HOUR FOR EXAMPLE
    #### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
    #### HOUR CLOCK
    startTime = 6  # Start at 6 am
    endTime = 21  # end at 9pm

    randomNumber = random.randint(0, 55)
    print randomNumber
    if randomNumber <= 38:
        sleepTime = randomNumber * 60
        currentHour = datetime.datetime.now().hour
        dayOfTheWeek = datetime.datetime.today().weekday()
        print ("the day of the week is {}".format(dayOfTheWeek))
        print ("the current hours is {}".format(currentHour))
        if dayOfTheWeek > 4 and dayOfTheWeek <= 6:
            # print ("weekend")
            sys.exit()
            None
        else:
            if currentHour >= startTime and currentHour <= endTime:
                print ("Weekday")
                # print ("""Sleep time {}""".format(sleepTime))
                time.sleep(sleepTime)
                twitterTweetBot()
            else:
                sys.exit()
                None
    else:
        sys.exit()
        None

