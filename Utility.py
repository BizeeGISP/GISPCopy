# -*- encoding: utf-8 -*-
import os
import requests
import time
from bs4 import BeautifulSoup


def getWorkingDirectory():
    return os.getcwd()

def CheckAndCreateDirectory(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

def printList(list):
    for item in list:
        print( item)



def GetPageInfo(url, type):
    data = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        data = soup.find_all(type)
    except Exception as e:
        print( e, "Connection Exception : " + url)

    return data

def isFirstCharacter(str, character):

    return str.find(character, 0, 1) > -1

def isJavaScript(str):
    return str.find('javascript', 0, len(str)) > -1

def getBaseURL(baseURL, href):
    url = None
    if "http" in href:
        url = href
    else:
        if href.find('/', 0, 1) > -1:
            url = baseURL + '/' + href.lstrip('/')

    return url

def GetContactPageURL(link_text, link_href, baseURL):
    url = None
    if ("Contact" in link_text) or ("Contact" in link_href):
        url = getBaseURL(baseURL, link_href)

    return url

def findContactPageURL(lLinks, baseURL):
    for link in lLinks:
        link_href = link[0]
        link_text = link[1]
        try:
            url = GetContactPageURL(link_text, link_href, baseURL)
        except:
            print( url, "no contact page")

    return url


def isURLExist(str, lists, position=0):
    lReturn = False
    for row in lists:
        if str == row[position]:
            lReturn = True

    return lReturn

