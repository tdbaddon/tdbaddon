# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import time,hashlib

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from resources.lib.modules import control


def fetch(items, lang):
    try:
        t2 = int(time.time())
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
    except:
        return items

    for i in range(0, len(items)):
        try:
            dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (items[i]['imdb'], lang, items[i]['tvdb'], lang))
            match = dbcur.fetchone()

            t1 = int(match[4])
            update = (abs(t2 - t1) / 3600) >= 720
            if update == True: raise Exception()

            item = eval(match[3].encode('utf-8'))
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')

            items[i].update(item)
            items[i].update({'metacache': True})
        except:
            pass

    return items


def insert(meta):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tvdb TEXT, ""lang TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tvdb, lang)"");")
        t = int(time.time())
        for m in meta:
            try:
                i = repr(m['item'])
                try: dbcur.execute("DELETE * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (m['imdb'], m['lang'], m['tvdb'], m['lang']))
                except: pass
                dbcur.execute("INSERT INTO meta Values (?, ?, ?, ?, ?)", (m['imdb'], m['tvdb'], m['lang'], i, t))
            except:
                pass

        dbcon.commit()
    except:
        return

