try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import json, os.path
import xbmc, xbmcaddon

ADDON_ID='plugin.video.javstream2'
addon = xbmcaddon.Addon(id=ADDON_ID)
profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
dbFile = os.path.join(profileDir, 'database.db')  

try:
    dbcon=database.connect(db.file)
    dbcur=dbcon.cursor()
    dbcur.execute("SELECT * FROM faves")
    faves=dbcur.fetchall()
    for a_row in faves:
        items.append(json.decode(a_row[1].encode("utf-8")))
except:
    pass