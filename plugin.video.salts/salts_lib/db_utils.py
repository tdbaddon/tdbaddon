"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
"""
import os
import time
import csv
import json
import hashlib
import cPickle
import xbmcvfs
import xbmcgui
import log_utils
import kodi
from utils2 import i18n

def enum(**enums):
    return type('Enum', (), enums)

class DatabaseRecoveryError(Exception):
    pass

DB_TYPES = enum(MYSQL='mysql', SQLITE='sqlite')
CSV_MARKERS = enum(REL_URL='***REL_URL***', OTHER_LISTS='***OTHER_LISTS***', SAVED_SEARCHES='***SAVED_SEARCHES***', BOOKMARKS='***BOOKMARKS***')
MAX_TRIES = 5
MYSQL_DATA_SIZE = 512
MYSQL_URL_SIZE = 255
MYSQL_MAX_BLOB_SIZE = 16777215

class DB_Connection():
    def __init__(self):
        global OperationalError
        global DatabaseError
        self.dbname = kodi.get_setting('db_name')
        self.username = kodi.get_setting('db_user')
        self.password = kodi.get_setting('db_pass')
        self.address = kodi.get_setting('db_address')
        self.db = None
        self.progress = None

        if kodi.get_setting('use_remote_db') == 'true':
            if self.address is not None and self.username is not None and self.password is not None and self.dbname is not None:
                import mysql.connector as db_lib
                from mysql.connector import OperationalError as OperationalError
                from mysql.connector import DatabaseError as DatabaseError
                log_utils.log('Loading MySQL as DB engine', log_utils.LOGDEBUG)
                self.db_type = DB_TYPES.MYSQL
            else:
                log_utils.log('MySQL is enabled but not setup correctly', log_utils.LOGERROR)
                raise ValueError('MySQL enabled but not setup correctly')
        else:
            from sqlite3 import dbapi2 as db_lib
            from sqlite3 import OperationalError as OperationalError
            from sqlite3 import DatabaseError as DatabaseError
            log_utils.log('Loading sqlite3 as DB engine', log_utils.LOGDEBUG)
            self.db_type = DB_TYPES.SQLITE
            db_dir = kodi.translate_path("special://database")
            self.db_path = os.path.join(db_dir, 'saltscache.db')
        self.db_lib = db_lib
        self.__connect_to_db()

    def flush_cache(self):
        sql = 'DELETE FROM url_cache'
        self.__execute(sql)
        if self.db_type == DB_TYPES.SQLITE:
            self.__execute('VACUUM')

    def get_bookmark(self, trakt_id, season='', episode=''):
        if not trakt_id: return None
        sql = 'SELECT resumepoint FROM bookmark where slug=? and season=? and episode=?'
        bookmark = self.__execute(sql, (trakt_id, season, episode))
        if bookmark:
            return bookmark[0][0]
        else:
            return None

    def get_bookmarks(self):
        sql = 'SELECT * FROM bookmark'
        bookmarks = self.__execute(sql)
        return bookmarks

    def bookmark_exists(self, trakt_id, season='', episode=''):
        return self.get_bookmark(trakt_id, season, episode) != None

    def set_bookmark(self, trakt_id, offset, season='', episode=''):
        if not trakt_id: return
        sql = 'REPLACE INTO bookmark (slug, season, episode, resumepoint) VALUES(?, ?, ?,?)'
        self.__execute(sql, (trakt_id, season, episode, offset))

    def clear_bookmark(self, trakt_id, season='', episode=''):
        if not trakt_id: return
        sql = 'DELETE FROM bookmark WHERE slug=? and season=? and episode=?'
        self.__execute(sql, (trakt_id, season, episode))

    def cache_url(self, url, body, data=None, res_header=None):
        now = time.time()
        if data is None: data = ''
        if res_header is None: res_header = []
        res_header = json.dumps(res_header)
        # truncate data if running mysql and greater than col size
        if self.db_type == DB_TYPES.MYSQL and len(url) > MYSQL_URL_SIZE:
            url = url[:MYSQL_URL_SIZE]
        if self.db_type == DB_TYPES.MYSQL and len(data) > MYSQL_DATA_SIZE:
            data = data[:MYSQL_DATA_SIZE]
        sql = 'REPLACE INTO url_cache (url, data, response, res_header, timestamp) VALUES(?, ?, ?, ?, ?)'
        self.__execute(sql, (url, data, body, res_header, now))

    def delete_cached_url(self, url, data=''):
        if data is None: data = ''
        # truncate data if running mysql and greater than col size
        if self.db_type == DB_TYPES.MYSQL and len(data) > MYSQL_DATA_SIZE:
            data = data[:MYSQL_DATA_SIZE]
        sql = 'DELETE FROM url_cache WHERE url = ? and data= ?'
        self.__execute(sql, (url, data))

    def get_cached_url(self, url, data='', cache_limit=8):
        if data is None: data = ''
        # truncate data if running mysql and greater than col size
        if self.db_type == DB_TYPES.MYSQL and len(data) > MYSQL_DATA_SIZE:
            data = data[:MYSQL_DATA_SIZE]
        html = ''
        res_header = []
        created = 0
        now = time.time()
        limit = 60 * 60 * cache_limit
        sql = 'SELECT timestamp, response, res_header FROM url_cache WHERE url = ? and data=?'
        rows = self.__execute(sql, (url, data))

        if rows:
            created = float(rows[0][0])
            res_header = json.loads(rows[0][2])
            age = now - created
            if age < limit:
                html = rows[0][1]
        log_utils.log('DB Cache: Url: %s, Data: %s, Cache Hit: %s, created: %s, age: %s, limit: %s' % (url, data, bool(html), created, now - created, limit), log_utils.LOGDEBUG)
        return created, res_header, html

    def get_all_urls(self, include_response=False, order_matters=False):
        sql = 'SELECT url, data'
        if include_response: sql += ',response'
        sql += ' FROM url_cache'
        if order_matters: sql += ' ORDER BY url, data'
        rows = self.__execute(sql)
        return rows

    def cache_function(self, name, args=None, kwargs=None, result=None):
        now = time.time()
        if args is None: args = []
        if kwargs is None: kwargs = {}
        pickle_result = cPickle.dumps(result)
        # do not cache a partial result
        if self.db_type == DB_TYPES.MYSQL and len(pickle_result) > MYSQL_MAX_BLOB_SIZE:
            return

        arg_hash = hashlib.md5(str(args)).hexdigest() + hashlib.md5(str(kwargs)).hexdigest()
        sql = 'REPLACE INTO function_cache (name, args, result, timestamp) VALUES(?, ?, ?, ?)'
        self.__execute(sql, (name, arg_hash, pickle_result, now))
        log_utils.log('Function Cached: |%s|%s|%s| -> |%s|' % (name, args, kwargs, len(pickle_result)), log_utils.LOGDEBUG)

    def get_cached_function(self, name, args=None, kwargs=None, cache_limit=60 * 60):
        max_age = time.time() - cache_limit
        if args is None: args = []
        if kwargs is None: kwargs = {}
        arg_hash = hashlib.md5(str(args)).hexdigest() + hashlib.md5(str(kwargs)).hexdigest()
        sql = 'SELECT result FROM function_cache WHERE name = ? and args = ? and timestamp >= ?'
        rows = self.__execute(sql, (name, arg_hash, max_age))
        if rows:
            log_utils.log('Function Cache Hit: |%s|%s|%s| -> |%d|' % (name, args, kwargs, len(rows[0][0])), log_utils.LOGDEBUG)
            return True, cPickle.loads(rows[0][0])
        else:
            return False, None
        
    def add_other_list(self, section, username, slug, name=None):
        sql = 'REPLACE INTO other_lists (section, username, slug, name) VALUES (?, ?, ?, ?)'
        self.__execute(sql, (section, username, slug, name))

    def delete_other_list(self, section, username, slug):
        sql = 'DELETE FROM other_lists WHERE section=? AND username=? and slug=?'
        self.__execute(sql, (section, username, slug))

    def rename_other_list(self, section, username, slug, name):
        sql = 'UPDATE other_lists set name=? WHERE section=? AND username=? AND slug=?'
        self.__execute(sql, (name, section, username, slug))

    def get_other_lists(self, section):
        sql = 'SELECT username, slug, name FROM other_lists WHERE section=?'
        rows = self.__execute(sql, (section,))
        return rows

    def get_all_other_lists(self):
        sql = 'SELECT * FROM other_lists'
        rows = self.__execute(sql)
        return rows

    def set_related_url(self, video_type, title, year, source, rel_url, season='', episode=''):
        if year is None: year = ''
        sql = 'REPLACE INTO rel_url (video_type, title, year, season, episode, source, rel_url) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.__execute(sql, (video_type, title, year, season, episode, source, rel_url))

    def clear_related_url(self, video_type, title, year, source, season='', episode=''):
        if year is None: year = ''
        sql = 'DELETE FROM rel_url WHERE video_type=? and title=? and year=? and source=?'
        params = [video_type, title, year, source]
        if season and episode:
            sql += ' and season=? and episode=?'
            params += [season, episode]
        self.__execute(sql, params)

    def get_related_url(self, video_type, title, year, source, season='', episode=''):
        if year is None: year = ''
        sql = 'SELECT rel_url FROM rel_url WHERE video_type=? and title=? and year=? and season=? and episode=? and source=?'
        rows = self.__execute(sql, (video_type, title, year, season, episode, source))
        return rows

    def get_all_rel_urls(self):
        sql = 'SELECT * FROM rel_url'
        rows = self.__execute(sql)
        return rows

    def get_searches(self, section, order_matters=False):
        sql = 'SELECT id, query FROM saved_searches WHERE section=?'
        if order_matters: sql += 'ORDER BY added desc'
        rows = self.__execute(sql, (section,))
        return rows

    def get_all_searches(self):
        sql = 'SELECT * FROM saved_searches'
        rows = self.__execute(sql)
        return rows

    def save_search(self, section, query, added=None):
        if added is None: added = time.time()
        sql = 'INSERT INTO saved_searches (section, added, query) VALUES (?, ?, ?)'
        self.__execute(sql, (section, added, query))

    def delete_search(self, search_id):
        sql = 'DELETE FROM saved_searches WHERE id=?'
        self.__execute(sql, (search_id, ))

    def get_setting(self, setting):
        sql = 'SELECT value FROM db_info WHERE setting=?'
        rows = self.__execute(sql, (setting,))
        if rows:
            return rows[0][0]

    def set_setting(self, setting, value):
        sql = 'REPLACE INTO db_info (setting, value) VALUES (?, ?)'
        self.__execute(sql, (setting, value))

    def increment_db_setting(self, setting):
        cur_value = self.get_setting(setting)
        cur_value = int(cur_value) if cur_value else 0
        self.set_setting(setting, str(cur_value + 1))

    def export_from_db(self, full_path):
        temp_path = os.path.join(kodi.translate_path("special://profile"), 'temp_export_%s.csv' % (int(time.time())))
        with open(temp_path, 'w') as f:
            writer = csv.writer(f)
            f.write('***VERSION: %s***\n' % self.get_db_version())
            if self.__table_exists('rel_url'):
                f.write(CSV_MARKERS.REL_URL + '\n')
                for fav in self.get_all_rel_urls():
                    writer.writerow(self.__utf8_encode(fav))
            if self.__table_exists('other_lists'):
                f.write(CSV_MARKERS.OTHER_LISTS + '\n')
                for sub in self.get_all_other_lists():
                    writer.writerow(self.__utf8_encode(sub))
            if self.__table_exists('saved_searches'):
                f.write(CSV_MARKERS.SAVED_SEARCHES + '\n')
                for sub in self.get_all_searches():
                    writer.writerow(self.__utf8_encode(sub))
            if self.__table_exists('bookmark'):
                f.write(CSV_MARKERS.BOOKMARKS + '\n')
                for sub in self.get_bookmarks():
                    writer.writerow(self.__utf8_encode(sub))

        log_utils.log('Copying export file from: |%s| to |%s|' % (temp_path, full_path), log_utils.LOGDEBUG)
        if not xbmcvfs.copy(temp_path, full_path):
            raise Exception('Export: Copy from |%s| to |%s| failed' % (temp_path, full_path))

        if not xbmcvfs.delete(temp_path):
            raise Exception('Export: Delete of %s failed.' % (temp_path))

    def __utf8_encode(self, items):
        l = []
        for i in items:
            if isinstance(i, basestring):
                try:
                    l.append(i.encode('utf-8'))
                except UnicodeDecodeError:
                    l.append(i)
            else:
                l.append(i)
        return l
        
    def import_into_db(self, full_path):
        temp_path = os.path.join(kodi.translate_path("special://profile"), 'temp_import_%s.csv' % (int(time.time())))
        log_utils.log('Copying import file from: |%s| to |%s|' % (full_path, temp_path), log_utils.LOGDEBUG)
        if not xbmcvfs.copy(full_path, temp_path):
            raise Exception('Import: Copy from |%s| to |%s| failed' % (full_path, temp_path))

        try:
            num_lines = sum(1 for line in open(temp_path))
            if self.progress:
                progress = self.progress
                progress.update(0, line2='Importing Saved Data', line3='Importing 0 of %s' % (num_lines))
            else:
                progress = xbmcgui.DialogProgress()
                progress.create('SALTS', line2='Import from %s' % (full_path), line3='Importing 0 of %s' % (num_lines))
            with open(temp_path, 'r') as f:
                    reader = csv.reader(f)
                    mode = ''
                    _ = f.readline()  # read header
                    i = 0
                    for line in reader:
                        line = self.__unicode_encode(line)
                        progress.update(i * 100 / num_lines, line3='Importing %s of %s' % (i, num_lines))
                        if progress.iscanceled():
                            return
                        if line[0] in [CSV_MARKERS.REL_URL, CSV_MARKERS.OTHER_LISTS, CSV_MARKERS.SAVED_SEARCHES, CSV_MARKERS.BOOKMARKS]:
                            mode = line[0]
                            continue
                        elif mode == CSV_MARKERS.REL_URL:
                            self.set_related_url(line[0], line[1], line[2], line[5], line[6], line[3], line[4])
                        elif mode == CSV_MARKERS.OTHER_LISTS:
                            name = None if len(line) != 4 else line[3]
                            self.add_other_list(line[0], line[1], line[2], name)
                        elif mode == CSV_MARKERS.SAVED_SEARCHES:
                            self.save_search(line[1], line[3], line[2])  # column order is different than method order
                        elif mode == CSV_MARKERS.BOOKMARKS:
                            self.set_bookmark(line[0], line[3], line[1], line[2])
                        else:
                            raise Exception('CSV line found while in no mode')
                        i += 1
        finally:
            if not xbmcvfs.delete(temp_path):
                raise Exception('Import: Delete of %s failed.' % (temp_path))
            progress.close()
            self.progress = None
            if self.db_type == DB_TYPES.SQLITE:
                self.__execute('VACUUM')

    def __unicode_encode(self, items):
        l = []
        for i in items:
            if isinstance(i, basestring):
                try:
                    l.append(unicode(i, 'utf-8'))
                except UnicodeDecodeError:
                    l.append(i)
            else:
                l.append(i)
        return l
        
    def execute_sql(self, sql):
        self.__execute(sql)

    # intended to be a common method for creating a db from scratch
    def init_database(self, db_version):
        try:
            cur_version = kodi.get_version()
            if db_version is not None and cur_version != db_version:
                log_utils.log('DB Upgrade from %s to %s detected.' % (db_version, cur_version))
                self.progress = xbmcgui.DialogProgress()
                self.progress.create('SALTS', line1='Migrating from %s to %s' % (db_version, cur_version), line2='Saving current data.')
                self.progress.update(0)
                self.__prep_for_reinit()
    
            log_utils.log('Building SALTS Database', log_utils.LOGDEBUG)
            if self.db_type == DB_TYPES.MYSQL:
                self.__execute('CREATE TABLE IF NOT EXISTS url_cache (url VARBINARY(%s) NOT NULL, data VARBINARY(%s) NOT NULL, response MEDIUMBLOB, res_header TEXT, timestamp TEXT, PRIMARY KEY(url, data))' % (MYSQL_URL_SIZE, MYSQL_DATA_SIZE))
                self.__execute('CREATE TABLE IF NOT EXISTS function_cache (name VARCHAR(255) NOT NULL, args VARCHAR(64), result MEDIUMBLOB, timestamp TEXT, PRIMARY KEY(name, args))')
                self.__execute('CREATE TABLE IF NOT EXISTS db_info (setting VARCHAR(255) NOT NULL, value TEXT, PRIMARY KEY(setting))')
                self.__execute('CREATE TABLE IF NOT EXISTS rel_url \
                (video_type VARCHAR(15) NOT NULL, title VARCHAR(255) NOT NULL, year VARCHAR(4) NOT NULL, season VARCHAR(5) NOT NULL, episode VARCHAR(5) NOT NULL, source VARCHAR(49) NOT NULL, rel_url VARCHAR(255), \
                PRIMARY KEY(video_type, title, year, season, episode, source))')
                self.__execute('CREATE TABLE IF NOT EXISTS other_lists (section VARCHAR(10) NOT NULL, username VARCHAR(68) NOT NULL, slug VARCHAR(255) NOT NULL, name VARCHAR(255), \
                PRIMARY KEY(section, username, slug))')
                self.__execute('CREATE TABLE IF NOT EXISTS saved_searches (id INTEGER NOT NULL AUTO_INCREMENT, section VARCHAR(10) NOT NULL, added DOUBLE NOT NULL,query VARCHAR(255) NOT NULL, \
                PRIMARY KEY(id))')
                self.__execute('CREATE TABLE IF NOT EXISTS bookmark (slug VARCHAR(255) NOT NULL, season VARCHAR(5) NOT NULL, episode VARCHAR(5) NOT NULL, resumepoint DOUBLE NOT NULL, \
                PRIMARY KEY(slug, season, episode))')
            else:
                self.__create_sqlite_db()
                self.__execute('PRAGMA journal_mode=WAL')
                self.__execute('CREATE TABLE IF NOT EXISTS url_cache (url VARCHAR(255) NOT NULL, data VARCHAR(255), response, res_header, timestamp, PRIMARY KEY(url, data))')
                self.__execute('CREATE TABLE IF NOT EXISTS function_cache (name VARCHAR(255) NOT NULL, args VARCHAR(64), result, timestamp, PRIMARY KEY(name, args))')
                self.__execute('CREATE TABLE IF NOT EXISTS db_info (setting VARCHAR(255), value TEXT, PRIMARY KEY(setting))')
                self.__execute('CREATE TABLE IF NOT EXISTS rel_url \
                (video_type TEXT NOT NULL, title TEXT NOT NULL, year TEXT NOT NULL, season TEXT NOT NULL, episode TEXT NOT NULL, source TEXT NOT NULL, rel_url TEXT, \
                PRIMARY KEY(video_type, title, year, season, episode, source))')
                self.__execute('CREATE TABLE IF NOT EXISTS other_lists (section TEXT NOT NULL, username TEXT NOT NULL, slug TEXT NOT NULL, name TEXT, PRIMARY KEY(section, username, slug))')
                self.__execute('CREATE TABLE IF NOT EXISTS saved_searches (id INTEGER PRIMARY KEY, section TEXT NOT NULL, added DOUBLE NOT NULL,query TEXT NOT NULL)')
                self.__execute('CREATE TABLE IF NOT EXISTS bookmark (slug TEXT NOT NULL, season TEXT NOT NULL, episode TEXT NOT NULL, resumepoint DOUBLE NOT NULL, \
                PRIMARY KEY(slug, season, episode))')
    
            # reload the previously saved backup export
            if db_version is not None and cur_version != db_version:
                log_utils.log('Restoring DB from backup at %s' % (self.mig_path), log_utils.LOGDEBUG)
                self.import_into_db(self.mig_path)
                log_utils.log('DB restored from %s' % (self.mig_path))
    
            sql = 'REPLACE INTO db_info (setting, value) VALUES(?,?)'
            self.__execute(sql, ('version', kodi.get_version()))
        finally:
            if self.progress is not None:
                self.progress.close()

    def __table_exists(self, table):
        if self.db_type == DB_TYPES.MYSQL:
            sql = 'SHOW TABLES LIKE ?'
        else:
            sql = 'select name from sqlite_master where type="table" and name = ?'
        rows = self.__execute(sql, (table,))

        if not rows:
            return False
        else:
            return True

    def reset_db(self):
        if self.db_type == DB_TYPES.SQLITE:
            try: self.db.close()
            except: pass
            os.remove(self.db_path)
            self.db = None
            self.__connect_to_db()
            self.init_database(None)
            return True
        else:
            return False

    def get_db_version(self):
        version = None
        try:
            sql = 'SELECT value FROM db_info WHERE setting="version"'
            rows = self.__execute(sql)
        except:
            return None

        if rows:
            version = rows[0][0]

        return version

    def attempt_db_recovery(self):
        header = i18n('recovery_header')
        if xbmcgui.Dialog().yesno(header, i18n('rec_mig_1'), i18n('rec_mig_2')):
            try: self.init_database('Unknown')
            except Exception as e:
                log_utils.log('DB Migration Failed: %s' % (e), log_utils.LOGWARNING)
                if self.db_type == DB_TYPES.SQLITE:
                    if xbmcgui.Dialog().yesno(header, i18n('rec_reset_1'), i18n('rec_reset_2'), i18n('rec_reset_3')):
                        try: self.reset_db()
                        except Exception as e:
                            log_utils.log('Reset Failed: %s' % (e), log_utils.LOGWARNING)
                            try: msg = i18n('reset_failed') % (e)
                            except: msg = 'Reset Failed: %s' % (e)
                        else:
                            msg = i18n('db_reset_success')
                        kodi.notify(msg=msg, duration=5000)
        
    def __execute(self, sql, params=None):
        if params is None:
            params = []

        rows = None
        sql = self.__format(sql)
        tries = 1
        while True:
            try:
                cur = self.db.cursor()
                # log_utils.log('Running: %s with %s' % (sql, params), log_utils.LOGDEBUG)
                cur.execute(sql, params)
                if sql[:6].upper() == 'SELECT' or sql[:4].upper() == 'SHOW':
                    rows = cur.fetchall()
                cur.close()
                self.db.commit()
                return rows
            except OperationalError as e:
                if tries < MAX_TRIES:
                    tries += 1
                    log_utils.log('Retrying (%s/%s) SQL: %s Error: %s' % (tries, MAX_TRIES, sql, e), log_utils.LOGWARNING)
                    self.db = None
                    self.__connect_to_db()
                elif any(s for s in ['no such table', 'no such column'] if s in str(e)):
                    self.db.rollback()
                    raise DatabaseRecoveryError(e)
                else:
                    raise
            except DatabaseError as e:
                self.db.rollback()
                raise DatabaseRecoveryError(e)

    # purpose is to save the current db with an export, drop the db, recreate it, then connect to it
    def __prep_for_reinit(self):
        self.mig_path = os.path.join(kodi.translate_path("special://database"), 'mig_export_%s.csv' % (int(time.time())))
        log_utils.log('Backing up DB to %s' % (self.mig_path), log_utils.LOGDEBUG)
        self.export_from_db(self.mig_path)
        log_utils.log('Backup export of DB created at %s' % (self.mig_path))
        self.__drop_all()
        log_utils.log('DB Objects Dropped', log_utils.LOGDEBUG)

    def __create_sqlite_db(self):
        if not xbmcvfs.exists(os.path.dirname(self.db_path)):
            try: xbmcvfs.mkdirs(os.path.dirname(self.db_path))
            except: os.mkdir(os.path.dirname(self.db_path))

    def __drop_all(self):
        if self.db_type == DB_TYPES.MYSQL:
            sql = 'show tables'
        else:
            sql = 'select name from sqlite_master where type="table"'
        rows = self.__execute(sql)
        db_objects = [row[0] for row in rows]

        for db_object in db_objects:
            sql = 'DROP TABLE IF EXISTS %s' % (db_object)
            self.__execute(sql)

    def __connect_to_db(self):
        if not self.db:
            if self.db_type == DB_TYPES.MYSQL:
                self.db = self.db_lib.connect(database=self.dbname, user=self.username, password=self.password, host=self.address, buffered=True)
            else:
                self.db = self.db_lib.connect(self.db_path)
                self.db.text_factory = str

    # apply formatting changes to make sql work with a particular db driver
    def __format(self, sql):
        if self.db_type == DB_TYPES.MYSQL:
            sql = sql.replace('?', '%s')

        if self.db_type == DB_TYPES.SQLITE:
            if sql[:7] == 'REPLACE':
                sql = 'INSERT OR ' + sql

        return sql
