# -*- encoding: utf-8 -*-
import Utility
import time
import db
import logging
import datetime
from urlparse import urlparse
import sys
# reload(sys)
# sys.setdefaultencoding('UTF8')

class ProcessHomePage:
    db = None
    updateQuery = ""
    InsertQuery = ""

    def __init__(self):

        now = datetime.datetime.now()
        date = now.strftime(" %Y-%m-%d ")

        #print date, type(date)
        Format = '%(asctime)s - %(levelname)s - %(message)s'
        LOG_FILENAME = 'log\Engine2' + date + '.log'

        logging.basicConfig(filename=LOG_FILENAME, format=Format,level=logging.DEBUG)

        logging.info("ENGINE 2 PROCESS STARTS")
        startTime = time.time()


        self.ExecuteURLS()
        processSec = time.time() - startTime

        logging.info("Time consumed: " + str( processSec ))
        #print "Time consumed: ", time.time() - startTime

    def ExecuteURLS(self):
        self.InsertQuery = """INSERT INTO home_page_links (link_text, links, home_url_id) VALUES (%s,%s, %s)"""
        self.db = db.DB()
        statement = """select id, url from urls where status = 'new' and id > 0 limit 10"""
        rows = self.db.executeSelectAll(statement)
        nLen = len(rows)
        nCtr = 0
        for row in rows:
            id  = row[0]
            url = row[1]
            url = str("http://" + url).strip()

            try:
                PageUrls = self.GetPageUrls(url, id)
                nCtr += 1
                logging.info("Processing: " + str(nCtr) + "/" + str(nLen))
                #print "Processing: " + str(nCtr) + "/" + str(nLen), url
                self.SaveData(self.InsertQuery, PageUrls)
                self.UpdateUrls(id, url)
            except:
                try:
                    self.SaveSingleData(self.InsertQuery, PageUrls)
                    self.UpdateUrls(id, url)
                except:
                    self.db = db.DB()
        self.db.close()



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
            contactURLS = []
            allLinks = []
            if len(hrefList) > 0:
                for href in hrefList:
                    href_link = href[0]
                    href_text = href[1]
                    if not href_link in self.GetDomain(url):
                        allLinks.append((href_text, href_link, id))
                        contactUS_url = Utility.GetContactPageURL(href_text, href_link, url)
                        if (contactUS_url != None) and not (Utility.isURLExist(contactUS_url, contactURLS)):
                            contactURLS.append((contactUS_url, id, 'New'))
                    if len(contactURLS) > 0:
                        query = """INSERT INTO contactus_url(url, url_id, status) VALUES (%s,%s, %s)"""
                        self.SaveData(query, contactURLS)
        except Exception as e:
            print(e)
        print(allLinks)
        return allLinks

    def GetPageLinks(self, url):

        links = Utility.GetPageInfo(url, 'a')
        hrefs = []

        for link in links:
            href = str(link.get('href')).strip()

            if not Utility.isFirstCharacter(href, '#') and not Utility.isURLExist(href, hrefs) and not Utility.isJavaScript(href):
                hrefs.append((href, link.text.strip()))
        return hrefs


    def GetDomain(self, url):
        parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        print(domain)
        return domain



ProcessHomePage()


