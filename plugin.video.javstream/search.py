try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import json, os.path
import xbmc, xbmcaddon

ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)
profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

dbFile = os.path.join(profileDir, 'search.db')  
dbcon=database.connect(dbFile)
dbcur=dbcon.cursor()
try:
    dbcur.execute("CREATE TABLE IF NOT EXISTS search (search_term);")
except:
    pass
dbcon.close()

def getSearch():
    items=[]
    try:
        dbcon=database.connect(dbFile)
        dbcur=dbcon.cursor()
        dbcur.execute("SELECT search_term FROM search")
        faves=dbcur.fetchall()
        for a_row in faves:
            if len(a_row)>0:
                items.append(a_row)
    except:
        pass
    dbcon.close()
    return items
    
def addSearch(keyword):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    dbcur.execute("INSERT INTO search (search_term) VALUES (?)", (keyword,))
    dbcon.commit()
    dbcon.close()
    
def removeSearch(params):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    try:
        if params["extras"]=="single-delete" :
            dbcur.execute("DELETE FROM search WHERE search_term=?", (params['name'],))
    except:
        dbcur.execute("DELETE FROM search")
    dbcon.commit()
    dbcon.close()

def inDatabase(term):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    dbcur.execute("SELECT search_term FROM search WHERE search_term=?", (term,))
    data=dbcur.fetchall()
    if len(data)==0:
        return False
    return True