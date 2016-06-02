#!/usr/bin/python
#encoding: utf-8

#/*
# *      Copyright (C) 2015-2016 gerikss, modded with permission by podgod
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  ===================
# *
# *  Sbnation API in this plugin belongs to sbnation.com and being used 
# *  only to find NBA/NHL/NFL/MLB games and scores (the same way as on sbnation.com/scoreboard website)
# *  
# *  All Reddit resources used in this plugin belong to their owners and reddit.com
# *  
# *  All logos used in this plugin belong to their owners
# *  
# *  All video streams used in this plugin belong to their owners
# *  
# *  
# */



import urllib, urllib2, sys, cookielib, base64, re
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from datetime import datetime, timedelta
import json
import calendar, time
import CommonFunctions
import praw
import urlparse
import random
import checkaddon
common = CommonFunctions

__addon__ = xbmcaddon.Addon('plugin.video.prosport')
__addonname__ = __addon__.getAddonInfo('name')
path = __addon__.getAddonInfo('path')
display_score = __addon__.getSetting('score')
display_status = __addon__.getSetting('status')
display_start_time = __addon__.getSetting('start_time')
show_sd = __addon__.getSetting('showsd')
show_hehe = __addon__.getSetting('showhehe')
show_cast = __addon__.getSetting('showcast')
show_xrxs  = __addon__.getSetting('showxrxs')
display_pattern = __addon__.getSetting('pattern')
username  = __addon__.getSetting('username')
password = __addon__.getSetting('password')
#checkaddon.do_block_check()


logos ={'nba':'http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png',
'nhl':'https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png',
'nfl':'http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif',
'mlb':'http://content.sportslogos.net/logos/4/490/full/1986.gif',
'soccer':'http://images.clipartpanda.com/soccer-ball-clipart-soccer-ball-clip-art-4.png'}

sd_streams = ['apollofm.website','giostreams.eu','watch-sportstv.boards.net', 'hdstream4u.com', 'stream24k.com', 'wizhdsports.com', 'antenasport.com', 'sportsnewsupdated.com', 'baltak.com', 'watchnba.tv', 'feedredsoccer.at.ua', 'jugandoes.com', 'wiz1.net', 'bosscast.net', 'watchsportstv.boards.net', 'tv-link.in', 'klivetv.co', 'videosport.me', 'livesoccerg.com', 'zunox.hk', 'serbiaplus.club', 'zona4vip.com', 'ciscoweb.ml', 'streamendous.com']

def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def GetURL(url, referer=None):
    url = url.replace('///','//')
    request = urllib2.Request(url)
    request.add_header('User-agent', randomagent())
    
    if referer:
    	request.add_header('Referer', referer)
    try:
    	response = urllib2.urlopen(request, timeout=10)
    	html = response.read()
    	return html
    except:
    	if 'reddit' in url:
    		xbmcgui.Dialog().ok(__addonname__, 'Looks like '+url+' is down... Please try later...')
    	return None

def GetJSON(url, referer=None):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
    if referer:
    	request.add_header('Referer', referer)
    try:
    	response = urllib2.urlopen(request, timeout=5)
    	f = response.read()
    	jsonDict = json.loads(f)
    	return jsonDict
    except:
    	xbmcgui.Dialog().ok(__addonname__, 'Looks like '+url+' is down... Please try later...')
    	return None

def GameStatus(status):
	statuses = {'pre-event':'Not started', 'mid-event':'[COLOR green]In progress[/COLOR]', 'post-event':'Completed', 'postponed':'Postponed'}
	if status in statuses:
		return statuses[status]
	else: return ''	

def Main():
	addDir("[COLOR=FF00FF00][ NBA GAMES ][/COLOR]", '', iconImg='http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png', mode="nba")
	addDir("[COLOR=FF00FF00][ NHL GAMES ][/COLOR]", '', iconImg='https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png', mode="nhl")
	addDir("[COLOR=FF00FF00][ NFL GAMES ][/COLOR]", '', iconImg='http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif', mode="nfl")
	addDir("[COLOR=FF00FF00][ MLB GAMES ][/COLOR]", '', iconImg='http://content.sportslogos.net/logos/4/490/full/1986.gif', mode="mlb")
	addDir("[COLOR=blue][ MY SUBREDDITS ][/COLOR]", '', iconImg='http://scitechconnect.elsevier.com/wp-content/uploads/2014/07/1reddit-logo2.png', mode="myreddit")
	addDir("[COLOR=FFFFFF00][ Archive ][/COLOR]", '', iconImg='special://home/addons/plugin.video.prosport/icon.png', mode="archive")
	xbmcplugin.endOfDirectory(h)

def Arch():
	addDir("[COLOR=FFFFFF00][ NBA Archive ][/COLOR]", '', iconImg='http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png', mode="nbaarch")
	addDir("[COLOR=FFFFFF00][ NFL Archive ][/COLOR]", '', iconImg='http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif', mode="nflarch")
	addDir("[COLOR=FFFFFF00][ NHL Archive ][/COLOR]", '', iconImg='https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png', mode="nhlarch")
	addDir("[COLOR=FFFFFF00][ XRXS NHL Archive ][/COLOR]", '', iconImg='https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png', mode="xrnhlarch")
	#addDir("[COLOR=FFFFFF00][ MLB Archive ][/COLOR]", '', iconImg='http://content.sportslogos.net/logos/4/490/full/1986.gif', mode="mlbarch")
	xbmcplugin.endOfDirectory(h)
	
