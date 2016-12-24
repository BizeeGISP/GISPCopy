# -*- encoding: utf-8 -*-
import openpyxl
import csv
import time
import BizEE
import MDB
import configUtilities
import os
import BizeeCons
from datetime import date


class ImportUrls:
    data = ()
    writer = None
    connection = None
    million = 0

    URL_FILE_PATH = configUtilities.getProperties('E1-FILES', 'URL_FILE_PATH')
    URL_FILE_TYPE = configUtilities.getProperties('E1-FILES', 'URL_FILE_TYPE')
    URL_DATA_POS  = int(configUtilities.getProperties('E1-FILES', 'URL_DATA_POS' ))


    def __init__(self):
        startTicks = time.time()

        self.log = BizEE.log('E1')
        self.log.info('ENGINE 1 PROCESS STARTS')
        try:
            if self.URL_FILE_TYPE == "EXCEL":
                self.ImportFromExcel()
            else:
                self.ImportFromCSV()
                self.log.info("E1 Consumed: " + str(time.time() - startTicks) + " second to process...")
        except Exception as e:
            self.log.error("Data generation consumed Time: " + str(time.time() - startTicks))

    def ImportFromExcel(self):
        values = []
        wb = openpyxl.load_workbook(r'data\url\url.xlsx')
        sheets = wb.get_sheet_names()
        for sheet in sheets:
            sheetdata = wb.get_sheet_by_name(sheet)
            rowmax = sheetdata.max_row
            row = 1
            while row <= rowmax:

                url = sheetdata['A' + str(row)].value
                if (url != None):
                    data = (url, self.GetTopLevelDomain(url), 'New')
                    values.append(data)
                row += 1
        return values

    def GetCSV_files(self,path_to_dir, suffix=".csv"):
        dir_files = os.listdir(path_to_dir)
        return [files for files in dir_files if files.endswith(suffix)]

    def ImportFromCSV(self):
        files = self.GetCSV_files(self.URL_FILE_PATH)
        for name in files:
            self.ProcessCSV(self.URL_FILE_PATH + name)

    def ProcessCSV(self, filename):
        self.million = 0
        try:
            self.log.info("Processing File: " + filename)
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                counter = 0
                values = []
                for row in reader:

                    url = row[self.URL_DATA_POS]
                    if (url != None):
                        counter += 1
                        data = {"url": url,"tld": self.GetTopLevelDomain(url),"eps":0}
                        values.append(data)
                        if ( counter == BizeeCons.LIST_PROC_MAX):
                            self.dbSave(values, filename)
                            counter = 0
                            values = []
                if counter > 0:
                    self.dbSave(values, filename)
            f.close()
            self.log.info("Renaming File : " + filename)
            os.rename(filename, filename + "_" + str(date.today()))
        except Exception as e:
            self.log.error(e)


    def dbSave(self, values, filename):
        val=len(values)
        self.million += val
        self.log.info("Saving: " + str(val) + " record from file: " + filename)

        startTime = time.time()
        mdb = MDB.MdbClient("GISP")
        mdb.Collection("H_URLs")
        mdb.insert_many(values)
        mdb.close()
        timeconsSec = time.time() - startTime
        self.log.info( "Time consumed to import "  + str(self.million)  + " record from file : " + filename + " in "+ str(round(timeconsSec,2)) + " seconds...")

    def GetTopLevelDomain(self, url):
        return url[url.find(".") + 1:].rstrip("/")



ImportUrls()