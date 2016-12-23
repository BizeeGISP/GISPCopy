import openpyxl
import csv
import time
import logging
import datetime
import MDB
import configUtilities
import os
from datetime import date



class ImportUrls:
    data = ()
    writer = None
    connection = None
    million = 0
    CSV_PATH = configUtilities.getProperties('E1-CSV', 'PATH')

    def __init__(self):
        #tempDir = Utility.CheckAndCreateDirectory(Utility.getWorkingDirectory() + "\temp")
        startTicks = time.time()

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")

        logging.basicConfig(filename='log\E1 ' + date + '.log', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        logging.info("ENGINE 1 PROCESS STARTS")


        lExcel = False
        if lExcel:
            self.ImportFromExcel()
        else:
           #Securepath= "C:\ProgramData\MySQL\MySQL Server 5.7\Uploads"
            # self.writecsv(filename, self.ImportFromCSV())
            data = self.ProcessCSV()
            # if len(data) >0:
            #self.dbSave()

            # basefilename = os.path.join(os.getcwd(), filename)
            # self.dbSaveFromFile(basefilename)

        datagenSec = time.time() - startTicks

        logging.info("Data generation consumed Time: " + str(datagenSec))
        print( time.time() - startTicks, " Data generation Time consumed ")

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
                    # print top_level_domain
                    data = (url, self.GetTopLevelDomain(url), 'New')

                    # print data
                    values.append(data)
                row += 1
        return values

    def GetCSV_files(self,path_to_dir, suffix=".csv"):
        dir_files = os.listdir(path_to_dir)
        return [files for files in dir_files if files.endswith(suffix)]

    def ProcessCSV(self):
        files = self.GetCSV_files(self.CSV_PATH)
        for name in files:
            self.ImportFromCSV(self.CSV_PATH + name)

    def ImportFromCSV(self, filename):

        try:

            with open(filename, 'r') as f:
                reader = csv.reader(f)
                counter = 0
                values = []
                for row in reader:

                    url = row[0]
                    if (url != None):
                        counter += 1
                        data = {"url": url,"tld": self.GetTopLevelDomain(url),"eps":0}
                        values.append(data)
                        if ( counter == 100000):
                            self.dbSave(values)
                            counter = 0
                            values = []
                if counter > 0:
                    self.dbSave(values)
            f.close()
            os.rename(self.CSV_PATH + f, self.CSV_PATH + f + "_" + str(date.today()))
        except Exception as e:
            logging.error(e)
            #print(e)

        return values


    def dbSave(self, values=None):
        val=len(values)
        self.million += val
        logging.info("Saving: " + str(val))

        print("Saving : ", val)

        startTime = time.time()
        mdb = MDB.MdbClient("GISP")
        mdb.Collection("H_URLs")
        mdb.insert_many(values)
        mdb.close()
        timeconsSec = time.time() - startTime
        logging.info( " Time consumed " + str(timeconsSec) + "to save" + str(self.million)  + " Million")
        print( timeconsSec, " Time consumed to save " + str(self.million) + " Thousand" )

    def GetTopLevelDomain(self, url):
        return url[url.find(".") + 1:].rstrip("/")



ImportUrls()