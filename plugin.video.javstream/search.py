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
try:
    dbcur.execute("CREATE TABLE IF NOT EXISTS versions (version_id);")
except:
    pass
try:
    dbcur.execute("CREATE TABLE IF NOT EXISTS realdebrid (client_id, client_secret, device_code)")
except:
    pass
try:
    dbcur.execute("CREATE TABLE IF NOT EXISTS bookmarks (name, code, poster, fanart)")
except:
    pass
    
dbcon.close()

def checkVersion(v):
    try:
        dbcon=database.connect(dbFile)
        dbcur=dbcon.cursor()
        
        
        dbcur.execute("SELECT version_id FROM versions")
        faves=dbcur.fetchall()
        if not faves:
            dbcur.execute("INSERT INTO versions (version_id) VALUES (?)", (v,))
            dbcon.commit()
            dbcon.close()
            return False
        else:
            for a_row in faves:
                if a_row[0]==v:
                    dbcon.close()
                    return True
                else:
                    dbcur.execute("DELETE FROM versions")
                    dbcon.commit()
                    dbcur.execute("INSERT INTO versions (version_id) VALUES (?)", (v,))
                    dbcon.commit()
                    dbcon.close()
                    return False
    except Exception, e:
        dbcon.close()
        return False
    dbcon.close()
    return False

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
    try:
        dbcon=database.connect(dbFile)
        dbcur=dbcon.cursor()
        dbcur.execute("INSERT INTO search (search_term) VALUES (?)", (keyword,))
        dbcon.commit()
        dbcon.close()
    except:
        pass
    
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
    
def removeBookmarks(params):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    try:
        if params["extras"]=="single-delete" :
            dbcur.execute("DELETE FROM bookmarks WHERE name=?", (params['name'],))
    except:
        dbcur.execute("DELETE FROM bookmarks")
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

def addBookmark(title, poster, fanart, url):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    dbcur.execute("SELECT name FROM bookmarks WHERE name=?", (title, ))
    data=dbcur.fetchall()
    if len(data)==0:
        dbcur.execute("INSERT INTO bookmarks (name, poster, fanart, code) VALUES (?, ?, ?, ?)", (title, poster, fanart, url))
        dbcon.commit()
    dbcon.close()
    
def getBookmarks():
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    dbcur.execute("SELECT name, poster, fanart, code FROM bookmarks ORDER BY name ASC")
    data=dbcur.fetchall()
    if len(data)==0:
        return False
    return data
    
def storeDebrid(client_id, client_secret, device_code):
    dbcon=database.connect(dbFile)
    dbcur=dbcon.cursor()
    dbcur.execute("DELETE FROM realdebrid")
    dbcur.execute("INSERT INTO realdebrid (client_id, client_secret, device_code) VALUES (?)", (client_id, client_secret, device_code,))
    dbcon.commit()
    dbcon.close()