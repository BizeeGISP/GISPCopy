import requests
import time
from bs4 import BeautifulSoup

class BS:
    soup = None
    def __init__(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def getSoup(self):
        return self.soup

    def getTitle(self):
        return self.soup.title

    def getFind_all(self, type):
        return self.soup.find_all(type)

