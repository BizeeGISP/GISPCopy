import GetPageUrls
import time
import db
import requests
from bs4 import BeautifulSoup



class ProcessContactUSPage:
    db = None
    soup = None
    updateQuery = ""
    InsertQuery = ""

    InputType   = [ "text", "email", "submit", "radio", "checkbox", "button", "number", "date" ]
    InputName   = [ "name" ]
    InputEmail  = [ "email" ]
    InputPhone  = [ "phone" ]
    InputDesc   = [ "comment" ]
    Elements    = [ "name", "email", "telephone", "phone", "comment" ]
    excludeType = [ "password" ]

    def __init__(self):
        startTime = time.time()

        url = "http://www.vidzpros.com/contact.html"

        self.ProcessPage()


        print "Time consumed: ", time.time() - startTime


    def GetURLString(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup( r.content, 'lxml' )


    def ProcessPagesFromDB(self):
        self.db = db.DB()
        statement = """select id, url from contactus_url where status = 'New' limit 1"""
        rows = self.db.executeSelectAll(statement)
        self.db.close()
        nLen = len(rows)


        for row in rows:
            id  = row[0]
            url = row[1]
            url = url.strip()
            url = "http://bizee.in/contacts.php"
            url = "http://www.vidzpros.com/contact.html"
            self.ProcessPage(url)

    def ProcessPage(self, url = ''):
        url = "http://www.vidzpros.com/contact.html"
        self.GetURLString(url)
        #self.GetPageStrings()

        self.ProcessForms(self.GetForms())


    def GetPageStrings(self):
        strings = self.soup.strings
        for string in strings:
            if not '\n' in string:
                print "string: ", repr(string)

    def ProcessForms(self, forms):
        nCtr = 0
        for form in forms:
            nCtr +=1
            formElement = form.find_all()
            nLen = len(formElement)
            i = 0
            for tag in formElement:
                i +=1
                print "Form: " + str(nCtr) + " | "+ str(i) + "/" + str(nLen), tag

    def GetForms(self):
        return self.soup.find_all('form')

    def FilterInputData(self, form):
        filterData = []
        nLen = len(form)
        nCtr = 0
        #########Loop on All the forms found in Contact Us Page########
        for formdata in form:
            nCtr += 1

            data = formdata.contents

            #self.AnalyzeformList(data)

            # if nCtr ==2:
            #
            #     print "Counter: " + str(nCtr) + "/" + str(nLen), data

            #########Loop on All type of element.Tag & NavigationString##########
            print "data ----> ", data
            for tag in data:
                classtype = str(type(tag))
                # if nCtr==2:
                #     print "Tag: " + classtype, tag
                if ("<class 'bs4.element.Tag'>" in classtype):
                    if nCtr == 2:
                        print "tag  ----> ", tag
                    tagdata = tag.find_all(["label", "input", "a", "textarea", "button"])

                    lastElement = ''
                    ###########Loop on all Tag Elements##############
                    #tagdata = self.SplitElementsfromString(tagdata)
                    if nCtr == 2:
                        print "TagData: " + str(len(tagdata))+ str(type(tagdata)), tagdata
                    for d in tagdata:
                        #if nCtr ==2:


                            #print "Element: " + "|", d
                        #self.ValidateElement(d)
                        #print "TagData: ", d

                        #if 'label' in d:
                        if d.name == 'label':
                            # print "Element:", d
                            # print "d.contents: ", d.contents
                            lastElementValue = self.GetLabelName(d.contents)
                            #print "Label: ", lastElementValue

                        # if d.name == 'label':
                        #     lastElementValue = self.GetLabelName(d.contents)
                        #     print "Label: ", lastElementValue
                        # elif d.name == 'input':
                        #     print "Input: ", d.contents



        return filterData
    def SplitElementsfromString(self, elementList):
        SplittedElement = []

        for elementString in elementList:

            element = str(elementString).split('\n')
            for e in element:
                    SplittedElement.append(e)

        return SplittedElement

    def ValidateElement(self, element):
        element_name = element.name
        attr = element.attrs
        lPrint = True

        # if   ( element_name == 'label' ):
        #     self.GetLabelName(element)
        #
        # elif ( element_name == 'input' ):
        #     self.Validate_input(element)
        #
        # elif ( element_name == 'a' ):
        #     self.Validate_a(element)
        #     lPrint = True
        #
        # elif (element_name == 'div'):
        #     lPrint = False
        #
        # if lPrint:
        #     print element_name, attr


    def GetLabelName(self, content):
        label_name = ''

        for items in content:
            items = str(items)
            label_name = self.CheckString_InsideList(items.lower(), self.Elements)
            #print "Label Name: " + items, label_name
            if label_name:
                #print "Return: ", label_name
                return label_name
                #break
        return label_name

    def CheckString_InsideList(self, DataString, DataList):

        for data in DataList:
           #print "Data: "+ data, "DataString: " + DataString
           #print "Items: " + str(type(DataString)),str(DataString)

            if data in DataString:
                #print "Found: ", data
                return data

        return ''

    def Validate_input(self, element):
        attr = element.attrs
        input_placeholder = attr['placeholder']
        input_type  = attr['type']
        input_id    = attr['id']
        input_name  = attr['name']
        input_value = attr['value']
        return [ input_id, input_placeholder, input_name, input_type, input_value ]

    def Validate_a(self, element):
        attr    = element.attrs
        a_class = attr['class']
        a_href  = attr['href']
        a_id    = attr['id']

    def ExecuteURLS(self):
        self.InsertQuery = """INSERT INTO home_page_links (link_text, links, home_url_id) VALUES (%s,%s, %s)"""
        self.db = db.DB()
        statement = """select id, url from urls where status = 'new' limit 1000"""
        rows = self.db.executeSelectAll( statement )
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

ProcessContactUSPage()


