import mysql.connector
import configUtilities
import MySQLdb

class DB:

    db_driver=configUtilities.getProperties('DatabaseSection-MySQL', 'db.driver')
    db_server=configUtilities.getProperties('DatabaseSection-MySQL', 'db.server')
    db_name=configUtilities.getProperties('DatabaseSection-MySQL', 'db.name')
    db_uid=configUtilities.getProperties('DatabaseSection-MySQL', 'db.uid')
    db_pwd=configUtilities.getProperties('DatabaseSection-MySQL', 'db.pwd')
    con = None

    def __init__(self):
        self.connect()
    def connect(self):
        try:
            self.con = MySQLdb.connect( host=self.db_server,user=self.db_uid, passwd=self.db_pwd,  db=self.db_name, charset='utf8')
            #self.con.autocommit = False
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

    def executemany(self, statement, values):
        cursor = self.con.cursor()
        cursor.executemany(statement, values)
        return cursor

    def execute(self, statement, values = None):
        cursor = self.con.cursor()
        cursor.execute(statement, values)
        return cursor

    def commit(self):
        return self.con.commit()

    def close(self):
        try:
            if self.con:
                self.con.close()
                #print '...Closed Database Connection: ' + str(self.con)
            else:
                print( '...No Database Connection to Close.')
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

    def executeSelectAll(self, statement):
        cursor = self.con.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        return rows






class DBConnector:

    db_driver = configUtilities.getProperties('DatabaseSection-MySQL', 'db.driver')
    db_server = configUtilities.getProperties('DatabaseSection-MySQL', 'db.server')
    db_name = configUtilities.getProperties('DatabaseSection-MySQL', 'db.name')
    db_uid = configUtilities.getProperties('DatabaseSection-MySQL', 'db.uid')
    db_pwd = configUtilities.getProperties('DatabaseSection-MySQL', 'db.pwd')
    con = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:

            """con = mysql.connector.connect(user=db_uid,
                                          password=db_pwd,
                                          host=db_server,
                                          database=db_name)"""
            self.con = mysql.connector.connect(user=self.db_uid, password=self.db_pwd, host=self.db_server,  database=self.db_name, charset='utf8')
        except (AttributeError, mysql.connector.OperationalError) as e:
            raise e

    def commit(self):
        return self.con.commit()
    def callproc(self, procedure, args):
        try:
            cursor = self.con.cursor()
            #print "Start: " + procedure, args
            if args == None:
                cursor.callproc(procedure)
                result_args = cursor.stored_results()
            else:
                result_args = cursor.callproc(procedure, args)
                #print "End: " + procedure, args
        except Exception as e:
            print(e)
        # finally:
        #     cursor.close()
        return result_args


    def close(self):
        try:
            if self.con:
                self.con.close()
                #print '...Closed Database Connection: ' + str(self.con)
            else:
                print('...No Database Connection to Close.')
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e
