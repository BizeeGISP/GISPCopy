import Utility
import time
import db
import requests
from bs4 import BeautifulSoup

class ProcessContactUSPage:
    db = None
    dbConnect = None
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
    url_id       = 0
    element_lookup = []

    def __init__(self):
        startTime = time.time()
        self.InsertQuery = """INSERT INTO form_elements ( cont_url_id, form, tag_name, tag_id, label_id, name_id, placeholder_id, content_id, type, value, element_id, status ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                                                #[0, element.name, input_label, input_name, input_placeholder, input_id, input_type, input_value, content, 'New']
        #self.ProcessPage()
        self.ProcessPagesFromDB()

        print "Time consumed: ", time.time() - startTime

    def GetURLString(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup( r.content, 'lxml' )

    def dbConnection(self, lConnector = False):
        if lConnector:
            if self.dbConnect == None and not self.dbConnect:
                self.dbConnect = db.DBConnector()
            return self.dbConnect
        else:
            if self.db == None and not self.db:
                self.db = db.DB()
            return self.db

    def SaveData(self, query, values):
        con = self.dbConnection()
        con.executemany(query, values)

    def closeDB(self):
        if self.dbConnect <> None and self.dbConnect:
            self.dbConnect.close()

        if self.db <> None and self.db:
            self.db.close()

    def ProcessPagesFromDB(self):
        self.dbConnection()
        statement = """select id, url from contactus_url where status = 'New' limit 10"""
        rows = self.db.executeSelectAll(statement)
        nLen = len(rows)

        for row in rows:
            self.url_id  = row[0]
            url = row[1]
            url = url.strip()
            # url = "http://bizee.in/contacts.php"
            # url = "http://www.vidzpros.com/contact.html"
            self.ProcessPage(url)

        self.closeDB()

    def ProcessPage(self, url = ''):
        #url = "http://www.vidzpros.com/contact.html"
        self.GetURLString(url)

        processData = self.ProcessForms(self.GetForms())
        #print processData
        if len(processData) > 0:

            #Utility.printList(processData)
            self.SaveData(self.InsertQuery, processData)
            self.db.commit()

    def ProcessForms(self, forms):
        nform = 0
        processData = []
        for form in forms:
            nform +=1
            formElement = form.find_all()
            nLen = len(formElement)
            i = 0
            for tag in formElement:
                i +=1
                #print "Form: " + str(nform) + " | "+ str(i) + "/" + str(nLen) + " | " + tag.name, tag
                data = self.ProcessElement(tag)
                if len(data) > 0:
                    data[0] = self.url_id
                    data[1] = nform
                    #print "Data -->", data
                    processData.append(data)
            #print "ProcessData ---> " + str(len(processData)), processData
        return processData
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
        self.element_lookup = []

        #print "Element ----------> ", element
        attr = element.attrs

        tag_id          = self.GetDictKeyValue( attr, 'id')
        tag_label       = self.GetIds( 'label'      , self.GetLastLabelName(element))
        tag_name        = self.GetIds( 'name'       , self.GetDictKeyValue( attr, 'name'))
        tag_placeholder = self.GetIds( 'placeholder', self.GetDictKeyValue( attr, 'placeholder'))
        tag_content     = self.GetIds( 'content'    , self.GetElementContentName(element))

        tag_type        = self.GetDictKeyValue( attr, 'type')
        tag_value       = self.GetDictKeyValue( attr, 'value')
        element_id      = self.GetElementLookupId()
            #cont_url_id, form, tag_name, tag_id, label_id, name_id, placeholder_id, content_id, type, value, element_id, status
        return [ 0, 0, element.name, tag_id, tag_label, tag_name, tag_placeholder, tag_content, tag_type, tag_value, element_id, 'New' ]

    def GetElementLookupId(self):
        resultId = 0
        for id in self.element_lookup:
            if resultId == 0 and id <> 0:
                resultId = id

        return resultId

    def GetIds(self, key, value):
        resultId = None
        if value <> None:
            resultId = 0
            args = self.Get_argsId(key, value)
            if len(args) > 0:
                resultId = args[1]
                self.element_lookup.append(args[2])

        return resultId

    def GetDictKeyValue(self, dictAttr, key):
        keys = dictAttr.keys()
        value = None
        if key in keys:
            value = dictAttr[key].strip()
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
            self.LabelName = None

    def GetLastLabelName(self, element):
        LabelName = None
        #print element.name in self.InputElement, 'label' == self.LastElement
        if ( element.name in self.InputElement ) and ( 'label' == self.LastElement ):
            LabelName = self.LabelName
            #print LabelName
        return LabelName
    def GetElementContentName(self, element):
        try:
            content = element.contents
            labelName = ""
            for data in content:
                #if isinstance(data, type(data)):
                if str(type(data)) == "<class 'bs4.element.NavigableString'>":
                    labelName += str(data)
            if labelName == "":
                labelName = None
        except Exception, e:
            print e, "Error while building tag content"

        return labelName

    def GetForms(self):
        return self.soup.find_all('form')

    def GetTagInfo(self, tag):
        tagName = tag.name
        tagContent = tag.contents
        tagAttr = tag.attrs
        self.ProcessLastElement(tag)

    def Get_argsId(self, key, value):
        results_args = []
        if not (value == ''):
            #value = "Search"
            #print "Value ----> " + argStr + " | " + str(type(value)), value

            if   ( key == 'label'):
                procedure = "Get_Lookup_Label_Id"
            elif ( key == 'name'):
                procedure = "Get_Lookup_Name_Id"
            elif ( key == 'content'):
                procedure = "Get_Lookup_Content_Id"
            elif ( key == 'placeholder'):
                procedure = "Get_Lookup_Placeholder_Id"

            con = self.dbConnection(True)
            results_args = con.callproc(procedure, [value, 0, 0 ] )
            self.dbConnect.commit()

            #print "Result: ", results_args
        return results_args




#### DISCARDED CODE START FROM HERE, NOT IN USE. KEPT ONLY FOR REFERENCE





    def GetPageStrings(self):
        strings = self.soup.strings
        for string in strings:
            if not '\n' in string:
                print "string: ", repr(string)

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




ProcessContactUSPage()

