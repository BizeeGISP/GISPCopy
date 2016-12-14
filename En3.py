
import sys
import geograpy

import time
import db
import requests
import logging
import datetime
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('UTF8')


class ContactUSPage:

    soup   = ""




    def __init__(self):

        startTime = time.time()

        self.ContactUsPage()
        #self.ProcessPagesFromDB()

        print "Time consumed: ", time.time() - startTime


    def GetURLString(self, url):
        try:
            r = requests.get(url)
            self.soup = BeautifulSoup( r.content, 'lxml' )
            #print self.soup
        except Exception, e:
            print e
            logging.warning(e)


    def ContactUsPage(self):
        #url = "http://sbi.co.in/portal/web/contact-us/contact-us"
        #url = "http://whatsappstatus77.in/www.blogger.com/rearrange?blogID=2115002729003145160&widgetType=ContactForm&widgetId=ContactForm1&action=editWidget&sectionId=footer1"
        url = "http://spicinemas.in/contact-us"
        #url = "http://babycenter.in/e536987/contact-us"
        #url = "http://www.pg.com/en_IN/company/contact-us.shtml"
        #url = "https://www.payubiz.in/contact"
        #url = "http://www.vidzpros.com/contact.html"
        success = False

        self.GetURLString(url)
        strings = self.soup.strings
        data = []
        dat = []

        for string in strings:
            print "string", repr(string)
            #string = string.title()
            if not string == '\n':
                dat += string

                if dat <> "" and not "Us" in dat:
                    places = geograpy.get_place_context(text=dat)
                    country = places.country_cities
                    # country = places.countries
                    # if len( cities ) > 0:
                    #     print "Print Cities:" , cities
                    if len(country) > 0:
                        #print "Print Country:" , country
                        if not country in data:
                            data.append(country)
        print "Result: ", data




ContactUSPage()

