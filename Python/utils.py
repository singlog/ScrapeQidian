'''
Created on Oct 23, 2017

@author: zyrgz
'''

from _datetime import date, timedelta

def formatDate(rawdate):
    return rawdate[0:4] + '-' + rawdate[5:7] + '-' + rawdate[8:10]

def yesterday():
    yesterday = date.today() - timedelta(days = 1)
    return str(yesterday)

def convertNum(num, numunit, unitlen):
    
    if len(numunit) == unitlen:
        unit = 1
    else:
        unit = 10000
    
    numchar = int(float(num) * unit)
    return numchar