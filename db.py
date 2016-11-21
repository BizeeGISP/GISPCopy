#import mysql.connector
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
        except (AttributeError, MySQLdb.OperationalError), e:
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
                print '...Closed Database Connection: ' + str(self.con)
            else:
                print '...No Database Connection to Close.'
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

    def executeSelectAll(self, statement):
        cursor = self.con.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        return rows

