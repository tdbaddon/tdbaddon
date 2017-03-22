# TVADDONS.ag / TVADDONS.ag - Addon Installer - Module By: Blazetamer (2013-2016)

siteTitle="TVADDONS.AG"
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil,downloader,extract,base64
base_url2='http://tvaddons.ag/kodi-addons'
indigo_url2='http://indigo.tvaddons.ag/'
indigo_url=indigo_url2+'installer/sources/'; base_url=base_url2+'/'
import traceback,sys
from libs import kodi
from libs import viewsetter
AddonTitle ="Indigo"
import ssl
if kodi.get_kversion() >16.5:
	#kodi.log(' VERSION IS ABOVE 16.5')
	ssl._create_default_https_context = ssl._create_unverified_context
else:
	#kodi.log(' VERSION IS BELOW 16.5')
	pass
from libs import addon_able
addon_id=kodi.addon_id
addon=(addon_id,sys.argv)

settings=xbmcaddon.Addon(id=addon_id)
ADDON=xbmcaddon.Addon(id=addon_id)
artPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art2/'));
def getArtwork(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2/',n))
def getArtworkJ(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2/',n+'.jpg'))
def catArtwork(n): return 'http://addons.tvaddons.ag/images/categories/%s.png'%n

artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2/'))

mainPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id))
fanart=xbmc.translatePath(os.path.join(mainPath,'fanart.jpg'))
iconart=xbmc.translatePath(os.path.join(mainPath,'icon.png'))
TxtAddonUpdater='Addon Updater'; ImgAddonUpdater=getArtworkJ('autoupdater')

Keymaps_URL = base64.b64decode("aHR0cDovL2luZGlnby50dmFkZG9ucy5hZy9rZXltYXBzL2N1c3RvbWtleXMudHh0")
KEYBOARD_FILE  =  xbmc.translatePath(os.path.join('special://home/userdata/keymaps/','keyboard.xml'))
openSub="https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/service.subtitles.opensubtitles_by_opensubtitles/service.subtitles.opensubtitles_by_opensubtitles-5.1.14.zip"
#****************************************************************
def MAININDEX():

	kodi.addDir('Search by: Addon/Author',base_url+'search/?keyword=','searchaddon',artwork+'search.png',description="Search for addons by Name or Author")
	if settings.getSetting('featured')=='true':
		kodi.addDir('Featured Addons',base_url+'category/featured/','addonlist',artwork+'featured.png',description="The most popular Kodi addons!")
	if settings.getSetting('livetv')=='true':
		kodi.addDir('Live TV Addons',base_url+'category/livetv/','addonlist',artwork+'livetv.png',description="The most popular live TV addons!")
	if settings.getSetting('sports')=='true':
		kodi.addDir('Sports Addons',base_url+'category/sports/','addonlist',artwork+'sports.png',description="The most popular sports addons!")
	if settings.getSetting('video')=='true':
		kodi.addDir('Video Addons',base_url+'category/video/','addonlist',artwork+'video.png',description="Every video addon in existence!")
	if settings.getSetting('audio')=='true':
		kodi.addDir('Audio Addons',base_url+'category/audio/','addonlist',artwork+'audio.png',description="Find addons to listen to music!")
	if settings.getSetting('program')=='true':
		kodi.addDir('Program Addons',base_url+'category/programs/','addonlist',artwork+'program.png',description="Every program addon you can imagine!")
	if settings.getSetting('playlist')=='true':
		kodi.addDir('Playlist Addons',base_url+'category/playlists/','addonlist',artwork+'playlists.png',description="The most popular playlist addons!")
	# if settings.getSetting('services')=='true':
	# 	kodi.addDir('Service Addons',base_url+'category/services/','addonlist',artwork+'service.png')
	if settings.getSetting('skincat')=='true':
		kodi.addDir('Kodi Skins',base_url+'category/skins/','addonlist',artwork+'kodi_skins.png',description="Change up your look!")
	if settings.getSetting('world')=='true':
		kodi.addDir('International Addons',base_url+'category/international/','interlist',artwork+'world.png',description="Foreign language addons and repos from across the globe!")
	if settings.getSetting('adult')=='true':
		kodi.addDir('Adult Addons',indigo_url+'xxx.php','adultlist',artwork+'adult.png',description="Must be 18 years or older! This menu can be disabled from within Add-on Settings.")
	if settings.getSetting('repositories')=='true':
		kodi.addDir('Repositories',base_url+'category/repositories/','addonlist',artwork+'repositories.png',description="Browse addons by repository!")
	kodi.addItem('Official OpenSubtitles Addon', openSub, 'addopensub', artwork + 'opensubicon.png',description="Install Official OpenSubtitles Addon!")
	viewsetter.set_view("sets")
