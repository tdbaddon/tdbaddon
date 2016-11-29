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
import requests
import re

#Default veriables
AddonTitle     = "XNXX.com"
addon_id       = 'plugin.video.xnxxcom'
dialog         = xbmcgui.Dialog()
ADDON          = xbmcaddon.Addon(id=addon_id)
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/next.png'))
search_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
PARENTAL_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'controls.txt'))
TERMS          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'disclaimer.txt'))
I_AGREE        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'agreed.txt'))
PARENTAL_FOLDER= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
NEW_VIDS       = 'http://www.xnxx.com/new'
BEST_VIDS      = 'http://www.xnxx.com/best'
HOT_VIDS       = 'http://www.xnxx.com/hot'
HITS_VIDS      = 'http://www.xnxx.com/hits'
featured_url   = 'http://www.xnxx.com'

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
				
	addDir("[COLOR yellow][B]SEARCH[/B][/COLOR]","url",2,search_icon,fanart,'')
	addDir("[COLOR royalblue][B][I]FEATURED VIDEOS[/I][/B][/COLOR]",featured_url,1,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]NEW VIDEOS[/I][/B][/COLOR]",NEW_VIDS,1,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]HOT VIDEOS[/I][/B][/COLOR]",HOT_VIDS,1,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]BEST OF[/I][/B][/COLOR]",BEST_VIDS,1,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]TOP HITS[/I][/B][/COLOR]",HITS_VIDS,1,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]PICTURES[/I][/B][/COLOR]",featured_url,4,icon,fanart,'')
	addDir("[COLOR royalblue][B][I]STORIES[/I][/B][/COLOR]",featured_url,8,icon,fanart,'')

	result = requests.get('http://www.xnxx.com')
	
	match = re.compile('<div id="side-categories" class="mobile-hide">(.+?)<div id="content-ad-side" class="mobile-hide">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('{(.+?)}',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('label":"(.+?)"').findall(item)[0]
		url=re.compile('"url":".+?/(.+?)"').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.xnxx.com/" + url4
		name = "[COLOR blue][B]" + title + "[/B][/COLOR]"
		addDir(name,url,1,icon,fanart,'')

	addItem("[COLOR yellow][B]Twitter Support: @echo_coding[/B][/COLOR]","url",999,icon,fanart,'')
	if not os.path.exists(PARENTAL_FILE):
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",11,icon,fanart,'')
	else:
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR lime]ON[/COLOR][/B][/COLOR]","url",11,icon,fanart,'')	
def PICTURE_MENU():
	
	result = requests.get('http://multi.xnxx.com')
	
	match = re.compile('visible-md visible-sm " id="leftPanel">(.+?)<div class="row"><div  class="boxImg',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<a hre(.+?)/a>',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('f=".+?" />(.+?)<').findall(item)[0]
		url=re.compile('f="(.+?)" />.+?<').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://multi.xnxx.com" + url4
		name = "[COLOR blue][B]" + title + "[/B][/COLOR]"
		addDir(name,url,5,icon,fanart,'')

def STORY_MENU():
	
	result = requests.get('http://sexstories.com')
	
	match = re.compile('<div id="menu">.+?<h2>Genres</h2>(.+?)<div id="content">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<li>(.+?)</li>',re.DOTALL).findall(string)
	for item in match2:
		title=re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
		url=re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.sexstories.com" + url4
		name = "[COLOR blue][B]" + title + "[/B][/COLOR]"
		addDir(name,url,9,icon,fanart,'')

def GET_CONTENT(url):

	checker = url
	result = requests.get(url)
	match = re.compile('<div id="video(.+?)</p></div>',re.DOTALL).findall(result.content)
	for item in match:
		title=re.compile('title=(.+?)">').findall(item)[0]
		try:
			res=re.compile('<span class="video-hd-mark">(.+?)</span>').findall(item)[0]
		except:
			res= 'SD'
			pass
		if str(res) == "HD":
			resolution = "[COLOR orangered][B]" + str(res) + "[/B][/COLOR] - "
		else:
			resolution = "[COLOR yellow][B]" + str(res) + "[/B][/COLOR] - "
		url=re.compile('<a href="(.+?)"').findall(item)[0]
		iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
		name = "[COLOR blue]" + title + "[/COLOR]"
		name = name.replace('"','')
		addItem(resolution + name,url,3,iconimage,iconimage,'')

	try:
		np=re.compile('<a href="([^"]*)" class="no-page">Next</a></li></ul></div>').findall(result.content)[0]
		np = 'http://www.xnxx.com'+np
		addDir('[COLOR yellow]Next Page >>[/COLOR]',np,1,next_icon,fanart,'')       
	except:pass

	if not "http://www.xnxx.com/home/10" in checker:
		if "/home/" in checker:
			a,b,c,d,e = checker.split('/')
			new = int(float(e)) + 1
			url = "http://www.xnxx.com/home/" + str(new)
			addDir('[COLOR yellow]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')   
		elif checker == "http://www.xnxx.com":
			url = "http://www.xnxx.com/home/1"
			addDir('[COLOR yellow]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')
	xbmc.executebuiltin('Container.SetViewMode(500)')

def PICTURE_CONTENT(url):
	
	result = requests.get(url)
	
	match = re.compile('<div class="smallMargin"></div><div class="clearfix">(.+?)<div class="bigMargin"></div><div class="clearfix">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<div class="boxImg size_small home1 thumb"(.+?)</div></a></div>',re.DOTALL).findall(string)

	for item in match2:
		url=re.compile('<a href="(.+?)" target=').findall(item)[0]
		image=re.compile('d=".+?" src="(.+?)"').findall(item)[0]
		title=re.compile('<span class="descHome"><.+?>(.+?)<').findall(item)[0]
		url3 = url
		url4 = url3.replace('//','')
		url = "http://multi.xnxx.com" + url4
		name = "[COLOR blue][B]" + title + "[/B][/COLOR]"
		addDir(name,url,6,image,image,'')

def LIST_STORIES(url):
	
	result = requests.get(url)
	
	match = re.compile('<ul class="stories_list">(.+?)<div class="pager">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<h4>(.+?)</h4>',re.DOTALL).findall(string)

	for item in match2:
		title=re.compile('<a href=".+?">(.+?)</a>.+?tby').findall(item)[0]
		url=re.compile('<a href="(.+?)">.+?</a>.+?by').findall(item)[0]
		author=re.compile('by <a href=".+?">(.+?)</a>').findall(item)[0]
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.sexstories.com" + url4
		title = CLEANUP(title)
		name = "[COLOR blue][B]" + title + " by " + author +"[/B][/COLOR]"
		addItem(name,url,10,icon,fanart,'')

def DISPLAY_STORY(url):
	
	result = requests.get(url)

	try:
		match = re.compile('<!-- CONTENT -->.+?<div (.+?)story_info">',re.DOTALL).findall(result.content)
		string = str(match)
		match2 = re.compile('class="block(.+?)ass="',re.DOTALL).findall(string)

		for item in match2:
			content=re.compile('_panel">(.+?)<div cl').findall(item)[0]
			display=str(content).replace('<!-- VOTES -->','')
			display.decode()
			a = CLEANUP(display)
			TextBoxes("%s" % a)
	except:
		dialog=xbmcgui.Dialog()
		dialog.ok('XNXX.com','There was an error processing the request. Please try another link.')

def SCRAPE_GALLERY(url):
	
	i = 0
	result = requests.get(url)
	
	match = re.compile('<div class="row galleryPage GalleryBlock" id="Gallery">(.+?)</div><div class="sponsorLink">',re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile('<img(.+?) data-id',re.DOTALL).findall(string)

	for item in match2:
		i = i + 1
		image=re.compile('src="(.+?)"').findall(item)[0]
		addItem("[COLOR blue][B]Picture " + str(i) + "[/B][/COLOR]",image,7,image,image,'')

def DISPLAY_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)

def SEARCH():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(' ','').capitalize()
        if len(string)>1:
            url = "http://www.xnxx.com/?k=" + string
            GET_CONTENT(url)
        else: quit()

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

	return text

def PLAY_URL(name,url,iconimage):

	dp = GET_LUCKY()
	url = "http://www.xnxx.com/" + url
	result = requests.get(url)
	match = re.compile('<head>(.+?)</html>',re.DOTALL).findall(result.content)
	string = str(match).replace('\\','').replace('(','').replace(')','')
	url = re.compile("setVideoHLS'(.+?)'").findall(string)[0]
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	time.sleep(2.00)
	dp.close()
	xbmc.Player ().play(url, liz, False)

def PARENTAL_CONTROLS():

	found = 0
	if not os.path.exists(PARENTAL_FILE):
		found = 1
		addItem("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')
	else:
		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				found = 1
				addItem("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR lime]ON[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR yellow][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR lime][B]Change Password[/B][/COLOR]","url",12,icon,fanart,'')
				addItem("[COLOR red][B]Disable Password[/B][/COLOR]","url",13,icon,fanart,'')

	if found == 0:
		addItem("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')

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
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]We are getting the moisturiser.[/B][/COLOR]','[B][COLOR azure]Do you have the wipes ready?[/B][/COLOR]' )
	elif lucky == 2:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]I am just taking off my pants.[/B][/COLOR]','[B][COLOR azure]Darn belt![/B][/COLOR]' )
	elif lucky == 3:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]Are the curtains closed?[/B][/COLOR]','[B][COLOR azure]Oh baby its cold outside![/B][/COLOR]' )
	elif lucky == 4:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]This is my fifth time today.[/B][/COLOR]','[B][COLOR azure]How about you?[/B][/COLOR]' )
	elif lucky == 5:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]Please no buffer, please no buffer![/B][/COLOR]')
	elif lucky == 6:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]I think I am going blind :-/[/B][/COLOR]','[B][COLOR azure]Oh no, just something in my eye.[/B][/COLOR]' )
	elif lucky == 7:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]Did I turn the oven off?[/B][/COLOR]','[B][COLOR azure]It can wait![/B][/COLOR]' )
	elif lucky == 8:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]Your video is coming.[/B][/COLOR]','[B][COLOR azure]Do you get it?[/B][/COLOR]' )
	elif lucky == 9:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]Kodi does not save your browsing history :-D[/B][/COLOR]','[B][COLOR azure]Thats lucky isnt it :-)[/B][/COLOR]' )
	else:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR dodgerblue]There are more XXX addons by ECHO.[/B][/COLOR]','[B][COLOR azure]Just so you know.[/B][/COLOR]' )

	return dp

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

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
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
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
elif mode==4: PICTURE_MENU()
elif mode==5: PICTURE_CONTENT(url)
elif mode==6: SCRAPE_GALLERY(url)
elif mode==7: DISPLAY_PICTURE(url)
elif mode==8: STORY_MENU()
elif mode==9: LIST_STORIES(url)
elif mode==10: DISPLAY_STORY(url)
elif mode==11: PARENTAL_CONTROLS()
elif mode==12: PARENTAL_CONTROLS_PIN()
elif mode==13: PARENTAL_CONTROLS_OFF()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
