"""
    Copyright (C) 2016 ECHO Wizard

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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
from urllib2 import urlopen
import extract
import downloader
import re
import time
addon_id = 'plugin.program.echowizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.echowizard'
AddonTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
HOME         =  xbmc.translatePath('special://home/')
dialog       =  xbmcgui.Dialog()
BASEURL = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
SUPPORT_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/support.png'))
FANART              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

#######################################################################
#						Add to menus
#######################################################################

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addItem(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDirWTW(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok

#######################################################################
#				INDIVIDUAL BUILDS MENU
#######################################################################

def BUILDER(name,url,iconimage,fanart,description):

	urla = url
	url = str(name + "," + urla)
	desca = description
	notice,hash,fresh,youtube,skin = desca.split(',')
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
	body = urllib2.urlopen(service_url).read()
	addDir("[COLOR lightskyblue][B]Download The Build Now[/B][/COLOR]",url,90,iconimage,fanart,description)
	url = name
	addItem("[COLOR white][B]---------------[/COLOR][/B] [COLOR lightskyblue][B]EXTRAS[/COLOR][/B] [COLOR white][B]---------------[/COLOR][/B]",url,666,iconimage,fanart,description)
	if "null" not in youtube.lower():
		addItem('[COLOR white][B]Watch YouTube Guide of The Build[/B][/COLOR]',youtube,95,iconimage,fanart,'')
	addItem("[COLOR white][B]Write A Review[/COLOR][/B]",url,58,iconimage,fanart,description)
	addDir("[COLOR white][B]Read All Reviews - [COLOR lightskyblue]" + body + " [/COLOR] [/COLOR][/B]",url,59,iconimage,fanart,description)
	addItem("[COLOR white][B]View Build Fanart[/COLOR][/B]",fanart,116,iconimage,fanart,description)

def BUILDER_COMMUNITY(name,url,iconimage,fanart,description):

	urla = url
	skin_used, developer = description.split(',')
	url = str(name + "," + urla + "," + skin_used + "," + developer)
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
	body = urllib2.urlopen(service_url).read()
	addDir("[COLOR lightskyblue][B]Download The Build Now[/B][/COLOR]",url,96,iconimage,fanart,description)
	url = name
	addItem("[COLOR white][B]---------------[/COLOR][/B] [COLOR lightskyblue][B]EXTRAS[/COLOR][/B] [COLOR white][B]---------------[/COLOR][/B]",url,666,iconimage,fanart,description)
	addItem("[COLOR white][B]Write A Review[/COLOR][/B]",url,58,iconimage,fanart,description)
	addDir("[COLOR white][B]Read All Reviews - [COLOR lightskyblue]" + body + " [/COLOR] [/COLOR][/B]",url,59,iconimage,fanart,description)
	addItem("[COLOR white][B]View Build Fanart[/COLOR][/B]",fanart,116,iconimage,fanart,description)


#######################################################################
#				INDIVIDUAL BUILDS MENU
#######################################################################

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def WriteReview(build_name):

	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'Enter Your Review')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your Name')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	name_text == "":
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1hZGQmdGV4dD0=') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	dialog.ok(AddonTitle, "[B][COLOR smokewhite]Thanks, For leaving A Review for : [/COLOR][/B]", "", build_name )

	xbmc.executebuiltin("Container.Refresh")

def ListReview(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1yZWFkJmJ1aWxkPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR blue][B]"+review['date']+"[/COLOR][/B] - [COLOR white][B] Read Review By : " +review['name']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,49,ICON,FANART,'')

def Write_Addon_Review(build_name):

	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'Enter Your Review')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your Name')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	name_text == "":
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1hZGQmdGV4dD0=') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	dialog.ok(AddonTitle, "[B][COLOR white]Thank you for leaving a review.[/COLOR][/B]")

def List_Addon_Review(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1yZWFkJmJ1aWxkPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR blue][B]"+review['date']+"[/COLOR][/B] - [COLOR white][B] Read Review By : " +review['name']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,49,ICON,FANART,'')

def WriteTicket():

	build_name = "[COLOR orangered][B]Ticket[/B][/COLOR]"
	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'What Is The Issue You Have Found?')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your E-Mail')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	"@" not in name_text:
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid e-mail![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)
		if 	"." not in name_text:
			dialog.ok(AddonTitle, "[B][COLOR smokewhite]Sorry not a valid e-mail![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9zdXBwb3J0LnBocD9hY3Rpb249YWRkJnRleHQ9') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	splitter = name_text
	ref,rest = splitter.split('@')
	ref2 = base64.b64encode(ref)
	ref3 = ref2.replace("=","")
	dialog.ok(AddonTitle, "[B][COLOR lightskyblue]Thank you for contacting us![/COLOR][/B]", "We will be in touch in 24-48 Hours", "[COLOR smokewhite][B]Reference: [/B][COLOR white][I]" + ref3.upper() + "[/COLOR][/I]")

	xbmc.executebuiltin("Container.Refresh")

def ListTickets():

	build_name = "[COLOR orangered][B]Ticket[/B][/COLOR]"
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9zdXBwb3J0LnBocD9hY3Rpb249cmVhZCZidWlsZD0=') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR blue][B]Ticket Raised: [/COLOR][/B][COLOR white][I]"+review['date']+"[/COLOR][/I] - [COLOR white][B]" +review['review']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,120,SUPPORT_ICON,FANART,'')

def review_parse(data):

    patron = "<item>(.*?)</item>"
    reviews = re.findall(patron,data,re.DOTALL)

    items = []
    for review in reviews:
        item = {}
        item["name"] = find_single_match(review,"<name>([^<]+)</name>")
        item["date"] = find_single_match(review,"<date>([^<]+)</date>")
        item["review"] = find_single_match(review,"<review>([^<]+)</review>")

        if item["name"]!="":
            items.append(item)

    return items

def add_one(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV90b3RhbC5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_community(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHkucGhwP2FjdGlvbj1hZGQmbmFtZT0=') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_addons_total(name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbnNfdG90YWwucGhwP2FjdGlvbj1hZGQmbmFtZT0=') + base64.b64encode(name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_addons_week(name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbnNfd2Vlay5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)
		
def add_one_fanriffic(name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9mYW5yaWZmaWMucGhwP2FjdGlvbj1hZGQmbmFtZT0=') + base64.b64encode(name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_community_dev_total(name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHlfZGV2X3RvdGFsLnBocD9hY3Rpb249YWRkJm5hbWU9') + base64.b64encode(name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_community_dev_week(name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHlfZGV2X3dlZWsucGhwP2FjdGlvbj1hZGQmbmFtZT0=') + base64.b64encode(name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def add_one_advanced(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZHZhbmNlZC5waHA/YWN0aW9uPWFkZCZuYW1lPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)
	
def add_one_backups(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9iYWNrdXBzLnBocD9hY3Rpb249YWRkJm5hbWU9') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except:
		sys.exit(0)

def community_dev_week(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHlfZGV2X3dlZWsucGhwP2FjdGlvbj1jb3VudCZuYW1lPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	return data

def community_dev_total(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHlfZGV2X3RvdGFsLnBocD9hY3Rpb249Y291bnQmbmFtZT0=') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	return data

def count_fanriffic(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9mYW5yaWZmaWMucGhwP2FjdGlvbj1jb3VudCZuYW1lPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	return data

def count_addons_week(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbnNfd2Vlay5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	return data

def count_addons_total(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbnNfdG90YWwucGhwP2FjdGlvbj1jb3VudCZuYW1lPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	return data

def count(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
		f = urllib2.urlopen(service_url)
		data = f.read()
		f.close()

		return data
	except:
		sys.exit(0)

def count_total(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV90b3RhbC5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
		f = urllib2.urlopen(service_url)
		data = f.read()
		f.close()

		return data
	except:
		sys.exit(0)

def count_community(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9jb21tdW5pdHkucGhwP2FjdGlvbj1jb3VudCZuYW1lPQ==') + base64.b64encode(build_name)
		f = urllib2.urlopen(service_url)
		data = f.read()
		f.close()

		return data
	except:
		sys.exit(0)

def count_advanced(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZHZhbmNlZC5waHA/YWN0aW9uPWNvdW50Jm5hbWU9') + base64.b64encode(build_name)
		f = urllib2.urlopen(service_url)
		data = f.read()
		f.close()

		return data
	except:
		sys.exit(0)

def count_backups(build_name):

	try:
		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9iYWNrdXBzLnBocD9hY3Rpb249Y291bnQmbmFtZT0=') + base64.b64encode(build_name)
		f = urllib2.urlopen(service_url)
		data = f.read()
		f.close()

		return data
	except:
		sys.exit(0)

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def find_single_match(text,pattern):

    result = ""
    try:    
        single = re.findall(pattern,text, flags=re.DOTALL)
        result = single[0]
    except:
        result = ""

    return result

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
			self.win.getControl(self.CONTROL_LABEL).setLabel('ECHO Wizard - View Log Facility') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def TextBoxesPlain(announce):
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
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR smokewhite][B]ECHO Wizard[/B][/COLOR]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link  

def OPEN_URL_NORMAL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'python-requests/2.9.1')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link  

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def convertSize(size):
   import math
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   
   return s,size_name[i]

##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
		
############################
###REMOVE EMPTY FOLDERS#####
############################

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
	print"########### Start Removing Empty Folders #########"
	empty_count = 0
	used_count = 0
	try:
		for curdir, subdirs, files in os.walk(HOME):
			if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
				empty_count += 1 #increment empty_count
				os.rmdir(curdir) #delete the directory
				print "successfully removed: "+curdir
			elif len(subdirs) > 0 and len(files) > 0: #check for used directories
				used_count += 1 #increment 
	except: pass

def REMOVE_EMPTY_FOLDERS_BUILDS():
#initialize the counters
	print"########### Start Removing Empty Folders #########"
	empty_count = 0
	used_count = 0
	
	EXCLUDES = ['Thumbnails']

	try:
		for dirs, subdirs, files in os.walk(HOME,topdown=True):
			subdirs[:] = [d for d in subdirs if d not in EXCLUDES]
			if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
				empty_count += 1 #increment empty_count
				os.rmdir(dirs) #delete the directory
				print "successfully removed: "+dirs
			elif len(subdirs) > 0 and len(files) > 0: #check for used directories
				used_count += 1 #increment 
	except: pass

###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
    dialog       =  xbmcgui.Dialog()
    choice = xbmcgui.Dialog().yesno('[COLOR=lightsteelblue]Force Close Kodi[/COLOR]', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='[COLOR=green]Yes, Close[/COLOR]')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    


def KillKodi():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    