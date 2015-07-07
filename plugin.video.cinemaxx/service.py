import os
import xbmc, xbmcgui
import re

db_dir  = os.path.join(xbmc.translatePath("special://database"), 'cinemaxxdotrocache.db')
tmp_dir = xbmc.translatePath("special://temp")

try:
	try: from sqlite3 import dbapi2 as database
	except: from pysqlite2 import dbapi2 as database
except: pass


def convert_seconds(seconds):
	m, s = divmod(seconds, 60)
	h, mins = divmod(m, 60)
	if m > 60: return "%02d:%02d:%02d" % (h, mins, s)
	else: return "%02d:%02d" % (m, s)


def titlecase(s):
	s = re.sub(r"\d{1,2}x\d{1,2}(-\d{1,2})?", "", s).strip()
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(), s)



class Service(xbmc.Player):
	def __init__(self, *args, **kwargs):
		xbmc.Player.__init__(self, *args, **kwargs)
		self.reset()

		self.last_run = 0
		
		xbmc.log('cinemaxx.ro: Service starting...')


	def reset(self):
		xbmc.log('cinemaxx.ro: Service: Resetting...')
		
		win = xbmcgui.Window(10000)
		win.clearProperty('cinemaxx.playing.title')

		self._totalTime = 999999
		self._lastPos = 0
		self._sought = False
		self.tracking = False
		self.video_type = ''
		self.video_table = ''
		self.title = ''


	def check(self):
		win = xbmcgui.Window(10000)
		if win.getProperty('cinemaxx.playing.title'): return True
		else: return False


	def onPlayBackStarted(self):
		try:
			xbmc.log('cinemaxx.ro: Service: Playback started')
			
			self._totalTime = self.getTotalTime()
			
			self.tracking = self.check()
			
			if self.tracking:			
				xbmc.log('cinemaxx.ro: Service: Tracking progress...')
				
				win = xbmcgui.Window(10000)
				self.title = win.getProperty('cinemaxx.playing.title')
				self.video_type = 'movie'
				
				sql = 'SELECT bookmark FROM bookmarks WHERE video_type=? AND title=?'
				
				db = database.connect(db_dir)
				cur = db.cursor()
				cur.execute(sql, (self.video_type, unicode(self.title, 'utf-8')))
				bookmark = cur.fetchone()
				db.close()
				
				if bookmark:
					bookmark = float(bookmark[0])
					if not (self._sought and (bookmark - 30 > 0)):
						question = 'Continuati %s de la %s?' % (titlecase(self.title), convert_seconds(bookmark))
						resume = xbmcgui.Dialog().yesno(titlecase(self.title), '', question, '', 'De la inceput', 'Continuati')
						if resume: self.seekTime(bookmark)
						self._sought = True
					
		except: pass
		
		
	def onPlayBackStopped(self):
		try:
			xbmc.log('cinemaxx.ro: Playback Stopped')
			
			if self.tracking:
				playedTime = int(self._lastPos)
				percent = int((playedTime / self._totalTime) * 100)
				
				pT = convert_seconds(playedTime)
				tT = convert_seconds(self._totalTime)
				
				xbmc.log('cinemaxx.ro: Service: %s played of %s, total = %s%%' % (pT, tT, str(percent)))
				
				if playedTime == 0 and self._totalTime == 999999:
					raise RuntimeError('XBMC silently failed to start playback')
				
				elif (percent > 85) and self.video_type:
					xbmc.log('cinemaxx.ro: Service: Threshold met. Removing bookmark')
					
					sql = 'DELETE FROM bookmarks WHERE video_type=? AND title=?'
					
					import db
					db = database.connect(db_dir)
					cur = db.cursor()
					cur.execute(sql, (self.video_type, unicode(self.title, 'utf-8')))
					db.commit()
					db.close()
				
				else:
					xbmc.log('cinemaxx.ro: Service: Threshold not met. Saving bookmark')
					
					sql = 'INSERT OR REPLACE INTO bookmarks (video_type, title, bookmark) VALUES (?,?,?)'
					
					db = database.connect(db_dir)
					cur = db.cursor()
					cur.execute(sql, (self.video_type, unicode(self.title, 'utf-8'), playedTime))
					db.commit()
					db.close()
		
		except: pass
		
		self.reset()
	
		
	def onPlayBackEnded(self):
		xbmc.log('cinemaxx.ro: Service: Playback completed')
		self.onPlayBackStopped()



monitor = Service()

try:
	while not xbmc.abortRequested:
		while monitor.tracking and monitor.isPlayingVideo():
			monitor._lastPos = monitor.getTime()
			xbmc.sleep(1000)
		xbmc.sleep(1000)
	xbmc.log('cinemaxx.ro: Service: Shutting Down...')
except: pass
