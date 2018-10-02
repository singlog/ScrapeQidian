'''
Created on Oct 23, 2017

@author: zyrgz
'''
import requests
from lxml import html
from _overlapped import NULL
from utils import formatDate,yesterday,convertNum
import json

def getPage(url):
    header = {
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding':'gzip, deflate, br',
              'Host':'book.qidian.com',
              'Referer' : 'https://www.qdmm.com/xyly',
              'User-Agent':'Mozilla/5.0 AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',       
              }
    with open('../config/proxy_config') as f:
        proxy = json.load(f)
        infopage = requests.get(url, headers = header, proxies = proxy)
    return infopage
    
def getBookInfo(url):
    infopage = getPage(url)
    #book_id
    book_id = url[29:len(url)]
    
    
    tree = html.fromstring(infopage.text)
    
    #date
    readurl = tree.xpath("""/html/body//div[@class='book-info ']/p[4]/a[1]/@href""")[0]
    date = getDate("https:" + readurl)
    
        
    #title
    title_elm = tree.xpath("/html/body//div[@class='book-info ']/h1/em")
    title = title_elm[0].text
    
    #last_upd
    raw_last_upd = tree.xpath("/html/body//div[@class='detail']/p[@class='cf']/em[@class='time']")[0].text
    if(len(raw_last_upd) != 10):
        last_upd = yesterday()
    else:
        last_upd = formatDate(raw_last_upd[0:10])
        
    #author
    author_url = tree.xpath("/html/body//div[@class='book-info ']/h1/span/a/@href")[0]
    author_id = author_url[36:len(author_url)]
    
    #number of characters
    raw_num_char = tree.xpath("/html/body//div[@class='book-info ']/p[3]/em[1]")[0].text
    num_char_unit = tree.xpath("/html/body//div[@class='book-info ']/p[3]/cite[1]")[0].text
    numchars = convertNum(raw_num_char, num_char_unit,1)
    
    #number of views
    raw_num_view = tree.xpath("/html/body//div[@class='book-info ']/p[3]/em[2]")[0].text
    num_view_unit = tree.xpath("/html//div[@class='book-info ']/p[3]/cite[2]")[0].text
    num_views = convertNum(raw_num_view, num_view_unit, 3)
    
    #number of recommendations
    raw_num_rcmd = tree.xpath("/html/body//div[@class='book-info ']/p[3]/em[3]")[0].text
    num_rcmd_unit = tree.xpath("/html/body//div[@class='book-info ']/p[3]/cite[3]")[0].text
    num_rcmds = convertNum(raw_num_rcmd, num_rcmd_unit, 3)
    #number of chapters
    raw_num_chap = tree.xpath("/html/body//div[@class='nav-wrap fl']//li[@class='j_catalog_block']//i/span")[0].text
    try:
        num_chapters = int(raw_num_chap[1:len(raw_num_chap)-2])
    except TypeError:
        num_chapters = 0
    #class
    categ_em = tree.xpath("/html/body//div[@class='book-info ']/p[@class='tag']/a[@class='red'][1]")
    categ = categ_em[0].text
    
    sub_categ_em = tree.xpath("/html/body//div[@class='book-info ']/p[@class='tag']/a[@class='red'][2]")
    sub_categ = sub_categ_em[0].text
    
    #isFinished
    isFinished = b'0'
    status = tree.xpath("/html/body//div[@class='book-info ']/p[1]/span[1]")[0].text
    if(status == "完本"):
        isFinished = b'1'
    
    #isFree
    isFree = b'1'
    raw_is_free = tree.xpath("/html/body//div[@class='book-info ']/p[@class='tag']/span[last()]")[0].text
    if(raw_is_free == 'VIP'):
        isFree = b'0'
    
    info = { "book_id": book_id, "title":title, "author_id": author_id, 
             "num_chars":numchars, "num_chapters":num_chapters, 
             "num_views":num_views, "num_rcmds":num_rcmds,
             "category":categ, "sub_category": sub_categ,
             "start_date":date, "last_update" : last_upd, 
             "finished":isFinished, "free": isFree}
    return info

def getRate(book_id):
    url = "https://book.qidian.com/ajax/comment/index?bookId=" + book_id
    header = {'Accept':'application/json, text/javascript, */*; q=0.01'}
    
    bookdata = requests.get(url, headers = header)
    return bookdata.json()['data']['rate']
    
def getDate(url):
    try:
        page = requests.get(url)    
    except requests.exceptions.MissingSchema:
        return NULL
    else:
        tree = html.fromstring(page.text)
        rawdate = tree.xpath("/html/body//div[@class='info-list cf']/ul/li[2]/em")[0].text
        return formatDate(rawdate)



