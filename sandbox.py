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

def feedToPost():
    feedList = []
    with open(str("{}/feeds.csv".format(pwdDir())), "r") as rawRSSfeeds:
        feedsData = csv.reader(rawRSSfeeds)
        for feedRow in feedsData:
            feedURL = feedRow[0]
            feedHashes = feedRow[1]
            feedList.append([feedURL,feedHashes])
    randomListReturn = (random.randint(0,len(feedList)-1))
    return (feedList[randomListReturn])

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def getCreds():
    credList = []
    with open(str('{}/mycreds.csv'.format(pwdDir())), 'r') as credsRaw:
        credsData = csv.reader(credsRaw, delimiter=",")
        for item in credsData:
            credList.append(item)
        return credList

def logToRead():
    logList = []
    with open(str('{}/logFile.csv'.format(pwdDir())), "r") as rawRSSlogs:
        logsData = csv.reader(rawRSSlogs)
        for logRow in logsData:
            logURL = logRow[0]
            logList.append(logURL)
    logList = sorted(list(set(logList)))
    return (logList)

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
    geos = [[37.427621,-122.161944], [37.793372,-122.39711], [37.334308,-121.890445], [38.897691,-77.036488],
            [38.889804,-77.009185], [40.762374,-73.973912],[37.3323,-121.8897], [37.22215,-121.98388], [37.79457,-122.400264],
            [47.603017,-122.33872]]
    cords = random.choice(geos)
    latitude = cords[0]
    longitude = cords[1]
    api.update_status(status=tweetString, lat=latitude, long=longitude)

#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = re.sub('[^A-Za-z0-9]+', '', str(dataString))
    return dataString

#### TWEET PROCESSING
def twitterTweetBot(logFile,cycleCount):
    print("Cycle Count: {}".format(cycleCount))
    if cycleCount < 30:
        print("step0")
        tweetRssLog = logToRead()
        print("step1")
        feedRow = feedToPost()
        print("step2")
        RssFeedURL = feedRow[0]
        RssFeedHashTag = feedRow[1]
        tweetLimitCount = 0
        print("step3")
        getRss = feedparser.parse(RssFeedURL)
        print("step4")
        entries = getRss.entries
        time.sleep(1)
        print("step5")
        for feed in entries:
            print("step6")
            rssFeedTitle = feed.title
            rssFeedLinkURL = feed.link
            rssSerialNumber = charcterCleaner(feed.link)[8:100]
            if rssSerialNumber not in tweetRssLog:
                ### POST TO TWITTER ##########
                print("POSTED TO TWITTER: {}".format(rssSerialNumber))
                with open(logFile, 'a') as tweetLog:
                    tweetLogFile = csv.writer(tweetLog, delimiter=',', quotechar='"')
                    tweetLogFile.writerow([rssSerialNumber])
                sys.exit()  #### End Program after post. 
            else:
                print("Already Posted: {}".format(rssSerialNumber))
                cycleCount+=1
                twitterTweetBot(logFile,cycleCount)
    else:
        print("step7")
        sys.exit()  #### End Program Nothing to post.




if __name__ == "__main__":
    # logFile = str('{}/logFile.csv'.format(pwdDir()))
    # twitterTweetBot(logFile, 0)


    #### CHANGE THE START AND END HOUR FOR EXAMPLE
    #### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
    #### HOUR CLOCK
    startTime = 5  # Start at 5 am
    endTime = 21  # end at 9pm

    randomNumber = random.randint(0, 55)
    print (randomNumber)
    if randomNumber <= 38:
        sleepTime = randomNumber * 30
        currentHour = datetime.datetime.now().hour
        print("Current Hour: {}".format(currentHour))
        if currentHour >= startTime and currentHour <= endTime:
            # time.sleep(sleepTime)
            logFile = str('{}/logFile.csv'.format(pwdDir()))
            twitterTweetBot(logFile, 0)
        else:
            sys.exit()
            None
    else:
        sys.exit()
        None