#****************************************************************

#********************************************************************
def INTERNATIONAL(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url); match=GetListItems(link); CMi=[]; viewsetter.set_view("sets");
	#CMi.append(['Information',"XBMC.Action(Info)"]);
	if 'repository' in url: ToMode='interrepolist'
	else: ToMode='addonlist'
	for url,image,name, in match:
		if name == "Repositories":
			kodi.addDir('International Repositories', base_url + 'category/international/repositories', 'interlist',artwork + 'world.png', description="Foreign language addons from across the globe!")
		else:

			iconimage=base_url+image;
			add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
	nmatch=GetListNextPage(link);
	if len(nmatch) > 0: kodi.addDir('Next Page',(nmatch[0]),'interrepolist',getArtworkJ('NextPage'))
	viewsetter.set_view("sets")
	return

def nolines(t): return t.replace('\r','').replace('\n','').replace('\t','').replace('\a','')

def WizardTypeInstaller(name,url):
	MyAddonInstaller(name,url,xbmc.translatePath(os.path.join('special://','home')))

def AddonTypeInstaller(name,url):
	MyAddonInstaller(name,url,xbmc.translatePath(os.path.join('special://','home','addons')))

def MyAddonInstaller(name,url,ToPath):
	if len(ToPath)==0: return
	path=xbmc.translatePath(os.path.join('special://home','addons','packages'))
	dp=xbmcgui.DialogProgress(); dp.create("Addon Installer","Downloading ",'','Please Wait')
	lib=os.path.join(path,name+'.zip')
	try: os.remove(lib)
	except: pass
	url=FireDrive(url)
	if '[error]' in url: print url; dialog=xbmcgui.Dialog(); dialog.ok("Error!",url); return
	else: print url
	downloader.download(url,lib,dp)
	addonfolder=ToPath
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait")
	print '======================================='; print addonfolder; print '======================================='
	extract.all(lib,addonfolder,dp)
	time.sleep(2)
	xbmc.executebuiltin("XBMC.UpdateLocalAddons()");
	addon_able.set_enabled("")
	dialog=xbmcgui.Dialog(); dialog.ok("Addon Instaler",name+" has been installed","","")
	##
#****************************************************************
def AutoUpdate(url): #Featured Addons
	print url; link=nolines(OPEN_URL(url))
	if "/featured-addons.php" in url:
		match=re.compile('name="(.+?)"url="(.+?)"').findall(link)
		for name,url2 in match:
			itemID=url2[0:-1].split('/')[-1]; print 'checking for addon: '+itemID;
			path=xbmc.translatePath(os.path.join('special://home/addons',itemID));
			AddonDotXml=xbmc.translatePath(os.path.join('special://home/addons',itemID,'addon.xml'));
			if (os.path.exists(path)==True) and (os.path.isfile(AddonDotXml)==True): print 'path and addon.xml found for: '+itemID; AutoUpdate_ADDONINDEX(name,url2,'addon',itemID);
			#add2HELPDir(name,url,'addonindex',fanart,fanart,'','addon')
	elif ("/featured-repos.php" in url) or ("/xxx.php" in url):
		match=re.compile("'name' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
		for name,url2 in match:
			lang='Featured'; name=name.replace('&rsquo;',"'"); name=name.capitalize();
			itemID=url2[0:-1].split('/')[-1]; print 'checking for addon: '+itemID;
			path=xbmc.translatePath(os.path.join('special://home/addons',itemID));
			AddonDotXml=xbmc.translatePath(os.path.join('special://home/addons',itemID,'addon.xml'));
			if (os.path.exists(path)==True) and (os.path.isfile(AddonDotXml)==True): print 'path and addon.xml found for: '+itemID; AutoUpdate_ADDONINDEX(name,url2,'addon',itemID);
	elif ("/category/programs/" in url) or ("/category/video/" in url) or ("/category/audio/" in url) or ("/category/" in url):
		#match=re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)
		match=re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" (?:width="100%" |class="pic" )?alt="(.+?)"').findall(link)
		for url2,image,name, in match:
			iconimage=base_url+image;
			itemID=url2[0:-1].split('/')[-1]; print 'checking for addon: '+itemID;
			path=xbmc.translatePath(os.path.join('special://home/addons',itemID));
			AddonDotXml=xbmc.translatePath(os.path.join('special://home/addons',itemID,'addon.xml'));
			if (os.path.exists(path)==True) and (os.path.isfile(AddonDotXml)==True): print 'path and addon.xml found for: '+itemID; AutoUpdate_ADDONINDEX(name,url2,'addon',itemID);
	else: print "url type mismatch in attempt to catch the right items match regex string."; return
def AutoUpdate_ADDONINDEX(name,url,filetype,itemID):
	description='No Description available'; print [name,url,filetype,itemID];
	path=xbmc.translatePath(os.path.join('special://home/addons',itemID))
	AddonDotXml=xbmc.translatePath(os.path.join('special://home/addons',itemID,'addon.xml'))
	LocalAddonDotXml=nolines(File_Open(AddonDotXml));
	LocalVersion=(re.compile('version=["\']([0-9a-zA-Z\.\-]+)["\']\s*').findall(LocalAddonDotXml.split('<addon')[1])[0]).strip(); print "LocalVersion: "+LocalVersion;
	try: link=OPEN_URL(url);
	except: print "failed to load url: "+url; return
	itemDirectDownload=re.compile('Direct Download:</strong><br /><a href="(.+?)"').findall(link)[0]
	itemAddonVersion=(re.compile('Version:</strong>(.+?)<br').findall(link)[0]).strip()
	print "RemoteVersion: "+itemAddonVersion;
	itemRepository=re.compile('Repository:</strong> <a href="(.+?)"').findall(link)[0]
	itemImage=base_url+(re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)[0])
	itemAuthor=re.compile('Author:</strong> <a href=".+?">(.+?)</a>').findall(link)[0]
	itemAddonName=re.compile('class="pic" /></span>\r\n\t\t\t\t<h2>(.+?)</h2>').findall(link)[0]
	## ### ##
	##DO SOMETHING HERE##
	#if not LocalVersion==itemAddonVersion:
	cV=compareVersions(LocalVersion,itemAddonVersion); print cV;
	if cV=='do_upgrade':
		try:
				ADDONINSTALL(itemAddonName,itemDirectDownload,description,filetype,itemRepository,True,itemAddonVersion,LocalVersion)
				addHELPDir('AutoUpdated: '+itemAddonName+' - v'+itemAddonVersion,itemDirectDownload,'addoninstall',itemImage,fanart,description,'addon',itemRepository,itemAddonVersion,itemAuthor)
		except: print "error while trying to install: "+itemAddonName; return
	## ### ##
