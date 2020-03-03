import os
import csv

def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

tweetRssLog = []
with open(str('{}/tweetBotLogger.csv'.format(pwdDir())), 'r') as tweetLog:
    tweetLogFile = csv.reader(tweetLog, delimiter=',', quotechar='"')
    print (tweetLogFile)
    for eachRow in tweetLogFile:
        tweetRssLog.append(eachRow)

    print(tweetRssLog)