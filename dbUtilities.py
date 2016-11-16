import mysql.connector
import configUtilities
import MySQLdb


db_driver=configUtilities.getProperties('DatabaseSection-MySQL', 'db.driver')
db_server=configUtilities.getProperties('DatabaseSection-MySQL', 'db.server')
db_name=configUtilities.getProperties('DatabaseSection-MySQL', 'db.name')
db_uid=configUtilities.getProperties('DatabaseSection-MySQL', 'db.uid')
db_pwd=configUtilities.getProperties('DatabaseSection-MySQL', 'db.pwd')


#SQL Server connection
"""con = pypyodbc.connect(
        'DRIVER='+db_driver+';'+
        'SERVER='+db_server+';'+
        'DATABASE='+db_name+';'+
        'UID='+db_uid+';'+
        'PWD='+db_pwd)
"""

#MySQL connection
"""con = mysql.connector.connect(user=db_uid,
                              password=db_pwd,
                              host=db_server,
                              database=db_name)"""

con = MySQLdb.connect( host=db_server,user=db_uid, passwd=db_pwd,  db=db_name)

def getConnection():
    print db_server
    global con
    if (con == None) or (con.open == 0):
       con = MySQLdb.connect( host=db_server,user=db_uid, passwd=db_pwd,  db=db_name)
    return con
def getCursor():

    return getConnection().cursor()
def connectDB():
    cur = con.cursor()
    return cur

def executeSelectAll(cur, statement):
    cur.execute(statement)
    rows = cur.fetchall()
    return rows

def executeUpdate(cur, statement):
    cur.execute(statement)
    rows = cur.fetchall()
    return rows

def executeSelect(cur, statement):
    cur.execute(statement)
    rows = cur.fetchall()
    return rows

def executeInsert(cur, statement, values):

    # Processing Query
    cur.execute(statement, values)

def executemany(cur, statement, values):
    cur.executemany(statement, values)

def commit():
    con.commit()
