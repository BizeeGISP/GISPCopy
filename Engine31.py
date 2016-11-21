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

    InputType    = [ "text", "email", "submit", "radio", "checkbox", "button", "number", "date" ]
    InputName    = [ "name" ]
    InputEmail   = [ "email" ]
    InputPhone   = [ "phone" ]
    InputDesc    = [ "comment" ]
    Elements     = [ "name", "email", "telephone", "phone", "comment" ]
    excludeType  = [ "password" ]
    InputElement = [ "input", "textarea" ]
    LastElement  = ""
    LabelName    = ""
    DataValues   = []

    def __init__(self):
        startTime = time.time()

        self.ProcessPage()
        #self.ProcessPagesFromDB()

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
        nform = 0
        for form in forms:
            nform +=1
            formElement = form.find_all()
            nLen = len(formElement)
            i = 0
            processData = []
            for tag in formElement:
                i +=1
                #print "Form: " + str(nform) + " | "+ str(i) + "/" + str(nLen) + " | " + tag.name, tag
                data = self.ProcessElement(tag)
                if len(data) > 0:
                    data[0] = nform
                    #print "Data -->", data
                    processData.append(data)
            print "ProcessData ---> " + str(len(processData)), processData

    def ProcessElement(self,element):
        DataValues = []
        if ( element.name in self.InputElement ) or ( element.name == 'button' ):
            DataValues = self.GetInputProperties(element)
        # elif ( element.name == 'button' ):
        #     DataValues = self.GetButtonProperties(element)

        #Should be executed always after processing element
        self.RecordLastElement(element)
        return DataValues
    def GetInputProperties(self, element):
        attr                = element.attrs
        input_label         = self.GetLastLabelName(element)
        input_placeholder   = self.GetDictKeyValue( attr, 'placeholder' )
        input_type          = self.GetDictKeyValue( attr, 'type' )
        input_id            = self.GetDictKeyValue( attr, 'id'   )
        input_name          = self.GetDictKeyValue( attr, 'name' )
        input_value         = self.GetDictKeyValue( attr, 'value')
        content             = self.GetElementContentName(element)

            #form, label, name, placeholder, element_id, type, value, status"""
        return [ 0, input_label, input_name, input_placeholder, input_id, input_type, input_value, content, 'New']

    def GetDictKeyValue(self, dictAttr, key):
        keys = dictAttr.keys()
        value = ""
        if key in keys:
            value = dictAttr[key]
        return value
    def RecordLastElement(self, element):
        if ('span' == element.name ) or ( 'div' == element.name ):
            #print "Escaping: " + self.LastElement, self.LabelName
            return
        elif 'label' == element.name:
            self.LastElement = element.name
            self.LabelName = self.GetElementContentName(element)
        else:
            #print element.name, self.LastElement + " | " + self.LabelName
            self.LastElement = element.name
            self.LabelName = ""

    def GetLastLabelName(self, element):
        LabelName = ""
        #print element.name in self.InputElement, 'label' == self.LastElement
        if ( element.name in self.InputElement ) and ( 'label' == self.LastElement ):
            LabelName = self.LabelName
            #print LabelName
        return LabelName
    def GetElementContentName(self, element):
        content = element.contents
        labelName = ""
        for data in content:
            #if isinstance(data, type(data)):
            if str(type(data)) == "<class 'bs4.element.NavigableString'>":
                labelName += str(data)
        return labelName

    def GetForms(self):
        return self.soup.find_all('form')

    def GetTagInfo(self, tag):
        tagName = tag.name
        tagContent = tag.contents
        tagAttr = tag.attrs
        self.ProcessLastElement(tag)




        #if   ( tagName == 'label' ):
             #self.GetLabelName(element)

        # elif ( tagName == 'input' ):
        #     self.Validate_input(element)
        #
        # elif ( tagName == 'a' ):
        #     self.Validate_a(element)
        #     lPrint = True
        #
        # elif (tagName == 'div'):
        #     lPrint = False
        #
        # if lPrint:
        #     print tagName, attr




    def SplitElementsfromString(self, elementList):
        SplittedElement = []

        for elementString in elementList:

            element = str(elementString).split('\n')
            for e in element:
                    SplittedElement.append(e)

        return SplittedElement


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
        self.InsertQuery = """INSERT INTO form_elements (form, name, label, placeholder, element_id, type, value, content, status ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
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


