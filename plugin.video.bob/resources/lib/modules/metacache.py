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

import time

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import control


def fetch(items, lang):
    try:
        t2 = int(time.time())
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
    except:
        return items

    try:
        dbcur.execute("SELECT * FROM version")
        match = dbcur.fetchone()
    except:
        try:
            dbcur.execute("DROP TABLE IF EXISTS meta")
            dbcur.execute("DROP TABLE IF EXISTS episode_meta")
            dbcur.execute("VACUUM")
            dbcon.commit()
        except:
            pass
        dbcur.execute("CREATE TABLE version (""version TEXT)")
        dbcur.execute("INSERT INTO version Values ('1.2.9')")
        dbcon.commit()

    for i in range(0, len(items)):
        try:
            dbcur.execute(
                "SELECT * FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tmdb = '%s' and lang = '%s' and not tmdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (
                    items[i]['imdb'], lang, items[i]['tmdb'], lang, items[i]['tvdb'], lang))
            match = dbcur.fetchone()

            t1 = int(match[5])
            update = (abs(t2 - t1) / 3600) >= 720
            if update == True: raise Exception()

            item = eval(match[4].encode('utf-8'))
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')

            if items[i]['fanart'] == '0':
                try:
                    items[i].update({'fanart': item['fanart']})
                except:
                    pass

            item = dict((k, v) for k, v in item.iteritems() if not k == 'fanart')
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
        dbcur.execute(
            "CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang)"");")
        t = int(time.time())
        for m in meta:
            try:
                i = repr(m['item'])
                try:
                    dbcur.execute(
                        "DELETE FROM meta WHERE (imdb = '%s' and lang = '%s' and not imdb = '0') or (tmdb = '%s' and lang = '%s' and not tmdb = '0') or (tvdb = '%s' and lang = '%s' and not tvdb = '0')" % (
                            m['imdb'], m['lang'], m['tmdb'], m['lang'], m['tvdb'], m['lang']))
                except:
                    pass
                dbcur.execute("INSERT INTO meta Values (?, ?, ?, ?, ?, ?)",
                              (m['imdb'], m['tmdb'], m['tvdb'], m['lang'], i, t))
            except:
                pass

        dbcon.commit()
    except:
        return


def fetch_episodes(items, lang):
    try:
        t2 = int(time.time())
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
    except:
        return items

    try:
        dbcur.execute("SELECT * FROM version")
        match = dbcur.fetchone()
    except:
        try:
            dbcur.execute("DROP TABLE IF EXISTS meta")
            dbcur.execute("DROP TABLE IF EXISTS episode_meta")
            dbcur.execute("VACUUM")
            dbcon.commit()
        except:
            pass
        dbcur.execute("CREATE TABLE version (""version TEXT)")
        dbcur.execute("INSERT INTO version Values ('1.2.9')")
        dbcon.commit()

    for i in range(0, len(items)):
        try:
            dbcur.execute(
                "SELECT * FROM episode_meta WHERE "
                "(imdb = '%s' and lang = '%s' and season = '%s' and episode = '%s' and not imdb = '0') or "
                "(tmdb = '%s' and lang = '%s' and season = '%s' and episode = '%s' and not tmdb = '0') or "
                "(tvdb = '%s' and lang = '%s' and season = '%s' and episode = '%s' and not tvdb = '0')" % (
                    items[i]['imdb'], lang, items[i]['season'], items[i]['episode'],
                    items[i]['tmdb'], lang, items[i]['season'], items[i]['episode'],
                    items[i]['tvdb'], lang, items[i]['season'], items[i]['episode']))
            match = dbcur.fetchone()

            t1 = int(match[7])
            update = (abs(t2 - t1) / 3600) >= 720
            if update == True: raise Exception()

            item = eval(match[6].encode('utf-8'))
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')

            if items[i]['fanart'] == '0':
                try:
                    items[i].update({'fanart': item['fanart']})
                except:
                    pass

            item = dict((k, v) for k, v in item.iteritems() if not k == 'fanart')
            items[i].update(item)

            items[i].update({'episode_metacache': True})
        except:
            pass

    return items


