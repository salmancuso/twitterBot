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
def twitterTweetBot():
    tweetRssLog = []
    #### CHANGE THE NUMBER OF TWEETS TO POST PER CYCLE
    tweetNumbToPost = 1
    with open(str('{}/tweetBotLogger.csv'.format(pwdDir())), 'r') as tweetLog:
        tweetLogFile = csv.reader(tweetLog, delimiter=',', quotechar='"')
        print (tweetLogFile)
        for eachRow in tweetLogFile:
            tweetRssLog.append(eachRow)

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
                     "http://feeds.arstechnica.com/arstechnica/tech-policy": "#tech #law",
                     "https://krebsonsecurity.com/feed/": "#security #data",
                     "https://www.darkreading.com/rss_simple.asp?f_n=644&f_ln=Attacks/Breaches": "#security #data #breach",
                     "https://www.darkreading.com/rss_simple.asp?f_n=645&f_ln=Application%20Security": "#security #data #Application",
                     "https://www.darkreading.com/rss_simple.asp?f_n=647&f_ln=Cloud": "#cloud #data",
                     "https://www.darkreading.com/rss_simple.asp?f_n=649&f_ln=Authentication": "#authentication #security",
                     "https://www.darkreading.com/rss_simple.asp?f_n=650&f_ln=Privacy": "#privacy #data",
                     "https://www.darkreading.com/rss_simple.asp?f_n=661&f_ln=Vulnerabilities%20/%20Threats": "#Vulnerability #security",
                     "https://www.darkreading.com/rss_simple.asp?f_n=659&f_ln=Threat%20Intelligence": "#ThreatIntelligence #security #data"
                     }

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
            print (rssSerialNumber)
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
    #### CHANGE THE START AND END HOUR FOR EXAMPLE
    #### 5 IS 5 AM WHILE 20 IS 8PM BASED ON THE 24
    #### HOUR CLOCK
    startTime = 5  # Start at 5 am
    endTime = 21  # end at 9pm

    randomNumber = random.randint(0, 55)
    print (randomNumber)
    if randomNumber <= 38:
        sleepTime = randomNumber * 30
        # sleepTime = 1 ### Use this for testing only 
        currentHour = datetime.datetime.now().hour
        dayOfTheWeek = datetime.datetime.today().weekday()
        print ("the current hours is {}".format(currentHour))
        if currentHour >= startTime and currentHour <= endTime:
            time.sleep(sleepTime)
            twitterTweetBot()
        else:
            sys.exit()
            None
    else:
        sys.exit()
        None

