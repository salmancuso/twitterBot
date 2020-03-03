import os
import csv

def pwdDir ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path


with open(str(pwdDir())+str('/mycreds.csv'), 'r') as credsRaw:
    credsData = csv.reader(credsRaw, delimiter=",")
    for row in credsData:
        print (row)