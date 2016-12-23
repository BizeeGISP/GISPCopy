# -*- encoding: utf-8 -*-
import configUtilities
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo

class MdbClient:

    db_driver=configUtilities.getProperties('Database-MDB', 'db.driver')
    db_server=configUtilities.getProperties('Database-MDB', 'db.server')
    db_name=configUtilities.getProperties('Database-MDB', 'db.name')
    db_uid=configUtilities.getProperties('Database-MDB', 'db.uid')
    db_pwd=configUtilities.getProperties('Database-MDB', 'db.pwd')

    conn = None
    db = None
    collection = None


    def __init__(self, dbName = None):
        self.conn = self.MongoClientConnect()
        #print(self.conn, "Vivek Connection")
        if dbName != None:
            self.ConnectDb(dbName)

    def MongoClientConnect(self):

        return MongoClient(host=self.db_server, port=27017, document_class=dict, tz_aware=False, connect=True)

    #### Customized Methods ------ STARTS HERE -------

    def ConnectDb(self, dbName):
        self.db = self.conn[dbName]
        return self.db

    def Collection(self, collectionName):
        self.collection = self.db[collectionName]
        return self.collection


    def find_one_by_ObjectId(self, strDoc):
        return self.collection.find_one({ "_id": ObjectId(strDoc)})

    def find_data(self, condition = None, sort_Key_Or_List = None, Asending = True):

        if sort_Key_Or_List != None:
            if Asending:
                Direct = pymongo.ASCENDING
            else:
                Direct = pymongo.DESCENDING

            data = (r for r in self.collection.find(condition).sort(sort_Key_Or_List, Direct))

        else:
            data = [r for r in self.collection.find(condition)]

        return data

    def ObjectId(self, ObjId):
        return ObjectId(ObjId)

    #### Library Based Methods ------ STARTS HERE -------  Refer the Pymongo Library for the properties, methods and functionality of the function.

    def insert_one(self, doc, bypass_document_validation=False ):
        return self.collection.insert_one(doc, bypass_document_validation ).inserted_id

    def insert_many(self, doc):
        return self.collection.insert_many(doc).inserted_ids

    def find_one(self, doc):
        return self.collection.find_one(doc)

    def find(self, condition = None):
        return self.collection.find(condition)

    def count(self, condition):
        return self.collection.count(condition)

    def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None):
        return self.collection.update_one(filter, update, upsert, bypass_document_validation, collation)

    def update_many(self,filter, update, upsert=False, bypass_document_validation=False, collation=None):
        return self.collection.update_many(filter, update, upsert, bypass_document_validation, collation)

    def delete_one(self, filter, collation=None):
        return self.collection.delete_one(filter, collation)

    def delete_many(self, filter, collation=None):
        return self.collection.delete_many(filter, collation)

    def close(self):
        return self.conn.close()