# -*- encoding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
#from urllib.parse import urlparse
from urllib.parse import urlparse
import E2_Form
#import E2_Regions
import pika
import configUtilities
import BizeeCons
import BizEE
import MDB

class ProcessPage:
    Q_server = configUtilities.getProperties('QUEUE-RMQ', 'Q.server')
    Q_port   = configUtilities.getProperties('QUEUE-RMQ', 'Q.port')
    Q_user   = configUtilities.getProperties('QUEUE-RMQ', 'Q.user')
    Q_pass   = configUtilities.getProperties('QUEUE-RMQ', 'Q.pass')
    rmq_connection = None
    rmq_channel    = None

    db = None
    updateQuery = ""
    InsertQuery = ""
    soup = None
    RMQ = None
    timeout = 60  #### 1 Min TimeOut.
    idealTime = 0
    iCtr = 0

    def __init__(self):

        startTicks = time.time()
        self.log = BizEE.log('E2')
        self.log.info('ENGINE 2 PROCESS STARTS')

        self.getRMQ_Channel()
        self.consume()
        self.close_RMQ()

        self.log.info("E2 Consumed: " + str(time.time() - startTicks) + " second to process...")

    def getRMQ_Channel(self):
        credentials = pika.PlainCredentials(self.Q_user, self.Q_pass)
        self.rmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.Q_server, int(self.Q_port), '/', credentials))
        self.rmq_channel = self.rmq_connection.channel()
        self.rmq_channel.queue_declare(queue=BizeeCons.CONS_E1_1_QUEUE, durable=True)

    def close_RMQ(self):
        self.rmq_connection.close()

    def callback(self, ch, method, properties, body):
        self.iCtr += 1
        message = body.decode("utf-8")
        value = message.split(",")
        if len(value) == 3:
            url_type = value[0]
            url = value[1]
            _id = value[2]
        else:
            url_type = BizeeCons.CONS_HOME_LINK_TABLE
            url = value[0]
            _id = value[1]

        if ( self.iCtr % 1000) ==0:
            print(value)
        #self.ProcessUrl(url_type, url, _id)

    def consume(self):
        try:
            self.rmq_channel.basic_consume(self.callback,
                                           queue=BizeeCons.CONS_E1_1_QUEUE,
                                           no_ack=True)
            self.rmq_channel.start_consuming()
        except Exception as e:
            self.log.error("Error while consuming message from the queue: " + BizeeCons.CONS_E1_1_QUEUE + " | " + str(e))

    def GetFQDN_URL(self, url):
        if not "http://" in url:
            url = str("http://" + url)
        return url.strip()

    def ProcessUrl(self, url_type, url, _id):
        url = self.GetFQDN_URL(url)
        self.soup = self.GetPageSoup(url)
        if self.soup != None:
            formData = E2_Form.WebForm(self.soup)
            #regionData = E2_Regions.ContactUsPage(self.soup)
            #ContactData =

            self.C_URLS = []
            self.F_URLS = []
            if   url_type == BizeeCons.CONS_HOME_LINK_TABLE:   ### D: Default URLS
                self.GetPageUrls(url, _id)    ### This function is creating two list C: Contact URL Link List and F: Foreign URL List.
                mdb = MDB.MdbClient("GISP")
                mdb.Collection(BizeeCons.CONS_CONTACT_LINK_TABLE  + "_URLs")
                mdb.insert_many({"url": self.C_URLS})
                mdb.Collection(BizeeCons.CONS_FOREIGN_LINK_TABLE + "_URLs")
                mdb.insert_many({"url": self.F_URLS})
                mdb.close()
            elif url_type == BizeeCons.CONS_FOREIGN_LINK_TABLE:  ### F: Foreign URLS
                self.GetPageUrls(url, _id)    ### This function is creating two list C: Contact URL Link List and F: Foreign URL List.
                self.F_URLS = []  #### Over here we are intentionally making the Foreign link empty, as we don't want to process recursive links from Foreign Link. We will handle this on 2nd Phase of Project

                mdb = MDB.MdbClient("GISP")
                mdb.Collection(BizeeCons.CONS_CONTACT_LINK_TABLE + "_URLs")
                mdb.insert_many({"url": self.C_URLS})



    def GetPageSoup(self, url):
        soup = None
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")
        except Exception as e:
            self.log.error(e, "Connection Exception : " + url)
            #### Append Logging Here
        return soup

    # def UpdateUrls(self, id, url):
    #     idStr = str(id)
    #     try:
    #         self.updateQuery = "update urls set status = 'Processed' where id = " + idStr
    #         self.db.execute(self.updateQuery)
    #         self.db.commit()
    #     except Exception as e:
    #
    #         logging.debug("Error while updating: " + self.updateQuery+ "|" +url)
    #         logging.warning(e)
    #          #print self.updateQuery
    #          #print  e, "Updating Error: ", url + " | " + idStr
    #
    # def SaveSingleData(self, query, values):
    #     nCtr = 0
    #     nLen = len(values)
    #     for data in values:
    #         try:
    #             nCtr+=1
    #             if (nCtr % 50) == 0:
    #                 logging.info(" Data Processing: " + str(nCtr)+ "/" + str(nLen))
    #                 #print "Data Processing: ", str(nCtr) + "/" + str(nLen)
    #             self.db.execute(query, data)
    #             self.db.commit()
    #         except Exception as e:
    #
    #             logging.debug("Internal loop Exception")
    #             logging.warning(e)
    #
    #             #print e, "Internal loop Exception"
    #
    # def SaveData(self, query, values):
    #     self.db.executemany(query, values)
    #     self.db.commit()

    def GetPageUrls(self, url, _id):
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
                        c_url_str = self.GetContactPageURL(href_text, href_link, url)
                        if (c_url_str != None) and not (self.isURLExist(c_url_str, self.C_URLS)):
                            self.C_URLS.append((c_url_str, _id, 'New'))
                    else:
                        self.F_URLS.append((href_text, href_link, _id))
        except Exception as e:
            self.log.error(e)

    def GetPageLinks(self, url):

        links = self.soup.find_all('a')

        hrefs = []

        for link in links:
            href = str(link.get('href')).strip()

            if not self.isFirstCharacter(href, '#') and not self.isURLExist(href, hrefs) and not self.isJavaScript(href):
                hrefs.append((href, link.text.strip()))
        return hrefs

    def getBaseURL(self, baseURL, href):
        url = None
        if "http" in href:
            url = href
        else:
            if href.find('/', 0, 1) > -1:
                url = baseURL + '/' + href.lstrip('/')

        return url

    def GetContactPageURL(self,link_text, link_href, baseURL):
        url = None
        if ("Contact" in link_text) or ("Contact" in link_href):
            url = self.getBaseURL(baseURL, link_href)

        return url

    def isFirstCharacter(self, str, character):

        return str.find(character, 0, 1) > -1

    def isJavaScript(self, str):

        return str.find('javascript', 0, len(str)) > -1

    def isURLExist(self, str, lists, position=0):
        lReturn = False
        for row in lists:
            if str == row[position]:
                lReturn = True

        return lReturn

    def GetDomain(self, url):
        parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain




ProcessPage()


