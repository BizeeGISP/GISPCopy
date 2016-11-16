import configUtilities
import MySQLdb


db_driver=configUtilities.getProperties('DatabaseSection-MySQL', 'db.driver')
db_server=configUtilities.getProperties('DatabaseSection-MySQL', 'db.server')
db_name=configUtilities.getProperties('DatabaseSection-MySQL', 'db.name')
db_uid=configUtilities.getProperties('DatabaseSection-MySQL', 'db.uid')
db_pwd=configUtilities.getProperties('DatabaseSection-MySQL', 'db.pwd')

con = None

def dbConnect():
    #MySQL connection
    global con
    if con == None:
        try:
            con = MySQLdb.connect(host=db_server, user=db_uid, passwd=db_pwd, db=db_name)

        except MySQLdb.Error as err:
            print(err)
        else:
            con.close()
    return con

def cursor():

    return dbConnect().cursor()

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

def executeInsert(statement, values):
    # Processing Query
    try:
        cur = cursor()
        cur.execute(statement, values)
        commit()
    except MySQLdb.Error as err:
        print (err)
        rollback()


def executeMany(statement, values):
    # Processing Query
    try:
        cur = cursor()
        cur.executemany(statement, values)
        commit()
    except MySQLdb.Error as err:
        print(err)
        rollback()


def commit():
    con.commit()

def rollback():
    con.rollback()
