import openpyxl
import dbUtilities
import csv
import time
import logging
import datetime
import Utility
import os
import db
import types


class ImportUrls:
    data = ()
    writer = None
    connection = None
    million = 0
    #connection = dbUtilities.getConnection()

    def __init__(self):
        #tempDir = Utility.CheckAndCreateDirectory(Utility.getWorkingDirectory() + "\temp")

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")

        logging.basicConfig(filename='log\Engine1 ' + date + '.log', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        logging.info("ENGINE 1 PROCESS STARTS")

        filename = "tmpdata.csv"
        startTicks = time.time()
        lExcel = False
        if lExcel:
            self.ImportFromExcel()
        else:
            SecurePath = "C:\ProgramData\MySQL\MySQL Server 5.7\Uploads"
            #self.writecsv(filename, self.ImportFromCSV())
            data = self.ImportFromCSV()
            #if len(data) >0:
                #self.dbSave(data)

            #basefilename = os.path.join(os.getcwd(), filename)
            #self.dbSaveFromFile(basefilename)

        datagenSec = time.time() - startTicks

        logging.info("Data generation consumed Time: " + str(datagenSec))
        #print time.time() - startTicks, " Data generation Time consumed "

    def ImportFromExcel(self):
        values = []
        wb = openpyxl.load_workbook('data\url\url.xlsx')
        sheets = wb.get_sheet_names()
        for sheet in sheets:
            sheetdata = wb.get_sheet_by_name(sheet)
            rowmax = sheetdata.max_row
            row = 1
            while row <= rowmax:

                url = sheetdata['A' + str(row)].value
                if (url <> None):
                    # print top_level_domain
                    data = (url, self.GetTopLevelDomain(url), 'New')

                    # print data
                    # dbUtilities.executeInsert(cur, query, data)
                    # dbUtilities.commit()
                    values.append(data)
                row += 1
        return values

    def ImportFromCSV(self):
        with open('in.csv', 'rb') as f:
            reader = csv.reader(f)
            counter = 0
            values = []
            for row in reader:
                url = row[0]
                if (url <> None):
                    if ( counter % 10000) == 0:
                        logging.info("counter-->" +str(counter))
                        #print counter

                    counter += 1
                    data = (url, self.GetTopLevelDomain(url), 'New')
                    values.append(data)
                    if ( counter == 10000):
                        self.dbSave(values)
                        #counter = 0
                        values = []
        return values

    def dbSaveFromFile(self, filename):
        Query = " LOAD DATA INFILE '"  + filename + "' INTO TABLE urls FIELDS TERMINATED BY ','  "
        self.db = db.DB()
        self.db.execute(Query)
        self.db.commit()
        self.db.close()


    def dbSave(self, values=None):
        val=len(values)
        logging.info("Processing: " + str(val))

        #print " Processing : ", len(values)

        self.million += 1
        startTime = time.time()
        self.db = db.DB()
        self.db.executemany("INSERT INTO urls(url, top_level_domain, status) VALUES (%s, %s, %s)", values)
        self.db.commit()
        self.db.close()
        timeconsSec = time.time() - startTime
        logging.info( " Time consumed " + str(timeconsSec) + "to save" + str(self.million)  + " Million")
        #print time.time() - startTime, " Time consumed to save " + str(self.million) + " Million"
        logging.info("delaying for 10 sec.")
        #print "delaying for 10 sec."
        time.sleep(10)
        logging.info("delaying for 10 sec.")
        #print "delayed for 10 sec."

    def writecsv(self, filename, datalist):
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(datalist)

    def GetTopLevelDomain(self, url):
        return url[url.find(".") + 1:].rstrip("/")



ImportUrls()