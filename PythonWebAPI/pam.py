# PAM interface in python

# sudo apt-get install libpam-python
# sudo apt-get install bluetooth libbluetooth-dev gobject
# sudo pip install pybluez

# Import required modules
import subprocess, sys, os, time, sqlite3
from sqlite3 import Error

def CreateConnection():
    try:
        conn = sqlite3.connect("/home/melwyn/Documents/PythonWebAPI/auth.db")
        return conn
    except Error as e:
        print(e)
    
    return None

def doAuth(pamh):
    """Do Authentication here"""
    search_time = 10
    con = CreateConnection()
    lastinsert = 0
    if con != None:
        cur = con.cursor()
        cur.execute("insert into authenticate(toauth) Values (0)")
        lastid = cur.lastrowid
        con.commit()
        #print("1:"+str(lastid))
        while search_time > 0:
            cur.execute("select toauth from authenticate where id = ?",(lastid,))
            for row in cur.fetchall():
                lastinsert = row[0]
            search_time = search_time - 1
            if lastinsert == 1:
                break
            else:
                time.sleep(1)
    con.close()
    if lastinsert == 1:
        return pamh.PAM_SUCCESS
    return pamh.PAM_SYSTEM_ERR

def pam_sm_authenticate(pamh, flags, args):
    """Called by PAM when the user wants to authenticate, in sudo for example"""
    return doAuth(pamh)

def pam_sm_open_session(pamh, flags, args):
    """Called when starting a session, such as su"""
    return doAuth(pamh)

def pam_sm_close_session(pamh, flags, argv):
    """We don't need to clean anyting up at the end of a session, so return true"""
    return pamh.PAM_SUCCESS

def pam_sm_setcred(pamh, flags, argv):
    """We don't need set any credentials, so return true"""
    return pamh.PAM_SUCCESS