def compareVersions(LocalV,RemoteV):
	if LocalV==RemoteV: return 'are_equal'
	if ('.' in LocalV) and ('.' in RemoteV):
		try: dotL=LocalV.split('.'); dotR=RemoteV.split('.');
		except: return 'do_upgrade'
		try:
			for i in [0,1,2,3]:
				if dotL[i] > dotR[i]: return 'local_greater_than_remote'
		except: return 'do_upgrade'
	return 'do_upgrade'
#****************************************************************
def GetListItems(link):
	try: return re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" (?:width="100%" |class="pic" )?alt="(.+?)"').findall(link)
	except: return []
def GetListNextPage(link):
	#kodi.log("Getting THE NEXT LINK ")
	try:
		return re.compile('"page last" href="(.+?)"><i class').findall(link)
	except:
		return []
def List_Addons_Inner_Tabs(Name,url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url); print 'url:  '+url; print  'length of html:  '+str(len(link));viewsetter.set_view("sets");
	if   'newest'  in Name.lower(): link=link.split('<div class="tabs-inner" id="newest">' )[-1].split('</div>')[0]
	elif 'updated' in Name.lower(): link=link.split('<div class="tabs-inner" id="updated">')[-1].split('</div>')[0]
	match=re.compile("<li><a href='(.+?)'><img src='(.+?)' width='60' height='60' alt='(.+?)' class='pic alignleft' /><b>\s*(.+?)\s*</b></a><span class='date'>\s*(\d\d\d\d-\d\d-\d\d)\s*</span></li").findall(link)
	for url,image,name,name2,released in match: iconimage=base_url+image; add2HELPDir('[COLOR FF0077D7]%s [COLOR FFFFFFFF][[COLOR FFFFFFFF]%s[/COLOR]][/COLOR][/COLOR]'%(name,released),url,'addonindex',iconimage,fanart,'','addon')
	viewsetter.set_view("sets")

def List_Inter_Addons(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url); match=GetListItems(link); CMi=[]; viewsetter.set_view("sets");
	#CMi.append(['Information',"XBMC.Action(Info)"]);
	if '/category/repositories/' in url: ToMode='addonlist'
	else: ToMode='addonindex'
	for url,image,name, in match: iconimage=base_url+image; add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
	nmatch=GetListNextPage(link);
	if len(nmatch) > 0: kodi.addDir('Next Page',(nmatch[0]),'addonlist',getArtworkJ('NextPage'))
	viewsetter.set_view("sets")


