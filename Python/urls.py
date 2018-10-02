'''
Created on Oct 20, 2017

@author: zyrgz
'''
import requests
from lxml import html
import json



def getBookUrls(url,page_num):
    print(page_num)
    page_num += 1
    
    page = requests.get(url)
    tree = html.fromstring(page.text)
    
    urls = tree.xpath("//body/div[@class='wrap']//div[@class='book-img-box']/a/@href")
    urlList = ["https:" + i for  i in urls ]
    nextUrl = getNextUrl(tree)    
    
    try:
        urlList.extend(getBookUrls(nextUrl,page_num))
    except requests.exceptions.InvalidURL:
        pass
        
    return urlList


def getNextUrl(tree):
    nexturl = tree.xpath("/html/body//li[@class='lbf-pagination-item'][last()]/a/@href")
    
    #print(nexturl[0])
    return "https:" + nexturl[0]


def saveUrls(filename, urlList):
    
    f = open(filename, 'w')
    
    for i in urlList:
        f.write(i)
        f.write("\n")

    f.close()
    


if __name__ == '__main__':
    with open('../config/file_config') as f:
        data = json.load(f)
        filename = data["filename"]
        targeturl = data["url"]
    with open(filename) as f:
        urlList = getBookUrls(targeturl,1)
        saveUrls(f, urlList)
    
    
    