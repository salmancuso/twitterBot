import tweepy
import feedparser
import tinyurl
import os
import csv
import datetime

tweetRssLog =[]

#### CHANGE THE NUMBER OF TWEETS TO POST PER CYCLE
tweetNumbToPost = 1

#### CHANGE THE START AND END HOUR FOR EXAMPLE
#### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
#### HOUR CLOCK
startTime = 6 # Start at 6 am
endTime = 21 # end at 9pm


#### TWITTER API INTERFACE, ADD YOUR KEYS AND TOKENS
#### YOU WILL NEED TO GET THESE KEYS AND TOKENS
#### AT http://apps.twitter.com
def tweetPoster(tweetString):
    # Consumer keys and access tokens, used for OAuth
    consumer_key = 'YOUR-CONSUMER-KEY-HERE-IN-QUOTES'
    consumer_secret = 'YOUR-CONSUMER-SECRET-HERE-IN-QUOTES'
    access_token = 'YOUR-ACCESS-TOKEN-HERE-IN-QUOTES'
    access_token_secret = 'YOUR-ACCESS-TOKEN-SECRET-HERE-IN-QUOTES'

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    # Sample method, used to update a status
    api.update_status(status = tweetString)

#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = dataString.replace('.', '')
    dataString = dataString.replace('!', '')
    dataString = dataString.replace(',', '')
    dataString = dataString.replace('-', '')
    dataString = dataString.replace("'", '')
    dataString = dataString.replace('@', '')
    dataString = dataString.replace('#', '')
    dataString = dataString.replace('$', '')
    dataString = dataString.replace('%', '')
    dataString = dataString.replace('^', '')
    dataString = dataString.replace('&', '')
    dataString = dataString.replace('*', '')
    dataString = dataString.replace("(", '')
    dataString = dataString.replace(')', '')
    dataString = dataString.replace('_', '')
    dataString = dataString.replace('?', '')
    dataString = dataString.replace(' ', '')
    dataString = dataString.replace(';', '')
    dataString = dataString.replace(':', '')
    dataString = dataString.replace('"', '')
    dataString = dataString.replace('/', '')
    dataString = dataString.replace('=', '')
    dataString = dataString.replace('~', '')
    return dataString

#### TWEET PROCESSING
def twitterTweetBot():
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
                        if len(passString)>140:
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
if currentHour >= startTime and currentHour <= endTime:
    twitterTweetBot()
