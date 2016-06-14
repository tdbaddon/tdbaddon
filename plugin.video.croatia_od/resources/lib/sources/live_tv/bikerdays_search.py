# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.modules import m3u_parser,parental,control
from resources.lib.modules.log_utils import log
import sys,os,xbmc


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'bikerdays_search'
        self.name = 'Bikerdays TV Lista (pretraga)'
        self.icon = 'bikerdays.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self,url = 'http://pastebin.com/raw.php?i=jmseyhvw'):
		self.base = 'http://pastebin.com/raw.php?i=jmseyhvw'
		self.url = url

	def channels(self):
		out = []
		keyboard = xbmc.Keyboard('', 'Pretraži TV kanale', False)
		keyboard.doModal()
		if keyboard.isConfirmed():
			query = keyboard.getText()
			tracks = m3u_parser.parseM3U(self.url)
			tracks = self.search_m3u(query,tracks)
			for track in tracks:
				title=track.title

				url=track.path
				img = icon_path(info().icon)
				out.append((url,title,img))
		return out

	def resolve(self,url):
		return url
	


	def search_m3u(self,query,shows):
	    words=query.lower().split(' ')
	    br=0
	    pom=0
	    out=[]
	    for show in shows:
	    	try:
	    		if 'ODRASLE' in show.title:
	    			if not parental.Parental().isVisible():
	    				break
	    	except:
	    		pass

	        for word in words:
	            try:
	                if word in show.title.lower():
	                    br+=1
	            except:
	                pass

	        if br>0:
	            tup=(br,pom)
	            out.append(tup)
	        br=0
	        pom+=1
	    from operator import itemgetter
	    out=sorted(out,key=lambda x: x[0], reverse=True)
	    outt=[]
	    for i in range(len(out)):
	    	index = out[i][1]
	    	track = shows[index]
	        outt.append(track)

	    return outt