def insert_episode(meta):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute(
            "CREATE TABLE IF NOT EXISTS episode_meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""season TEXT"
            ", ""episode TEXT, ""lang TEXT, ""item TEXT, ""time TEXT"
            ", ""UNIQUE(imdb, tmdb, tvdb, season, episode, lang)"");")
        t = int(time.time())
        for m in meta:
            try:
                i = repr(m['item'])
                try:
                    dbcur.execute(
                        "DELETE FROM episode_meta WHERE "
                        "(imdb = '%s' and season = '%s' and episode = '%s' and lang = '%s' and not imdb = '0') or "
                        "(tmdb = '%s' and season = '%s' and episode = '%s' and lang = '%s' and not tmdb = '0') or "
                        "(tvdb = '%s' and season = '%s' and episode = '%s' and lang = '%s' and not tvdb = '0')" % (
                            m['imdb'], m['season'], m['episode'], m['lang'],
                            m['tmdb'], m['season'], m['episode'], m['lang'],
                            m['tvdb'], m['season'], m['episode'], m['lang']))
                except:
                    pass
                dbcur.execute("INSERT INTO episode_meta Values (?, ?, ?, ?, ?, ?, ?, ?)",
                              (m['imdb'], m['tmdb'], m['tvdb'], m['season'], m['episode'], m['lang'], i, t))
            except:
                pass

        dbcon.commit()
    except:
        return


def episodes_set_watched(imdb, tmdb, tvdb, season, episode, watched=True):
    if watched:
        playcount = '1'
    else:
        playcount = '0'

    item = [{'rating': '0', 'tmdb': tmdb, 'plot': '', 'season': season, 'tvshowtitle': '', 'year': '',
             'episode_metacache': False, 'vip': "", 'code': '', 'imdb': imdb, 'fanart': '',
             'genre': '', 'banner': '0', 'metacache': True, 'content': 'episodes', 'episode': episode,
             'name': '', 'title': '', 'tvdb': tvdb, 'duration': '',
             'premiered': '', 'summary': '', 'originaltitle': '',
             'url': '',
             'poster': '', 'action': '', 'studio': '', 'folder': False}]
    premeta = fetch_episodes(item, 'en')[0]
    meta = {'rating': premeta["rating"], 'code': premeta["code"], 'tvshowtitle': premeta["tvshowtitle"],
            'duration': premeta["duration"], 'imdb': premeta["imdb"], 'year': premeta["year"],
            'genre': premeta["genre"], 'plot': premeta["plot"], 'tvdb': premeta["tvdb"], 'studio': premeta["studio"],
            'playcount': playcount}
    insert_episode([{'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': 'en', 'season': season,
                     'episode': episode, 'item': meta}])


def movies_set_watched(imdb, tmdb, tvdb, watched=True):
    if watched:
        playcount = '1'
    else:
        playcount = '0'

    item = [{'tmdb': tmdb, 'season': '0', 'tvshowtitle': '0', 'year': '', 'episode_metacache': False, 'vip': '',
             'imdb': imdb, 'fanart': '', 'banner': '0', 'metacache': False, 'content': 'movies', 'episode': '0',
             'name': "", 'title': "", 'tvdb': '', 'premiered': '', 'summary': '', 'originaltitle': "", 'url': "",
             'poster': '', 'action': '', 'folder': False}]
    premeta = fetch(item, 'en')[0]
    meta = {'rating': premeta['rating'], 'code': premeta['code'], 'director': premeta['director'],
            'genre': premeta['genre'], 'imdb': premeta['imdb'], 'year': premeta['year'],
            'duration': premeta['duration'], 'plot': premeta['plot'], 'votes': premeta['votes'],
            'title': premeta['title'], 'mpaa': premeta['mpaa'], 'writer': premeta['writer'],
            'premiered': premeta['premiered'], 'cast': premeta['cast'], 'playcount': playcount}
    insert([{'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': 'en', 'item': meta}])
