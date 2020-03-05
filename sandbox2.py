import csv
import random

def logToRead():
    logList = []
    with open("logFile.csv", "r") as rawRSSlogs:
        logsData = csv.reader(rawRSSlogs)
        for logRow in logsData:
            logURL = logRow[0]
            logList.append(logURL)
    logList = sorted(list(set(logList)))
    return (logList)

print(logToRead())