def Games(mode):
	today = datetime.utcnow() - timedelta(hours=8)
	today_from = str(today.strftime('%Y-%m-%d'))+'T00:00:00.000-05:00'
	today_to = str(today.strftime('%Y-%m-%d'))+'T23:59:00.000-05:00'
	url = 'http://www.sbnation.com/sbn_scoreboard/ajax_leagues_and_events?ranges['+mode+'][from]='+today_from+'&ranges['+mode+'][until]='+today_to+'&_='+str(int(time.time()))
	js = GetJSON(url)
	js = js['leagues'][mode]
	if js:	
		if mode == 'nfl':
			addDir('[COLOR=FF00FF00][B]NFL Redzone[/B][/COLOR]', GAMEURL, iconImg=logos[mode], home='redzone', away='redzone', mode="STREAMS")
		for game in js:
			home = game['away_team']['name']
			away = game['home_team']['name']
			if 'mlb' in mode:
				try:
					hs = str(game['score']['home'][game['score']['cols'].index('R')])
					if not hs:
						hs = '0'
				except:
					hs = '0'
				try:
					avs = str(game['score']['away'][game['score']['cols'].index('R')])
					if not avs:
						avs = '0'
				except:
					avs = '0'
			else:
				hs = str(game['score']['home'][game['score']['cols'].index('Total')])
				if not hs:
					hs = '0'
				avs = str(game['score']['away'][game['score']['cols'].index('Total')])
				if not avs:
					avs = '0'
			score = ' - '+avs+':'+hs
			start_time = game['start_time']
			try:
				plus = False
				st = start_time.replace('T', ' ')
				if '+' in st:
					plus = True
					str_new = st.split('+')[-1]
					st = st.replace('+'+str_new,'')
				else:
					str_new = st.split('-')[-1]
					st = st.replace('-'+str_new,'')
				str_new = str_new.split(':')[0]
				if plus:
					st_time_utc = datetime(*(time.strptime(st, '%Y-%m-%d %H:%M:%S')[0:6]))-timedelta(hours=int(str_new))
				else:
					st_time_utc = datetime(*(time.strptime(st, '%Y-%m-%d %H:%M:%S')[0:6]))+timedelta(hours=int(str_new))
				local_game_time = utc_to_local(st_time_utc)
				local_time_str = ' - '+local_game_time.strftime(xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))
			except:
				local_time_str = ''
			status = GameStatus(game['status'])
			status = ' - '+status
			title = '[COLOR=FF00FF00][B]'+game['title'].replace(game['title'].split()[-1],'')+'[/B][/COLOR]'
			if display_start_time=='true':
				title = title+'[COLOR=FFFFFF00]'+local_time_str+'[/COLOR]'
			if display_status=='true':
				title = title+'[COLOR=FFFF0000]'+status+'[/COLOR]'
			if display_score=='true':
				title = title+'[COLOR=FF00FFFF]'+score+'[/COLOR]'
			addDir(title, mode, iconImg=logos[mode], home=home, away=away, mode="prostreams")
	else:
		addDir("[COLOR=FFFF0000]Could not fetch today's "+mode.upper()+" games... Probably no games today?[/COLOR]", '', iconImg="", mode="")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def MyReddits():
	sys_url = sys.argv[0] + '?mode=addnew'
	item = xbmcgui.ListItem('[COLOR=FFFF0000][ Add new subreddit ][/COLOR]', iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=False)
	reddits = __addon__.getSetting('reddits').split(',')
	if len(reddits)>0:
		for reddit in reddits:
			popup = []
			uri = sys.argv[0] + "?url="+reddit+"&mode=edit"
			popup.append(('Edit subreddit', 'RunPlugin(%s)'%uri,))
			uri2 = sys.argv[0] + "?url="+reddit+"&mode=remove"
			popup.append(('Remove subreddit', 'RunPlugin(%s)'%uri2,))
			if ':' in reddit:
				title = reddit.split(":")[0]
				pattern = ''
				if display_pattern == 'true':
					pattern = " - "+reddit.split(":")[-1]
				if len(title)>0:
					addDir2("[COLOR=FF00FF00][ "+title.upper()+" ]"+pattern+"[/COLOR]", reddit, '', iconImg='', popup=popup, mode="topics")
			else:
				if len(reddit)>0:
					addDir2("[COLOR=FF00FF00][ "+reddit.upper()+" ][/COLOR]", reddit, '', iconImg='', popup=popup, mode="topics")
	xbmcplugin.endOfDirectory(h)

def Topics(url):
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	if username and password:
		try:
			r.login(username, password)
		except:
			dialog = xbmcgui.Dialog()
			dialog.notification('Pro Sport', 'Please make sure reddit login and password are correct', xbmcgui.NOTIFICATION_WARNING, 3000)
	r.config.api_request_delay = 0
	for submission in r.get_subreddit(url.split(':')[0]).get_hot(limit=30):
		if ":" in url:
			pattern = url.split(":")[-1]
			if pattern.lower() in submission.title.encode('utf-8').lower():
				addDir("[COLOR=FFFFFF00][ "+submission.title.encode('utf-8')+" ][/COLOR]", submission.id, iconImg='', home=submission.title.encode('utf-8'), away='', mode="mystreams")
		else:
			addDir("[COLOR=FFFFFF00][ "+submission.title.encode('utf-8')+" ][/COLOR]", submission.id, iconImg='', home=submission.title.encode('utf-8'), away='', mode="mystreams")
	xbmcplugin.endOfDirectory(h)

def Addnew():
	kbd = xbmc.Keyboard()
	kbd.setDefault('')
	kbd.setHeading("Add new subreddit")
	kbd.doModal()
	s = None
	if kbd.isConfirmed():
	    s = kbd.getText()
	words = []
	history = __addon__.getSetting('reddits')
	if history:
	    words = history.split(",")
	if s and s not in words:
	    words.append(s)
	    __addon__.setSetting('reddits', ','.join(words))
	xbmc.executebuiltin("Container.Refresh")

def Edit(url):
	kbd = xbmc.Keyboard()
	kbd.setDefault(url)
	kbd.setHeading("Edit subreddit")
	kbd.doModal()
	s = None
	if kbd.isConfirmed():
	    s = kbd.getText()
	words = []
	history = __addon__.getSetting('reddits')
	if history:
	    words = history.split(",")
	for el in words:
		if el==url and s:
			words[words.index(el)] = s
	__addon__.setSetting('reddits', ','.join(words))
	xbmc.executebuiltin("Container.Refresh")

def Remove(url):
	title = xbmc.getInfoLabel('ListItem.Title')
	title = title.replace('[COLOR=FFFFFF00][','').replace('][/COLOR]','').strip()
	reddits = __addon__.getSetting('reddits').split(',')
	reddits = [x.lower() for x in reddits]
	reddits.remove(url.lower())
	__addon__.setSetting('reddits', ','.join(reddits))
	xbmc.executebuiltin("Container.Refresh")

def getProStreams(ur, home, away):
	orig_title = '[COLOR=FF00FF00][B]'+away+' at '+home+'[/B][/COLOR]'
	if 'redzone' in orig_title:
		orig_title = '[COLOR=FF00FF00][B]NFL Redzone[/B][/COLOR]'
	home_f = home.lower().split()[0]
	away_f = away.lower().split()[0]
	home_l = home.lower().split()[-1]
	away_l = away.lower().split()[-1]
	if 'nba' in ur and show_hehe=='true':
		addDir('[ Hehestreams ]', '', iconImg='', home=home_l, away=away_l, mode="hehestreams")
	if 'nhl' in ur and show_xrxs=='true':
		addDir('[ Xrxs ]', '', iconImg='', home=home_l, away=away_l, mode="xrxsstreams")
	if 'nhl' in ur and show_cast=='true':
		addLink('Caststreams', orig_title, 'caststreams', mode="play")
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	r.config.api_request_delay = 0
	links=[]
	for submission in r.get_subreddit(ur+'streams').get_hot(limit=30):
		if (home_l in submission.title.lower() and away_l in submission.title.lower()) or (home_f in submission.title.lower() and away_l in submission.title.lower()) or (home_l in submission.title.lower() and away_f in submission.title.lower()) or (home_f in submission.title.lower() and away_f in submission.title.lower()):
			regex = re.compile(r'([-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)',re.IGNORECASE)
			link = re.findall(regex, submission.selftext.encode('utf-8'))
			links = links + link
			flat_comments = praw.helpers.flatten_tree(submission.comments)
			for comment in flat_comments:
				if not isinstance(comment,praw.objects.Comment):
					flat_comments.remove(comment)
			try:
				flat_comments.sort(key=lambda comment: comment.score , reverse=True)
			except:
				pass
			for comment in flat_comments:
				try:
					link = re.findall(regex, comment.body.encode('utf-8'))
					links = links + link
				except:
					pass	
	if links:
		DisplayLinks(links, orig_title)
	else:
		addDir("[COLOR=FFFF0000]Could not find any streams on reddit...[/COLOR]", '', iconImg="", mode="")
		xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def getMyStreams(url, home):
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	if username and password:
		try:
			r.login(username, password)
		except:
			dialog = xbmcgui.Dialog()
			dialog.notification('Pro Sport', 'Please make sure reddit login and password are correct', xbmcgui.NOTIFICATION_WARNING, 3000)
	r.config.api_request_delay = 0
	submission = r.get_submission(submission_id=url)
	links=[]
	regex = re.compile(r'([-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)',re.IGNORECASE)
	link = re.findall(regex, submission.selftext.encode('utf-8'))
	links = links + link
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if not isinstance(comment,praw.objects.Comment):
			flat_comments.remove(comment)
	try:
		flat_comments.sort(key=lambda comment: comment.score , reverse=True)
	except:
		pass
	for comment in flat_comments:
		try:
			link = re.findall(regex, comment.body.encode('utf-8'))
			links = links + link
		except:
			pass
	if links:
		DisplayLinks(links, home)
	else:
		addDir("[COLOR=FFFF0000]Could not find any streams...[/COLOR]", '', iconImg="", mode="")
		xbmcplugin.endOfDirectory(h, cacheToDisc=True)


