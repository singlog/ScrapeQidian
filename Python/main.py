'''
Created on Oct 20, 2017

@author: zyrgz
'''

from bookinfo import getBookInfo
from condb import Connection
import time
import random
import json

with open('../config/file_config') as f:
    data = json.load(f)
    filename = data["filename"]
    tempfile = open(filename,'r+')


conn = Connection()

try:
    for line in tempfile:
        info = getBookInfo(line)
        conn.saveBookInfo(**info)
        time.sleep(1 + random.random())

        rand = random.randrange(1,100,1)
        if(rand == 67 or rand == 83):
            time.sleep(15 + 5 * random.random())
        elif(rand < 8):
            time.sleep(3 + 2*random.random())

except IndexError:
    print(line)
finally:
    tempfile.close()
    conn.end()



