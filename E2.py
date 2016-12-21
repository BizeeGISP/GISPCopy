# -*- encoding: utf-8 -*-
import Utility
import time
import db
import logging
import datetime
import requests
import time
from bs4 import BeautifulSoup
from urlparse import urlparse
import E2_Form
import E2_Regions
import sys
# reload(sys)
# sys.setdefaultencoding('UTF8')

class ProcessPage:
    db = None
    updateQuery = ""
    InsertQuery = ""
    soup = None
    RMQ = None
    timeout = 60  #### 1 Min TimeOut.
    idealTime = 0

    def __init__(self):

        now = datetime.datetime.now()
        date = now.strftime(" %Y-%m-%d ")

        #print date, type(date)
        Format = '%(asctime)s - %(levelname)s - %(message)s'
        LOG_FILENAME = 'log\Engine2' + date + '.log'

        logging.basicConfig(filename=LOG_FILENAME, format=Format,level=logging.DEBUG)

        logging.info("ENGINE 2 PROCESS STARTS")
        startTime = time.time()

        self.Execute_E2()
        #self.ExecuteURLS()
        processSec = time.time() - startTime

        logging.info("Time consumed: " + str( processSec ))
        #print "Time consumed: ", time.time() - startTime

    def ExecuteURLS(self):  # Need to Comment / Remove this code
        self.InsertQuery = """INSERT INTO home_page_links (link_text, links, home_url_id) VALUES (%s,%s, %s)"""
        self.db = db.DB()
        statement = """select id, url from urls where status = 'new' and id > 0 limit 10"""
        rows = self.db.executeSelectAll(statement)
        nLen = len(rows)
        nCtr = 0
        for row in rows:
            id = row[0]
            url = row[1]
            self.ProcessUrl(url)

        self.db.close()

    def callback(self, ch, method, properties, body):
        value = body.split(",")

        url = value[0]
        url_type = value[1] ## D: Default URL, F: Foreign URL, C: Contact Page URL

        self.ProcessUrl( url, url_type)

    def Execute_E2(self):
        self.idealTime = 0
        while True:
            if self.RMQ.isMessage():
                self.idealTime = 0
                self.Msg_Time = time.time()
                self.ProcessUrl()
            else:
                self.idealTime = time.time() - self.Msg_Time
            if self.idealTime >= self.timeout:
                break

    def Read_msg_Q(self):
        #try:
            if self.RMQ.ReConnect():
                self.ReadMQ()
            else:
                print ("Exception while connecting to RabbitMQ Server")
                # Log Exception

            # rmqConn = RMQ()
            # url = None


        #return url



    def GetFQDN_URL(self, url):
        if not "http://" in url:
            url = str("http://" + url)
        return url.strip()

    def ProcessUrl(self, url, url_type):
        self.url = self.GetFQDN_URL(self.url)
        self.soup = self.GetPageSoup()
        formData = E2_Form.WebForm(self.soup)
        regionData = E2_Regions.ContactUsPage(self.soup)
        #ContactData =

        self.C_URLS = []
        self.F_URLS = []
        if   url_type == "D":   ### D: Default URLS
            self.GetPageUrls(self, url, id)    ### This function is creating two list C: Contact URL Link List and F: Foreign URL List.
        elif url_type == "F":  ### F: Foreign URLS
            self.GetPageUrls(self, url, id)    ### This function is creating two list C: Contact URL Link List and F: Foreign URL List.
            self.F_URLS = []   #### Over here we are intentionally making the Foreign link empty, as we don't want to process recursive links from Foreign Link. We will handle this on 2nd Phase of Project


        #if len(self.F_URLS) > 0:

        #
        # try:
        #     PageUrls = self.GetPageUrls(url, id)
        #     self.SaveData(self.InsertQuery, PageUrls)
        #     self.UpdateUrls(id, url)
        # except:
        #     try:
        #         self.SaveSingleData(self.InsertQuery, PageUrls)
        #         self.UpdateUrls(id, url)
        #     except:
        #         self.db = db.DB()


    def GetPageSoup(self):
        soup = None
        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content, "lxml")
        except Exception as e:
            print(e, "Connection Exception : " + self.url)
            #### Append Logging Here
        return soup

    def UpdateUrls(self, id, url):
        idStr = str(id)
        try:
            self.updateQuery = "update urls set status = 'Processed' where id = " + idStr
            self.db.execute(self.updateQuery)
            self.db.commit()
        except Exception as e:

            logging.debug("Error while updating: " + self.updateQuery+ "|" +url)
            logging.warning(e)
             #print self.updateQuery
             #print  e, "Updating Error: ", url + " | " + idStr

    def SaveSingleData(self, query, values):
        nCtr = 0
        nLen = len(values)
        for data in values:
            try:
                nCtr+=1
                if (nCtr % 50) == 0:
                    logging.info(" Data Processing: " + str(nCtr)+ "/" + str(nLen))
                    #print "Data Processing: ", str(nCtr) + "/" + str(nLen)
                self.db.execute(query, data)
                self.db.commit()
            except Exception as e:

                logging.debug("Internal loop Exception")
                logging.warning(e)

                #print e, "Internal loop Exception"

    def SaveData(self, query, values):
        self.db.executemany(query, values)
        self.db.commit()

    def GetPageUrls(self, url, id):
        try:
            hrefList = self.GetPageLinks(url)
            self.C_URLS = []
            self.F_URLS = []
            baseDomain = self.GetDomain(url)
            if len(hrefList) > 0:
                for href in hrefList:
                    href_link = href[0]
                    href_text = href[1]
                    if baseDomain in href_link:
                        c_url_str = Utility.GetContactPageURL(href_text, href_link, url)
                        if (c_url_str != None) and not (Utility.isURLExist(c_url_str, self.C_URLS)):
                            self.C_URLS.append((c_url_str, id, 'New'))
                    else:
                        self.F_URLS.append((href_text, href_link, id))

        except Exception as e:
            print(e)

    def GetPageLinks(self, url):

        links = self.soup.find_all('a')

        hrefs = []

        for link in links:
            href = str(link.get('href')).strip()

            if not Utility.isFirstCharacter(href, '#') and not self.isURLExist(href, hrefs) and not Utility.isJavaScript(href):
                hrefs.append((href, link.text.strip()))
        return hrefs

    def isFirstCharacter(str, character):

        return str.find(character, 0, 1) > -1

    def isJavaScript(str):
        return str.find('javascript', 0, len(str)) > -1

    def isURLExist(str, lists, position=0):
        lReturn = False
        for row in lists:
            if str == row[position]:
                lReturn = True

        return lReturn

    def GetDomain(self, url):
        parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        print(domain)
        return domain



ProcessPage()


