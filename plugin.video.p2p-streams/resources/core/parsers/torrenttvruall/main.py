# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not it is not part of the p2p-streams addon

Torrent-tv.ru (All categories)

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

base_url = "http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: torrenttv()
	elif parserfunction == 'channels': torrenttv_play(name,url)
    
def torrenttv():
	dict_torrent = {}
	html_source = get_page_source(base_url)
	match = re.compile('#EXTINF:-1,(.+?)\n(.*)').findall(html_source)
	for title, acehash in match:
    		channel_name = re.compile('(.+?) \(').findall(title)
    		match_cat = re.compile('\((.+?)\)').findall(title)
    		for i in xrange(0,len(match_cat)):
    			if match_cat[i] == "Для взрослых" and settings.getSetting('hide_porn') == "true":
    				pass
    			elif match_cat[i] == "Ночной канал" and settings.getSetting('hide_porn') == "true":
                                pass
    			else:
                		if settings.getSetting('russian_translation') == "true": categorie = russiandictionary(match_cat[i])
                		else: categorie=match_cat[i]
                		if categorie not in dict_torrent.keys():
                			try:
            					dict_torrent[categorie] = [(channel_name[0],acehash)]
            				except: pass
            			else:
            				try:
            					dict_torrent[categorie].append((channel_name[0],acehash))
            				except: pass
	for categories in dict_torrent.keys():
		addDir(categories,str(dict_torrent),401,os.path.join(current_dir,"icon.png"),401,True,parser="torrenttvruall",parserfunction="channels")
		
def torrenttv_play(name,url):
	dict_torrent=eval(url)
	for channel in dict_torrent[name]:
		try: addDir(channel[0],channel[1],1,os.path.join(current_dir,"icon.png"),2,False)
		except:pass
		
def russiandictionary(string):
	if string == "Eng": return translate(40077)
	elif string == "Спорт": return translate(40078)
	elif string == "Новостные": return translate(40079)
	elif string == "Свадебный": return translate(40080)
	elif string == "Общие": return translate(40081)
	elif string == "Познавательные": return translate(40082)
	elif string == "СНГ": return translate(40083)
	elif string == "Мужские": return translate(40084)
	elif string == "Ukraine": return translate(40085)
 	elif string == "резерв": return translate(40086)
 	elif string == "Донецк": return translate(40087)
 	elif string == "Региональные": return translate(40088)
 	elif string == "Для взрослых": return translate(40089)
 	elif string == "TV21": return translate(40090)
 	elif string == "Украина": return translate(40091)
 	elif string == "Детские": return translate(40092)
 	elif string == "Фильмы": return translate(40093)
 	elif string == "Ночной канал": return translate(40094)
 	elif string == "Европа": return translate(40095)
 	elif string == "укр": return translate(40096)
 	elif string == "Музыка": return translate(40097)
 	elif string == "Религиозные": return translate(40098)
 	elif string == "Развлекательные": return translate(40099)
	elif string == "украина": return translate(40151)
	elif string == "Казахстан": return "Kazakstan"
 	else: return string
