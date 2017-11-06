#!/usr/bin/env python
# -- coding: utf-8 --

__author__ = 'shizf'

import os
import requests
import re
import datetime
from PIL import Image
import win32con, win32api, win32gui

str_BingUrl = 'https://cn.bing.com'
currentTime = datetime.datetime.now()
currentDay = currentTime.strftime('%Y-%m-%d')

def getReqContent(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        # print(resp.content)
        return resp.text

def canUseInternet():
    '''
    测试网络连接情况
    '''
    resp = requests.get('http://www.baidu.com')
    if resp.status_code == 200:
        return True
    else:
        return False

# g_img={url: "/az/hprichbg/rb/TaProhm_ZH-CN9310499614_1920x1080.jpg",id

def getImageUrl(html):
    """
    dfsfsd
    """
    p1 = '(g_img={url: "[\d\D]*.jpg)",id'
    pattern1 = re.compile(p1)
    matcher1 = re.search(pattern1,str(html))
    if len(matcher1.groups())>0:
        return matcher1.group(0)[13:-4]
    else:
        return 'error'

def downloadByUrl(url):
    info = requests.get(url)
    if info.status_code == 200:
        fileName = 'imgs/' + currentDay + '.jpg'
        with open(fileName,'wb') as files:
            files.write(info.content)
            fSeed = open('seed.cfg','w')
            fSeed.write(currentDay)
            return True
    else:
        return False

def setWallPaper(imagePath):
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")
    return newPath


def isNeedUpdate():
    with open('seed.cfg','r') as target:
        info = target.readline()
        if info == currentDay:
            return False
        else:
            return True

def setWallpaperFromBMP():
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    path = setWallPaper(currentPwd())
    print('newPath:'+path)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 3)

def currentPwd():
    ll = os.getcwd()+'/imgs/'+currentDay+'.jpg'
    return ll

if __name__ == '__main__':
    isok = canUseInternet()
    if isok:
        if isNeedUpdate():
            url = getImageUrl(getReqContent(str_BingUrl))
            print(str_BingUrl+url)
            downloadByUrl(str_BingUrl+url)
            setWallpaperFromBMP()
            print ('setup Success')
        else:
            setWallpaperFromBMP()
            print ('no need update')
    else:
        print ('no internet connection')
