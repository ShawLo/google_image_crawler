# a copy from stackoverflow.com
# https://www.google.com.tw/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwioncq-lOfTAhXEoJQKHbrBBA8QFggvMAE&url=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F35809554%2Fhow-to-download-google-image-search-results-in-python&usg=AFQjCNHQ7vhztmREXB4vi2M1pii0fuYcMg&sig2=hmcYoabTzYaWAXdiw4gDmA

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


query = raw_input("Key word? ")# you can change the query for the image  here
image_type="beauty"
query= query.split()
query='+'.join(query)

url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print url

#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image

for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print "ActualImages[0]: %s"%str(ActualImages[0])

print  "there are total" , len(ActualImages),"images"

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate(ActualImages):
    try:
        print img
        print header
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e
