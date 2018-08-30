import subprocess, sys, os, time, sqlite3
from sqlite3 import Error

def CreateConnection():
    try:
        conn = sqlite3.connect('auth.db')
        return conn
    except Error as e:
        print(e)
    return None

def DoAuth():
    search_time = 10
    con = CreateConnection()
    lastinsert = 0
    if con != None:
        cur = con.cursor()
        cur.execute("insert into authenticate(toauth) Values (0)")
        lastid = cur.lastrowid
        con.commit()
        print("1:"+str(lastid))
        while search_time > 0:
            cur.execute("select toauth from authenticate where id = ?",(lastid,))
            for row in cur.fetchall():
                lastinsert = row[0]
            search_time = search_time - 1
            if lastinsert == 1:
                break
            else:
                time.sleep(1)
    if lastinsert == 0:
        print "Not Authenticated"
    else:
        print "Authenticated"

if __name__ == '__main__':
    DoAuth()