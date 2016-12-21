import MDB

import Utility


mdb = MDB.MdbClient("GISP")
mdb.Collection("urls")

#print(mdb.count({"Status": ""}))

returnList = mdb.find_data({ "Status": "New"}, "URL", False)
Utility.printList(returnList)
#print(mdb.find_one_by_ObjectId("585a5b2c816fb945843cc088"))


#
# data = [{ "URL":"google.fr", "Status":"New", "URL_TYPE":"D"}, { "URL":"google.cd", "Status":"New", "URL_TYPE":"D"}]
# returnValue = mdb.InsertMany(data)
#Utility.printList(returnValue)



mdb.close()
#mdb.CreateDB("GISP_TEST")