# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of p2p-streams addon

Livefootballvideo.com

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from peertopeerutils.webutils import *
from peertopeerutils.pluginxbmc import *
from peertopeerutils.directoryhandle import *
from peertopeerutils.timeutils import translate_months

base_url = 'http://livefootballvideo.com/streaming'


#<div class="team column"><img width="32" alt="Gimnasia La Plata" src="/images/teams/small/gimnasia-la-plata.png"><span>Gimnasia La Plata</span></div>
#<div class="versus column">vs.</div>
#<div class="team away column"><span>Nueva Chicago</span><img width="32" alt="Nueva Chicago" src="/images/teams/small/nueva-chicago.png"></div>
#<div class="live_btn column">
#<a class="online" href="http://livefootballvideo.com/streaming/argentina/primera-division/gimnasia-la-plata-vs-nueva-chicago">
#Online </a>


def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: livefootballvideo_events()
	elif parserfunction == 'sources': livefootballvideo_sources(url)

def livefootballvideo_events():
	try:
		source = get_page_source(base_url)
	except: source ="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('<a href=".+?" title=".+?">(.+?)</a>\n</div>\n.+?<span class="starttime time" rel=".+?">(.+?)</span>.+?<span class="startdate date".+?rel=".+?">(.+?)/span>.+?\n<div class="team column"><.+?<span>(.+?)</span></div>\n.+?\n.+?class=".+?"><span>(.+?)</span>.+?\n.+?\n<a class=".+?" href="(.+?)">\n(.+?) </a>').findall(source)
		for comp,timetmp,datetmp,home,away,url,live in match:
			mes_dia = re.compile(', (.+?) (.+?)<').findall(datetmp)
			for mes,dia in mes_dia:
				dia = re.findall('\d+', dia)
				month = translate_months(mes)
				hora_minuto = re.compile('(\d+):(\d+)').findall(timetmp)
				try:
                                        import datetime
					from peertopeerutils import pytzimp
					d = pytzimp.timezone(str(pytzimp.timezone('Atlantic/Azores'))).localize(datetime.datetime(2014, int(month), int(dia[0]), hour=int(hora_minuto[0][0]), minute=int(hora_minuto[0][1])))
					timezona= settings.getSetting('timezone_new')
                                        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                                        convertido=d.astimezone(my_location)
                                        fmt = "%d/%m %H:%M"
                                        time=convertido.strftime(fmt)
					
					if "Online" in live: time = '[B][COLOR green](Online)[/B][/COLOR]'
					else: time = '[B][COLOR orange]' + time + '[/B][/COLOR]'
					addDir(time + ' - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,401,os.path.join(addonpath,'resources','art','football.png'),len(match),True,parser='livefootballvideo',parserfunction='sources')
				except: addDir('[B][COLOR orange]' + timetmp + ' ' + datetmp + '[/B][/COLOR] - [B]('+comp+')[/B] ' + home + ' vs ' + away,url,401,os.path.join(addonpath,'resources','art','football.png'),len(match),True,parser='livefootballvideo',parserfunction='sources')


def livefootballvideo_sources(url):
	print url
	try:
		source = get_page_source(url)
	except: source = ""; xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile("<td align='left'>(.+?)</td>\n<td>(.+?)</td><td>(.+?)</td><td><a href='(.+?)'").findall(source)
		if match:
			i=0
			for name,language,quality,link in match:
				if 'sop://' in link:
					i += 1
					addDir("[B][COLOR orange][SopCast] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,2,os.path.join(addonpath,'resources','art','sopcast_logo.jpg'),len(match),False)
				elif 'acestream://' in link:
					i +=1
					addDir("[B][COLOR orange][Acestream] [/COLOR][/B]" + name + ' (' + language + ') ('+quality+')',link,1,os.path.join(addonpath,'resources','art','acelogofull.jpg'),len(match),False)
			if i == 0:
				xbmcgui.Dialog().ok(translate(40000),translate(40022))
				sys.exit(0)
		else:
			xbmcgui.Dialog().ok(translate(40000),translate(40022))
			sys.exit(0)

