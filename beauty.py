import queue
import threading
import time
import os
from bs4 import BeautifulSoup
import requests 
import re
from urllib.request import urlopen 
import urllib.request

class myThread (threading.Thread):
    def __init__(self, threadID, name, fileurl, dlfolder):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.fileurl = fileurl
        self.dlfolder = dlfolder
    def run(self):
        process_data(self.name, self.fileurl, self.dlfolder)

def process_data(threadName, fileurl, dlfolder):
    while not exitFlag:
        if not fileurl.empty():               
            url = fileurl.get()
            data = url.split("filename=")
            code = data[0]
            filename = data[1]
            dname = data[2]
            name = re.sub('[?/<:>"\\* ]', '', filename)
            dlurl = get_download_url(code)
            if (code == dlurl):
                #print ("%s %s" %( code, name))
                save_file(code, dlfolder, name, dname)
            else :
                print("%s %s下載失敗" %(code, dlurl))
        time.sleep(1)

def download_file(dlurl):
    req = urllib.request.Request(dlurl)
    response = urllib.request.urlopen(req)
    return response.read()

def get_all_page():
    res = requests.get("https://www.ptt.cc/bbs/Beauty/index.html")
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.find_all('a', 'btn wide')
    title = str(a[1]['href'])
    title = re.sub("[^0-9]", "",title)
    value = int(title)
    first = value+1
    return str(first)

def get_page_article(firstpage,num):
    url = "https://www.ptt.cc/bbs/Beauty/index"
    articleList = []
    pageNum = 0
    pageUrl = url + str(firstpage - num + 1) + ".html"
    res = requests.get(pageUrl)
    soup = BeautifulSoup(res.text, 'html.parser')
    for article in soup.select('.r-ent a'):
        if "[正妹]" in str(article):
            articleList.append(article)
        else:
            continue
    return articleList


    
    

if __name__ == "__main__":
    articleList = get_page_article(2325,1)
    print(articleList)