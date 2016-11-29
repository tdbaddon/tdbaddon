"""
    Copyright (C) 2016 ECHO Coder

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
#Imports
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import time
import base64
import requests
import re

#Default veriables
AddonTitle     = "[COLOR ghostwhite][B]Porn.[/COLOR][COLOR red]com[/B][/COLOR]"
addon_id       = 'plugin.video.porncom'
dialog         = xbmcgui.Dialog()
ADDON          = xbmcaddon.Addon(id=addon_id)
HOME           = xbmc.translatePath('special://home/')
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/next.png'))
search_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
twitter_icon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/twitter.png'))
pc_icon        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pc.png'))

PARENTAL_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'controls.txt'))
TERMS          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'disclaimer.txt'))
I_AGREE        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'agreed.txt'))
PARENTAL_FOLDER= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))

def MAIN_MENU():

	if not os.path.exists(I_AGREE): 
		f = open(TERMS,mode='r'); msg = f.read(); f.close()
		TextBoxes("%s" % msg)
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR white]Do you agree to the terms and conditions of this addon?[/COLOR]','',yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			if not os.path.exists(PARENTAL_FOLDER):
				os.makedirs(PARENTAL_FOLDER)
			open(I_AGREE, 'w')
		else:
			sys.exit(0)

	if not os.path.exists(PARENTAL_FOLDER):
		choice = xbmcgui.Dialog().yesno(AddonTitle, "[COLOR white]We can see that this is your first time using the addon. Would you like to enable the parental controls now?[/COLOR]","" ,yeslabel='[B][COLOR red]NO[/COLOR][/B]',nolabel='[B][COLOR lime]YES[/COLOR][/B]')
		if choice == 0:
			PARENTAL_CONTROLS_PIN()
		else:
			os.makedirs(PARENTAL_FOLDER)

	elif os.path.exists(PARENTAL_FILE):
		vq = _get_keyboard( heading="Please Enter Your Password" )
		if ( not vq ): 
			dialog.ok(AddonTitle,"Sorry, no password was entered.")
			sys.exit(0)
		pass_one = vq

		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				if not password == pass_one:
					if not current_pin == pass_one:
						dialog.ok(AddonTitle,"Sorry, the password you entered was incorrect.")
						sys.exit(0)

	addDir("[COLOR red][B]SEARCH[/B][/COLOR]","url",2,search_icon,fanart,'')

	result = requests.get('http://www.porn.com/categories')
	match = re.compile('<div class="main"><h1>Featured Categories</h1>(.+?)<h2>All Categories</h2>',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<a class="thum(.+?)data-id="',re.DOTALL).findall(string)
	for item in match2:
		url=re.compile('bs" href="(.+?)"').findall(item)[0]
		title=re.compile('title="(.+?)"').findall(item)[0]
		icon_cat=re.compile('<img src="(.+?)"').findall(item)[0]
		title = title.replace("porn",'')
		name = "[COLOR ghostwhite][B]" + title + "[/COLOR][/B]"
		name = CLEANUP(name)
		url = 'http://porn.com' + url
		addDir(name,url,1,icon_cat,fanart,'')

	addItem("[COLOR red][B]Twitter Support: @echo_coding[/B][/COLOR]","url",999,twitter_icon,fanart,'')
	if not os.path.exists(PARENTAL_FILE):
		addDir("[COLOR orange][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')
	else:
		addDir("[COLOR orange][B]PARENTAL CONTROLS - [COLOR lime]ON[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')

def GET_CONTENT(url):

	namelist=[]
	urllist=[]
	iconlist=[]
	ratinglist=[]

	result = requests.get(url)
	match = re.compile('<ul class="listThumbs">(.+?)<span class="numbers">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<a(.+?)class="icon-thumbs-up">',re.DOTALL).findall(string)
	for item in match2:
		title=re.compile('class="title">(.+?)<').findall(item)[0]
		url=re.compile('href="(.+?)"').findall(item)[0]
		iconimage=re.compile('src="(.+?)"').findall(item)[0]
		url = "http://porn.com" + str(url)
		try:
			rating=re.compile('class="rating">(.+?)<i').findall(item)[0]
			rating = rating.replace('% ','')
			rating = int(rating)
		except:
			rating = 0
		name = CLEANUP(title)
		if '<span class="hd">' in item:
			name = '[COLOR white] - [/COLOR][COLOR deepskyblue][B]HD[/B][/COLOR] - [COLOR white]' + name + '[/COLOR]'
		else:
			name = '[COLOR white] - [/COLOR][COLOR orange][B]SD[/B][/COLOR] - [COLOR white]' + name + '[/COLOR]'

		namelist.append(name)   
		urllist.append(url)		
		iconlist.append(iconimage)
		ratinglist.append(rating)
		combinedlists = list(zip(ratinglist,namelist,urllist,iconlist))

	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for rating,name,url,iconimage in tup:
		addItem('[COLOR red][B]' + str(rating) + '%[/B][/COLOR]' + name,url,3,iconimage,iconimage,'')

	try:
		np=re.compile('<link rel="next" href="(.+?)"').findall(result.content)[0]
		url = "http://porn.com" + str(np) 
		addDir('[COLOR red]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')       
	except:pass

	xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(' ','').capitalize()
        if len(string)>1:
            url = "http://www.pornhd.com/search?search=" + string.lower()
            GET_CONTENT(url)
        else: quit()

def PLAY_URL(name,url,iconimage):

	try:
		result = requests.get(url)
		match = re.compile('html>(.+?)</html>',re.DOTALL).findall(result.content)
		a = str(match)
		match = a.replace('\\','')
		
		if "dlOptions" in str(match):

			choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Watch Video[/B][/COLOR]','[COLOR deepskyblue][B]Download Video[/B][/COLOR]'])
		
			if choice == 0:
				try:
					url1 = re.compile('id:"1080p",url:"(.+?)"').findall(match)[0]
				except: url1 = "null"
				try:
					url2 = re.compile('id:"720p",url:"(.+?)"').findall(match)[0]
				except:url2 = "null"
				try:
					url3 = re.compile('id:"480p",url:"(.+?)"').findall(match)[0]
				except:url3 = "null"
				try:
					url4 = re.compile('id:"360p",url:"(.+?)"').findall(match)[0]
				except: url4 = "null"
				try:
					url5 = re.compile('id:"240p",url:"(.+?)"').findall(match)[0]
				except: url5 = "null"

				if "http" in url1:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Watch in 1080p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 720p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 480p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 360p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 240p[/B][/COLOR]'])
					if choice == 0: url_play = url1
					elif choice == 1: url_play = url2
					elif choice == 2: url_play = url3
					elif choice == 3: url_play = url4
					elif choice == 4: url_play = url5
				elif "http" in url2:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Watch in 720p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 480p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 360p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 240p[/B][/COLOR]'])
					if choice == 0: url_play = url2
					elif choice == 1: url_play = url3
					elif choice == 2: url_play = url4
					elif choice == 3: url_play = url5
				elif "http" in url3:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Watch in 480p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 360p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 240p[/B][/COLOR]'])
					if choice == 0: url_play = url3
					elif choice == 1: url_play = url4
					elif choice == 2: url_play = url5
				elif "http" in url4:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Watch in 360p[/B][/COLOR]','[COLOR deepskyblue][B]Watch in 240p[/B][/COLOR]'])
					if choice == 0: url_play = url4
					elif choice == 1: url_play = url5
				elif "http" in url5:
					url_play = url5
				liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
				xbmc.Player ().play(url_play, liz, False)
		
			elif choice == 1:

				try:
					size1 = re.compile('MP4 1080p<span class="hd"></span><span class="l1">(.+?)</span></a><a href=".+?"').findall(match)[0]
					url1 = re.compile('MP4 1080p<span class="hd"></span><span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
				except: 
					size1 = "null"
					url1  = "null"
				try:
					size2 = re.compile('MP4 720p<span class="hd"></span><span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
					url2 = re.compile('MP4 720p<span class="hd"></span><span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
				except: 
					size2 = "null"
					url2  = "null"
				try:
					size3 = re.compile('MP4 480p.+?<span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
					url3 = re.compile('MP4 480p.+?<span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
				except: 
					size3 = "null"
					url3  = "null"
				try:
					size4 = re.compile('MP4 360p.+?<span class="l1">(.+?)</span></a><a href=".+?.mp4"').findall(match)[0]
					url4 = re.compile('MP4 360p.+?<span class="l1">.+?</span></a><a href="(.+?)"').findall(match)[0]
				except: 
					size4 = "null"
					url4  = "null"

				if "download" in url1:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Download 1080p ' + str(size1) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 720p ' + str(size2) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 480p ' + str(size3) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 360p ' + str(size4) + '[/B][/COLOR]'])
					if choice == 0: url_play = url1
					elif choice == 1: url_play = url2
					elif choice == 2: url_play = url3
					elif choice == 3: url_play = url4
				elif "download" in url2:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Download 720p ' + str(size2) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 480p ' + str(size3) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 360p ' + str(size4) + '[/B][/COLOR]'])
					if choice == 0: url_play = url2
					elif choice == 1: url_play = url3
					elif choice == 2: url_play = url4
				elif "download" in url3:
					choice = dialog.select("[COLOR red][B]Please select an option[/B][/COLOR]", ['[COLOR deepskyblue][B]Download 480p ' + str(size3) + '[/B][/COLOR]','[COLOR deepskyblue][B]Download 360p ' + str(size4) + '[/B][/COLOR]'])
					if choice == 0: url_play = url3
					elif choice == 1: url_play = url4
				elif "download" in url4:
					url_play = url4
				
				import downloader
				
				_in = 'http://www.porn.com/' + url_play
				_out = dialog.browse(3, AddonTitle, 'files', '', False, False, HOME)
				name = name.replace(' ','_')
				a = name.split('[COLOR_white]')[2]
				name = a.replace('[/COLOR]','')
				_out = _out + name + '.mp4'
				downloader.download(_in,_out,dp=None)
			
			else: quit()
	except:
		dialog.ok(AddonTitle, 'There was an error fetching the video. Please try a differnt video.')
		sys.exit(0)

def PARENTAL_CONTROLS():

	found = 0
	if not os.path.exists(PARENTAL_FILE):
		found = 1
		addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR white][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')
	else:
		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				found = 1
				addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR lime]ON[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR white][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR lime][B]Change Password[/B][/COLOR]","url",12,icon,fanart,'')
				addItem("[COLOR red][B]Disable Password[/B][/COLOR]","url",13,icon,fanart,'')

	if found == 0:
		addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR white][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')

def PARENTAL_CONTROLS_PIN():

	vq = _get_keyboard( heading="Please Set Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		sys.exit(0)
	pass_one = vq

	vq = _get_keyboard( heading="Please Confirm Your Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		sys.exit(0)
	pass_two = vq
		
	if not os.path.exists(PARENTAL_FILE):
		if not os.path.exists(PARENTAL_FOLDER):
			os.makedirs(PARENTAL_FOLDER)
		open(PARENTAL_FILE, 'w')

		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			sys.exit(0)
	else:
		os.remove(PARENTAL_FILE)
		
		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			sys.exit(0)

def PARENTAL_CONTROLS_OFF():

	try:
		os.remove(PARENTAL_FILE)
		dialog.ok(AddonTitle,'Parental controls have been disabled.')
		xbmc.executebuiltin("Container.Refresh")
	except:
		dialog.ok(AddonTitle,'There was an error disabling the parental controls.')
		xbmc.executebuiltin("Container.Refresh")

def GET_LUCKY():

	import random
	lucky = random.randrange(10)
	
	dp = xbmcgui.DialogProgress()
	
	if lucky == 1:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]We are getting the moisturiser.[/B][/COLOR]','[B][COLOR azure]Do you have the wipes ready?[/B][/COLOR]' )
	elif lucky == 2:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]I am just taking off my pants.[/B][/COLOR]','[B][COLOR azure]Darn belt![/B][/COLOR]' )
	elif lucky == 3:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]Are the curtains closed?[/B][/COLOR]','[B][COLOR azure]Oh baby its cold outside![/B][/COLOR]' )
	elif lucky == 4:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]This is my fifth time today.[/B][/COLOR]','[B][COLOR azure]How about you?[/B][/COLOR]' )
	elif lucky == 5:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]Please no buffer, please no buffer![/B][/COLOR]')
	elif lucky == 6:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]I think I am going blind :-/[/B][/COLOR]','[B][COLOR azure]Oh no, just something in my eye.[/B][/COLOR]' )
	elif lucky == 7:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]Did I turn the oven off?[/B][/COLOR]','[B][COLOR azure]It can wait![/B][/COLOR]' )
	elif lucky == 8:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]Your video is coming. Are you?[/B][/COLOR]','[B][COLOR azure]Do you get it?[/B][/COLOR]' )
	elif lucky == 9:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]Kodi does not save your browsing history :-D[/B][/COLOR]','[B][COLOR azure]Thats lucky isnt it :-)[/B][/COLOR]' )
	else:
		dp.create(AddonTitle,"[B][COLOR red]Please wait.[/B][/COLOR]",'[B][COLOR ghostwhite]There are more XXX addons by ECHO.[/B][/COLOR]','[B][COLOR azure]Just so you know.[/B][/COLOR]' )

	return dp

def CLEANUP(text):

	text = str(text)
	text = text.replace('\\r','')
	text = text.replace('\\n','')
	text = text.replace('\\t','')
	text = text.replace('\\','')
	text = text.replace('<br />','\n')
	text = text.replace('<hr />','')
	text = text.replace('&#039;',"'")
	text = text.replace('&quot;','"')
	text = text.replace('&rsquo;',"'")
	text = text.replace('&amp;',"&")

	return text

def TextBoxes(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('XNXX.com - Story') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

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

def addItem(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

params=get_params(); url=None; name=None; mode=None; site=None; description=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: mode=int(params["mode"])
except: pass
try: description=urllib.quote_plus(params["description"])
except: pass

if mode==None or url==None or len(url)<1: MAIN_MENU()
elif mode==1: GET_CONTENT(url)
elif mode==2: SEARCH()
elif mode==3: PLAY_URL(name,url,iconimage)
elif mode==11: PARENTAL_CONTROLS()
elif mode==12: PARENTAL_CONTROLS_PIN()
elif mode==13: PARENTAL_CONTROLS_OFF()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
