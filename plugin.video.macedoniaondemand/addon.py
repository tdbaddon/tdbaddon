# -*- coding: utf-8 -*- 

"""
	Macedonia On Demand XBMC addon.
	Watch videos and live streams from Macedonian TV stations, and listen to live radio streams.
	Author: Viktor Mladenovski
"""

import urllib,urllib2,re,xbmcplugin,xbmcaddon,xbmcgui,HTMLParser,json
import sys,os,os.path

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0'
str_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

ADDON=__settings__ = xbmcaddon.Addon(id='plugin.video.macedoniaondemand')
DIR_USERDATA = xbmc.translatePath(ADDON.getAddonInfo('profile'))
VERSION_FILE = DIR_USERDATA+'version.txt'
VISITOR_FILE = DIR_USERDATA+'visitor.txt'
VOLIMTV_UID  = DIR_USERDATA+'volimtvuid.txt'
VOLIMTV_PWD  = DIR_USERDATA+'volimtvpwd.txt'

__version__ = ADDON.getAddonInfo("version")

if not os.path.isdir(DIR_USERDATA):
	os.makedirs(DIR_USERDATA)

def platformdef():
	if xbmc.getCondVisibility('system.platform.osx'):
		if xbmc.getCondVisibility('system.platform.atv2'):
			log_path = '/var/mobile/Library/Preferences'
			log = os.path.join(log_path, 'xbmc.log')
			logfile = open(log, 'r').read()
		else:
			log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
			log = os.path.join(log_path, 'xbmc.log')
			logfile = open(log, 'r').read()
	elif xbmc.getCondVisibility('system.platform.ios'):
		log_path = '/var/mobile/Library/Preferences'
		log = os.path.join(log_path, 'xbmc.log')
		logfile = open(log, 'r').read()
	elif xbmc.getCondVisibility('system.platform.windows'):
		log_path = xbmc.translatePath('special://home')
		log = os.path.join(log_path, 'xbmc.log')
		logfile = open(log, 'r').read()
	elif xbmc.getCondVisibility('system.platform.linux'):
		log_path = xbmc.translatePath('special://home/temp')
		log = os.path.join(log_path, 'xbmc.log')
		logfile = open(log, 'r').read()
	else:
		logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'

	match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
	for build, platform in match:
		if re.search('12.0',build,re.IGNORECASE):
			build="Frodo"
		if re.search('11.0',build,re.IGNORECASE):
			build="Eden"
		if re.search('13.0',build,re.IGNORECASE):
			build="Gotham"
		return platform

	return "Unknown"

def fread(filename):
	ver = ''
	h = open(filename, "r")
	try:
		data = h.read()
	finally:
		h.close()
	return data

def fwrite(filename, data):
	h = open(filename, "wb")
	try:
		h.write(data)
	finally:
		h.close()

def get_visitorid():
	if os.path.isfile(VISITOR_FILE):
		visitor_id = fread(VISITOR_FILE)
	else:
		from random import randint
		visitor_id = str(randint(0, 0x7fffffff))
		fwrite(VISITOR_FILE, visitor_id)

	return visitor_id

__visitor__ = get_visitorid()

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

def setView(content='movies', mode=503):
	return 0
#	xbmcplugin.setContent(int(sys.argv[1]), content)
#	xbmc.executebuiltin("Container.SetViewMode("+str(mode)+")")


# ZULU live 

def createZuluListing():
	url='http://on.net.mk/zulu_tv.aspx'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a href="(.+?)" > *?<img src="(.+?)" class="imgclassresponsive"').findall(link)
	#for station, thumb in match:
	#	print station, thumb
	return match

