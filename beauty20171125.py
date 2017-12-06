import queue
import threading
import time
import os
from bs4 import BeautifulSoup
import requests 
import re
from urllib.request import urlopen 
import urllib.request
exitFlag = 0


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

def save_file(dlurl, dlfolder, filename, dname):
    name = re.sub('[:]', '', dname)
    mkdir('{}'.format(dlfolder)+"\\"+'{}'.format(name))
    if (dname == " "):
        os.chdir(dlfolder)
        dlfile = download_file(dlurl)
        with open(filename, 'wb') as f:
            f.write(dlfile)
            f.close()
    else:
        os.chdir('{}'.format(dlfolder)+"\\"+'{}'.format(name))
        dlfile = download_file(dlurl)
        with open('{}'.format(dlfolder)+"\\"+'{}'.format(name)+"\\"+'{}'.format(filename), 'wb') as f:
            f.write(dlfile)
            f.close()
    return None

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        title = os.makedirs(path)
        return True
    else:
        return False

def get_download_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
    response = urllib.request.urlopen(req)
    dlurl = response.geturl()
    return dlurl


def page(num):
    res = requests.get("https://www.ptt.cc/bbs/Beauty/index.html")
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find_all('a', 'btn wide')
    title = str(a[1]['href'])
    title = re.sub("[^0-9]", "",title)
    value = int(title)
    first = value+1
    pag = first- num+1
    print(pag)
    return int(pag)

threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7"]
workQueue = queue.Queue(0)
threads = []
threadID = 1
print("歡迎來到PTT表特版下載器")
a = input("起始頁面:")
print("起始頁面請勿大於終止頁面")
b = input("終止頁面:")
agress = input("下載地點")

first = page(int(a))
final = page(int(b))

for x in range(final, first):
    res = requests.get(("https://www.ptt.cc/bbs/Beauty/index%d.html")%x)
    soup = BeautifulSoup(res.text, 'lxml')
    for article in soup.select('.r-ent a'):
        url = 'https://www.ptt.cc' + article['href']
        res = requests.get(url)
        pagesoup = BeautifulSoup(res.text, 'lxml')
        #print(len(pagesoup.find_all('a', {'href':re.compile('https://i.imgur.com/.*')})))
        
    
        if len(pagesoup.find_all('a', {'href':re.compile('https://i.imgur.com/.*')})) > 0 or len(pagesoup.find_all('a', {'href':re.compile('http://i.imgur.com/.*')})) > 0:
            
            for index, img_url in enumerate(pagesoup.find_all('a', {'href':re.compile('http://i.imgur.com/.*')})):
                title = re.search('\[\w+\]', article.text)
                if title :
                    fileurl= img_url['href']+'filename={}_{}.jpg'.format(article.text, index)+'filename={}'.format(title.group())
                    workQueue.put(fileurl)
                else:
                    fileurl= img_url['href']+'filename={}_{}.jpg'.format(article.text, index)+'filename={}'.format(" ")
                    workQueue.put(fileurl)
                    
                for tName in threadList:
                    thread = myThread(threadID, tName, workQueue, str(agress))
                    thread.start()
                    threads.append(thread)
                    threadID += 1
                
                while not workQueue.empty():
                    pass


            for index, img_url in enumerate(pagesoup.find_all('a', {'href':re.compile('https://i.imgur.com/.*')})):
                title = re.search('\[\w+\]', article.text)
                if title :
                    fileurl= img_url['href']+'filename={}_{}.jpg'.format(article.text, index)+'filename={}'.format(title.group())
                    workQueue.put(fileurl)
                else:
                    fileurl= img_url['href']+'filename={}_{}.jpg'.format(article.text, index)+'filename={}'.format(" ")
                    workQueue.put(fileurl)

                
                for tName in threadList:
                    thread = myThread(threadID, tName, workQueue, str(agress))
                    thread.start()
                    threads.append(thread)
                    threadID += 1
                
                while not workQueue.empty():
                    pass


exitFlag = 1
for t in threads:
    t.join()
print ("下載完畢")


