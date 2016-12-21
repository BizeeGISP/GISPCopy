# -*- encoding: utf-8 -*-

import re
import time

import requests
import logging
from bs4 import BeautifulSoup
import phonenumbers
import pycountry
from langdetect import detect
from phonenumbers.phonenumberutil import region_code_for_number



class ContactDetails:


    soup   = ""
    regex  = [  (r'^(\d{3})[\- ](\d{8})$')
              , (r'^\D*(\d+)\D+(\d+)\D*(\d+)\D*(\d{4})$')
              , (r'^[\+](\d{2})[\- ](\d{3})[\- ](\d{2})[\- ](\d{2})[\- ](\d{3})$')
              , (r'^(\d{10})[\ ]$')
              , (r'^[\+ ](\d{2})[\- ](\d{2})[\- ](\d{8})[\- ][\/](\d{8})$')
              , (r'^[\( ](\d{2})[\- ](\d{2})[\) ][\ ](\d{4})[\- ](\d{4})$')
              , (r'^[\+ ](\d{2})[\- ](\d{2})[\- ](\d{9})$')
              , (r'^[\( ][\+ ](\d{2})[\-) ](\d{2})[\- ](\d{4})[\- ](\d{4})$')
              , (r'^(\d{11})$')
              , (r'^(\d{2})[\- ](\d{10})$')
              , (r'^[\+ ](\d{2})[\- ](\d{5})[\- ](\d{5})$')
              , (r'^[\+ ](\d{2})[\- ](\d{2})[\- ](\d{4})[\- ](\d{4})$')
              , (r'^(\d{3})[\- ](\d{4})[\- ](\d{4})$')
              , (r'^(\d{1})[\- ](\d{5})[\- ](\d{5})$')
              , (r'^(\d{1})[\- ](\d{4})[\- ](\d{3})[\- ](\d{3})$')
              , (r'^(\d{4})[\- ](\d{4})[\- ](\d{3})$')
              , (r'^[\+ ](\d{2})[\- ](\d{3})[\- ](\d{7})$')
              , (r'^(\d{3})[\- ](\d{4})[\- ](\d{4})$')
              , (r'^[\+](\d{2})[\- ](\d{3})[\- ](\d{3})[\- ](\d{4})$')
              ]

    def __init__(self, soup):


        startTime = time.time()

        self.GetPhoneNumbers()
        processSec = time.time() - startTime



    def GetPhoneNumbers(self):

        strings = soup.strings
        for string in strings:
            string = string.replace("\n","")


            self.GetPhoneNumber(string)



    def GetPhoneNumber(self, string):
        phone = []

        for reg in self.regex:
            r = re.compile(reg)
            results = r.findall(string)

            for x in results:
                s = ''.join(x)
                s = self.RemoveSpecialCharacter(s)
                print(s)
                if len(s) >11 and len(s) <= 13:
                    if not s.rfind('1800',0,4)== 0 and not s.rfind('0', 0, 1) == 0:
                        if not s in phone:
                            s = '+' + s
                            phone.append([s,self.GetCountryfromPhone(s)])
        return phone

    def RemoveSpecialCharacter(self, string):
        s = string
        b = ".,-()+ "
        for char in b:
            s = s.replace(char, "")
        return s


    def GetCountryfromPhone(self, phone):
        pn = phonenumbers.parse(phone)
        country =  pycountry.countries.get(alpha_2=region_code_for_number(pn))
        print(country.name)
        return country.name

    def GetEmailId(self):
        email = []
        strings = self.soup.strings
        for string in strings:
            r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
            results = r.findall(string)
            if len(results) > 0:
                if not results in email:
                    email.append(results)
        print( "Email ID:", email)


    def LangDetect(self):
        data = ""
        strings = self.soup.strings
        for string in strings:
            if not (string == '\n' and string == ""):
                data += string
        return detect(data)

ContactDetails()