def DisplayLinks(links, orig_title):	
	urls = []
	print links
	for url in links:
		url = url[0]
		if 'http://' not in url and 'https://' not in url:
			url = 'http://www.'+url
		if url not in urls and 'blabseal.com' in url:
			addLink('Blabseal.com', orig_title, url, mode="play")
			urls.append(url)
		if url not in urls and 'iceballet' in url:
			addLink('Iceballet', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '1apps.com' in url:
			addLink('Oneapp', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '//youtu' in url or '.youtu' in url and 'list' not in url:
			addLink('Youtube.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'freecast.in' in url:
			addLink('Freecast.in', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamsus.com' in url:
			addLink('Streamsus.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamboat.tv' in url:
			addLink('Streamboat.tv', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nbastream.net' in url:
			addLink('Nbastream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nhlstream.net' in url:
			addLink('Nhlstream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'livenflstream.net' in url:
			addLink('Livenflstream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'fs.anvato.net' in url:
			addLink('Fox ToGo (US IP Only)', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'mlblive-akc' in url:
			addLink('MLB app', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamsarena.eu' in url:
			addLink('Streamsarena.eu', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamup.com' in url and 'm3u8' not in url:
			addLink('Streamup.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'torula' in url:
			addLink('Torula.us', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'webm' in url or ('caststreams' in url and 'getGame' in url):
			addLink('caststreams', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'gstreams.tv' in url:
			addLink('Gstreams.tv', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nfl-watch.com/live/watch' in url or 'nfl-watch.com/live/-watch' in url or 'nfl-watch.com/live/nfl-network' in url:
			addLink('Nfl-watch.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'ducking.xyz' in url:
			addLink('Ducking.xyz', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamandme' in url:
			addLink('Streamandme', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'henno.info' in url:
			addLink('Henno', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'stream2hd.net' in url:
			addLink('Stream2hd', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'serbiaplus.club/cbcsport.html' in url:
			addLink('CbcSportAz', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'moonfruit.com' in url:
			addLink('Moonfruit', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'castalba.tv' in url:
			addLink('Castalba', orig_title, url, mode="play")
			urls.append(url)
		elif ('room' in url or 'YES' in url) and 'm3u8' in url:
			room = url.split('/')[6]
			if room not in urls:
				addLink('Room HD (US IP Only)', orig_title, url, mode="play")
				urls.append(room)
		elif url not in urls and '101livesportsvideos.com' in url and 'ace' not in url:
			addLink('101livesportsvideos.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '.m3u8' in url and 'room' not in url and 'anvato' not in url and 'mlblive-akc' not in url and 'YES' not in url:
			addLink('M3U8 stream', orig_title, url, mode="play")
			urls.append(url)
		if show_sd=='true':
			if url not in urls and 'ace' not in url and any(el in url for el in sd_streams):
				title = '(SD) '
				try:
					title = title+urlparse.urlparse(url).netloc
				except:
					pass
				addLink(title, orig_title, url, mode="play")
				urls.append(url)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)
	
def ParseLink(el, orig_title):
	el = 'http'+el.split('http')[-1]
	if 'caststreams' in el:
		url = Caststreams(orig_title)
		return url
	elif any(e in el for e in sd_streams):
		url = Universal(el)
		return url
	elif 'blabseal.com' in el:
		url = Blabseal(el)
		return url
	elif 'iceballet' in el:
		url = Universal(el)
		return url
	elif '1apps.com' in el:
		url = Universal(el)
		return url
	elif 'youtu' in el and 'list' not in el:
		url = Universal(el)
		return url
	elif 'freecast.in' in el:
		url = Freecastin(el)
		return url
	elif 'streamsus.com' in el:
		url = Streamsus(el)
		return url
	elif 'streamboat.tv' in el:
		url = Streambot(el)
		return url
	elif 'nbastream.net' in el:
		url = Universal(el)
		return url
	elif 'nhlstream.net' in el:
		url = Universal(el)
		return url
	elif 'livenflstream.net' in el:
		url = Universal(el)
		return url
	elif 'fs.anvato.net' in el:
		url = Getanvato(el)
		return url
	elif 'mlblive-akc' in el:
		url = Getmlb(el)
		return url
	elif 'streamsarena.eu' in el:
		url = Streamarena(el)
		return url
	elif 'streamup.com' in el and 'm3u8' not in el:
		url = GetStreamup(el.split('/')[3])
		return url
	elif 'torula' in el:
		url = Torula(el)
		return url
	elif 'gstreams.tv' in el:
		url = Gstreams(el)
		return url
	elif 'nfl-watch.com/live/watch' in el or 'nfl-watch.com/live/-watch' in el or 'nfl-watch.com/live/nfl-network' in el:
		url = Nflwatch(el)
		return url
	elif 'ducking.xyz' in el:
		url = Ducking(el)
		return url
	elif 'webm' in el or ('caststreams' in el and 'getGame' in el):
		url = el
		return url
	elif 'streamandme' in el:
		url = Universal(el)
		return url
	elif 'henno.info' in el:
		url = Henno(el)
		return url
	elif 'stream2hd.net' in el:
		url = Stream2hd(el)
		return url
	elif 'serbiaplus.club/cbcsport.html' in el:
		url = CbcSportAz(el)
		return url
	elif 'moonfruit.com' in el:
		url = Moonfruit(el)
		return url
	elif 'castalba.tv' in el:
		url = Castalba(el)
		return url
	elif ('room' in el or 'YES' in el) and 'm3u8' in el:
		url = Getroom(el)
		return url
	elif '101livesportsvideos.com' in el:
		url = Universal(el)
		return url
	elif '.m3u8' in el and 'room' not in el and 'anvato' not in el and 'mlblive-akc' not in el:
		return el
				

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def Archive(page, mode):
	if mode == 'mlbarch':
		url = 'http://www.life2sport.com/category/basketbol/nba/page/'+str(page)
	if mode == 'nbaarch':
		url = 'http://www.life2sport.com/category/basketbol/nba/page/'+str(page)
	elif mode == 'nflarch':
		url = 'http://www.life2sport.com/category/american-football/page/'+str(page)
	html = GetURL(url)
	links = common.parseDOM(html, "a", attrs={"rel": "bookmark"}, ret="href")
	titles = common.parseDOM(html, "a", attrs={"rel": "bookmark"}, ret="title")
	if links:
		del links[1::2]
	for i, el in enumerate(links):
		if '-nba-' in el or '-nfl-' in el:
			title = common.parseDOM(html, "a", attrs={"href": el}, ret="title")[0]
			title = title.split('/')[-1]+' - '+title.split('/')[len(title.split('/'))-2]
			title = strip_non_ascii(title)
			title = title.replace('&#8211;','').strip()
			addDir(title, el, iconImg="", mode="playarchive")
	uri = sys.argv[0] + '?mode=%s&page=%s' % (mode, str(int(page)+1))
	item = xbmcgui.ListItem("next page...", iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(h, uri, item, True)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)
	
def Nhlarchive(page, mode):
	url = 'http://rutube.ru/api/video/person/979571/?page='+str(page)+'&format=json'
	json = GetJSON(url)
	json = json['results']
	for el in json:
		title = el['title']
		id = el['id']
		img = el['thumbnail_url']
		addLink(title, title, id, iconImg=img, mode="playnhlarchive")
	uri = sys.argv[0] + '?mode=%s&page=%s' % (mode, str(int(page)+1))
	item = xbmcgui.ListItem("next page...", iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(h, uri, item, True)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Xrxsarch():
	for i in range (1,5,1):
		yesterday = datetime.today() - timedelta(i)
		yesterday = yesterday.strftime('%Y-%m-%d')
		addDir(yesterday, yesterday, iconImg='', home='', away='', mode="xrxsday")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Xrxsday(yesterday):
	html = GetURL("http://xrxs.net/nhl/?date="+yesterday)
	titles = re.findall('(PM.+?<)',html)
	for title in titles:
		title = title.replace('PM','').replace('|','').replace('<','').strip()
		links = html.split(title)[-1].split('<hr/>')[0]
		addDir(title, links, iconImg='', home=title, away='', mode="xrxsgame")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Xrxsgame(links, orig_title):
	links = common.parseDOM(links, "a", ret="href")
	nhlcookie = GetURL("https://raw.githubusercontent.com/iCanuck/NHLstreams/master/cookie")
	for link in links:
		link = 'http://xrxs.net/nhl/'+link
		if 'HOME' in link:
			title = re.findall('(HOME.+?\.m3u8)',link)[0].replace('.m3u8','')
			addDirectLink(title, {'Title': orig_title}, link+nhlcookie)
		elif 'VISIT' in link:
			title = re.findall('(VISIT.+?\.m3u8)',link)[0].replace('.m3u8','')
			addDirectLink(title, {'Title': orig_title}, link+nhlcookie)
		elif 'FRENCH' in link:
			title = re.findall('(FRENCH.+?\.m3u8)',link)[0].replace('.m3u8','')
			addDirectLink(title, {'Title': orig_title}, link+nhlcookie)
		elif 'NATIONAL' in link:
			title = re.findall('(NATIONAL.+?\.m3u8)',link)[0].replace('.m3u8','')
			addDirectLink(title, {'Title': orig_title}, link+nhlcookie)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Playnhlarchive(url):
	orig_title = xbmc.getInfoLabel('ListItem.Title')
	url = 'http://rutube.ru/api/play/options/'+url+'?format=json'
	json = GetJSON(url)
	link = json['video_balancer']['m3u8']
	Play(link, orig_title)
	
def PlayArchive(url):
	orig_title = xbmc.getInfoLabel('ListItem.Title')
	html = GetURL(url)
	html = html.split('>english<')[-1]
	link = common.parseDOM(html, "iframe", ret="src")[0]
	link = link.replace('https://videoapi.my.mail.ru/videos/embed/mail/','http://videoapi.my.mail.ru/videos/mail/')
	link = link.replace('html','json')
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
	conn = urllib2.Request(link)
	connection = opener.open(conn)
	f = connection.read()
	connection.close()
	js = json.loads(f)
	for cookie in cookieJar:
		token = cookie.value
	js = js['videos']
	for el in js:
		addDirectLink(el['key'], {'Title': orig_title}, el['url']+'|Cookie=video_key='+token)
		#addLink(el['key'], orig_title, el['url']+'|Cookie=video_key='+token, mode="play")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def GetStreamup(channel):
	try:
		chan = GetJSON('https://api.streamup.com/v1/channels/'+channel)
		if chan['channel']['live']:
			videoId = chan['channel']['capitalized_slug'].lower()
			domain = GetURL('https://lancer.streamup.com/api/redirect/'+videoId)
			return 'https://'+domain+'/app/'+videoId+'_aac/playlist.m3u8'
	except:
		return None	

def GetYoutube(url):
	try:
		if ('channel' in url or 'user' in url) and 'live' in url:
			html = GetURL(url)
			videoId = html.split("https://www.youtube.com/watch?v=")[-1].split('">')[0]
			link = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + videoId
			return link
		regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
		youtube_regex_match = re.match(regex, url)
		videoId = youtube_regex_match.group(6)
		link = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + videoId
		return link
	except:
		return None
		
def Getmlb(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'3000K').replace(lst[len(lst)-1],'3000_slide.m3u8')
			return link
	except:
		return None

def Getanvato(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'4028k')
			return link
	except:
		return None
		
def Getroom(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'4028k')
			return link
	except:
		return url
		
def Blabseal(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		pass
	try:
		channel = 'asljkdfasdf'
		link = GetStreamup(channel)
		return link
	except:
		return None
		
def Hehestreams(home, away):
	try:
		html = GetURL("http://hehestreams.xyz/")
		titles = common.parseDOM(html, "a", attrs={"class": "results-link"})
		links = common.parseDOM(html, "a", attrs={"class": "results-link"}, ret="href")
		for title in titles:
			if home.lower() in title.lower() and away.lower() in title.lower():
				link = links[titles.index(title)]
				link = "http://hehestreams.xyz"+link
				html = GetURL(link)
				lnks = common.parseDOM(html, "option", ret="value")
				if lnks:
					for lnk in lnks:
						lnk = 'http://'+lnk.split('http://')[-1]
						if 'turner' in lnk:
							try:
								timest = lnk.split("exp=")[-1].split("~acl")[0]
								time_exp = datetime.fromtimestamp(int(timest)).strftime(xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))
							except:
								time_exp = ''
							addDirectLink('Turner - (external player) link expires '+time_exp, {'Title': away+' @ '+home}, lnk)
						elif 'neulion' in lnk:
							lnk = lnk.replace('amp;','')
							lnk = lnk.replace('androidtab', '3000')
							try:
								timest = lnk.split("expires=")[-1].split("~access")[0]
								time_exp = datetime.fromtimestamp(int(timest)).strftime(xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))
							except:
								time_exp = ''
							addDirectLink('Neulion link expires '+time_exp, {'Title': away+' @ '+home}, lnk)
				else:
					addDir("[COLOR=FFFF0000]Could not find any streams on hehestreams...[/COLOR]", '', iconImg="", mode="")
		xbmcplugin.endOfDirectory(h, cacheToDisc=True)
	except:
		pass	


def Xrxs(home, away):
	try:
		today = datetime.utcnow() - timedelta(hours=8)
		today = str(today.strftime('%Y-%m-%d'))
		html = GetURL("http://xrxs.net/nhl/?date="+today)
		html = html.split('<br/><hr/>')
		for el in html:
			if home.lower() in el.lower() and away.lower() in el.lower():
				links = common.parseDOM(el, "a", ret="href")
				nhlcookie = GetURL("https://raw.githubusercontent.com/iCanuck/NHLstreams/master/cookie")
				for link in links:
					if 'http://xrxs.net' not in link:
						link = 'http://xrxs.net/nhl/'+link
					if 'HOME' in link:
						title = re.findall('(HOME.+?\.m3u8)',link)[0].replace('.m3u8','')
						addDirectLink(title, {'Title': away+' @ '+home}, link+nhlcookie)
					elif 'VISIT' in link:
						title = re.findall('(VISIT.+?\.m3u8)',link)[0].replace('.m3u8','')
						addDirectLink(title, {'Title': away+' @ '+home}, link+nhlcookie)
					elif 'FRENCH' in link:
						title = re.findall('(FRENCH.+?\.m3u8)',link)[0].replace('.m3u8','')
						addDirectLink(title, {'Title': away+' @ '+home}, link+nhlcookie)
					elif 'NATIONAL' in link:
						title = re.findall('(NATIONAL.+?\.m3u8)',link)[0].replace('.m3u8','')
						addDirectLink(title, {'Title': away+' @ '+home}, link+nhlcookie)
						#addDirectLink(title, {'Title': away+' @ '+home}, link+nhlcookie)
						
	except:
		pass	


def Caststreams(orig_title):
	try:
		orig_title = orig_title.replace('[COLOR=FF00FF00][B]','').replace('[/B][/COLOR]','')
		home = orig_title.split('at')[0].split()[0]
		away = orig_title.split('at')[-1].split()[0]
		url = 'http://caststreams.com:2053/login-web'
		data = json.dumps({"email":"prosport4@testmail.com","password":"prosport","ipaddress":"desktop","androidId":"","deviceId":"","isGoogleLogin":0})
		request = urllib2.Request(url, data)
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request, timeout=5)
		resp = response.read()
		jsonDict = json.loads(resp)
		token = jsonDict['token']
		url = 'http://caststreams.com:2053/feeds'
		request = urllib2.Request(url)
		request.add_header('Authorization', token)
		response = urllib2.urlopen(request, timeout=5)
		resp = response.read()
		jsonDict = json.loads(resp)
		feeds = jsonDict['feeds']
		for feed in feeds:
			title = feed['nam'].lower().replace('ny', 'new')
			if home.lower() in title.lower() and away.lower() in title.lower() and 'testing' not in title.lower():
				channel = feed['url'][0]
				link = 'http://caststreams.com:2053/getGame?rUrl='+channel
				return link	
			else:
				continue
	except:
		return None	
		
def Oneapp(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		return None
		
def Torula(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "input", attrs={"id": "vlc"}, ret="value")[0]
		link = block_content
		return link
	except:
		return None

def Freecastin(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", attrs={"width": "100%"}, ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		return None
		
def Streamsus(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		pass
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "a", ret="href")[0]
		if 'streamboat' in block_content:
			link = Streambot(block_content)
			return link
	except:
		return None

def CbcSportAz(url):
	try:
		html = GetURL('http://serbiaplus.club/embedhls/cbcsport.html')
		regex = re.compile(r'([-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)',re.IGNORECASE)
		links = re.findall(regex, html)
		for link in links:
			if 'http' in link[0] and 'm3u8' in link[0]:
				return link[0]
	except:
		return None
			
def Streambot(url):
	try:
		html = GetURL(url, referer=url)
		link1 = 'http://' + html.split("cdn_host: '")[-1].split("',")[0]
		link2 = html.split("playlist_url: '")[-1].split("',")[0]
		link = link1+link2
		return link
	except:
		return None
	

def Nbanhlstreams(url):
	try:
		if 'nba' in url:
			URL = 'http://www.nbastream.net/'
		elif 'nhl' in url:
			URL = 'http://www.nhlstream.net/'
		elif 'nfl' in url:
			URL = 'http://www.livenflstream.net/'
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		html  = GetURL(URL+link)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'streamup' in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
	except:
		return None
		
def Streamandme(url):
	try:
		html = GetURL(url)
		if 'https://streamboat.tv/@' in html:
			url = html.split('https://streamboat.tv/@')[-1].split('"')[0]
			url = 'https://streamboat.tv/@'+url
			url = Streambot(url)
			return url
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		channel = link.split('/')[3]
		link = GetStreamup(channel)
		return link
	except:
		return None

def Henno(url):
	try:
		url = 'http://henno.info/stream?stream=Streamup&source=&template=any&ticket=&user='
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		channel = link.split('/')[3]
		link = GetStreamup(channel)
		return link
	except:
		return None
		
def Stream2hd(url):
	try:
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'streamup' in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
	except:
		return None

def Gstreams(url):
	try:
		html = GetURL(url, referer=url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'gstreams.tv' in link:
			html  = GetURL(link)
			link = html.split('https://')[1]
			link = link.split('",')[0]
			link = 'https://' + link 
			return link
		elif 'streamup.com' in link and 'm3u8' not in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
		elif 'youtu' in link:
			link = GetYoutube(link)
			return link
		elif '.m3u8' in link:
			return link
	except:
		return None
	
		
def Moonfruit(url):
	try:
		cookieJar = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
		conn = urllib2.Request(url)
		connection = opener.open(conn, timeout=5)
		for cookie in cookieJar:
			token = cookie.value
		headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Content-Type" : "application/x-www-form-urlencoded",
            "Cookie":"markc="+token,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8,bg;q=0.6,it;q=0.4,ru;q=0.2,uk;q=0.2",
		}
		html = connection.read()
		link = common.parseDOM(html, "iframe",  ret="src")
		link = url+link[-1]
		conn = urllib2.Request(link, headers=headers)
		connection = opener.open(conn, timeout=5)
		html = connection.read()
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'streamup.com' in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
	except:
		return None

def Nflwatch(url):
	try:
		html = GetURL(url)
		links = common.parseDOM(html, "iframe",  ret="src")
		for link in links:
			if 'streamup' in link:
				channel = link.split('/')[3]
				link = GetStreamup(channel)
				return link
			else:
				continue
		if 'p2pcast' in html:
			id = html.split("'text/javascript'>id='")[-1]
			id = id.split("';")[0]
			link = p2pcast(id)
			return link
	except:
		return None

def Ducking(url):
	try:
		html = GetURL(url)
		link = common.parseDOM(html, "iframe", ret="src")[1]
		url = 'http://www.ducking.xyz/quack/'+link
		html = GetURL(url, referer=url)
		if 'p2pcast' in html:
			id = html.split('php?id=')[-1].split('&')[0]
			link = p2pcast(id)
			return link
	except:
		return None
	
		
def Streamarena(url):
	try:
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		link = link.replace('..','http://www.streamsarena.eu/')
		html  = GetURL(link)
		if 'streamup' in html:
			link = common.parseDOM(html, "iframe",  ret="src")[0]
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
		elif 'p2pcast' in html:
			id = html.split("'text/javascript'>id='")[-1]
			id = id.split("';")[0]
			link = p2pcast(id)
			return link
	except:
		return None
		
def Livesports101(url):
	try:
		html = GetURL(url)
		try:
			block_content = common.parseDOM(html, "meta", attrs={"property": "og:description"}, ret="content")
			for el in block_content:
				if 'youtube.com' in el:
					link = GetYoutube(block_content)
					return link
				elif 'streamboat.tv' in el:
					link = el
					link = link.split('http://')[1]
					link = link.split("'")[0]
					link = 'http://' + link 
					return link
				elif 'streamup' in el:
					link = el
					link = link.split('https://')[1]
					link = link.split("'")[0]
					link = 'https://' + link 
					return link
		except:
			pass
		try:	
			block_content = common.parseDOM(html, "embed", attrs={"id": "vlcp"}, ret="target")[0]
			if 'streamboat' in block_content or 'streamup' in block_content:
				link = block_content
				return link
		except:
			pass
		try:
			block_content = common.parseDOM(html, "iframe", ret="src")[0]
			if 'streamup' in block_content:
				channel = block_content.split('/')[3]
				link = GetStreamup(channel)
				return link
			elif 'youtube.com' in block_content:
					link = GetYoutube(block_content)
					return link
			elif 'wiz1' in block_content:
				this = GetURL(block_content, referer=block_content)
				link = re.compile('src="(.+?)"').findall(str(this))[0]
				if 'sawlive' in link:
					link = sawresolve(link)
					return link
		except:
			pass
	except:
		return None

def Castalba(url):
	try:
		try:
			cid  = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0] 
		except:
			cid = re.compile('channel/(.+?)(?:/|$)').findall(url)[0]
		try:
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer='http://castalba.tv'        
		url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&r=%s'%(cid,urlparse.urlparse(referer).netloc)
		pageUrl=url
		request = urllib2.Request(url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		request.add_header('Referer', referer)
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		result=urllib.unquote(result)
		if 'm3u8' in result:
			link = re.compile('filez\s*=\s*(?:unescape\()\'(.+?)\'').findall(result)[0]
			link = 'http://' + url + '.m3u8'
			link += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})          
		else:
			try:
				filePath = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
			except:
				file = re.findall('var file\s*=\s*(?:unescape\()?(?:\'|\")(.+?)(?:\'|\")',result)[0]
				try:
					file2 = re.findall("'file':\s*unescape\(file\)\s*\+\s*unescape\('(.+?)'\)",result)[0]
					filePath = file+file2
				except:
					filePath = file
			swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]
			'''try:
				streamer=re.findall('streamer\(\)\s*\{\s*return \'(.+?)\';\s*\}',result)
				if 'rtmp' not in streamer:
					streamer = 'rtmp://' + streamer
			except:
				try:
					streamer = re.compile("var sts\s*=\s*'(.+?)'").findall(result)
				except:
					streamer=re.findall('streamer\(\)\s*\{\s*return \'(.+?)\';\s*\}',result)'''
			try:
				streamer = re.findall("('://.+?\live)",result)[-1]
				streamer = 'rtmp' + streamer.replace("'","")
			except:
				streamer = re.findall("(rtmp://.+?\live)",result)[0]
			link = streamer.replace('///','//') + ' playpath=' + filePath +' swfUrl=' + swf + ' flashver=WIN\\2020,0,0,228 live=true timeout=15 swfVfy=true pageUrl=' + pageUrl
		return link
	except:
		return None


def Universal(url):
	if 'zona4vip.com/live' in url:
		url = url.replace('/live','')
	if 'serbiaplus.club/wlive' in url:
		url = 'http://serbiaplus.club/whd/'+url.split('/w')[-1]
	if 'wiz1.net/ch' in url or 'live9.net' in url:
		this = GetURL(url, referer=url)
		links = re.compile('src="(.+?)"').findall(str(this))
		for link in links:
			if 'sawlive' in link:
				lnk = sawresolve(link)
				return lnk
	if 'sawlive' in url:
		lnk = sawresolve(link)
		return lnk
	if 'streamup' in url:
		if 'm3u8' in url:
			return url
		channel = url.split('/')[3]
		link = GetStreamup(channel)
		return link
	if 'youtu' in url:
		link = GetYoutube(url)
		return link
	if 'lshstream' in url:
		link = lshstream(url)
		return link
	if 'p2pcast' in url and 'streamcdn' in url:
		link = p2pcast2(url)
		return link
	if 'hdcast.org' in url:
		id = url.split('u=')[-1].split('&')[0]
		link = hdcast(id)
		return link
	if 'm3u8' in url:
		return url
	html = GetURL(url, referer=url)
	if html and 'weplayer.pw' in html:
		id = html.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		link = weplayer(id)
		return link
	elif html and 'p2pcast' in html and 'streamcdn' not in html:
		id = html.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		link = p2pcast(id)
		return link
	elif html and 'castup' in html:
		id = html.split('fid="')[-1].split('";')[0]
		link = castup(id)
		return link
	elif html and 'rocktv.co' in html:
		id = html.split("fid='")[-1].split("';")[0]
		link = rocktv(id)
		return link
	elif html and 'castamp.com' in html:
		id = html.split('<script type="text/javascript">channel="')[-1].split('";')[0]
		link = castamp(id)
		return link
	elif html and 'broadcast/player' in html:
		id = html.split("<script type='text/javascript'>id='")[-1].split("';")[0]
		link = broadcast(id)
		return link
	elif html and 'streamking.cc' in html:
		id = re.findall("(http://streamking.+?')",html)[0]
		id = id.replace("'","")
		link = streamking(id)
		return link
	elif html and 'hdcast.org' in html and 'fid=' in html:
		id = html.split('fid="')[-1]
		id = id.split('";')[0]
		link = hdcast(id)
		return link
	elif html and 'sostart.pw' in html and 'fid=' in html:
		id = html.split('fid="')[-1]
		id = id.split('";')[0]
		url = 'http://www.sostart.pw/jwplayer6.php?channel='+id
		link = sostart(url)
		return link
	if html and 'https://streamboat.tv/@' in html:
			url = html.split('https://streamboat.tv/@')[-1].split('"')[0]
			url = 'https://streamboat.tv/@'+url
			url = Streambot(url)
			return url
	elif html and 'sawlive.tv' in html:
		#url = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(html)[0]
		#url = 'http://%s/embed/%s' % (url[0], url[1])
		url = re.findall('(http://www3.sawlive.tv/embed/.+?")',html)[0]
		url = url.replace('"','')
		print url
		link = sawresolve(url)
		return link
	elif html and '.m3u8' in html:
		link = re.findall('(http://.+?\.m3u8)',html)[0]
		return link
	elif html and 'rtmp' in html and 'jwplayer' in html:
		link = re.findall('(rtmp://.+?")',html)[0]
		link = link.replace('"','')
		return link
	else:
		domain = urlparse.urlparse(url).netloc
		scheme = urlparse.urlparse(url).scheme
		urls = common.parseDOM(html, 'iframe', ret='src')
		if urls:
			for url in urls:
				if 'http://' not in url and 'https://' not in url:
					if not url.startswith('/'):
						url = '/'+url
					if scheme:
						url = scheme+'://'+domain+url
					else:
						url = 'http://'+domain+url
				ss = Universal(url)
				if ss:
					return ss
				else:
					Universal(url)

	
def sawresolve2(url):
	
		result = GetURL(url)
		if 'var sw=' not in result:
			try:
				result = result.replace('sw=', 'var sw=')
			except:
				pass
		if 'var ch=' not in result:
			try:
				result = result.replace('ch=', 'var ch=')
			except:
				pass
		url = common.parseDOM(result, 'iframe', ret='src')[-1]
		url = url.replace(' ', '').replace('+','')
		var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
		for i in range(100):
			for v in var: result = result.replace(" %s " % v[0], ' %s '%v[1])
		var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
		var_dict = dict(var)
		for v in var:
			if '+' in v[1]:
				ss = v[1].rstrip('+').replace('"+','').split('+')
				sg = v[1].rstrip('+').replace('"+','')
				for s in ss:
					sg = sg.replace(s, var_dict[s])
				var_dict[v[0]]=sg.replace('+','')       
		for i in range(100):
			for v in var_dict.keys(): url = url.replace("'%s'" % v, var_dict[v])
			for v in var_dict.keys(): url = url.replace("(%s)" % v, "(%s)" % var_dict[v])
		url = url.replace(' ', '').replace('+','').replace('"','').replace('\'','')
		result = GetURL(url, referer=url)
		var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
		print result
		var_dict = dict(var)       
		file = re.compile("'file'\s*(.+?)\)").findall(result)[0]
		file = file.replace('\'','')
		for v in var_dict.keys():
			file = file.replace(v,var_dict[v])
		file = file.replace('+','').replace(',','').strip()
		try:
			if not file.startswith('http'): raise Exception()
			request = urllib2.Request(file)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			request.add_header('Referer', file)
			response = urllib2.urlopen(request, timeout=5)
			url = response.geturl()
			if not '.m3u8' in url: raise Exception()
			url += '|%s' % urllib.urlencode({'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Referer': file})
			return url
		except:
			pass
		strm = re.compile("'streamer'\s*(.+?)\)").findall(result)[0]
		strm = strm.replace('\'','')
		for v in var_dict.keys():
			strm = strm.replace(v,var_dict[v])
		strm = strm.replace('+','').replace(',','').strip()
		swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]
		url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=60' % (strm, file, swf, url)
		url = urllib.unquote(url).replace('unescape(','')
		return url
	
def sawresolve(url):
	try:     
		page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
		page = 'http://%s/embed/%s' % (page[0], page[1])        
		try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except: referer = page 
		result = GetURL(page, referer=referer)
		result = urllib.unquote_plus(result)
		vars = re.compile('var (.+?=".+?");').findall(str(result))
		for item in vars:
			var = item.split('=')
		rep = re.findall('.+?=.+?\.replace\("(.+?)","(.+?)"\)',str(result))[0]
		result = re.sub('\s\s+', ' ', result)
		url = common.parseDOM(result, 'iframe', ret='src')[-1]
		url = url.replace(' ', '').split("'")[0]      
		try:
			ch = re.compile('ch=""(.+?)""').findall(str(result))[0]
		except:
			ch = re.compile("ch='(.+?)'").findall(str(result))[0]
		try:
			sw = re.compile("sw='(.+?)'").findall(str(result))[0]
		except:
			sw = re.compile('sw=""(.+?)""').findall(str(result))[0]
		if ' ' in sw:
			for item in vars:
				var = item.replace('"','').replace("'",'').split('=')
				sw = re.sub(var[0], var[1], str(sw))
			sw = sw.replace(' ','')
		if ' ' in ch:
			for item in vars:
				var = item.replace('"','').replace("'",'').split('=')
				ch = re.sub(var[0], var[1], str(ch))
			ch = ch.replace(' ','')
		if len(str(ch)) > len(str(sw)):url = str(url)+str(sw)+'/'+str(ch)
		if len(str(sw)) > len(str(ch)):url = str(url)+str(ch)+'/'+str(sw)
		if rep[0] in str(url): url = str(url).replace(rep[0],rep[1])
		result = GetURL(url, referer=referer)
		file = re.compile("\('file',(.+?)\)").findall(result)[0]
		file = urllib.unquote_plus(file)
		var2= re.compile("var (.+?) = '(.+?)';").findall(result)
		strm = re.compile("\('streamer',(.+?)\)").findall(result)[0]
		strm =strm.replace("'",'').replace('"','')
		for name, parts in var2:
			name = name.replace("'",'').replace('"','')
			parts = parts.replace("'",'').replace('"','')
			if (name) in file:file = file.replace(name,parts)
			if (name) in strm: strm = parts
		file = file.replace(' ','').replace('"','').replace("'","")
		try:
			if not file.startswith('http'): raise Exception()
			request = urllib2.Request(file)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			request.add_header('Referer', file)
			response = urllib2.urlopen(request, timeout=5)
			url = response.geturl()
			if not '.m3u8' in url: raise Exception()
			url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
			return url    
		except:
			pass
		swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]
		url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=30' % (strm, file, swf, url)
		return url
	except:
		return None
          
       
		
def castup(id):
	try:
		url = 'http://www.castup.tv/embed_2.php?channel='+id
		pageUrl = url
		try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except: referer = url
		result = GetURL(url, referer)
		json_url = re.compile('\$.getJSON\("(.+?)", function\(json\){').findall(result)[0]
		token = re.compile("\('token', '(.+?)'\);").findall(result)[0]
		data = GetJSON(json_url, referer)
		file = data['streamname']
		rtmp = data['rtmp']
		swf ='http://www.castup.tv' + re.compile('.*?SWFObject\([\'"]([^\'"]+)[\'"].*').findall(result)[0]
		url = rtmp + ' playpath=' + file + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=' + pageUrl
		return url
	except:
		return None


def castamp(id):
	try:
		url = 'http://castamp.com/embed.php?c=%s&tk=H0SKNbzC&vwidth=640&vheight=380'%id
		pageUrl=url
		result = GetURL(url, referer=url)
		result = urllib.unquote(result).replace('unescape(','').replace("'+'",'')
		result = re.sub('\/\*[^*]+\*\/','',result)
		var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
		var_dict = dict(var)
		file = re.compile('\'file\'\s*:\s*(.+?),').findall(result)[-1]
		fle = var_dict[file]
		if file+'.replace' in result:
			rslt = result.split(file+'.replace(')[-1].split(');')[0].replace("'","").strip()
			vars = rslt.split(',')
			fle = fle.replace(vars[0].strip(),vars[1].strip())
		rtmp = re.compile('(rtmp://[^\"\']+)').findall(result)[0]
		url = rtmp + ' playpath=' + fle + ' swfUrl=http://p.castamp.com/cplayer.swf' + ' flashver=WIN/2019,0,0,185 live=true timeout=15 swfVfy=1 pageUrl=' + pageUrl
		return url
	except:
		return None
	


def p2pcast(id):
	try:
		agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0'
		url = 'http://p2pcast.tech/stream.php?id='+id+'&live=0&p2p=0&stretching=uniform'
		request = urllib2.Request(url)
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		token = html.split('murl = "')[1].split('";')[0]
		link = base64.b64decode(token)
		request = urllib2.Request('http://p2pcast.tech/getTok.php')
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		js = json.loads(html)
		tkn = js['token']
		link = link+tkn
		link = link + '|User-Agent='+agent+'&Referer='+url
		return link
	except:
		return None
		
def broadcast(id):
	try:
		url = 'http://bro.adca.st/stream.php?id='+id
		ref = url
		result = GetURL(url, referer=url)
		curl = re.findall('curl\s*=\s*[\"\']([^\"\']+)',result)[0]
		url = base64.b64decode(curl)
		token = GetJSON('http://bro.adcast.tech/getToken.php')
		token = token['token']
		url+= 'wfNz6Pz_jNZfR8wmB8JEPw'
		url+='|%s' % urllib.urlencode({'User-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36','Referer':ref,'X-Requested-With':'ShockwaveFlash/21.0.0.216','Host':urlparse.urlparse(url).netloc,'Accept-Encoding':'gzip, deflate, lzma, sdch'})
		return url 
	except:
		return None


def p2pcast2(url):
	try:
		agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
		request = urllib2.Request(url)
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		token = html.split('murl = "')[1].split('";')[0]
		link = base64.b64decode(token)
		link = link + '|User-Agent='+agent+'&Referer='+url
		return link
	except:
		return None

def weplayer(id):
	try:
		url = 'http://weplayer.pw/stream.php?id='+id
		request = urllib2.Request(url)
		request.add_header('Host', urlparse.urlparse(url).netloc)
		request.add_header('Referer', 'http://wizhdsports.com')
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		id = result.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		url2 = 'http://deltatv.xyz/stream.php?id='+id
		request = urllib2.Request(url2)
		request.add_header('Referer', url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		streamer = result.split("streamer=")[-1].split("&amp;")[0]
		file = result.split("file=")[-1].split("&amp;")[0]
		url = streamer+' playpath='+file+' swfUrl=http://cdn.deltatv.xyz/players.swf token=Fo5_n0w?U.rA6l3-70w47ch pageUrl='+url2+' live=1'
		return url
	except:
		return None

def streamking(url):
	try:
		html = GetURL(url, referer=url)
		link = re.findall('(http://.+?\.m3u8)',html)[0]
		link += '|User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36&Referer='+url
		return link
	except:
		return None	


def hdcast(id):
	try:
		page = 'http://www.hdcast.org/embedlive2.php?u=%s&vw=640&vh=400&domain=www.nhlstream.net' % id
		request = urllib2.Request(page)
		request.add_header('Referer', 'http://www.nhlstream.net')
		request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		streamer = re.compile('file\s*:\s*\'(.+?)\'').findall(result)[0]
		token = 'SECURET0KEN#yw%.?()@W!'
		url = '%s swfUrl=http://player.hdcast.org/jws/jwplayer.flash.swf pageUrl=%s token=%s swfVfy=1 live=1 timeout=15' % (streamer, page, token)
		return url
	except:
		return None

def lshstream(url):
	try:
		url = 'http://'+url.split('http://')[-1]
		id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
		result = GetURL(url, referer=url)
		streamer = result.replace('//file', '')
		streamer = re.compile("file *: *'(.+?)'").findall(streamer)[-1]
		url=streamer + ' swfUrl=http://www.lshstream.com/jw/jwplayer.flash.swf flashver=WIN/2019,0,0,185 live=1 token=SECURET0KEN#yw%.?()@W! timeout=14 swfVfy=1 pageUrl=http://cdn.lshstream.com/embed.php?u=' + id
		return url
	except:
		return None


def rocktv(id):
	try:
		url = 'http://www.rocktv.co/embed.php?live='+id
		result = GetURL(url, referer=url)
		token = re.findall('securetoken\s*:\s*(?:\'|\")(.+?)(?:\'|\")',result)[0]
		rtmp = re.findall('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")',result)[0]
		url = rtmp + ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf live=1 flashver=WI/2020,0,0,286 token='  + token + ' timeout=14 swfVfy=1 pageUrl=' + url
		return url
	except:
		return None
		
def sostart(url):
	try:
		try:
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer=url
		result = GetURL(url, referer=referer)
		rtmp = re.findall('.*?[\'"]?file[\'"]?[:,]\s*[\'"]([^\'"]+)[\'"].*',result)[0]
		url = rtmp+' swfUrl=http://sostart.org/jw/jwplayer.flash.swf flashver=WI/2020,0,0,286 token=SECURET0KEN#yw%.?()@W! live=1 timeout=14 swfVfy=1 pageUrl='+url
		return url
	except:
		return None

def randomagent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))

###################TVA############################
'''
This check has been put in place to stop the inclusion of TVA (and friends) addons in builds
from build makers that publicly insult or slander TVA's developers and friends. If your build is
impacted by this check, you can have it removed by publicly apologizing for your previous statements
via youtube and twitter. Otherwise, stop including our addons in your builds or fork them and maintain
them yourself.
                                                                                           http://i.imgur.com/TqIEnYB.gif
                                                                                           TVA developers (and friends)
'''
def do_block_check(uninstall=True):
    import hashlib
    import xbmcvfs
    f = xbmcvfs.File('special://home/media/splash.png')
    splash_md5 = hashlib.md5(f.read()).hexdigest()
    bad_md5s = ['926dc482183da52644e08658f4bf80e8', '084e2bc2ce2bf099ce273aabe331b02e']
    bad_addons = ['plugin.program.targetin1080pwizard', 'plugin.video.targetin1080pwizard']
    has_bad_addon = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in bad_addons)
    if has_bad_addon or splash_md5 in bad_md5s:
        import xbmcgui
        import sys
        line2 = 'Press OK to uninstall this addon' if uninstall else 'Press OK to exit this addon'
        xbmcgui.Dialog().ok('Incompatible System', 'This addon will not work with the build you have installed', line2)
        if uninstall:
            import xbmcaddon
            import shutil
            addon_path = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
            shutil.rmtree(addon_path)
        sys.exit()
		
######################################

def Play(url, orig_title):
    url = ParseLink(url, orig_title)
    if not url:
    	dialog = xbmcgui.Dialog()
    	dialog.notification('Pro Sport', 'Stream not found', xbmcgui.NOTIFICATION_INFO, 3000)
    else:
    	item = xbmcgui.ListItem(path=url)
    	item.setInfo('video', { 'Title': orig_title })
    	xbmcplugin.setResolvedUrl(h, True, item)

    	
def addDir(title, url, iconImg="DefaultVideo.png", home="", away="", mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&home=' + urllib.quote_plus(str(home)) +'&away=' + urllib.quote_plus(str(away)) +'&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=True)

def addDir2(title, url, next_url, iconImg="DefaultVideo.png", popup=None, mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url)+'&next_url=' + urllib.quote_plus(next_url) +'&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels={'Title': title})
    if popup:
    	item.addContextMenuItems(popup, True)
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=True)

def addLink(title, orig_title, url, iconImg="DefaultVideo.png", mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))+ '&orig=' + urllib.quote_plus(str(orig_title))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setLabel(title)
    item.setInfo(type='Video', infoLabels={'Title': title})
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item)
    
def addDirectLink(title, infoLabels, url, iconImg="DefaultVideo.png"):
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels=infoLabels)
    xbmcplugin.addDirectoryItem(handle=h, url=url, listitem=item)
       
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param

h = int(sys.argv[1])
params = get_params()

mode = None
url = None

try: mode = urllib.unquote_plus(params['mode'])
except: pass

try: url = urllib.unquote_plus(params['url'])
except: pass

try: home = urllib.unquote_plus(params['home'])
except: pass

try: away = urllib.unquote_plus(params['away'])
except: pass

try: orig_title = urllib.unquote_plus(params['orig'])
except: pass

try: page = params['page'] if 'page' in params else 1
except: pass

if mode == None: Main()
elif mode == 'nfl': Games(mode)
elif mode == 'nba': Games(mode)
elif mode == 'nhl': Games(mode)
elif mode == 'mlb': Games(mode)
elif mode == 'soccer': Games(mode)
elif mode == 'myreddit': MyReddits()
elif mode == 'nbaarch': Archive(page, mode)
elif mode == 'nflarch': Archive(page, mode)
elif mode == 'nhlarch': Nhlarchive(page, mode)
elif mode == 'xrnhlarch': Xrxsarch()
elif mode == 'archive': Arch()
elif mode == 'playarchive': PlayArchive(url)
elif mode == 'playnhlarchive': Playnhlarchive(url)
elif mode == 'xrxsday': Xrxsday(url)
elif mode == 'xrxsgame': Xrxsgame(url, home)
elif mode == 'prostreams': getProStreams(url, home, away)
elif mode == 'hehestreams': Hehestreams(home, away)
elif mode == 'xrxsstreams': Xrxs(home, away)
elif mode == 'mystreams': getMyStreams(url, home)
elif mode == 'play': Play(url, orig_title)
elif mode == 'topics': Topics(url)
elif mode == 'addnew': Addnew()
elif mode == 'remove': Remove(url)
elif mode == 'edit': Edit(url)

xbmcplugin.endOfDirectory(h)