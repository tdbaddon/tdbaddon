"""
    Ported from 1Channel Kodi Addon for use in Icefilms

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
import urllib
import time
import csv
import xbmc, xbmcvfs

def enum(**enums):
    return type('Enum', (), enums)

DB_TYPES= enum(MYSQL='mysql', SQLITE='sqlite')
CSV_MARKERS = enum(FAVOURITES='***FAVOURITES***', SUBSCRIPTIONS='***SUBSCRIPTIONS***', BOOKMARKS='***BOOKMARKS***', EXT_SUBS='***EXTERNAL SUBSCRIPTIONS***')


class DB_Connection():
    def __init__(self, addon):
        global database
        self.addon = addon
        self.dbname = addon.get_setting('db_name')
        self.username = addon.get_setting('db_user')
        self.password = addon.get_setting('db_pass')
        self.address = addon.get_setting('db_address')
        self.db=None
        
        if addon.get_setting('use_remote_db') == 'true':
            if self.address is not None and self.username is not None \
            and self.password is not None and self.dbname is not None:
                import mysql.connector as database
                addon.log('Loading MySQL as DB engine version: %s' % database.version.VERSION_TEXT)
                self.db_type = DB_TYPES.MYSQL
            else:
                addon.log_error('MySQL is enabled but not setup correctly')
                raise ValueError('MySQL enabled but not setup correctly')
        else:
            try:
                from sqlite3 import dbapi2 as database
                addon.log('Loading sqlite3 as DB engine version: %s' % database.sqlite_version, 2)
            except:
                from pysqlite2 import dbapi2 as database
                addon.log('Loading pysqlite2 as DB engine')
            self.db_type = DB_TYPES.SQLITE
            self.profile_path = addon.get_profile()
            self.cache_path = xbmc.translatePath('special://temp/')
            self.db_path = os.path.join(self.profile_path, 'ice_cache.db')
        self.__connect_to_db()


    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.db.close()
        except: pass


    def flush_cache(self):
        sql = 'DELETE FROM url_cache'
        self.__execute(sql)
        sql = 'DELETE FROM cache_data'
        self.__execute(sql)
        

    # return the bookmark for the requested url or None if not found
    def get_bookmark(self,url):
        if not url: return None
        sql='SELECT resumepoint FROM new_bkmark where url=?'
        bookmark = self.__execute(sql, (url,))
        if bookmark:
            return bookmark[0][0]
        else:
            return None

    # get all bookmarks
    def get_bookmarks(self):
        sql='SELECT * FROM new_bkmark'
        bookmarks = self.__execute(sql)
        return bookmarks
    
    # return true if bookmark exists
    def bookmark_exists(self, url):
        return self.get_bookmark(url) != None
    
    def set_bookmark(self, url,offset):
        if not url: return
        sql = 'REPLACE INTO new_bkmark (url, resumepoint) VALUES(?,?)'
        self.__execute(sql, (url,offset))
        
    def clear_bookmark(self, url):
        if not url: return
        sql = 'DELETE FROM new_bkmark WHERE url=?'
        self.__execute(sql, (url,))
        

    ###### QUEUE LIST
    def get_queue(self, type):
        sql='SELECT a.*, b.resumepoint FROM queue_list a left join new_bkmark b on a.url=b.url where type=? order by timestamp desc'
        queue = self.__execute(sql, (type,))
        return queue
       
    def save_queue(self, url, type, name, year, season, episode, imdbid):
        now = time.time()
        if not url: return
        sql = 'INSERT INTO queue_list (url, type, name, year, season, episode, imdbid, timestamp) VALUES(?,?,?,?,?,?,?,?)'
        try:
            title = urllib.unquote_plus(unicode(name, 'latin1'))
            self.__execute(sql, (url, type, title, year, season, episode, imdbid, now))
        except database.IntegrityError:
            raise     
        
    def clear_queue(self, url):
        if not url: return
        sql = 'DELETE FROM queue_list WHERE url=?'
        self.__execute(sql, (url,))

    def flush_queue(self, type=None):
        if type:
            sql = 'DELETE FROM queue_list WHERE type=?'
            self.__execute(sql, (type,))
        else:
            sql = 'DELETE FROM queue_list'
            self.__execute(sql)

            
    ###### RECENT WATCHED
    def get_watched(self, type):
        sql='SELECT a.*, b.resumepoint FROM recent_watched a left join new_bkmark b on a.url=b.url where type=? order by timestamp desc'
        watched = self.__execute(sql, (type,))
        return watched
    
    # return true if watched exists
    def watched_exists(self, url):
        return self.get_watched(url) != None
    
    def set_watched(self, url, type, name, year, season, episode, imdbid):
        now = time.time()
        if not url: return
        sql = 'REPLACE INTO recent_watched (url, type, name, year, season, episode, imdbid, timestamp) VALUES(?,?,?,?,?,?,?,?)'
        self.__execute(sql, (url, type, name, year, season, episode, imdbid, now))
        
    def clear_watched(self, url):
        if not url: return
        sql = 'DELETE FROM recent_watched WHERE url=?'
        self.__execute(sql, (url,))

    def flush_watched(self, type=None):
        if type:
            sql = 'DELETE FROM recent_watched WHERE type=?'
            self.__execute(sql, (type,))
        else:
            sql = 'DELETE FROM recent_watched'
            self.__execute(sql)


    ###### FAVOURITES
    def get_favourites(self, fav_type=None):
        sql = 'SELECT * FROM favourites'
        if fav_type:
            sql = sql + self.__format(' WHERE type = ? ORDER BY NAME')
            favs=self.__execute(sql, (fav_type,))
        else:
            favs=self.__execute(sql)
        return favs
    
    def get_favourites_count(self, fav_type=None):
        sql = 'SELECT count(*) FROM favourites'
        if fav_type:
            sql = sql + self.__format(' WHERE type = ?')
            rows=self.__execute(sql, (fav_type,))
        else:
            rows=self.__execute(sql)

        return rows[0][0]
    
    def save_favourite(self, fav_type, name, url, imdbid):
        sql = 'INSERT INTO favourites (type, name, url, imdbid) VALUES (?, ?, ?, ?)'
        try:
            title = urllib.unquote_plus(unicode(name, 'latin1'))
            self.__execute(sql, (fav_type, title, url, imdbid))
        except database.IntegrityError:
            raise

    def clear_favourites(self, fav_type=None):
        sql = self.__format('DELETE FROM favourites')
        if type:
            sql = sql + self.__format(' WHERE type = ?')
        self.__execute(sql, (fav_type,))
            
    # delete a list of favourites, urls must be a list
    def delete_favourites(self, urls):
        url_string=', '.join('?' for _ in urls)
        sql = self.__format('DELETE FROM favourites WHERE url in ('+url_string+')')
        self.__execute(sql, urls)
        
    def delete_favourite(self, url):
        self.delete_favourites([url])

    def get_subscriptions(self, day=None, order_matters=False):
        sql = 'SELECT * FROM subscriptions'
        if day is not None: sql += ' WHERE days like ?'

        # order subscription by their days values, forcing ALLs to the top, forcing disabled (i.e. nulls and blank) to the end, with the rest sorted lexicographically, then by alphabetically by title
        if order_matters: sql += ' ORDER BY CASE WHEN days="0123456" THEN 0 WHEN days IS NULL THEN 2 WHEN days="" THEN 2 ELSE 1 END, days,title'
        if day is None:
            rows=self.__execute(sql)
        else:
            rows=self.__execute(sql,('%{0}%'.format(day),))
        return rows
    
    def add_subscription(self, url, title, img, year, imdbnum, days):
        sql = 'REPLACE INTO subscriptions (url, title, img, year, imdbnum, days) VALUES (?, ?, ?, ?, ?, ?)'
        self.__execute(sql, (url, title, img, year, imdbnum, days))

    def delete_subscription(self, url):
        sql = 'DELETE FROM subscriptions WHERE url=?'
        self.__execute(sql, (url,))

    def edit_days(self, url, days):
        sql = "UPDATE subscriptions SET days=? WHERE url=?"
        self.__execute(sql, (days, url))
    
    def add_ext_sub(self, sub_type, url, imdbnum, days):
        sql = 'REPLACE INTO external_subs (type, url, imdbnum, days) VALUES (?, ?, ?, ?)'
        self.__execute(sql, (sub_type, url, imdbnum, days))

    def delete_ext_sub(self, sub_type, url):
        sql = 'DELETE FROM external_subs WHERE type=? and url=?'
        self.__execute(sql, (sub_type, url,))

    def edit_external_days(self, sub_type, url, days):
        sql = "UPDATE external_subs SET days=? WHERE type=? and url=?"
        self.__execute(sql, (days, sub_type, url))

    def get_external_subs(self, sub_type=None, day=None):
        sql = 'SELECT type, url, imdbnum, days FROM external_subs'
        if sub_type: sql +=' WHERE type=?'
        if day:
            if sub_type:
                sql += ' AND'
            else:
                sql += ' WHERE' 
            sql += ' days LIKE ?'

        params=None
        if sub_type and day:
            params=(sub_type, day)
        elif sub_type:
            params = (sub_type,)
        elif day:
            params = (day,)

        if not params:
            rows=self.__execute(sql)
        else:
            rows=self.__execute(sql, params)

        return rows


    def cache_data(self,name,value):
        sql = 'REPLACE INTO cache_data (name,value) VALUES(?, ?)'
        self.__execute(sql, (url, body))


    def get_cache_data(self, name):
        sql = 'SELECT * FROM cache_data WHERE name = ?'
        return self.__execute(sql, (name))


    def cache_url(self,url,body):
        now = time.time()
        sql = 'REPLACE INTO url_cache (url,response,timestamp) VALUES(?, ?, ?)'
        self.__execute(sql, (url, body, now))
    
    def get_cached_url(self, url, cache_limit=8):
        html=''
        now = time.time()
        limit = 60 * 60 * cache_limit
        sql = 'SELECT * FROM url_cache WHERE url = ?'
        rows=self.__execute(sql, (url,))
            
        if rows:
            created = float(rows[0][2])
            age = now - created
            if age < limit:
                html=rows[0][1]
        return html
    
    def cache_season(self, season_num,season_html):
        sql = 'REPLACE INTO seasons(season,contents) VALUES(?, ?)'        
        self.__execute(sql, (season_num, season_html))
    
    def get_cached_season(self, season_num):
        sql = 'SELECT contents FROM seasons WHERE season=?'
        season_html=self.__execute(sql, (season_num,))[0][0]
        return season_html
    
    def export_from_db(self, full_path):
        temp_path = os.path.join(self.profile_path,'temp_export_%s.csv' % (int(time.time())))
        with open(temp_path, 'w') as f:
            writer=csv.writer(f)
            f.write('***VERSION: %s***\n' % self.__get_db_version())
            if self.__table_exists('favourites'):
                f.write(CSV_MARKERS.FAVOURITES+'\n')
                for fav in self.get_favourites():
                    writer.writerow(fav)
            if self.__table_exists('subscriptions'):
                f.write(CSV_MARKERS.SUBSCRIPTIONS+'\n')
                for sub in self.get_subscriptions():
                    writer.writerow(sub)
            if self.__table_exists('new_bkmark'):
                f.write(CSV_MARKERS.BOOKMARKS+'\n')
                for bookmark in self.get_bookmarks():
                    writer.writerow(bookmark)
            if self.__table_exists('external_subs'):
                f.write(CSV_MARKERS.EXT_SUBS+'\n')
                for sub in self.get_external_subs():
                    writer.writerow(sub)
        
        self.addon.log('Copying export file from: |%s| to |%s|' %(temp_path, full_path))
        if not xbmcvfs.copy(temp_path, full_path):
            raise Exception('Export: Copy from |%s| to |%s| failed' % (temp_path, full_path))
          
        if not xbmcvfs.delete(temp_path):
            raise Exception('Export: Delete of %s failed.' % (temp_path))
    
    def import_into_db(self, full_path):
        temp_path = os.path.join(self.profile_path, 'temp_import_%s.csv' % (int(time.time())))
        self.addon.log('Copying import file from: |%s| to |%s|' %(full_path, temp_path))
        if not xbmcvfs.copy(full_path, temp_path):
            raise Exception('Import: Copy from |%s| to |%s| failed' % (full_path, temp_path))
        
        try:
            with open(temp_path,'r') as f:
                    reader=csv.reader(f)
                    mode=''
                    _=f.readline() #read header
                    for line in reader:
                        if CSV_MARKERS.FAVOURITES in line[0] or CSV_MARKERS.SUBSCRIPTIONS in line[0] or CSV_MARKERS.BOOKMARKS in line[0] or CSV_MARKERS.EXT_SUBS in line[0]:
                            mode=line[0]
                            continue
                        elif mode==CSV_MARKERS.FAVOURITES:
                            try:
                                self.save_favourite(line[0], line[1], line[2], line[3])
                            except: pass # save_favourite throws exception on dupe
                        elif mode==CSV_MARKERS.SUBSCRIPTIONS:
                            # don't allow import of days with values other than 0-6
                            if line[5].translate(None,'0123456'): line[5] = '0123456' 
                            self.add_subscription(line[0], line[1], line[2], line[3], line[4], line[5])
                        elif mode==CSV_MARKERS.BOOKMARKS:
                            self.set_bookmark(line[0], line[1])
                        elif mode==CSV_MARKERS.EXT_SUBS:
                            self.add_ext_sub(line[0], line[1], line[2], line[3])
                        else:
                            raise Exception('CSV line found while in no mode')
        finally:
            if not xbmcvfs.delete(temp_path):
                raise Exception('Import: Delete of %s failed.' % (temp_path))
    
    def execute_sql(self, sql):
        self.__execute(sql)

    # intended to be a common method for creating a db from scratch
    def init_database(self):

        self.addon.log('Building Icefilms Database')
        if self.db_type == DB_TYPES.MYSQL:
            self.__execute('CREATE TABLE IF NOT EXISTS seasons (season INTEGER UNIQUE, contents TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS favourites (type VARCHAR(10), name TEXT, url VARCHAR(255) UNIQUE, imdbid VARCHAR(10))')
            self.__execute('CREATE TABLE IF NOT EXISTS subscriptions (url VARCHAR(255) UNIQUE, title TEXT, img TEXT, year TEXT, imdbnum TEXT, days VARCHAR(7))')
            self.__execute('CREATE TABLE IF NOT EXISTS url_cache (url VARCHAR(255) NOT NULL, response MEDIUMBLOB, timestamp TEXT, PRIMARY KEY(url))')
            self.__execute('CREATE TABLE IF NOT EXISTS db_info (setting TEXT, value TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS new_bkmark (url VARCHAR(255) PRIMARY KEY NOT NULL, resumepoint DOUBLE NOT NULL)')            
            self.__execute('CREATE TABLE IF NOT EXISTS external_subs (type INTEGER NOT NULL, url VARCHAR(255) NOT NULL, imdbnum TEXT, days VARCHAR(7), PRIMARY KEY (type, url))')
            self.__execute('CREATE TABLE IF NOT EXISTS cache_data (name TEXT, value TEXT, PRIMARY KEY(name(250)))')
            self.__execute('CREATE TABLE IF NOT EXISTS recent_watched (url VARCHAR(255) PRIMARY KEY NOT NULL, type TEXT, name TEXT, year TEXT, season TEXT, episode TEXT, imdbid TEXT, timestamp TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS queue_list (url VARCHAR(255) PRIMARY KEY NOT NULL, type TEXT, name TEXT, year TEXT, season TEXT, episode TEXT, imdbid TEXT, timestamp TEXT)')
            try: self.__execute('DROP INDEX unique_db_info ON db_info')
            except: pass # ignore failures if the index doesn't exist
            self.__execute('CREATE UNIQUE INDEX unique_db_info ON db_info (setting (255))')
        else:
            self.__create_sqlite_db()
            self.__execute('CREATE TABLE IF NOT EXISTS seasons (season UNIQUE, contents)')
            self.__execute('CREATE TABLE IF NOT EXISTS favourites (type, name, url, imdbid)')
            self.__execute('CREATE TABLE IF NOT EXISTS subscriptions (url, title, img, year, imdbnum, days VARCHAR(7))')
            self.__execute('CREATE TABLE IF NOT EXISTS url_cache (url UNIQUE, response, timestamp)')
            self.__execute('CREATE TABLE IF NOT EXISTS db_info (setting TEXT, value TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS new_bkmark (url TEXT PRIMARY KEY NOT NULL, resumepoint DOUBLE NOT NULL)')
            self.__execute('CREATE TABLE IF NOT EXISTS external_subs (type INTEGER NOT NULL, url TEXT NOT NULL, imdbnum TEXT, days VARCHAR(7), PRIMARY KEY (type, url))')
            self.__execute('CREATE TABLE IF NOT EXISTS cache_data (name TEXT, value TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS recent_watched (url TEXT PRIMARY KEY NOT NULL, type TEXT, name TEXT, year TEXT, season TEXT, episode TEXT, imdbid TEXT, timestamp TEXT)')
            self.__execute('CREATE TABLE IF NOT EXISTS queue_list (url, type, name, year, season, episode, imdbid, timestamp)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_fav ON favourites (url)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_sub ON subscriptions (url)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_url ON url_cache (url)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_db_info ON db_info (setting)') 
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_name ON cache_data (name)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_watched ON recent_watched (url)')
            self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_queue ON queue_list (url)')
        
        # reload the previously saved backup export
        # if db_version is not None and cur_version !=  db_version:
            # self.addon.log('Restoring DB from backup at %s' % (self.mig_path))
            # self.import_into_db(self.mig_path)
            # self.addon.log('DB restored from %s' % (self.mig_path))

        #sql = 'REPLACE INTO db_info (setting, value) VALUES(?,?)'
        #self.__execute(sql, ('version', self.addon.get_version()))

    def __table_exists(self, table):
        if self.db_type==DB_TYPES.MYSQL:
            sql='SHOW TABLES LIKE ?'
        else:
            sql='select name from sqlite_master where type="table" and name = ?'
        rows=self.__execute(sql, (table,))
        
        if not rows:
            return False
        else:
            return True


    def reset_db(self):
        if self.db_type==DB_TYPES.SQLITE:
            self.db.close()
            try:
                self.addon.log('Delete database file: %s' % self.db_path)
                xbmcvfs.delete(self.db_path)
            except Exception, e:
                self.addon.log_error('Failed to delete: %s with error: %s' % (self.db_path, e))
                return False
            self.db=None
            self.__connect_to_db()
            self.init_database()
            return True
        else:
            return False


    def __execute(self, sql, params=None):
        if params is None:
            params=[]
            
        rows=None
        sql=self.__format(sql)
        cur = self.db.cursor()
        self.addon.log_debug('Running: %s with %s' % (sql, params))
        cur.execute(sql, params)
        if sql[:6].upper() == 'SELECT' or sql[:4].upper() == 'SHOW':
            rows=cur.fetchall()
        cur.close()
        self.db.commit()
        return rows

    def __get_db_version(self):
        version=None
        try:
            sql = 'SELECT value FROM db_info WHERE setting="version"'
            rows=self.__execute(sql)
        except:
            return None
        
        if rows: 
            version=rows[0][0]
            
        return version
    
    # purpose is to save the current db with an export, drop the db, recreate it, then connect to it
    def __prep_for_reinit(self):
        self.mig_path = os.path.join(self.profile_path, 'mig_export_%s.csv' % (int(time.time())))
        self.addon.log('Backing up DB to %s' % (self.mig_path))
        self.export_from_db(self.mig_path)
        self.addon.log('Backup export of DB created at %s' % (self.mig_path))
        self.__drop_all()
        self.addon.log('DB Objects Dropped')
        
    def __create_sqlite_db(self):
        if not xbmcvfs.exists(os.path.dirname(self.db_path)): 
            try: xbmcvfs.mkdirs(os.path.dirname(self.db_path))
            except: os.mkdir(os.path.dirname(self.db_path))
    
    def __drop_all(self):
        if self.db_type==DB_TYPES.MYSQL:
            sql = 'show tables'
        else:
            sql = 'select name from sqlite_master where type="table"'
        rows=self.__execute(sql)
        db_objects = [row[0] for row in rows]
            
        for db_object in db_objects:
            sql = 'DROP TABLE IF EXISTS %s' % (db_object)
            self.__execute(sql)
            
    def __connect_to_db(self):
        if not self.db:
            if self.db_type == DB_TYPES.MYSQL:
                self.db = database.connect(database=self.dbname, user=self.username, password=self.password, host=self.address, buffered=True)
            else:
                self.db = database.connect(self.db_path)
                self.db.text_factory = str

    # apply formatting changes to make sql work with a particular db driver
    def __format(self, sql):
        if self.db_type ==DB_TYPES.MYSQL:
            sql = sql.replace('?', '%s')
            
        if self.db_type == DB_TYPES.SQLITE:
            if sql[:7]=='REPLACE':
                sql = 'INSERT OR ' + sql

        return sql
