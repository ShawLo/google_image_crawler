#coding=utf-8

import time
from bs4 import BeautifulSoup
import json
import urllib.request
import urllib.parse
from urllib.parse import quote
import os
import threading
import socket
socket.setdefaulttimeout(10) #set time out

class Downloader(threading.Thread):
    """ Downloader is designed for downloading the picture file from web """

    def __init__(self, parent=None):
        self.parent = parent
        super(Downloader, self).__init__()

    def setDownloadInfo(self, _filename, _foldername, _url, _type):
        self.url = _url
        self.fileName = _filename
        self.type = _type
        self.folderName = _foldername
        # init data params
        self.DIR = "Pictures"
        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)

        self.DIR = os.path.join(self.DIR, self.folderName)
        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)

    def finish(self):
        # print "%s download finish\n" % self.fileName
        self.parent and self.parent.on_thread_finished(self, -1)

    def run(self):

        if len(self.type) == 0:
            self.type = "jpg"

        savePath = os.path.join(self.DIR, self.fileName + "." + self.type)

        if os.path.exists(savePath):
            print (" [Notice]File has downloaded before\nPlease Check: " + savePath)
            self.finish()
            return

        try:
            if len(self.url) == 0:
                return

            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(self.url, savePath)

            self.finish()
        except Exception as e:
            print ("could not load : " + self.url)
            print (e)


class ImageTaskMgr(object):
    """ ImageTaskMgr is designed to handle multi thread download event"""

    def __init__(self, keyword):
        self.index = 0
        self.workers = 0
        self.MAX_WORKER = 10
        self.completeTask = 0
        self.run(keyword)

    def addWorkers(self):
        if self.workers < self.MAX_WORKER:
            self.workers = self.workers + 1

    def on_thread_finished(self, thread, data):
        self.workers = self.workers + data
        self.completeTask = self.completeTask + 1
        print ("complete (%3d/%3d)" % (self.completeTask, len(self.DownList)))

    def new_thread(self):
        self.addWorkers()
        return Downloader(parent=self)

    def wait(self):
        print ("waiting for workers...")
        time.sleep(1)

    def IsFinish(self, dnList):
        return self.index <= len(dnList)

    def IsWorkersBusy(self):
        return self.workers > self.MAX_WORKER

    def get_soup(self, url, header):
        req = urllib.request.Request(url, headers=header);
        resp = urllib.request.urlopen(req);
        respData = str(resp.read().decode('utf-8'));
        return BeautifulSoup(respData, 'html.parser')

    def getDownList(self, query):
        query = quote(query)

        url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"

        header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url, header)

        ActualImages = []  # contains the link for Large original images, type of  image

        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))

        return ActualImages

    def run(self, keyword):

        query = keyword.split()
        query = '+'.join(query)

        start = int(round(time.time() * 1000))
        # get the download url list from response
        self.DownList = self.getDownList(query)
        print ("DownList: %d" % (len(self.DownList)))
        print ("Start Download Imgaes of %s" % keyword)
        threads = []

        while self.IsFinish(self.DownList):
            if self.IsWorkersBusy():
                self.wait()
            else:
                thread = self.new_thread()
                # print "current workers: %d" % self.workers

                if self.index >= len(self.DownList):
                    break

                link, Type = self.DownList[self.index]

                thread.setDownloadInfo("%03d" % self.index, keyword, link, Type)
                thread.start()
                threads.append(thread)
                self.index = self.index + 1

        for t in threads:
            t.join()

        finish = int(round(time.time() * 1000))
        finishTime = (finish - start)/1000

        print ("=============================")
        print ("Search Result: %s" % keyword)
        print ("=============================")
        print ("Success : %4d" % self.completeTask)
        print ("Fail    : %4d" % (len(self.DownList) - self.completeTask))
        print ("Time Consume: %d sec" % finishTime)
        print ("=============================")

    def search(self, keyword):
        self.__init__(keyword)


# for unit test
def main():
    # just put the keyword you want to search to the class
    # ImageTaskMgr will auto download images
    mgr = ImageTaskMgr("saorise ronan")
    # for testing chinese character
    mgr.search("瑟夏·羅南")

if __name__ == "__main__":
    main()
