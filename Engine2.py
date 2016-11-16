import GetPageUrls
import time
import db


class ProcessHomePage:
    db = None
    updateQuery = ""
    InsertQuery = ""

    def __init__(self):
        startTime = time.time()

        self.ExecuteURLS()


        print "Time consumed: ", time.time() - startTime

    def ExecuteURLS(self):
        self.InsertQuery = """INSERT INTO home_page_links (link_text, links, home_url_id) VALUES (%s,%s, %s)"""
        self.db = db.DB()
        statement = """select id, url from urls where status = 'new' and id > 2100 limit 100"""
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
                print "Processing: " + str(nCtr) + "/" + str(nLen), url
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
        except Exception, e:
            print self.updateQuery
            print  e, "Updating Error: ", url + " | " + idStr
    def SaveSingleData(self, query, values):
        nCtr = 0
        nLen = len(values)
        for data in values:
            try:
                nCtr+=1
                if (nCtr % 50) == 0:
                    print "Data Processing: ", str(nCtr) + "/" + str(nLen)
                self.db.execute(query, data)
                self.db.commit()
            except Exception, e:
                print e, "Internal loop Exception"

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
                    allLinks.append((href_text, href_link, id))
                    contactUS_url = GetPageUrls.GetContactPageURL(href_text, href_link, url)
                    if (contactUS_url <> None) and not (GetPageUrls.isURLExist(contactUS_url, contactURLS)):
                        contactURLS.append((contactUS_url, id, 'New'))
                if len(contactURLS) > 0:
                    query = """INSERT INTO contactus_url(url, url_id, status) VALUES (%s,%s, %s)"""
                    self.SaveData(query, contactURLS)
        except Exception, e:
            print e

        return allLinks

    def GetPageLinks(self, url):

        links = GetPageUrls.GetPageInfo(url, 'a')
        hrefs = []

        for link in links:
            href = str(link.get('href')).strip()

            if not GetPageUrls.isFirstCharacter(href, '#') and not GetPageUrls.isURLExist(href, hrefs) and not GetPageUrls.isJavaScript(href):
                hrefs.append((href, link.text.strip()))
        return hrefs

ProcessHomePage()


