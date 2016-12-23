import MDB
import BizeeCons
import configUtilities
import os
import time
import datetime
import Utility


# CSV_PATH = configUtilities.getProperties('E1-CSV', 'PATH')
# dir_files = os.listdir(CSV_PATH)
# print( [files for files in dir_files if files.endswith(".csv")])
# try:
#     os.rename(CSV_PATH + 'in.csv', CSV_PATH + 'in.csv' + "_"+ str(date.today()))
# except Exception as e:
#     print(e)

mdb = MDB.MdbClient("GISP")
mdb.Collection("H_URLs")

Obj_Id = mdb.ObjectId('585bc74445711325008460b7')

date = datetime.datetime.now()

print(date, type(date))

#print(mdb.count({"Status": ""}))
mdb.update_one({"_id" : Obj_Id}, {'$set': {"eps": BizeeCons.CONS_EPS_MESSAGE_PUSHED_TO_QUEUE, "eps_dt": date}} )

# returnList = mdb.find_data({ "Status": "New"}, "URL", False)
# Utility.printList(returnList)
#print(mdb.find_one_by_ObjectId("585a5b2c816fb945843cc088"))
#
# data = { "URL":"google.fr", "Status":"New", "URL_TYPE":{"D":{"D":{"D":"DDDD"}}, "F":{"F":"FFFF"}}}
#
# mdb.insert_one(data)


# cursor = mdb.find()
# for data in cursor:
#     print(data['URL_TYPE'], type(data['URL_TYPE']))

# data = [{ "URL":"google.fr", "Status":"New", "URL_TYPE":"D"}, { "URL":"google.cd", "Status":"New", "URL_TYPE":"D"}]
# returnValue = mdb.InsertMany(data)
#Utility.printList(returnValue)



mdb.close()
#mdb.CreateDB("GISP_TEST")