def List_Addons(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url); match=GetListItems(link); CMi=[];
	#kodi.log(link)
	if '/category/repositories/' in url: ToMode='addonlist'
	else: ToMode='addonindex'
	for url,image,name, in match: iconimage=base_url+image; add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
	nmatch=GetListNextPage(link);
	if len(nmatch) > 0:
		kodi.addDir('Next Page',(nmatch[0]),'addonlist',getArtworkJ('NextPage'))

	viewsetter.set_view("sets")

def List_Repo_Top_Developers(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url); print 'url:  '+url; #print link; #return
	try: link=link.split('<span class="sidebar-widget-header"><h3 class="sidebar-widget-header">Top developers</h3></span>')[-1]; link=link.split('</ul>')[0];
	except: pass
	match=re.compile("<li><img src='(.+?)' height='20' width='20' alt='(.+?)' /><a href='(.+?)' title='Show all addons from this author'>\s*(.+?)\s+\((\d+)\s+uploads\)</a></li").findall(link.replace('</li>','</li\n\r\a>')); #print match
	for (image,rank,url,name,uploads) in match: iconimage=base_url+image; add2HELPDir("[COLOR FF0077D7]%s [COLOR FFFFFFFF][[COLOR FFFFFFFF]%s[/COLOR]][/COLOR][/COLOR]"%(name,uploads),url,'addonlist',iconimage,fanart,'','addon')
	viewsetter.set_view("sets")
