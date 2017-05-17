# 參考下列網址得來的 Google Image Search 下載範例
# https://www.google.com.tw/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwioncq-lOfTAhXEoJQKHbrBBA8QFggvMAE&url=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F35809554%2Fhow-to-download-google-image-search-results-in-python&usg=AFQjCNHQ7vhztmREXB4vi2M1pii0fuYcMg&sig2=hmcYoabTzYaWAXdiw4gDmA

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import time

# python 定義呼叫的function，用來回傳html裡面語法整理好的結果給外部呼叫使用，
# 舉例來說，用網頁google完後會看到搜尋完美美的網頁，其實網頁原本的模樣是
# <!doctype html><html itemscope="" itemtype="http://schema.org/SearchResultsPage" lang="zh-TW"><head><meta content="/images/br.....
# 用任何瀏覽器，點選“檢視網頁原始碼”就可以看到了！
# BeautifulSoup 型態（別人寫好的 Tool)
# 用這個 Tool 可以很輕鬆擷取 html 語法裡面的 tag, class, 或一些 attr的屬性，就可以用來爬蟲啦～
def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

# 這邊在等外部使用者輸入要搜尋的keyword
query = raw_input("Key word? ")# you can change the query for the image  here
image_type="beauty"
query= query.split()
query='+'.join(query)
# Google 搜尋網址定義
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
# 用來存開始執行程式的時間，塞到start變數裡
start = int(round(time.time() * 1000))
# 檔案下載的路徑定義
DIR="Pictures"
# header 在連線時用來宣告一些瀏覽器的參數，在跟網路連線的時候，告訴對方說我們的瀏覽器ＯＳ等一些狀態，不是很重要～
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
# 呼叫上面那個定義function後可以拿到 BeautifulSoup 物件實體，就可以用來擷取圖片下載的網址啦～ＹＡ～
soup = get_soup(url,header)

# 宣告一下 存放下載網址的array
ActualImages=[]# contains the link for Large original images, type of  image

# 這邊就是最重要滴！從上面 soup 中我們可以拿到 html 轉換後的結果 Tool，
# 從網頁語法中可以發現一個固定模式，就是Google都把圖片下載的網址藏在 “rg_meta" 這個class裡面
# 而這個class裡面有兩個最重要的屬性，"ou" 存放的就是下載網址，”ity"存放的是這個圖片檔的檔案格式，可能為jpg, png...
# 附註：要是未來Google更改了搜尋圖片的html語法，這邊就會失敗了
# 目前是還可以work的狀態
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

# 這邊只是叫系統印出來說有總共有多少個來源要下載
print  "there are total" , len(ActualImages),"images"
# 檢查路徑 DIR 存不存在於系統當中，不存在的話就建一個資料夾吧！
if not os.path.exists(DIR):
            os.mkdir(DIR)
# 這邊是在把原本存在放在DIR的路徑多增加一個資料夾名稱為query
DIR = os.path.join(DIR, query.split()[0])
# 一樣在檢查是否存在，不存在就新建一個資料夾吧～
if not os.path.exists(DIR):
            os.mkdir(DIR)
###這邊就是把剛剛上面存好下載網址的array，一個一個抓網址出來下載，不過這樣做是一個很慢的做法～
###ImageTaskMgr改寫了這段下載流程，讓下載速度可以提昇好幾倍！！
for i , (img , Type) in enumerate(ActualImages):
    try:
        # 下面這行就是在做連線的準備，把你要跟誰連線，連線的位置做初始
        # 初始完就可以準備下載圖片檔囉～
        req = urllib2.Request(img, headers={'User-Agent' : header})
        # 這行就是成功下載到圖片的檔案啦，裡面是一堆機器才看得懂的代碼，這些代碼都會存到raw_img這個變數當中
        raw_img = urllib2.urlopen(req).read()
        # 設定存檔名稱
        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        # 判斷如果圖片檔定義不存在，就直接預設塞jpg檔案的格式給他
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')

        # 把我們剛剛下載到的圖片檔案代碼，寫到系統當中，原本下載回來的圖片代碼是存在在記憶體當中
        # 寫完檔以後才會存在在電腦系統中供我們觀看喔！
        f.write(raw_img)
        # 寫完檔以後，就要跟系統說我們寫完檔了，現在可以關閉了，這個很重要喔～
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e
# 全部的下載都做完事情了，記錄結束的存到 finish 變數中
finish = int(round(time.time() * 1000))
# finishTime 就是 完成時間 減去 開始的時間，就知道下載圖片總共花了多少時間啦～
finishTime = (finish - start)/1000
# 把總共花多少時間印出來看看囉！
print "Time: %d" % finishTime
