# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of p2p-streams addon

Arenavision.in

"""
import sys,os,requests
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from peertopeerutils.webutils import *
from peertopeerutils.pluginxbmc import *
from peertopeerutils.directoryhandle import *
import acestream as ace
import sopcast as sop
from cleaner import *

base_url = "http://www.arenavision.in"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: arenavision_menu()
	elif parserfunction == "arenavision_streams": arenavision_streams(name,url)
	elif parserfunction == "arenavision_schedule": arenavision_schedule(url)
	elif parserfunction == "arenavision_chooser": arenavision_chooser(url)
	


def arenavision_menu():
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(base_url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('leaf"><a href="(.+?)">(.+?)</a').findall(source)
		for link, nome in match:
			if "agenda" in nome.lower():
				addDir("[B][COLOR red]Agenda/Schedule[/COLOR][/B]",base_url+link,401,os.path.join(current_dir,"icon.png"),1,True,parser="arenavision",parserfunction="arenavision_schedule")
			elif "#" in nome.lower() or "av" in nome.lower() or "arenavision" in nome.lower():
				addDir(nome,base_url+link,401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision",parserfunction="arenavision_streams")
			else: pass


def arenavision_streams(name,url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('sop://(.+?)"').findall(source)
		if match: sop.sopstreams(name,os.path.join(current_dir,"icon.png"),"sop://" + match[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: ace.acestreams(name,os.path.join(current_dir,"icon.png"),match[0])
			else: xbmcgui.Dialog().ok(translate(40000),translate(40022))

def arenavision_schedule(url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.findall('Bruselas(.*?)</footer>', source, re.DOTALL)
		for event in match:
			eventmatch = re.compile('(\d+)/(\d+)/(\d+) (.+?):(.+?) CET (.+?)<').findall(event)
			for dia,mes,year,hour,minute,evento in eventmatch:
				try:
					import datetime
					from peertopeerutils import pytzimp
					d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(mes), int(dia), hour=int(hour), minute=int(minute)))
					timezona= settings.getSetting('timezone_new')
					my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
					convertido=d.astimezone(my_location)
					fmt = "%d-%m-%y %H:%M"
					time=convertido.strftime(fmt)
				except:
					time='N/A'
				event_array = evento.split('/')
				event_name = ''
				event_channels = []
				i = 1
				for parc in event_array:
					if 'AV' in parc:
						event_channels.append(parc)
				try: addDir('[B][COLOR red]' + time + '[/B][/COLOR] ' + removeNonAscii(clean(event_array[0])),str(event_channels),401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision",parserfunction="arenavision_chooser")
				except:pass

	
	
def arenavision_chooser(url):
	dictionary = eval(url)
	index = xbmcgui.Dialog().select("On...", dictionary)
	if index > -1:
		headers = {
			"Cookie" : "beget=begetok; has_js=1;"
		}
		try:
			source = requests.get(base_url,headers=headers).text
		except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
		if source:
			match = re.compile('leaf"><a href="(.+?)">(.+?)</a').findall(source)
			for link,name in match:
				if (dictionary[index] == name) or (dictionary[index] == name.replace('AV','#')) or (dictionary[index] == name.replace('#','AV')) or (dictionary[index] == name.replace('ArenaVision ','AV')):
					arenavision_streams(name,base_url+link)
					
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
		