#****************************************************************
def List_Indigo_WorldAlone(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
	match=re.compile("'name' => '(.+?)','language' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
	if len(match)==0: return
	for name,lang,dload in match: lang=lang.capitalize(); addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon','none','','')
	viewsetter.set_view("sets")
def List_Indigo_WorldList(url):
	if not '://' in url: url=base_url2+url
	link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
	match=re.compile("'name' => '(.+?)','language' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
	viewsetter.set_view("sets")
	if len(match)==0: return
	for name,lang,dload in match: lang=lang.capitalize(); addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon','none','','')
	List_Indigo_WorldAlone(indigo_url+'world-solo.php')
	viewsetter.set_view("sets")




def List_Indigo_Adult(url):
	if settings.getSetting('adult')=='true':
		confirm=xbmcgui.Dialog().yesno("Please Confirm","                Please confirm that you are at least 18 years of age.","                                       ","              ","NO (EXIT)","YES (ENTER)")
		if confirm:

			link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','');
			match=re.compile("'name' => '(.+?)'.+?dataUrl' => '(.+?)'.+?xmlUrl' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
			for name,dataurl,url, repourl in match:
				lang='Adults Only'
				add2HELPDir(name+' ('+lang+')',url,'getaddoninfo','',fanart,dataurl,repourl)
				#addHELPDir(name+' ('+lang+')',url,'getaddoninfo','',fanart,'',dataurl,repourl,'','')
				if len(match)==0:
					return
		else:
			kodi.set_setting('adult','false')
			return
		viewsetter.set_view("sets")

def getaddoninfo(url,dataurl,repourl):
	lang='Adults Only'
	link = OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
	match=re.compile('<addon id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(link)
	for adid,name,version in match:
				dload = dataurl+adid+"/"+adid+"-"+version+".zip"
				addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon',repourl,'','')
				viewsetter.set_view("sets")
	#****************************************************************







def ADDONINDEX(name,url,filetype):
	link=OPEN_URL(url); description='Description not available at this time'; CMi=[];
	try:    ifanart=re.compile('<div id="featured-image">\s*<img width="\d+" height="\d+" src="(cache/images/[0-9A-Za-z]+_fanart.jpg)" class=".*?" alt="" />\s*</div>').findall(link)[0]
	except: ifanart=fanart
	try:    iconimage=re.compile('<span class="thumbnail"><img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)[0]
	except: iconimage=''
	if (not '://' in ifanart) and (not artPath in ifanart) and (not mainPath in ifanart): ifanart=base_url+ifanart
	if  not '://' in iconimage: iconimage=base_url+iconimage
	print ['ifanart',ifanart,'iconimage',iconimage];
	name=re.compile('class="pic" /></span>[\r\a\n\t]*\s*<h2>(.+?)</h2>').findall(link)[0]; print ['name',name];
	repourl=re.compile('Repository:</strong> <a href="(.+?)"').findall(link)[0]; repourl=repourl.replace('https://github','http://github'); print ['repourl',repourl];
	try:    description=re.compile('Description:</h4><p>\s*(.+?)\s*</p>').findall(link.replace('\n','').replace('\t',''))[0]; print ['description',description];
	except: description='No Description available'
	addonurl=re.compile('Download:</strong><br /><a href="(.+?)"').findall(link)[0]; print ['addonurl',addonurl];
	(aurthorUrl,author)=re.compile('Author:</strong> <a href="(.+?)">\s*(.+?)\s*</a>').findall(link)[0]; print ['author',author,'aurthorUrl',aurthorUrl];
	version=re.compile('Version:</strong>\s*(.+?)\s*<br').findall(link)[0]; print ['version',version];
	releaseddate=re.compile('>Released:</strong>\s*(.+?)\s*<').findall(link)[0]; print ['version',version];
	try:    forumUrl=re.compile('>Forum:</strong><br /><a href="(.+?)"').findall(link)[0]; print ['version',version];
	except: forumUrl=''
	CMi.append(['Check Others by %s'%author,"XBMC.Container.Update(plugin://%s/?mode=addonlist&url=%s)"%(addon_id,aurthorUrl)])
	CMi.append(['Visit Page',"XBMC.Container.Update(plugin://%s/?mode=BrowseUrl&url=%s)"%(addon_id,urllib.quote_plus(url))])
	if len(forumUrl) > 0: CMi.append(['Visit Forum',"XBMC.Container.Update(plugin://%s/?mode=BrowseUrl&url=%s)"%(addon_id,urllib.quote_plus(forumUrl))])
	#kodi.log("BEFORE INSTALL")
	addHELPDir('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]%s[/COLOR][COLOR FF0077D7] (v%s) [%s][/COLOR] [COLOR FF0077D7][I]by[/I][/COLOR]  [COLOR FFFFFFFF]%s[/COLOR]'%(name,version,releaseddate,author),addonurl,'addoninstall',iconimage,ifanart,description,'addon',repourl,version,author,CMi,True);
#****************************************************************
def Note(header="",message="",sleep=5000): xbmc.executebuiltin("XBMC.Notification(%s,%s,%i)" % (header,message,sleep))
def File_Save(path,data): file=open(path,'w'); file.write(data); file.close()
def File_Open(path):
	if os.path.isfile(path): file=open(path, 'r'); contents=file.read(); file.close(); return contents ## File found.
	else: return '' ## File not found.


def OPEN_URL(url):
	req=urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
	response=urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link




def FireDrive(url):
	if ('http://m.firedrive.com/file/' not in url) and ('https://m.firedrive.com/file/' not in url) and ('http://www.firedrive.com/file/' not in url) and ('http://firedrive.com/file/' not in url) and ('https://www.firedrive.com/file/' not in url) and ('https://firedrive.com/file/' not in url): return url ## contain with current url if not a filedrive url.
	#else:
	try:
		if 'https://' in url: url=url.replace('https://','http://')
		html=net.http_GET(url).content; #print html;
		if ">This file doesn't exist, or has been removed.<" in html: return "[error]  This file doesn't exist, or has been removed."
		elif ">File Does Not Exist | Firedrive<" in html: return "[error]  File Does Not Exist."
		elif "404: This file might have been moved, replaced or deleted.<" in html: return "[error]  404: This file might have been moved, replaced or deleted."
		data={}; r=re.findall(r'<input\s+type="\D+"\s+name="(.+?)"\s+value="(.+?)"\s*/>',html);
		for name,value in r: data[name]=value
		#print data;
		if len(data)==0: return '[error]  input data not found.'
		html=net.http_POST(url,data,headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0','Referer': url,'Host': 'www.firedrive.com'}).content
		r=re.search('<a\s+href="(.+?)"\s+target="_blank"\s+id=\'top_external_download\'\s+title=\'Download This File\'\s*>',html)
		if r: print urllib.unquote_plus(r.group(1)); return urllib.unquote_plus(r.group(1))
		else: return url+'#[error]'
	except: return url+'#[error]'
#****************************************************************
def HUBINSTALL(name,url,description,filetype,repourl):
		path=xbmc.translatePath(os.path.join('special://home','addons','packages'))
		dp=xbmcgui.DialogProgress();
		dp.create("Starting up","Initializing ",'','Please Stand By....')
		lib=os.path.join(path,name+'.zip')
		try: os.remove(lib)
		except: pass
		downloader.download(url,lib,dp)
		if filetype=='addon':
			addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
		time.sleep(2)
		extract.all(lib,addonfolder,'')
#****************************************************************


def OPENSUBINSTALL(url):
		filetype = 'addon'
		path=xbmc.translatePath(os.path.join('special://home','addons','packages'))
		dp=xbmcgui.DialogProgress();
		dp.create("Please Wait"," ",'','Installing Official OpenSubtitles Addon')
		lib=os.path.join(path,'opensubtitlesOfficial.zip')
		try: os.remove(lib)
		except: pass
		downloader.download(url,lib,dp)
		if filetype=='addon':
			addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
		time.sleep(2)
		extract.all(lib,addonfolder,'')
		xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
		addon_able.set_enabled("service.subtitles.opensubtitles_by_opensubtitles")
		dialog = xbmcgui.Dialog();
		dialog.ok("Installation Complete!", "    We hope you enjoy your Kodi addon experience!",
				  "    Brought To You By %s " % siteTitle)
#################################################################
def DEPENDINSTALL(name,url,description,filetype,repourl):
		#Split Script Depends============================
		files=url.split('/'); dependname=files[-1:]; dependname=str(dependname);
		dependname=dependname.replace('[','').replace(']','').replace('"','').replace('[','').replace("'",'').replace(".zip",'');
		#StoprSplit======================================
		path=xbmc.translatePath(os.path.join('special://home','addons','packages')); dp=xbmcgui.DialogProgress();
		dp.create("Configuring Requirements:","Downloading and ",'','Installing '+name);
		lib=os.path.join(path,name+'.zip');
		try: os.remove(lib)
		except: pass
		downloader.download(url,lib,dp)
		if filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
		time.sleep(2)
		#dp.update(0,"","Installing selections.....")
		print '======================================='; print addonfolder; print '======================================='
		extract.all(lib,addonfolder,'')
		#Start Script Depend Search==================================================================
		depends=xbmc.translatePath(os.path.join('special://home','addons',dependname,'addon.xml'));
		source=open(depends,mode='r'); link=source.read(); source.close();

		dmatch=re.compile('import addon="(.+?)"').findall(link)
		for requires in dmatch:
			if not 'xbmc.python' in requires:
				#kodi.log('Script Requires --- '+requires)
				dependspath=xbmc.translatePath(os.path.join('special://home','addons',requires))
				if not os.path.exists(dependspath): DEPENDINSTALL(requires,indigo_url2+'installer/dependencies/'+requires+'.zip','','addon','none')
				xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
				addon_able.set_enabled(requires)
		#kodi.log("Creating enable for "+name)
		addon_able.set_enabled(name)
		#End Script Depend Search======================================================================
def ADDONINSTALL(name,url,description,filetype,repourl,Auto=False,v='',vO=''):
  #kodi.log("HERE IS THE INSTALL PROCESS")
  try: name=name.split('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]')[1].split('[/COLOR][COLOR FF0077D7] (v')[0]
  except: pass
  #Start Depend Setup================================================================================
  newfile='-'.join(url.split('/')[-1].split('-')[:-1]); ##folder=newfile.split('/');
  addonname=str(newfile).replace('[','').replace(']','').replace('"','').replace('[','').replace("'",'');
  #kodi.log('newfile'+newfile+'addonname'+addonname);

  print 'SOURCE FILE IS '+addonname;
  #End of Depend Setup==================================================================================
  path=xbmc.translatePath(os.path.join('special://home','addons','packages')); vTag='';
  if len(v)  > 0: vTag+=" v"+v
  if len(vO) > 0: vTag+=" [local v"+vO+"]"
  confirm=xbmcgui.Dialog().yesno("Please Confirm","                Do you wish to install the chosen add-on and","                        its respective repository if needed?              ","              ","Cancel","Install")
  #if Auto==True: confirm=True
  if confirm:
		dp=xbmcgui.DialogProgress()
		dp.create("Download Progress:","Downloading your selection ",'','Please Wait')
		lib=os.path.join(path,name+'.zip')
		try: os.remove(lib)
		except: pass
		downloader.download(url,lib,dp)
		if   filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
		elif filetype=='media': addonfolder=xbmc.translatePath(os.path.join('special://','home'))
		elif filetype=='main':  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
		time.sleep(2)
		extract.all(lib,addonfolder,dp)
		try:
			#Start Addon Depend Search==================================================================
			depends=xbmc.translatePath(os.path.join('special://home','addons',addonname,'addon.xml'));
			source=open(depends,mode='r'); link=source.read(); source.close();
			dmatch=re.compile('import addon="(.+?)"').findall(link)
			for requires in dmatch:
				if not 'xbmc.python' in requires:
					print 'Requires --- '+requires; dependspath=xbmc.translatePath(os.path.join('special://home/addons',requires));
					print dependspath
					if not os.path.exists(dependspath): DEPENDINSTALL(requires,indigo_url2+'installer/dependencies/'+requires+'.zip','','addon','none')
		except: traceback.print_exc(file=sys.stdout)
			#End Addon Depend Search======================================================================
		if  'none' not in repourl:
			path=xbmc.translatePath(os.path.join('special://home/addons','packages')); dp=xbmcgui.DialogProgress();
			dp.create("Updating Repo if needed:","Configuring Installation ",'',' ');
			lib=os.path.join(path,name+'.zip')
			#kodi.log("REPO TO INSTALL IS  "+repourl)
			files=repourl.split('/')
			dependname=files[-1:]
			dependname=str(dependname)
			reponame=dependname.split('-')
			#print reponame
			nextname = reponame[:-1]
			#print nextname
			nextname=str(nextname).replace('[','').replace(']','').replace('"','').replace('[','').replace("'",'').replace(".zip",'');
			#print nextname
			#kodi.log("REPO TO ENABLE IS  "+nextname)
			try: os.remove(lib)
			except: pass
			downloader.download(repourl, lib, '')
			if   filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home/addons'))
			elif filetype=='media': addonfolder=xbmc.translatePath(os.path.join('special://','home'))
			elif filetype=='main':  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
			time.sleep(2)
			#dp.update(0,"","Checking Installation......")
			extract.all(lib,addonfolder,dp);
			xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
			addon_able.set_enabled(nextname)
			addon_able.set_enabled(addonname)

			dialog=xbmcgui.Dialog()
			if Auto==True: Note("Installation Complete!",name+" "+v+" Installed")
			else: dialog.ok("Installation Complete!","    We hope you enjoy your Kodi addon experience!","    Brought To You By %s "% siteTitle)
		else:
			xbmc.executebuiltin("XBMC.UpdateLocalAddons()");
			addon_able.set_enabled(addonname)
			dialog=xbmcgui.Dialog();
			if Auto==True: Note("Success!",name+" "+v+" Installed")
			else: dialog.ok("Installation Complete!","     We hope you enjoy your Kodi addon experience!","    Brought To You By %s "% siteTitle)
		'''confirm=xbmcgui.Dialog().yesno("Installation Complete!","                Please Restart To Take Effect","                        Brought To You By %s              "% siteTitle,"                    ","Later","Restart")
		if confirm: xbmc.executebuiltin('Quit')
		else: pass'''
  else: return
#****************************************************************
def set_content(content):
	xbmcplugin.setContent(int(sys.argv[1]), content)




# HELPDIR**************************************************************
def addDir(name,url,mode,thumb):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name); ok=True;
		liz=xbmcgui.ListItem(name,iconImage=iconart,thumbnailImage=thumb);
		#liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description})
		try: liz.setProperty("fanart_image",fanart)
		except: pass
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True); return ok
def addHELPDir(name,url,mode,iconimage,fanart,description,filetype,repourl,version,author,contextmenuitems=[],contextreplace=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)+"&repourl="+urllib.quote_plus(repourl)+"&author="+urllib.quote_plus(author)+"&version="+urllib.quote_plus(version);  ok=True;
		liz=xbmcgui.ListItem(name,iconImage=iconart,thumbnailImage=iconimage); #"DefaultFolder.png"
		#if len(contextmenuitems) > 0:
		liz.addContextMenuItems(contextmenuitems,replaceItems=contextreplace)
		liz.setInfo(type="Video",infoLabels={"title":name,"plot":description});
		liz.setProperty("fanart_image",fanart); liz.setProperty("Addon.Description",description); liz.setProperty("Addon.Creator",author); liz.setProperty("Addon.Version",version)
		#properties={'Addon.Description':meta["plot"]}
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False); return ok
def add2HELPDir(name,url,mode,iconimage,fanart,description,filetype,contextmenuitems=[],contextreplace=False):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype); ok=True;
		liz=xbmcgui.ListItem(name,iconImage=iconart,thumbnailImage=iconimage);
		#if len(contextmenuitems) > 0:
		liz.addContextMenuItems(contextmenuitems,replaceItems=contextreplace)
		liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description});
		liz.setProperty("fanart_image",fanart);
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True); return ok
#****************************************************************
def _get_keyboard(default="",heading="",hidden=False): #Start Ketboard Function
	""" shows a keyboard and returns a value """
	keyboard=xbmc.Keyboard(default,heading,hidden ); keyboard.doModal()
	if (keyboard.isConfirmed()): return unicode(keyboard.getText(),"utf-8")
	return default
