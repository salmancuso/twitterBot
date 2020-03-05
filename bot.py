#!/usr/bin/python3
import feedparser
import csv
import sys
import os
import random
import tweepy
import re
import urllib.request
import datetime


#### GET CURRENT FULL PATH TO DIRECTORY
def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

#### GET CREDS AND CREATE LIST.
def getCreds():
    credList = []
    with open(str('{}/mycreds.csv'.format(pwdDir())), 'r') as credsRaw:
        credsData = csv.reader(credsRaw, delimiter=",")
        for item in credsData:
            credList.append(item)
        return credList


#### OPEN LIST OF RSS FEEDS AND RANDOMLY PICK ONE TO PUBLISH. 
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


#### CLEAN UP SERIAL NUMBER FOR TRACKING
def charcterCleaner(dataString):
    dataString = re.sub('[^A-Za-z0-9]+', '', str(dataString))
    dataString = str(dataString).upper()
    return dataString

#### BUILD A TINY URL TO PUSH 
def tinyUrl(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

#### TWITTER API INTERFACE, ADD YOUR KEYS AND TOKENS
def tweetPusher(tweetString):
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


#### RETURN LIST OF POSTS ALREADY MADE
def logToRead():
    logList = []
    with open(str('{}/logFile.csv'.format(pwdDir())), "r") as rawRSSlogs:
        logsData = csv.reader(rawRSSlogs)
        for logRow in logsData:
            logURL = logRow[0]
            logList.append(logURL)
    logList = sorted(list(set(logList)))
    return logList

def tweetPoster(tryCounter):
    feedCombo = feedToPost()

    logFile = list(logToRead())
    feedURL = feedCombo[0]
    feedHashTags = feedCombo[1]
    feedData = feedparser.parse(feedURL)
    if feedData[ "bozo" ] == 0: ## if 0, then it is a good feed.
        # print(feedData[ "bozo" ])
        print(feedData[ "url" ])
        # print(feedData[ "channel" ][ "title" ] )
        # print(feedData[ "channel" ][ "description" ])
        # print(feedData[ "channel" ][ "link" ])
        for item in feedData["items"]:
            print("Attempt {}".format(tryCounter))
            if tryCounter < 10:
                title = (item[ "title" ])
                link = tinyUrl(item[ "link" ])
                hashTags = (feedHashTags)
                UID = str(charcterCleaner(str(title + link + hashTags)))[0:50]
                print(UID)
                if UID not in logFile:
                    tweetString = ("""{} {} {}""".format(title, link, hashTags))
                    tweetPusher(tweetString)
                    print("POSTED TO TWITTER: {}".format(UID))
                    with open(str('{}/logFile.csv'.format(pwdDir())), 'a') as tweetLog:
                        tweetLogFile = csv.writer(tweetLog, delimiter=',', quotechar='"')
                        tweetLogFile.writerow([UID])
                    tryCounter += 1
                    sys.exit()
                    None
                else:
                    tryCounter += 1
            else:
                sys.exit()
                None



######################
if __name__ == "__main__": 
    #### HOUR CLOCK
    startTime = 5  # Start at 5 am
    endTime = 21  # end at 9pm

    randomNumber = random.randint(0, 55)
    print (randomNumber)
    if randomNumber <= 35:
        sleepTime = randomNumber * 30
        currentHour = datetime.datetime.now().hour
        print("Current Hour: {}".format(currentHour))
        if currentHour >= startTime and currentHour <= endTime:
            time.sleep(sleepTime)
            tryCounter = 0
            tweetPoster(tryCounter)
        else:
            sys.exit()
            None
    else:
        sys.exit()
        None
