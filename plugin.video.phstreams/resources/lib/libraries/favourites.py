# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import json

from resources.lib.libraries import control


def getFavourites(content):
    try:
        dbcon = database.connect(control.favouritesFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM %s" % content)
        match = dbcur.fetchall()
        match = [eval(i[1].encode('utf-8')) for i in match]
        match = [(i['imdb'], i['title'], i['year'], i['poster']) for i in match]
    except:
        match = []
    try:
        dbcon = database.connect(control.databaseFile)
        dbcur = dbcon.cursor()
        content2 = 'Movie' if content == 'movies' else 'TV Show'
        dbcur.execute("SELECT * FROM favourites WHERE video_type ='%s'" % content2)
        match2 = dbcur.fetchall()
        match2 = [(i[0], i[2], i[3], i[6]) for i in match2]
    except:
        match2 = []


    items = match + match2 ; seen = set()
    items = [i for i in items if i[0] not in seen and not seen.add(i[0])]
    return items


def addFavourite(meta, content, query):
    try:
        item = dict()
        meta = json.loads(meta)
        imdb = item['imdb'] = meta['imdb']
        if 'title' in meta: title = item['title'] = meta['title']
        if 'tvshowtitle' in meta: title = item['title'] = meta['tvshowtitle']
        if 'year' in meta: item['year'] = meta['year']
        if 'poster' in meta: item['poster'] = meta['poster']
        if 'fanart' in meta: item['fanart'] = meta['fanart']
        if 'tmdb' in meta: item['tmdb'] = meta['tmdb']
        if 'tvdb' in meta: item['tvdb'] = meta['tvdb']
        if 'tvrage' in meta: item['tvrage'] = meta['tvrage']

        control.makeFile(control.dataPath)
        dbcon = database.connect(control.favouritesFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
        dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, imdb))
        dbcur.execute("INSERT INTO %s Values (?, ?)" % content, (imdb, repr(item)))
        dbcon.commit()

        if query == None: control.refresh()
        control.infoDialog(control.lang(30411).encode('utf-8'), heading=title)
    except:
        return


def deleteFavourite(meta, content):
    try:
        meta = json.loads(meta)
        imdb = meta['imdb']
        if 'title' in meta: title = meta['title']
        if 'tvshowtitle' in meta: title = meta['tvshowtitle']

        try:
            dbcon = database.connect(control.favouritesFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, imdb))
            dbcon.commit()
        except:
            pass
        try:
            dbcon = database.connect(control.databaseFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % imdb)
            dbcon.commit()
        except:
            pass

        control.refresh()
        control.infoDialog(control.lang(30412).encode('utf-8'), heading=title)
    except:
        return


def alterFavourites(content, favourites):
    try:
        dbcon = database.connect(control.databaseFile)
        dbcur = dbcon.cursor()
        dbcon2 = database.connect(control.favouritesFile)
        dbcur2 = dbcon2.cursor()
        dbcur2.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
    except:
        return

    for i in favourites:
        try:
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % i['imdb'])
        except:
            pass
        try:
            dbcur2.execute("INSERT INTO %s Values (?, ?)" % content, (i['imdb'], repr({'title': i['title'], 'year': i['year'], 'imdb': i['imdb'], 'tmdb': i['tmdb'], 'tvdb': i['tvdb'], 'tvrage': i['tvrage'], 'poster': i['poster'], 'fanart': i['fanart']})))
        except:
            pass

    try:
        dbcon.commit()
        dbcon2.commit()
    except:
        return


