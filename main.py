from bs4 import BeautifulSoup
import requests
from urllib import request
import re
import json
import os
from math import floor, ceil


def get_by_url(url):
    res = request.urlopen(url)
    return res


def savePic(picSrc, savePath):
    picName = picSrc.split('/')[5]
    savePath = savePath + picName
    if not os.path.exists(savePath):
        request.urlretrieve(picSrc, savePath, print('儲存圖片: %s' % savePath))
    else:
        print('已有重複檔案:%s' % picName)
    return


def grab(up_id, savePath_t, keywords):

    urlList = []

    url1 = 'https://api.bilibili.com/x/space/navnum?mid=%s' % up_id
    res = get_by_url(url1)
    page = json.load(res)
    imgTotalCount = page['data']['album']
    if(imgTotalCount <= 0):
        print("相簿沒有內容")
        return
    else:
        print("總共有%d個相簿" % imgTotalCount)
        page_count = ceil(imgTotalCount/30)

    for page_num in range(0, page_count):

        #print("在第%d頁" % (page_num+1))
        url2 = 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid=%s&page_num=%d&page_size=30&biz=all&jsonp=jsonp' % (
            up_id, page_num)
        res = get_by_url(url2)
        articals = json.load(res)
        articals = articals['data']
        for i in articals['items']:

            keywordFound = False
            title = i['description']
            for str in keywords:
                if(title.find(str) != -1):
                    keywordFound = True
                    break

            if(keywordFound == True):
                for j in i['pictures']:
                    picSrc = j['img_src']
                    urlList.append(picSrc)

    imgTotal = len(urlList)
    print("共%d張圖片符合關鍵字" % imgTotal)

    imgCount = 0

    for i in urlList:
        savePath = ''
        picSrc = i
        picName = picSrc.split('/')[5]
        savePath = savePath_t + picName
        if not os.path.exists(savePath):
            request.urlretrieve(picSrc, savePath)
            imgCount += 1
            print('儲存圖片(%d/%d): %s' % (imgCount, imgTotal, savePath))
        else:
            print('已有重複檔案:%s' % picName)

    print("結束抓取")


save_path = 'D:/fuck/'
up_id = '256667467'
keywords = ['壁纸', 'cg', 'CG']

grab(up_id, save_path, keywords)
