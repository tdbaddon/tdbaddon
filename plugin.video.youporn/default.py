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
AddonTitle     = "[COLOR pink][B]YouPorn[/B][/COLOR]"
addon_id       = 'plugin.video.youporn'
dialog         = xbmcgui.Dialog()
ADDON          = xbmcaddon.Addon(id=addon_id)
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
next_icon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/next.png'))
search_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
discussed_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/discussed.png'))
fav_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/fav.png'))
new_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/new.png'))
pc_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/pc.png'))
top_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/top.png'))
twitter_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/twitter.png'))
viewed_icon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/viewed.png'))

PARENTAL_FILE  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'controls.txt'))
PARENTAL_FOLDER= xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
NEW_VIDS       = 'http://www.youporn.com/'
TOP_VIDS       = 'http://www.youporn.com/top_rated/'
MOST_FAV       = 'http://www.youporn.com/most_favorited/'
MOST_VIEW      = 'http://www.youporn.com/most_viewed/'
MOST_DIS       = 'http://www.youporn.com/most_discussed/'

def MAIN_MENU():

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

	if not os.path.exists(PARENTAL_FILE):
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')
	else:
		addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR lime]ON[/COLOR][/B][/COLOR]","url",11,pc_icon,fanart,'')
	addItem("[COLOR yellow][B]Twitter Support: @echo_coding[/B][/COLOR]","url",999,twitter_icon,fanart,'')
	addDir("[COLOR yellow][B]SEARCH[/B][/COLOR]","url",2,search_icon,fanart,'')
	addDir("[COLOR pink][B][I]NEW VIDEOS[/I][/B][/COLOR]",NEW_VIDS,1,new_icon,fanart,'')
	addDir("[COLOR pink][B][I]TOP RATED[/I][/B][/COLOR]",TOP_VIDS,1,top_icon,fanart,'')
	addDir("[COLOR pink][B][I]MOST VIEWED[/I][/B][/COLOR]",MOST_VIEW,1,viewed_icon,fanart,'')
	addDir("[COLOR pink][B][I]MOST FAVORITED[/I][/B][/COLOR]",MOST_FAV,1,fav_icon,fanart,'')
	addDir("[COLOR pink][B][I]MOST DISCUSSED[/I][/B][/COLOR]",MOST_DIS,1,discussed_icon,fanart,'')

	result = requests.get('http://www.youporn.com/categories')
	
	match = re.compile("id='categoryList'>(.+?)<div class='title-bar sixteen-column'>",re.DOTALL).findall(result.content)
	string = str(match)
	match2 = re.compile("<a h(.+?)</p>",re.DOTALL).findall(string)
	fail = 0
	videos = 0
	for item in match2:
		url=re.compile('ref="(.+?)"').findall(item)[0]
		title=re.compile('alt="(.+?)"').findall(item)[0]
		icon_cat=re.compile('original="(.+?)"').findall(item)[0]
		a = str(icon_cat)
		icon_cat = a.replace(' ','%20')
		if "http" not in str(icon_cat):
			icon_cat = icon
		number=re.compile('<span>(.+?)</span>').findall(item)[0]
		b = str(number)
		c = b.replace(',','').replace(' Videos','')
		videos = videos + int(float(c))
		url3 = url
		url4 = url3.replace('\\','')
		url = "http://www.youporn.com" + url4
		name = "[COLOR rose][B]" + title + " - " + number + "[/B][/COLOR]"
		addDir(name,url,1,icon_cat,fanart,'')
		
	try:
		addDir("[COLOR red][B]Total Videos: {:,}".format(videos) + "[/B][/COLOR]",NEW_VIDS,1,icon,fanart,'')
	except:
		try:
			addDir("[COLOR red][B]Total Videos: " + str(videos) + "[/B][/COLOR]",NEW_VIDS,1,icon,fanart,'')
		except: pass

