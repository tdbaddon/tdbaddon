import os
import xbmc

try:
	from sqlite3 import dbapi2 as database
	print 'cinemaxx.ro: Loading sqlite3 as DB engine version: %s' % database.sqlite_version
except:
	from pysqlite2 import dbapi2 as database
	print 'cinemaxx.ro: pysqlite2 as DB engine'

class DB:
	def __init__(self):
		self.succes = False
		try:
			self.videocache = os.path.join(xbmc.translatePath("special://database"), 'cinemaxxdotrocache.db')
			self.dbcon = database.connect(self.videocache)
			self.dbcon.row_factory = database.Row
			self.dbcur = self.dbcon.cursor()
			self.create_tables()
			self.succes = True
		except: pass
	
	
	def create_tables(self):
		self.dbcon.execute('CREATE TABLE IF NOT EXISTS bookmarks (video_type, title, bookmark)')
		self.dbcon.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_bmk ON bookmarks (video_type, title)')
		self.dbcon.commit()
		
		xbmc.log('cinemaxx.ro: All tables have been successfully loaded.')
	
	
	def __del__(self):
		try:
			self.dbcur.close()
			self.dbcon.close()
		except: pass
		