def SEARCHADDON(url): #Start Search Function
	searchUrl=url; vq=_get_keyboard(heading="Search add-ons")
	if (not vq): return False,0 # if blank or the user cancelled the keyboard, return
	title=urllib.quote_plus(vq); searchUrl+=title+'&criteria=title'; print "Searching URL: "+searchUrl; List_Addons(searchUrl); viewsetter.set_view("sets")
#****************************************************************
def get_params():
	param=[]; paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]; cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&'); param={}
		for i in range(len(pairsofparams)):
			splitparams={}; splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
	return param
params=get_params(); url=None; name=None; mode=None; year=None; imdb_id=None
def grbPrm(n):
	try:    return urllib.unquote_plus(params[n])
	except: return ''
url=grbPrm("url"); filetype=grbPrm("filetype"); iconimage=grbPrm("iconimage"); fanart=grbPrm("fanart"); description=grbPrm("description"); name=grbPrm("name"); repourl=grbPrm("repourl"); author=grbPrm("author"); version=grbPrm("version");
try:		mode=urllib.unquote_plus(params["mode"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
#****************************************************************
#if mode==None or url==None or len(url)<1: STATUSCATS()



######################KEYMAP INSTALLER####################
def keymaps():
	#xbmc.executebuiltin("Container.Refresh")
	link = OPEN_URL(Keymaps_URL).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(link)
	if os.path.isfile(KEYBOARD_FILE):
		kodi.addDir("Remove Current Keymap Configuration",'','uninstall_keymap',artwork+'unkeymap.png')
		#Common.addItem('[COLOR white][B]Remove Current Keymap Configuration[/B][/COLOR]',BASEURL,128,ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		kodi.addDir(name,url,'install_keymap',artwork+'keymapadd.png')
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		#bname = " - [COLOR lightskyblue][COLOR white]This Week - [/COLOR][B]" + str(Common.count_advanced(name)) + "[/B][/COLOR]"
		#Common.addItem(name + bname,url,130,ADVANCED_SET_ICON,FANART,description)
	#xbmc.executebuiltin("Container.Refresh")
	viewsetter.set_view("files")


def install_keymap(name,url):

	#KEYBOARD_FILE       =  xbmc.translatePath(os.path.join('special://home/userdata/keymaps/','keyboard.xml'))
	if os.path.isfile(KEYBOARD_FILE):
		try:
			os.remove(KEYBOARD_FILE)
		except: pass
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	path_key = xbmc.translatePath(os.path.join('special://home/userdata','keymaps'))
	if not os.path.exists(path_key):
		os.makedirs(path_key)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create("Keymap Installer","","","[B]Keymap: [/B]" + buildname)
	buildname = "customkeymap"
	lib=os.path.join(path, buildname+'.zip')

	try:
		os.remove(lib)
	except:
		pass

	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Installing Please wait..","")
	#unzip(lib,addonfolder,dp)
	extract.all(lib,addonfolder,dp);
	time.sleep(1)
	#add_download = Common.add_one_advanced(name)
	try:
		os.remove(lib)
	except:
		pass

	xbmc.executebuiltin("Container.Refresh")
	dialog.ok("Custom Keymap Installed!","     We hope you enjoy your Kodi addon experience!","    Brought To You By %s "% siteTitle)

def uninstall_keymap():
	dialog = xbmcgui.Dialog()
	try:
		os.remove(KEYBOARD_FILE)
	except:
		pass

	dialog.ok("Indigo", "[B][COLOR white]Success, we have removed the keyboards.xml file.[/COLOR][/B]",'[COLOR white]Thank you for using Indigo[/COLOR]')
	#xbmc.executebuiltin("Container.Refresh")


def libinstaller(name,url):


	if "Android" in name:
		if not xbmc.getCondVisibility('system.platform.android'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - Android", "[B][COLOR white]Sorry, this file is only for Android devices[/COLOR][/B]",'')
			sys.exit(1)
		else:
			name = "librtmp.so"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "Windows" in name:
		if not xbmc.getCondVisibility('system.platform.windows'):
			dialog = xbmcgui.Dialog()
			dialog.ok( AddonTitle + " -Windows", "[B][COLOR white]Sorry, this file is only for Windows devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.dll"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "Linux" in name:
		if not xbmc.getCondVisibility('system.platform.linux'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - Linux", "[B][COLOR white]Sorry, this file is only for Linux devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.so.1"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "OSX" in name:
		if not xbmc.getCondVisibility('system.platform.osx'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - MacOSX", "[B][COLOR white]Sorry, this file is only for MacOSX devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "TV" in name:
		if not xbmc.getCondVisibility('system.platform.atv2'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - ATV", "[B][COLOR white]Sorry, this file is only for ATV devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "iOS" in name:
		if not xbmc.getCondVisibility('system.platform.ios'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - iOS", "[B][COLOR white]Sorry, this file is only for iOS devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)

	if "RPi" in name:
		if not xbmc.getCondVisibility('system.platform.rpi'):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle + " - RPi", "[B][COLOR white]Sorry, this file is only for RPi devices[/COLOR][/B]",'')
			return
		else:
			name = "librtmp.1.so"
			path = xbmc.translatePath(os.path.join('special://home',''))
			make_lib(path,name)


def make_lib(path,name):
	AddonTitle = "Indigo Installer"
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","")
	lib=os.path.join(path, name)
	try:
		os.remove(lib)
	except:
		pass
	downloader.download(url, lib, dp)
	dialog = xbmcgui.Dialog()
	dialog.ok(AddonTitle, "[COLOR gold]Download complete, File can be found at: [/COLOR][COLOR blue]" + lib + "[/COLOR]")


