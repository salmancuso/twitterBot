import tweepy
import feedparser
import tinyurl
import random
import csv
import datetime
import re

def randomDice():
    threshold = 30
    roll =(int(random.uniform(1, 100)))
    if roll < int(threshold):
        return True
    else:
        return False

def getCreds():
    with open('mycreds.csv', 'r') as credsRaw:
        credsData = csv.reader(credsRaw, delimiter=",")
        return credsData


#### TWITTER API INTERFACE, ADD YOUR KEYS AND TOKENS
#### YOU WILL NEED TO GET THESE KEYS AND TOKENS
#### AT http://apps.twitter.com
def tweetPoster(tweetString):
    # Consumer keys and access tokens, used for OAuth
    creds=getCreds()
    consumer_key = creds[0]
    consumer_secret = creds[0]
    access_token = creds[0]
    access_token_secret = creds[0]

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    # Sample method, used to update a status
    api.update_status(status = tweetString)

#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = re.sub('[^A-Za-z0-9]+', '', dataString)
    return dataString

#### TWEET PROCESSING
def twitterTweetBot():
    #### CHANGE THE NUMBER OF TWEETS TO POST PER CYCLE
    tweetNumbToPost = 1

    tweetRssLog = []
    with open('tweetBotLogger.csv', 'rb') as tweetLog:
        tweetLogFile = csv.reader(tweetLog, delimiter=',', quotechar='"')
        for eachRow in tweetLogFile:
            tweetRssLog.append(eachRow[0])

    with open('tweetData.csv', 'rb') as rssStuff:
        rssFeedData = csv.reader(rssStuff, delimiter=',', quotechar='"')
        rssFeedData.next()
        tweetLimitCount = 0
        for feedRow in rssFeedData:
            RssFeedURL =  feedRow[1]
            RssFeedHashTag = feedRow[0]
            getRss = feedparser.parse(RssFeedURL)
            for feed in getRss.entries:
                rssFeedTitle = feed.title
                rssFeedLinkURL = feed.link
                rssSerialNumber = charcterCleaner(feed.link)[8:48]
                if rssSerialNumber in tweetRssLog:
                    None
                else:
                    with open('tweetBotLogger.csv', 'a') as tweetLog:
                        tweetLogFile = csv.writer(tweetLog, delimiter=',', quotechar='"')
                        tweetLogFile.writerow([rssSerialNumber])
                        passString = rssFeedTitle + " " + tinyurl.create_one(rssFeedLinkURL) + " " + RssFeedHashTag
                        if len(passString)>280:
                            None
                        else:
                            if tweetLimitCount <= tweetNumbToPost:
                                tweetPoster(passString)
                                tweetLimitCount = tweetLimitCount + 1
                            else:
                                None


#### HOURS TO OPERATE TWITTER BOT
#### CHANGE THE HOURS TO CHANGE POSTING WITHIN TIMES
#### THIS IS POSTING BETWEEN 6AM & 9PM
currentHour = datetime.datetime.now().hour
#### CHANGE THE START AND END HOUR FOR EXAMPLE
#### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
#### HOUR CLOCK
startTime = 6  # Start at 6 am
endTime = 21  # end at 9pm
if currentHour >= startTime and currentHour <= endTime:
    twitterTweetBot()