def playZuluStream(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Zulu Stream', 'Initializing')
	pDialog.update(30, 'Fetching video stream')
	req = urllib2.Request('http://on.net.mk/'+url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	nextframe = re.compile('<iframe src="(.+?)"').findall(link)
	pDialog.update(60, 'Fetching video stream')
	req = urllib2.Request('http://on.net.mk/'+nextframe[0])
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	streammatch=re.compile('<video .+? src="(.+?)"').findall(link)
	pDialog.update(80, 'Playing')
	#playurl(streammatch[0].replace('_2/', '_1/'))
	playurl(streammatch[0])

	return True

# TELEKABEL live

def createTelekabelListing():
	url='http://telekabel.com.mk/index.php/mk/%D1%81%D1%82%D1%80%D0%B8%D0%BC%D0%B8%D0%BD%D0%B3?view=featured'

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<li class="level2.+?"><a href=\"(.+?)\".+?<span>(.+?)</span></a></li>').findall(link)
	return match


def playTelekabelStream(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Telekabel Stream', 'Initializing')
	req = urllib2.Request('http://telekabel.com.mk'+url)
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	pDialog.update(30, 'Fetching video stream 30%')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	nextframematch = re.compile('name="iframe"\n\t\tsrc="(.+?)"').findall(link)

	req = urllib2.Request('http://telekabel.com.mk'+nextframematch[0])
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	pDialog.update(60, 'Fetching video stream 60%')
	response = urllib2.urlopen(req)
	link = response.read()
	streammatch = re.compile("file:'(.+?)'").findall(link)

	pDialog.update(80, 'Playing')
	playurl(streammatch[0])
	pDialog.close()

	return True

# OFF NET methods

def createOffnetRadioListing():
	url='http://off.net.mk/radio'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a class=".+?" data-id=".+?" data-stream="(.+?)" data-frequency="(.*?)">(.+?)</a>').findall(link[link.find('block-views-live-stream-block'):])
	#for stream,freq,name in match:
	#	print freq+" "+name+" "+stream
	return match

# 24 Vesti methods

def play24VestiVesti():
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('24 Vesti', 'Initializing')
	url='http://24vesti.mk/video/vesti'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(50, 'Finding stream')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('file: "(.+?)"').findall(link)

	pDialog.update(80, 'Playing')
	playurl('http://24vesti.com.mk'+match[0]+'|Cookie=macedoniaondemand')
	pDialog.close()
	return True

def create24VestiEmisiiListing(urlpagenr):
	if urlpagenr == None or urlpagenr == '':
		url = 'http://24vesti.mk/video/emisii'
	else:
		url = 'http://24vesti.mk/video/emisii?page='+urlpagenr


	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<div class="views-field views-field-field-teaser-image-fid">.+?<a href="(.+?)" .+?><img src="(.+?)" .+?  \n  .+?  \n  .+?<a href=".+?">(.+?)</a>.+?').findall(link)

	#for u,thumb,title in match:
	#	print title

	return match

def create24VestiVideoSodrzina():
	url='http://24vesti.mk/'

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()

	match=re.compile('<span class="field-content"><div class="text-wrap">\n   <div class="views-field-title"><a href="(.+?)" class="imagecache imagecache-teaser-medium-wide imagecache-linked imagecache-teaser-medium-wide_linked"><img src="(.+?)" .+?\n   <div class="video-flag">(.+?)</div>\n   <div class="views-field-title"><a href=".+?">(.+?)</a></div>\n</div></span>  </div></li>\n').findall(link)

	#for u,thumb,title1,title2 in match:
	#	print title2.strip()
	return match


def play24VestiVideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('24Vesti Video', 'Initializing')
	req = urllib2.Request('http://24vesti.com.mk/'+str(url))
	req.add_header('User-Agent', user_agent)
	pDialog.update(30, 'Fetching video stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	filematch = re.compile('<param name="movie" value="(.+?)"').findall(link)
	titlematch = re.compile('<title>(.+?)</title>').findall(link)

	if filematch[0].__contains__('dailymotion'):
		stream = 'plugin://plugin.video.dailymotion_com/?url='+filematch[0].split('/')[-1]+'&mode=playVideo'
	elif filematch[0].__contains__('youtube'):
		stream = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+filematch[0].split('/')[-1]
	else:
		stream = filematch[0]

	pDialog.update(60, 'Playing')
	playurl(stream)
	pDialog.close()

	return True


# NOVATV methods

def createNovatvListing(page):
	url = 'http://novatv.mk/index.php?navig=8&cat='

	if page == 'novatv_makedonija':
		url += '2'
	elif page == 'novatv_evrozum':
		url += '9'
	elif page == 'novatv_sekulovska':
		url += '8'
	elif page == 'novatv_dokument':
		url += '14'
	elif page == 'novatv_studio':
		url += '16'
	elif page == 'novatv_aktuel':
		url += '18'
	elif page == 'novatv_globus':
		url += '17'
	elif page == 'novatv_kultura':
		url += '4'
	elif page == 'novatv_zanimlivosti':
		url += '1'

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	match=re.compile('<a class="ostanati_wrap" href="(.+?)"> \t  \t\r\n \t  .+? \r\n \t  <img src="(.+?)"  .+?  />\r\n \t  <h2 style="color:black;">(.+?)</h2>\r\n \t  <p>(.+?)</p>\r\n \t.+?<div class="more" style=".+?">.+?</div> \r\n \t  <div class=".+?" style=".+?">(.+?)</div> </div>\r\n \t  </div>\r\n \t  </a>').findall(link)
	return match


def playNovatvVideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Nova Tv Video', 'Initializing')
	req = urllib2.Request('http://novatv.mk/'+str(url))
	req.add_header('User-Agent', user_agent)
	pDialog.update(30, 'Fetching video stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	playlist=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)

	filematch = re.compile('<iframe style=".+?" title="YouTube video player" class="youtube-player" type="text/html" \r\n\r\nwidth=".+?" height=".+?" src="(.+?)" frameborder="0" allowfullscreen></iframe>').findall(link)
	if filematch != []:
		titlematch = re.compile('<h2 class="news_title" >(.+?)</h2>').findall(link)
		listitem = xbmcgui.ListItem(titlematch[0]);

		if filematch[0].__contains__('dailymotion'):
			playlist.add('plugin://plugin.video.dailymotion_com/?url='+filematch[0].split('/')[-1]+'&mode=playVideo', listitem)
		elif filematch[0].__contains__('youtube'):
			playlist.add('plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+filematch[0].split('?')[0].split('/')[-1], listitem)
		else:
			playlist.add(filematch[0], listitem)

	filematch = re.compile('<iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" allowfullscreen></iframe>').findall(link)
	if filematch != []:
		titlematch = re.compile('<h2 class="news_title" >(.+?)</h2>').findall(link)
		listitem = xbmcgui.ListItem(titlematch[0]);

		oldurl=''
		for u in filematch:
			if u.__contains__('youtube') and u != oldurl:
				listitem = xbmcgui.ListItem('video')
				#listitem.setProperty("PlayPaty", u)
				playlist.add('plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+u.split('/')[-1], listitem)
				oldurl=u

	if playlist.size() != 0:
		pDialog.update(60, 'Playing')
		player.play(playlist)
		pDialog.close()

	return True


# RADIOMK methods

def createRadiomkListing():
	url = 'http://www.radiomk.com/live/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	match = re.compile('<li><a href="(.+?)" rel="dofollow" ><img src="(.+?)" alt=".+?">(.+?)</a></li>').findall(link)
	return match

def playRadiomkstream(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Radiomk Stream', 'Initializing')

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(30, 'Fetching radio stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	titlematch = re.compile('<title>(.+?)</title>').findall(link)
	streammatch = re.compile("var stream = '(.+?)'").findall(link)
	if streammatch == []:
		streammatch = re.compile('file=(.+?);').findall(link)
		if streammatch == []:
			streammatch = re.compile('<embed src="(.+?)"').findall(link)

	pDialog.update(60, 'Playing')
	playurl(streammatch[0])
	pDialog.close()

	return True

# TV SITEL methods

def createSitelVideoListing():
	url='http://sitel.com.mk/video'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('href="(.+?)" class="video-priloog clearfix">\n<div class="teaser-image"><div class="icon"></div><img src="(.+?)" width=".+?" height=".+?" alt="" /></div>\n<div class="category">.+?</div>\n<h3 class="title">(.+?)</h3>').findall(link)
	return match

def playSitelVideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Sitel Video', 'Initializing')
	req = urllib2.Request("http://sitel.com.mk"+str(url))
	req.add_header('User-Agent', user_agent)
	pDialog.update(50, 'Fetching video stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	filematch = re.compile('file: "(.+?)"').findall(link)
	titlematch = re.compile('<title>(.+?)</title>').findall(link)

	if filematch[0].__contains__('rtmp'):
		rtmpurl = filematch[0]
		app=rtmpurl.split('/')[3]+'/'
		apos=rtmpurl.find(app)
		y=rtmpurl[apos+len(app):]
		stream = rtmpurl[:apos+len(app)]+' app='+app+' pageUrl=http://sitel.com.mk swfUrl=http://sitel.com.mk/sites/all/libraries/jw.player/jwplayer.flash.swf playpath='+y+' swfVfy=true'
	else:
		stream = filematch[0]
	pDialog.update(90, 'Playing')
	playurl(stream)
	pDialog.close()

	return True

def playSitelDnevnik():
	playurl('rtmp://video.sitel.com.mk/vod/ app=vod/ pageUrl=http://sitel.com.mk swfUrl=http://sitel.com.mk/sites/all/libraries/jw.player/jwplayer.flash.swf playpath=mp4:default/files/dnevnik/dnevnik/dnevnik.mp4 swfVfy=true')
	return True

#  MTV methods

def createmrtfrontList():
	url = 'http://play.mrt.com.mk/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<li class="">\n        <a href="(.+?)">\n            (.+?)        </a>\t\n    </li>').findall(link)
	return match

def duration_in_minutes(duration):
	split_duration=duration.split(':')
	minutes=0
	for i in range(0, len(split_duration)-1):
		minutes = minutes*60 + int(split_duration[i])
	return minutes

def list_mrtchannel(url):
	url = 'http://play.mrt.com.mk'+url
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	list=[]
	match=re.compile('<div class="col-xs-6 col-sm-3 (.+?) content">\n.+?<a href="(.+?)".+?\n.+?<img src="(.+?)".+?\n.+?\n.+?<span class="title gradient">(.+?)</span>').findall(link)

	# extract channels
	for type,url,thumb,title in match:
		list.append([type,url,thumb,'',title])

	match=re.compile('<div class="col-xs-6 col-sm-3 (.+?) content">\n.+?<a href="(.+?)".+?\n.+?<img src="(.+?)".+?\n.+?\n.+?<span class="duration">(.+?)</span>\n.+?<span class="title gradient">(.+?)</span>').findall(link)

	# extract latest videos on current channel
	for type,url,thumb,duration,title in match:
		list.append([type,url,thumb,str(duration_in_minutes(duration)),title])

	nextpage=''
	nextpagestart = link.find('class="next"')
	if nextpagestart != -1:
		nextpageend = link.find('</div>', nextpagestart)
		nextpagematch = re.compile("url:'(.+?)'").findall(link, nextpagestart, nextpageend)
		if nextpagematch != []:
			nextpage = nextpagematch[0]

	return [list, nextpage]

def list_mrtlive():
	url = 'http://play.mrt.com.mk/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	start=link.find('<ul class="dropdown-menu text-left')
	end=link.find('</ul', start)
	match=re.compile('<a class="channel" href=".+?" data-href="(.+?)" .+? title="(.+?)">\n.*?<img src="(.+?)"').findall(link[start:end])
	return match

def playmrtvideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('MRT Play live stream', 'Initializing')
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(50, 'Fetching video stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	match2=re.compile('"playlist":\[{"url":"(.+?)"').findall(link)
	match1 = re.compile('"baseUrl":"(.+?)"').findall(link)

	title = re.compile('<meta property="og:title" content="(.+?)"').findall(link)

	if match2 != [] and match1 != []:
		stream=match1[0]+"/"+match2[0]
		stream=stream[:stream.rfind('/')]+'/master.m3u8'
		if title != []:
			videotitle = title[0]
		else:
			videotitle = 'MRT Video'
		pDialog.update(70, 'Playing')
		playurl(stream)
		pDialog.close()
	elif match2 != []:
		stream=match2[0]
		if title != []:
			videotitle = title[0]
		else:
			videotitle = 'MRT Video'
		pDialog.update(70, 'Playing')
		playurl(stream)
		pDialog.close()

	return True

#  OTHER live streams methods

def createOtherListing():
	list=[]
	list.append(['Al Jazeera Balkans', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live app=aljazeeraflashlive-live swfUrl=http://www.nettelevizor.com/playeri/player.swf pageUrl=http://ex-yu-tv-streaming.blogspot.se playpath=aljazeera_balkans_high live=true swfVfy=true', 'http://balkans.aljazeera.net/profiles/custom/themes/aljazeera_balkans/images/banner.png'])
	return list

# HRT Methods

def createHRTSeriesListing():
	url='http://www.hrt.hr/enz/'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	start=link.find('<div class="all_shows">')
	end=link.find('</div>', start)
	match=re.compile('<li><a.+?href="(.+?)"><span>(.+?)</span></a></li>').findall(link[start:end])
	return match

def listHRTEpisodes(url):
	list=[]
	url = url.replace('&amp;', '&')
	if url[0:2] == '//':
		url = 'http:'+url

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)

	try:
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
	except:
		return list

	match=re.compile('<option selected="selected" value="(.+?)">(.+?)<').findall(link)
	for value,title in match:
		list.append([title.strip(), url+value])

	match=re.compile('option value="(.+?)">(.+?)<').findall(link)
	for value,title in match:
		list.append([title.strip(), url+value])

	return list

def playHRTVideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('HRT Video', 'Initializing')
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(50, 'Fetching video stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	filematch = re.compile('<video data-url="(.+?)"').findall(link)
	if filematch == []:
		filematch = re.compile('<video src="(.+?)"').findall(link)
	titlematch = re.compile('<title>(.+?)</title>').findall(link)

	if filematch[0].__contains__('youtu.be'):
		url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+filematch[0].split('/')[-1].strip()
	else:
		url = filematch[0]
	pDialog.update(90, 'Playing')
	playurl(url)
	pDialog.close()

	return True

# serbiaplus methods

def listSerbiaPlusTVs():
	htmltext = readurl('http://www.serbiaplus.com')
	match=re.compile('<frame src="(.+?)" ').findall(htmltext)
	if match != []:
		newurl = match[0]
		htmltext = readurl(newurl)
	else:
		newurl='http://www.serbiaplus.com'

	match = re.compile('<iframe name="iFrame1" .+? src="(.+?)"').findall(htmltext)
	if newurl[-1] != '/':
		newurl += '/'
	link = readurl(newurl+match[0])
	match=re.compile('<a href="(.+?)".+?target="_blank"><div class="wpmd">\n<div align=center><font face=".+?" class="ws12">(.+?)</font></div>').findall(link)
	return [newurl, match]

def playSerbiaPlusStream(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Serbia Plus', 'Initializing')

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(40, 'Finding stream')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()

	stream = serbiaplussearchurl(link)
	if stream == '':
		stream=findSerbiaPlusStream(link)

	if stream != '':
		if stream.__contains__('youtube.com'):
			stream = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+stream.split('=')[-1].strip()

		pDialog.update(80, 'Playing')
		playurl(stream)
		return True
	else:
		pDialog.close()
		return False

def serbiaplussearchurl(intext):
	stream = []
	if intext.find("file: \"") != -1 or intext.find("file:\"") != -1:
		stream=re.compile('file:.*?"(.+?)"').findall(intext)
	if intext.find("\"file\"") != -1:
		stream=re.compile(', *?"file":"(.+?)"').findall(intext)
	if intext.find("'file':") != -1:
		stream=re.compile("'file' *?: *?'(.+?)'").findall(intext)
	if intext.find("application/x-vlc-plugin") != -1 or intext.find("application/x-google-vlc-plugin") != -1:
		start = intext.find("application/x-vlc-plugin")
		if start == -1:
			start = intext.find("application/x-google-vlc-plugin")

		if start > 200:
			start -= 200
		else:
			start = 0

		stream=re.compile('target="(.+?)"').findall(intext, start)
	if intext.find("streamer=rtmp://") != -1:
		tmp=re.compile('file=(.+?)&streamer=(.+?)&').findall(intext)
		if tmp != []:
			stream = [tmp[0][1]+tmp[0][0]]
	if intext.find('flashvars="src') != -1 or intext.find('flashvars="streamer') != -1:
		tmp=re.compile('flashvars=".+?=(.+?)"').findall(intext)
		if tmp != []:
			stream=[urllib.unquote_plus(tmp[0]).strip()]
			stream[0]=stream[0].split(' ')[0]
			stream[0]=stream[0].split('&')[0]

	if stream != []:
		return HTMLParser.HTMLParser().unescape(stream[0])
	else:
		return ''

def decode_serbiaplus_frame(s, splitconst, appendconst, offsetconst):
	r = ""
	tmp = s.split(splitconst)
	s = urllib.unquote(tmp[0])
	k = urllib.unquote(tmp[1]+appendconst)

	for i in range(0, len(s)):
		r = r + chr((int(k[i%len(k)]) ^ ord(s[i])) + offsetconst)

	return r

def findSerbiaPlusStream(htmltext):
	start = 0
	end = -1

	searcharea = htmltext[start:]

	if searcharea.find("unescape('")!=-1:
		start = searcharea.find("unescape('")
		end = searcharea.find("')", start)
		encframe = searcharea[start+10:end]
		decframe = urllib.unquote(encframe)
		frame=decframe
	else:
		frame=searcharea

	if frame.__contains__('split("') and frame.__contains__("charCodeAt"):
		splitmatch = re.compile('split\("(.+?)"\);').findall(frame)
		appendmatch = re.compile('tmp\[1\].*?"(.+?)"').findall(frame)
		offsetmatch = re.compile('charCodeAt\(i\)\)\+(.+?)\)').findall(frame)

		payloadstart = searcharea.find("eval(unescape('")
		payloadstart = searcharea.find("unescape('", payloadstart+16)
		payloadstart = searcharea.find("'", payloadstart+11)
		payloadstart = searcharea.find("'", payloadstart+2)
		payloadend = searcharea.find("'", payloadstart+1)
		decframe = decode_serbiaplus_frame(searcharea[payloadstart+1:payloadend], splitmatch[0], appendmatch[0], int(offsetmatch[0]))
		frame = decframe

	frame=frame.replace('\n', ' ').replace('\r', ' ')
	stream=serbiaplussearchurl(frame)

	return stream

# volimtv methods

def setVolimtvMailPass():
	currentlogindetails = getVolimtvMailPass()
	currentuid=''
	currentpwd=''
	if currentlogindetails != False:
		currentuid = currentlogindetails.get('email')
		currentpwd = currentlogindetails.get('pass')
	kb = xbmc.Keyboard('', 'volim.tv login', False)
	kb.setHeading('Enter volim.tv username/email')
	kb.setHiddenInput(False)
	kb.setDefault(currentuid)
	kb.doModal()
	if (kb.isConfirmed()):
		email=kb.getText()
		kb = xbmc.Keyboard('', 'volim.tv login', True)
		kb.setHeading('Enter volim.tv password')
		kb.setHiddenInput(True)
		kb.setDefault(currentpwd)
		kb.doModal()
		if (kb.isConfirmed()):
			passwd=kb.getText()
			fwrite(VOLIMTV_UID, email)
			fwrite(VOLIMTV_PWD, passwd)
			return True
	return False

def getVolimtvMailPass():
	if os.path.isfile(VOLIMTV_UID):
		volimtv_uid = fread(VOLIMTV_UID)
		if os.path.isfile(VOLIMTV_PWD):
			volimtv_pwd = fread(VOLIMTV_PWD)
			return {'email':volimtv_uid, 'pass':volimtv_pwd}
	return False


def listVolimtv():
	url='http://www.volim.tv/rts-1'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("url\(http://volim.tv/images/design/watchlive.png\);' href='(.+?)'>(.+?)</a></li>").findall(link)

	return match

def playvolimtvurl(url):
	logindata = getVolimtvMailPass()
	if logindata == False:
		xbmcgui.Dialog().ok('Macedonia On Demand', 'Wrong username or password.', 'Register on http://volim.tv', 'And edit Settings on this page')
		return False
	loginurl='http://volim.tv/includes/ajax/login.php'

	pDialog = xbmcgui.DialogProgress()
	pDialog.create('volim.tv', 'Initializing')

	pDialog.update(30, 'Verifying userid and password')
	req = urllib2.Request(loginurl)
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	req.add_data(urllib.urlencode(logindata))
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	if link.find('location.reload();') == -1:
		pDialog.close()
		xbmcgui.Dialog().ok('Macedonia On Demand', 'Wrong username or password.', 'Register on http://volim.tv', 'And edit Settings on this page')
		return False
	cookiestr = response.info().get('set-cookie')

	pDialog.update(50, 'Fetching video stream')

	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	req.add_header('Accept', str_accept)
	req.add_header('Cookie', cookiestr)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	match=re.compile("ipadUrl: '(.+?)'").findall(link)

	if match == []:
		match = re.compile('"application/x-mpegurl".*?src="(.+?)"').findall(link)

	if match != []:
		stream_url = match[0]
		if stream_url[0:7] != 'http://':
			stream_url = 'http://edge3.volim.tv/live/'+stream_url
		pDialog.update(90, 'Playing')
		playurl(stream_url)
	pDialog.close()
	return True

# netraja methods

def listNetrajaCategories():
	url='http://www.netraja.net'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	start = link.find('TV KANALI</a>')
	end = link.find('</ul>', start)
	match=re.compile("<a href='(.+?)'>(.+?)</a>").findall(link[start:end])

	return match

def listNetrajaTvs(url):
	category = url.split('/')[-1]
	url = 'http://www.netraja.net/feeds/posts/summary/-/'+category+'?start-index=1&max-results=200&alt=json'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	data = json.load(response)
	response.close()
	if data.get('feed'):
		t=data['feed']
		if t.get('entry'):
			return t['entry']

	return {}

def playNetrajaStream(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Netraja', 'Initializing')
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(50, 'Finding stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	start = link.find("<div class='post-body entry-content'")
	end = link.find("<div style='clear: both;'></div>", start)

	stream=serbiaplussearchurl(link[start:end])

	if stream == '':
		if link[start:end].find("www.youtube.com/embed/") != -1:
			match=re.compile('www.youtube.com/embed/(.+?)"').findall(link[start:end])
			if match != []:
				stream='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+match[0]

	if stream != '':
		if stream.__contains__('youtube.com'):
			stream = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+stream.split('=')[-1].strip()

		pDialog.update(80, 'Playing')
		playurl(stream)

	pDialog.close()
	return True

# rts methods

def playrtsvideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('RTS', 'Initializing')
	req = urllib2.Request('http://www.rts.rs'+url)
	req.add_header('User-Agent', user_agent)
	pDialog.update(30, 'Finding stream')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	box = re.compile('<div class=\'boxFull\'>.*?<box box-left (.+?) box>').findall(link)
	if box == []:
		pDialog.close()
		return False

	url = 'http://www.rts.rs/boxes/boxBox.jsp?boxId='+box[0]
	content = readurl(url)
	pDialog.update(60, 'Finding stream')
	match = re.compile('src="(.+?)"').findall(content)

	stream = ''
	if match[0].__contains__('youtube'):
		stream = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+match[0].split('/')[-1].split('?')[0]

	if stream != '':
		pDialog.update(80, 'Playing')
		playurl(stream)
		pDialog.close()
		return True

	pDialog.close()
	return False

# prvatv methods

def listPrvaTvCategories():
	url = 'http://www.prva.rs/web-tv.html'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	link = link.replace('\n', '').replace('\r', '').replace('<span class=" ">', '').replace('</span>', '')

	start = link.find('<div class="horizontalSubNavigation fix">')
	end = link.find('</div>', start)

	match = re.compile('<a href="(.+?)".+?>(.+?)</a>').findall(link[start:end])
	return match

def listPrvaTvSeries_old(url):
	req = urllib2.Request('http://www.prva.rs'+url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	link = link.replace('\n', '').replace('\r', '').replace('<span class=" ">', '').replace('</span>', '')

	start = link.find('<li class="   depth3 first">')
	if start == -1:
		start = link.find('div id="topFullDepth3"')

	end = link.find('</div>', start)

	match = re.compile('<a href="(.+?)".+?>(.+?)</a>').findall(link[start:end])
	return match

def listPrvaTvSeries(url):
	req = urllib2.Request('http://www.prva.rs'+url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	link = link.replace('\n', '').replace('\r', '').replace('<span class=" ">', '').replace('</span>', '')

	start = link.find('div class="primary-content"')

	match = re.compile('<div class="children-box hero-item red">.+?<img src="(.+?)".+?>.+?<h3><a href="(.+?)">(.+?)</a>').findall(link[start:])
	return match

def listPrvaTvEpisodes(url):
	req = urllib2.Request('http://www.prva.rs'+url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	link = link.replace('\n', '').replace('\r', '').replace('<span class=" ">', '').replace('</span>', '')

	start = link.find('class="mediaTitle"')

	match = re.compile('<a class="mediumThumb fix" href="(.+?)" title="(.+?)">.+?<img src="(.+?)"').findall(link[start:])
	return match

def listPrvaTvMode2frontvideos(baseurl):
	req = urllib2.Request(baseurl)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	link = link.replace('\n', '').replace('\r', '')
	match = re.compile('<a class="largeThumb fix" href="(.+?)" title="(.+?)">.+?<img src="(.+?)"').findall(link)

	start = link.find('<li class="centralLi">')
	end = link.find('</ul>', start)
	activestart = link.find('<li class="active">', start)

	nextpagematch = re.compile('<a href="(.+?)">').findall(link, activestart, end)
	nextpage = ''
	if nextpagematch != []:
		nextpage = nextpagematch[0]

	return [match, nextpage]

def listPrvaTvMode2videos(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()

	link = link.replace('\n', '').replace('\r', '')
	start = link.find('<div class="mediaListVideo1">')
	if start == -1:
		start = 0;
	match = re.compile('<div class="mediaHolder ajaxMediaElements">.+?<a class=".*?" href="(.+?)" title="(.+?)" rel=".+?" name=".+?">.+?<div class="centerHVGalleryML">.+?<img src="(.+?)"').findall(link, start)

	return match

def prvatv_playvideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('PrvaTv', 'Initializing')
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	pDialog.update(50, 'Fetching video stream')
	link = response.read()
	response.close()

	start = link.find('class="mediaDescription"')

	titlematch=re.compile("title: '(.+?)'").findall(link[start:])
	videourlmatch=re.compile('src: "(.+?)"').findall(link[start:])

	if titlematch != []:
		name = titlematch[0]

	if videourlmatch == []:
		return False

	videourl=videourlmatch[0]
	if videourl[0] == '/':
		videourl='http://'+url.split('/')[2]+videourl

	pDialog.update(80, 'Playing')
	playurl(videourl)
	pDialog.close()
	return True

# TVBOX methods

def listtvboxchannels():
	req = urllib2.Request('http://tvboxuzivo.blogspot.com')
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link = response.read()
	response.read()

	match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(link)

	return match

# NET-TV methods

def listnettvchannels():
	req = urllib2.Request('http://net-tv.wix.com/ulaz')
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	data = response.read()
	response.close()

	start = data.find('var publicModel =')
	if start == -1:
		return []

	start = start + 17
	end = data.find(';', start)
	if end == -1:
		return []

	j = json.loads(data[start:end])
	return j

def nettv_playvideo(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)
		data = response.read()
		response.close()
	except:
		return False

	match = re.compile('"url":"(.+?)",').findall(data)
	if match == []:
		return False

	streamurl = 'http://net-tv.wix.com.usrfiles.com/'+match[0]
	return playGenericChannel(streamurl)

# VESTI.MK methods

def listvestimkvideos(pagenr):
	req = urllib2.Request('http://vesti.mk/videos/news?page='+pagenr)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	data = response.read()
	response.close()

	start = data.find('<div class=\'top-news-header\'>')
	if start == -1:
		return []

	match = re.compile("<li><div class='thumb-wrap'><a target='_blank' href='(.+?)' class='thumb-img'><div class='thumb-img-wrap'><img src=\"(.+?)\".+?<span class='thumb-source'(( title='(.+?)'|))>(.+?)</span>").findall(data, start)
	return match

def vestimk_playvideo(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('vesti.mk', 'reading')
	pDialog.update(30, 'Fetching video stream')
	data = readurl('http://vesti.mk'+url)
	data = data.replace('\n', '').replace('\r', '')
	match1 = re.compile('<div class="topbar-close">.*?<a href="(.+?)" ').findall(data)
	if match1 == []:
		return False
	print "Reading "+match1[0]
	pDialog.update(60, 'Fetching video stream')
	data = readurl(match1[0])

	ogv = re.compile('<source src="(.+?)" type="video/ogg"').findall(data)
	if ogv != []:
		host = re.compile("http://(.+?)/").findall(match1[0])
		if host == []:
			return False
		playurl("http://"+host[0]+"/"+ogv[0])
		pDialog.close()
		return True

	yt = re.compile('youtube.com/(embed/|watch\?v=)(.+?)( |"|\'|\?)').findall(data)
	if yt != []:
		pDialog.update(90, 'Playing video')
		print "playing youtube "+yt[0][1]
		playurl('plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+yt[0][1])
		pDialog.close()

	dm = re.compile('dailymotion.com/embed/video/(.+?)( |"|\'|\?)').findall(data)
	if dm != []:
		pDialog.update(90, 'Playing video')
		print "playing dailymotion "+dm[0][0]
		playurl('plugin://plugin.video.dailymotion_com/?url='+dm[0][0]+'&mode=playVideo')
		pDialog.close()

	return True

# general methods

def sendto_ga(page,url='',name=''):
	try:
		if page == None or page == '':
			page = 'Home Page'

		ga_link = 'http://www.google-analytics.com/collect?payload_data&v=1&tid=UA-40698392-3&cid='+__visitor__+'&t=appview&an=Macedonia%20On%20Demand&av='+__version__+'&cd='

		if page != None and page != '':
			ga_link += urllib.quote(page)

		if name != None and name != '':
			ga_link += '('+urllib.quote(name)+')'

		if url != None and url != '':
			ga_link += '('+urllib.quote(url)+')'

		req = urllib2.Request(ga_link)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	except:
		return True

def playurl(url):
	if name == '':
		guititle = 'Video'
	else:
		guititle = name

	if url[:4] == 'rtmp':
		url = url + ' timeout=10'

	listitem = xbmcgui.ListItem(guititle)
	play=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	play.clear()
	play.add(url, listitem)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(play)
	return True

def playGenericChannel(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Macedonia On Demand', 'Initializing')

	pDialog.update(50, 'Finding stream')
	try:
		content=readurl(url)
		stream=serbiaplussearchurl(content)
	except:
		return False

	if stream != '':
		pDialog.update(80, 'Playing')
		playurl(stream)
		return True
	else:
		pDialog.close()
		return False

def readurl(url):
	#if url==urllib.unquote(url):
	#	quoted_url=urllib.quote(url).replace('%3A', ':')
	#else:
	#	quoted_url=url
	quoted_url=url
	req = urllib2.Request(quoted_url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link



def PROCESS_PAGE(page,url='',name=''):

	sendto_ga(page,url,name)

	if page == None:
		addDir('Телевизија', 'tv_front', '', '')
		addDir('Радио', 'liveradio_front', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "radio_front":
		addDir("Слушај во живо", "liveradio_front", '', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "liveradio_front":
		addDir('radiomk.com', 'liveradio_radiomk', '', '')
		addDir('off.net.mk', 'liveradio_offnet', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "liveradio_radiomk":
		listing = createRadiomkListing()
		for link, thumb, title in listing:
			addLink(title, link, 'radiomk_playstream', 'http://www.radiomk.com/live/'+thumb)
		xbmc.executebuiltin("Container.SetViewMode(500)")
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "radiomk_playstream":
		playRadiomkstream(url)

	elif page == "liveradio_offnet":
		listing = createOffnetRadioListing()
		for stream, freq, title in listing:
			addLink((freq+" "+title).strip(), 'rtmp://off.net.mk/radio app=radio pageUrl=http://off.net.mk swfUrl=http://off.net.mk/sites/all/libraries/jwplayer/player.swf live=true playpath='+stream+' timeout=3 swfVfy=true', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


	elif page == "tv_front":
		stations = []
		stations.append(["24 Вести", "24vesti_front", ''])
		stations.append(["НОВА ТВ", "novatv_front", ''])
		stations.append(["Сител", "sitel_front", ''])
		stations.append(["МРТ Play", "mrt_front", ''])
		stations.append(["HRT", "hrt_front", ''])
		stations.append(["РТС", "rts_front", ''])
		stations.append(["Prva Srpska TV", "prvatv_front", ''])
		stations.append(["Vesti.mk", "vestimk_front", ''])

		stations.append(["", "break", ''])
		stations.append(["Гледај во живо", "live_front", ''])

		for statname, statpage, fanart in stations:
			addDir(statname, statpage, '', '', fanart)

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))


	elif page == 'live_front':
		addDir('telekabel.com.mk', 'live_telekabelmk', '', '')
		addDir('zulu.mk', 'live_zulumk', '', '')
		addDir('мрт play', 'list_mrtlive', '', 'http://mrt.com.mk/sites/all/themes/mrt/logo.png')
		addDir('volim.tv', 'volimtv_front', '', 'http://www.volim.tv/images/banners/logo.png')
		addDir('serbiaplus (beta)', 'serbiaplus_front', '', '')
		addDir('netraja.net (beta)', 'netraja_front', '', 'http://3.bp.blogspot.com/-_z6ksp3rY6Q/U0HL30rMwaI/AAAAAAAADAs/_hSEFNwNZ_8/s1600/7.png')
		addDir('tvboxuzivo (beta)', 'tvboxuzivo_front', '', '')
		addDir('останати...', 'live_other', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'serbiaplus_front':
		listing = listSerbiaPlusTVs()
		for url, title in listing[1]:
			addLink(title.replace('&nbsp;', ''), listing[0]+url, 'playserbiaplus_stream', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'playserbiaplus_stream':
		playSerbiaPlusStream(url)

	elif page == 'volimtv_front':
		listing = listVolimtv()
		for url, title in listing:
			addLink(title, url, 'playvolimtv', '')
		addDir('', 'break', '', '')
		addDir('Settings', 'volimtv_settings', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'volimtv_settings':
		setVolimtvMailPass()

	elif page == 'playvolimtv':
		playvolimtvurl(url)

	elif page == 'netraja_front':
		listing = listNetrajaCategories()
		for url, name in listing:
			addDir(name, 'netraja_list_tvs', url, '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'netraja_list_tvs':
		listing = listNetrajaTvs(url)
		for item in listing:
			addLink(item['link'][-1]['title'].encode('ascii', 'ignore'), item['link'][-1]['href'], 'netraja_play_stream', item.values()[7].values()[0] )
		xbmc.executebuiltin("Container.SetViewMode(500)")
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'netraja_play_stream':
		playNetrajaStream(url)

	elif page == 'live_zulumk':
		listing = createZuluListing()
		#for station, thumb in match:
		#	print station, thumb
		for station, thumb in listing:
			addLink(station.split('/')[-1], station, 'playzulustream', 'http://on.net.mk/'+thumb)
		setView('files', 500)
		xbmc.executebuiltin("Container.SetViewMode(500)")

		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page=='playzulustream':
		playZuluStream(url)

	elif page == 'live_telekabelmk':
		listing = createTelekabelListing()
		for u, streamname in listing:
			if not u.startswith('mms'):
				addLink(streamname, u, 'playtelekabelstream', '')
			else:
				addLink('Радио '+streamname, u, '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page=='playtelekabelstream':
		playTelekabelStream(url)

	elif page == 'live_other':
		listing = createOtherListing()
		for i in range(len(listing)):
			addLink(listing[i][0], 'u'+str(i), 'play_live_other', listing[i][2])
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'play_live_other':
		nr = int(url[1:])
		listing = createOtherListing()
		item=listing[nr]
		playurl(item[1])

	elif page == '24vesti_front':
		addLink('Вести', '', '24vesti_vesti', '')
		addDir('Емисии', '24vesti_emisii', '', '')
		addDir('Видео содржина', '24vesti_videosodrzina', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == '24vesti_emisii':
		listing = create24VestiEmisiiListing(url)
		for u,thumb,title in listing:
			if title.__contains__('Вин Вин'):
				addLink(title, u, '24vesti_playvideo', thumb,'http://a1on.mk/wordpress/wp-content/uploads/2013/01/olivera-trajkovska.jpg')
			else:
				addLink(title, u, '24vesti_playvideo', thumb, thumb)
		if url == '' or url == None:
			addDir('Претходно', '24vesti_emisii', '1', '')
		else:
			urlpage = int(url)+1
			addDir('Претходно', '24vesti_emisii', str(urlpage), '')

		setView('movies', 500)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == '24vesti_videosodrzina':
		listing = create24VestiVideoSodrzina()
		for u,thumb,title1,title2 in listing:
			addLink(title2.strip(), u, '24vesti_playvideosodrzina', thumb)
		setView('files', 500)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page=='24vesti_vesti':
		play24VestiVesti()

	elif page=='24vesti_playvideo':
		play24VestiVideo(url)

	elif page=='24vesti_playvideosodrzina':
		play24VestiVideo(url)

	elif page == 'novatv_front':
		addDir('Македонија', 'novatv_makedonija', '', '')
		addDir('Еврозум', 'novatv_evrozum', '', '')
		addDir('Секуловска', 'novatv_sekulovska', '', '')
		addDir('Документ', 'novatv_dokument', '', '')
		addDir('Студио', 'novatv_studio', '', '')
		addDir('Актуел', 'novatv_aktuel', '', '')
		addDir('Глобус', 'novatv_globus', '', '')
		addDir('Култура', 'novatv_kultura', '', '')
		addDir('Занимливости', 'novatv_zanimlivosti', '', '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page=='novatv_playvideo':
		playNovatvVideo(url)

	elif page.__contains__('novatv_'):
		listing = createNovatvListing(page)

		if page == 'novatv_evrozum':
			fanart = 'http://novatv.mk/photos/u2.jpg'
		elif page == 'novatv_sekulovska':
			fanart = 'http://novatv.mk/photos/u4.jpg'
		elif page == 'novatv_dokument':
			fanart = 'http://novatv.mk/photos/u2.jpg'
		else:
			fanart = ''
		for u,thumb,title,description,date in listing:
			addLink(title+' '+date, u, 'novatv_playvideo', 'http://novatv.mk/'+thumb, fanart)
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "sitel_front":
		addDir('Видео', 'sitel_video', '', '')
		addLink('Дневник', '', 'sitel_dnevnik', 'http://sitel.com.mk/sites/all/themes/siteltv/images/video-dnevnik.jpg')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == "sitel_video":
		listing = createSitelVideoListing()
		for u, thumb, title in listing:
			addLink(title, u, 'playsitelvideo',thumb)
		setView('files', 500)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page=='playsitelvideo':
		playSitelVideo(url)

	elif page == 'sitel_dnevnik':
		playSitelDnevnik()

	elif page == "mrt_front":
		listing = createmrtfrontList()
		for url,channel in listing:
			addDir(channel, 'list_mrtchannel', url, '')
		addDir('ВО ЖИВО', 'list_mrtlive', '', '')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'list_mrtlive':
		listing = list_mrtlive()
		for url,title,thumb in listing:
			addLink(title, url, 'play_mrt_video', thumb)

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'list_mrtchannel':
		[listing, nextpage] = list_mrtchannel(url)

		for type,url,thumb,duration,title in listing:
			if type=="video":
				addLink(title, url, 'play_mrt_video', thumb, '', duration)
			elif type=="channel":
				addDir(">>  "+title, 'list_mrtchannel', url, thumb)

		if nextpage != '':
			addDir(">> Следна Страна", 'list_mrtchannel', nextpage.replace('&amp;', '&'), '')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'play_mrt_video':
		playmrtvideo(url)

	elif page == 'hrt_front':
		addLink('HRT1 Live', 'http://5323.live.streamtheworld.com/HTV1?streamtheworld_user=1&nobuf=1361039552824', '', 'http://upload.wikimedia.org/wikipedia/commons/1/1f/HRT1_Logo_aktuell.jpg')
		addLink('HRT4 Live', 'http://4623.live.streamtheworld.com/HRT4?streamtheworld_user=1&nobuf=1384296611008', '', 'http://images3.wikia.nocookie.net/__cb20121221162236/logopedia/images/d/dc/HRT4.png')
		addDir('', 'break', '', '')
		listing = createHRTSeriesListing()
		for link, title in listing:
			addDir(title, 'list_hrt_episodes', link, '')
		setView('files', 500)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'list_hrt_episodes':
		listing = listHRTEpisodes(url)
		for title,link in listing:
			addLink(title, link, 'play_hrt_video', '')
		setView('files', 500)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'play_hrt_video':
		playHRTVideo(url)

	elif page == 'rts_front':

		addLink('РТС Уживо', 'http://rts.videostreaming.rs/rts', '', 'http://www.rts.rs/upload/storyBoxImageData/2008/07/19/18865/rts%20logo.bmp')
		addLink('Радио Београд 1', 'http://rts.ipradio.rs:8002', '', '')
		addLink('Радио Београд 2/ Радио Београд 3', 'http://rts.ipradio.rs:8004', '', '')
		addLink('Радио Београд 202', 'http://rts.ipradio.rs:8006', '', '')
		addLink('Радио Београд стереорама (Викендом)', 'http://rts.ipradio.rs:8008', '', '')
		addDir('', 'break', '', '')

		content=readurl('http://www.rts.rs/page/podcast/ci.html')
		start=0
		while True:
			start=content.find('class="section"', start)
			if start != -1:
				delimstart=content.find('<h2>', start)
				delimend=content.find('</h2>', start)
				station=content[delimstart+4:delimend]
				next=content.find('class="section"', start+20)
				if next==-1:
					next=content.find('<div class="comment">', start+4)
				match=re.compile('<a href="(.+?)".*?>(.+?)</a>').findall(content[start:next])
				for url, title in match:
					addDir(station+"   "+title, 'list_rts_episodes', url, '')
				start=start+4
			else:
				break

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'list_rts_episodes':
		art=''
		content=readurl('http://www.rts.rs'+url)
		content=content.replace('\n', '').replace('\r', '')
		metadata=re.compile('<meta name="description" content="(.+?)"').findall(content)
		if metadata != []:
			image=re.compile('src=&#034;(.+?)&#034;').findall(metadata[0])
			if image != []:
				art=image[0]
				if art[0] == '/':
					art='http://www.rts.rs'+art

			start=0
			while True:
				start = content.find('<div class="element ', start)
				if start == -1:
					break;
				next = content.find('<div class="element "', start+20)
				if next == -1:
					next = len(content)

				thumb=re.compile('<img class="img-responsive" src="(.+?)"').findall(content, start, next)
				title=re.compile('title="(.+?)"').findall(content, start, next)
				uptitle=re.compile('<p class="lead">(.+?)</p>').findall(content, start, next)
				startfiles=content.find('<div class="files">', start, next)
				videopage=re.compile('<h3><a href="(.+?)">').findall(content, start, next)
				files = []

				if startfiles != -1:
					if next != -1:
						files=re.compile('<a href="(.+?)"').findall(content, startfiles, next)
					else:
						files=re.compile('<a href="(.+?)"').findall(content, startfiles)

				if title != []:
					titlestr = title[0]
				else:
					titlestr = ""

				if thumb != []:
					thumbstr = thumb[0]
				else:
					thumbstr = ""

				if uptitle != []:
					uptitlestr=uptitle[0]
				else:
					uptitlestr=""

				if files != []:
					addLink(titlestr.strip()+' - '+uptitlestr.strip().replace('&nbsp;', ' '), 'http://www.rts.rs'+files[1], '', 'http://www.rts.rs'+thumbstr, art)
				else:
					addLink(titlestr.strip()+' - '+uptitlestr.strip().replace('&nbsp;', ' '), videopage[0], 'rts_play_video', 'http://www.rts.rs'+thumbstr, art)

				start=start+16

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'rts_play_video':
		playrtsvideo(url)

	elif page == 'prvatv_front':
		categories = listPrvaTvCategories()
		for url, name in categories:
			addDir(name.strip(), 'prvatv_listseries', url, '')

		addDir('Tvoje Lice Zvuci Poznato', 'prvatv_mode2_front', 'http://tlzp.prva.rs/video.html',  'http://www.prva.rs/sw4i/thumbnail/tlzp.prva.rs.jpg?thumbId=399640&fileSize=82820&lastModified=1413815770000&contentType=image/jpeg')
		addDir('Ples sa zvezdama', 'prvatv_mode2_front', 'http://plessazvezdama.prva.rs/video.html', 'http://www.prva.rs/sw4i/thumbnail/ples.jpg?thumbId=275072&fileSize=102847&lastModified=1396024641000&contentType=image/jpeg')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'prvatv_listseries':
		series = listPrvaTvSeries(url)
		for thumb, url, name in series:
			if thumb[0] == '/':
				thumb='http://www.prva.rs'+thumb
			if name.strip()[0:5] == 'Tvoje' or name.strip()[0:4] == "Ples":
				continue

			else:
				addDir(name.strip(), 'prvatv_listepisodes', url, thumb)

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'prvatv_listepisodes':
		episodes = listPrvaTvEpisodes(url)
		for url, name, thumb in episodes:
			addLink(name.strip(), 'http://www.prva.rs'+url, 'prvatv_playvideo', 'http://www.prva.rs'+thumb.replace(' ', '%20'))

		xbmc.executebuiltin("Container.SetViewMode(500)")
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'prvatv_mode2_front':
		baseurl = 'http://'+url.split('/')[2]
		listing = listPrvaTvMode2frontvideos(url)
		for nexturl, title, thumb in listing[0]:
			addDir('>> '+title, 'prvatv_list_mode2_videos', baseurl+nexturl, baseurl+thumb)

		if listing[1] != '':
			addDir('>> Next Page', 'prvatv_mode2_front', baseurl+listing[1], '')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'prvatv_list_mode2_videos':
		baseurl='http://'+url.split('/')[2]
		listing = listPrvaTvMode2videos(url)

		for nexturl, title, thumb in listing:
			addLink(title, baseurl+nexturl, 'prvatv_playvideo', baseurl+thumb)

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'prvatv_playvideo':
		prvatv_playvideo(url)

	elif page == 'tvboxuzivo_front':
		listing = listtvboxchannels()
		for url, title in listing:
			addLink(title, url, 'tvboxuzivo_playvideo', '')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'tvboxuzivo_playvideo':
		playGenericChannel(url)

	elif page == 'nettv_front':
		listing = listnettvchannels()
		for tv in listing['pageList']['pages']:
			addLink(tv['title'].encode('ascii', 'ignore'), tv['urls'][0], 'nettv_playvideo', '')

		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'nettv_playvideo':
		nettv_playvideo(url)

	elif page == 'vestimk_front':
		if url == '' or url == None:
			url = '1'
		listing = listvestimkvideos(url)
		for link, thumb, title_enc1, title_enc2, title_long, title_short in listing:
			title = title_long
			if title_long == '':
				title = title_short
			addLink(title, link, 'vestimk_playvideo', thumb)
		if url != '10':
			urlpage = int(url)+1
			addDir(' >> Претходно', 'vestimk_front', str(urlpage), '')
		setView()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	elif page == 'vestimk_playvideo':
		vestimk_playvideo(url)


def addLink(name,url,page,iconimage,fanart='',duration='00:00', published='0000-00-00', description=''):
        ok=True
	if page != '':
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&page="+str(page)+"&name="+urllib.quote_plus(name)
	else:
		u=url
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if duration != '00:00':
		liz.setInfo('video', { 'Duration':duration })

	if published != '0000-00-00':
		liz.setInfo('video', {'Aired':published})

	if description != '':
		liz.setInfo('video', { 'plot':description })

	#liz.setProperty('IsPlayable', 'false')
	if fanart!='':
		liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,page,url,iconimage,fanart=''):
        u=sys.argv[0]+"?page="+urllib.quote_plus(page)+"&url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	if fanart!='':
		liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None
name=None
page=None

#for i in range(0,4):
#	try:
#		print "arg["+str(i)+"]"+str(sys.argv[i])
#	except:
#		pass

# Inspired by xbmc-iplayer2

old_version = ''

if os.path.isfile(VERSION_FILE):
	old_version = fread(VERSION_FILE)

if old_version != __version__:
	result = True
	if result:
		fwrite(VERSION_FILE, __version__)
result = True

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass

try:
        name=urllib.unquote_plus(params["name"])
except:
        pass

try:
	page=urllib.unquote_plus(params["page"])
except:
        pass

if result:
	PROCESS_PAGE(page, url, name)