def GET_CONTENT(url):

	checker = url
	result = requests.get(url)
	match = re.compile('video-box four-column(.+?)<div class="video-box-title">',re.DOTALL).findall(result.content)
	for item in match:
		try:
			title=re.compile("alt=(.+?)'").findall(item)[0]
			url=re.compile('<a href="(.+?)"').findall(item)[0]
			iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
			if "icon-hd-text" in item:
				name = "[B][COLOR orangered]HD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
			else:
				name = "[B][COLOR yellow]SD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
			name = name.replace("'",'')
			addItem(name,url,3,iconimage,iconimage,'')
		except: pass
	try:
		np=re.compile('<li class="current"(.+?)<div id="next">',re.DOTALL).findall(result.content)
		for item in np:
			current=re.compile('<div class="currentPage" data-page-number=".+?">(.+?)</div>').findall(item)[0]
			url=re.compile('<a href="(.+?)=').findall(item)[0]
			next = int(float(current)) + 1
			url = "http://youporn.com" + str(url) + "=" + str(next)
			addDir('[COLOR pink]Next Page >>[/COLOR]',url,1,next_icon,fanart,'')       
	except:pass

	xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(' ','').capitalize()
        if len(string)>1:
            url = "http://www.youporn.com/search/?query=" + string
            GET_CONTENT(url)
        else: quit()

def PLAY_URL(name,url,iconimage):

	dp = GET_LUCKY()
	url = "http://www.youporn.com" + url
	result = requests.get(url)
	match = re.compile('sources: {(.+?)}',re.DOTALL).findall(result.content)
	a = str(match)
	match = a.replace('\\','')
	try:
		url1 = re.compile("1080_60.+?'(.+?)',").findall(match)[0]
	except: url1 = "null"
	try:
		url2 = re.compile("1080.+?'(.+?)',").findall(match)[0]
	except:url2 = "null"
	try:
		url3 = re.compile("720_60+?'(.+?)',").findall(match)[0]
	except:url3 = "null"
	try:
		url4 = re.compile("720.+?'(.+?)',").findall(match)[0]
	except: url4 = "null"
	try:
		url5 = re.compile("480.+?'(.+?)',").findall(match)[0]
	except: url5 = "null"
	try:
		url6 = re.compile("240.+?'(.+?)',").findall(match)[0]
	except: url6 = "null"
	
	if "http" in url1:
		url_play = url1
	elif "http" in url2:
		url_play = url2
	elif "http" in url3:
		url_play = url3
	elif "http" in url4:
		url_play = url4
	elif "http" in url5:
		url_play = url5
	elif "http" in url6:
		url_play = url6
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	time.sleep(2.00)
	dp.close()
	xbmc.Player ().play(url_play, liz, False)

def PARENTAL_CONTROLS():

	found = 0
	if not os.path.exists(PARENTAL_FILE):
		found = 1
		addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
		addItem("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",12,icon,fanart,'')
	else:
		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				found = 1
				addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR lime]ON[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR yellow][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,icon,fanart,'')
				addItem("[COLOR lime][B]Change Password[/B][/COLOR]","url",12,icon,fanart,'')
				addItem("[COLOR red][B]Disable Password[/B][/COLOR]","url",13,icon,fanart,'')

	if found == 0:
		addItem("[COLOR rose][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,icon,fanart,'')
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
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]We are getting the moisturiser.[/B][/COLOR]','[B][COLOR azure]Do you have the wipes ready?[/B][/COLOR]' )
	elif lucky == 2:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I am just taking off my pants.[/B][/COLOR]','[B][COLOR azure]Darn belt![/B][/COLOR]' )
	elif lucky == 3:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Are the curtains closed?[/B][/COLOR]')
	elif lucky == 4:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Its my fifth time today.[/B][/COLOR]','[B][COLOR azure]How about you?[/B][/COLOR]' )
	elif lucky == 5:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Please no buffer, please no buffer![/B][/COLOR]')
	elif lucky == 6:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]I think I am goin blind :-/[/B][/COLOR]')
	elif lucky == 7:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Did I turn the oven off?[/B][/COLOR]','[B][COLOR azure]It can wait![/B][/COLOR]' )
	elif lucky == 8:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Your video is coming.[/B][/COLOR]','[B][COLOR azure]Do you get it?[/B][/COLOR]' )
	elif lucky == 9:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]Kodi does not sabe your browsing history :-D[/B][/COLOR]')
	else:
		dp.create(AddonTitle,"[B][COLOR yellow]Please wait.[/B][/COLOR]",'[B][COLOR pink]There more XXX addons by ECHO.[/B][/COLOR]','[B][COLOR azure]Just so you know.[/B][/COLOR]' )

	return dp

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
