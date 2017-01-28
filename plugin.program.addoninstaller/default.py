# TVADDONS.ag / TVADDONS.ag - Addon Installer - Module By: Blazetamer (2013-2014)
# Thanks to Blazetamer, Eleazar Coding, Showgun,  ....
siteTitle="TVADDONS.AG"; #siteTitle="XBMCHUB.COM";
addon_id='plugin.program.addoninstaller'; import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil,downloader,extract
base_url2='http://addons.tvaddons.ag'; #'http://addons.xbmchub.com'
tribeca_url2='http://tribeca.tvaddons.ag/tools/'; #tribeca_url2='http://tribeca.xbmchub.com/tools/';
tribeca_url=tribeca_url2+'installer/sources/'; base_url=base_url2+'/';
import traceback,sys

try: 			from addon.common.addon 	import Addon
except:
    try: 		from t0mm0.common.addon import Addon
    except: from t0mm0_common_addon import Addon
addon=Addon(addon_id,sys.argv)
try: 			from addon.common.net 	import Net
except:
    try: 		from t0mm0.common.net import Net
    except: from t0mm0_common_net import Net
net=Net(); settings=xbmcaddon.Addon(id=addon_id); ADDON=xbmcaddon.Addon(id=addon_id);
artPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art2/'));
def getArtwork(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2',n))
def getArtworkJ(n): return xbmc.translatePath(os.path.join('special://home','addons',addon_id,'art2',n+'.jpg'))
def catArtwork(n): return 'http://addons.tvaddons.ag/images/categories/%s.png'%n

mainPath=xbmc.translatePath(os.path.join('special://home','addons',addon_id));
fanart=xbmc.translatePath(os.path.join(mainPath,'fanart.jpg')); #fanart=artPath+'fanart.jpg'; #fanart=xbmc.translatePath(os.path.join('special://home','addons',addon_id+'/'))+'fanart.jpg'; #fanart=getArtworkJ('fanart')
iconart=xbmc.translatePath(os.path.join(mainPath,'icon.png')); #print ['fanart',fanart,'iconart',iconart];
TxtAddonUpdater='Addon Updater'; ImgAddonUpdater=getArtworkJ('autoupdater');
#****************************************************************
def MAININDEX():
    hubpath=xbmc.translatePath(os.path.join('special://home','addons','repository.xbmchub'))
    hubnotespath=xbmc.translatePath(os.path.join('special://home','addons','plugin.program.xbmchub.notifications'))
    try:
        if not os.path.exists(hubpath): HUBINSTALL('TVADDONS.AG.Repository','http://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.6.zip','','addon','none')
        if not os.path.exists(hubnotespath): HUBINSTALL('TVADDONS.AG.Notifications','http://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/plugin.program.xbmchub.notifications/plugin.program.xbmchub.notifications-1.0.2.zip','','addon','none')
    except: pass
    addDir('Search by: Addon/Author',base_url+'search/?keyword=','searchaddon',getArtworkJ('Search')) #catArtwork('webinterface')) #
    #if settings.getSetting('newest')=='true':  addDir('Newest Addons',base_url,'innertabs',getArtworkJ('NewestAddons'))
    #if settings.getSetting('updated')=='true':  addDir('Recently Updated',base_url,'innertabs',getArtworkJ('RecentlyUpdated'))
    #if settings.getSetting('toprepositories')=='true':  addDir('Top Developers',base_url,'toprepolist',getArtworkJ('TopDevs'))
    if settings.getSetting('featured')=='true':       	addDir('Featured Addons',base_url+'category/featured/','addonlist',getArtworkJ('Featuredaddons')) #catArtwork('featured')) #
    if settings.getSetting('video')=='true':          	addDir('Video Addons',base_url+'category/video/','addonlist',getArtworkJ('VideoAddons')) #catArtwork('video')) #
    if settings.getSetting('audio')=='true':          	addDir('Audio Addons',base_url+'category/audio/','addonlist',getArtworkJ('AudioAddons')) #catArtwork('audio')) #
    #if settings.getSetting('picture')=='true':        	addDir('Picture Addons',base_url+'category/pictures/','addonlist',getArtworkJ('PictureAddons')) #catArtwork('pictures')) #
    if settings.getSetting('program')=='true':        	addDir('Program Addons',base_url+'category/programs/','addonlist',getArtworkJ('ProgramAddons')) #catArtwork('programs')) #
    if settings.getSetting('services')=='true':       	addDir('Service Addons',base_url+'category/services/','addonlist',getArtworkJ('ServiceAddons')) #catArtwork('services')) #
    if settings.getSetting('repositories')=='true':   	addDir('Repositories',base_url+'category/repositories/','addonlist',getArtworkJ('Repositories')) #catArtwork('repositories')) #
    #if settings.getSetting('world')=='true':          	addDir('World Section',tribeca_url+'world.php','worldlist',getArtworkJ('WorldSection')) #catArtwork('metadata')) #
    if settings.getSetting('world')=='true':          	addDir('World Section',base_url+'category/international/repositories','interlist',getArtworkJ('WorldSection')) #catArtwork('video')) #
    if settings.getSetting('adult')=='true':          	addDir('Adult Addons',tribeca_url+'xxx.php','adultlist',getArtworkJ('AdultAddons')) #catArtwork('pictures')) #

    ForPrimeWire();
    #addDir(TxtAddonUpdater,base_url+'category/featured/','autoupdate',ImgAddonUpdater);
    ##addDir(TxtAddonUpdater,'...','autoupdate2',ImgAddonUpdater);
    addDir('Installer Settings','none','settings',getArtworkJ('InstallerSettings')); #catArtwork('programs')) #
    AUTO_VIEW('addons')
#****************************************************************

#********************************************************************
def INTERNATIONAL(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url); match=GetListItems(link); CMi=[]; #AUTO_VIEW('list');
    #CMi.append(['Information',"XBMC.Action(Info)"]);
    if 'repository' in url: ToMode='interrepolist'
    else: ToMode='addonlist'
    for url,image,name, in match: iconimage=base_url+image; add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
    nmatch=GetListNextPage(link);
    if len(nmatch) > 0: addDir('Next Page',(nmatch[0]),'interrepolist',getArtworkJ('NextPage'))
    AUTO_VIEW('list')
    return

def nolines(t): return t.replace('\r','').replace('\n','').replace('\t','').replace('\a','')
def ForPrimeWire():
    html=nolines(OPEN_URL(tribeca_url2+'wizard/links.txt')); #print html
    if ("1CHANNEL" in html.upper()):
        match=re.compile('name="(1CHANNEL.*?)"\s*url="(.+?)"\s*img="(.+?)"\s*fanart="(.+?)"', re.IGNORECASE).findall(html)[0]; #print match
        if len(match) > 0: (name2,url2,img2,fanart2)=match; addDir(name2,url2,'WizardTypeInstaller',img2);
def WizardTypeInstaller(name,url): MyAddonInstaller(name,url,xbmc.translatePath(os.path.join('special://','home')))
def AddonTypeInstaller(name,url): MyAddonInstaller(name,url,xbmc.translatePath(os.path.join('special://','home','addons')))
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
    try: return re.compile('"page last" href="(.+?)"><dfn title="next Page">').findall(link)
    except: return []
def List_Addons_Inner_Tabs(Name,url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url); print 'url:  '+url; print  'length of html:  '+str(len(link));
    if   'newest'  in Name.lower(): link=link.split('<div class="tabs-inner" id="newest">' )[-1].split('</div>')[0]
    elif 'updated' in Name.lower(): link=link.split('<div class="tabs-inner" id="updated">')[-1].split('</div>')[0]
    match=re.compile("<li><a href='(.+?)'><img src='(.+?)' width='60' height='60' alt='(.+?)' class='pic alignleft' /><b>\s*(.+?)\s*</b></a><span class='date'>\s*(\d\d\d\d-\d\d-\d\d)\s*</span></li").findall(link)
    for url,image,name,name2,released in match: iconimage=base_url+image; add2HELPDir('[COLOR FF0077D7]%s [COLOR FFFFFFFF][[COLOR FFFFFFFF]%s[/COLOR]][/COLOR][/COLOR]'%(name,released),url,'addonindex',iconimage,fanart,'','addon')
    AUTO_VIEW('list')

def List_Inter_Addons(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url); match=GetListItems(link); CMi=[]; #AUTO_VIEW('list');
    #CMi.append(['Information',"XBMC.Action(Info)"]);
    if '/category/repositories/' in url: ToMode='addonlist'
    else: ToMode='addonindex'
    for url,image,name, in match: iconimage=base_url+image; add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
    nmatch=GetListNextPage(link);
    if len(nmatch) > 0: addDir('Next Page',(nmatch[0]),'addonlist',getArtworkJ('NextPage'))
    AUTO_VIEW('list')


def List_Addons(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url); match=GetListItems(link); CMi=[]; #AUTO_VIEW('list');
    #CMi.append(['Information',"XBMC.Action(Info)"]);
    if '/category/repositories/' in url: ToMode='addonlist'
    else: ToMode='addonindex'
    for url,image,name, in match: iconimage=base_url+image; add2HELPDir(name,url,ToMode,iconimage,fanart,'','addon',CMi,True)
    nmatch=GetListNextPage(link);
    if len(nmatch) > 0: addDir('Next Page',(nmatch[0]),'addonlist',getArtworkJ('NextPage'))
    AUTO_VIEW('addons')
    #AUTO_VIEW('list')
def List_Repo_Top_Developers(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url); print 'url:  '+url; #print link; #return
    try: link=link.split('<span class="sidebar-widget-header"><h3 class="sidebar-widget-header">Top developers</h3></span>')[-1]; link=link.split('</ul>')[0];
    except: pass
    match=re.compile("<li><img src='(.+?)' height='20' width='20' alt='(.+?)' /><a href='(.+?)' title='Show all addons from this author'>\s*(.+?)\s+\((\d+)\s+uploads\)</a></li").findall(link.replace('</li>','</li\n\r\a>')); #print match
    for (image,rank,url,name,uploads) in match: iconimage=base_url+image; add2HELPDir("[COLOR FF0077D7]%s [COLOR FFFFFFFF][[COLOR FFFFFFFF]%s[/COLOR]][/COLOR][/COLOR]"%(name,uploads),url,'addonlist',iconimage,fanart,'','addon')
    AUTO_VIEW('list')
#****************************************************************
def List_Tribeca_WorldAlone(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
    match=re.compile("'name' => '(.+?)','language' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
    if len(match)==0: return
    for name,lang,dload in match: lang=lang.capitalize(); addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon','none','','')
    #AUTO_VIEW('list',50)
def List_Tribeca_WorldList(url):
    if not '://' in url: url=base_url2+url
    link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
    match=re.compile("'name' => '(.+?)','language' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link)
    AUTO_VIEW('list')
    if len(match)==0: return
    for name,lang,dload in match: lang=lang.capitalize(); addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon','none','','')
    List_Tribeca_WorldAlone(tribeca_url+'world-solo.php')
    AUTO_VIEW('list',50)
def List_Tribeca_Adult(url):
    link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','');
    match=re.compile("'name' => '(.+?)'.+?downloadUrl' => '(.+?)'").findall(link);
    if len(match)==0: return
    for name,dload in match: lang='Adults Only'; addHELPDir(name+' ('+lang+')',dload,'addoninstall','',fanart,'','addon','none','','')
    AUTO_VIEW('list',50)
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
    #CMi.append(['Information',"XBMC.Action(Info)"])
    CMi.append(['Check Others by %s'%author,"XBMC.Container.Update(plugin://%s/?mode=addonlist&url=%s)"%(addon_id,aurthorUrl)])
    #CMi.append(['*Check Others by %s'%author,"XBMC.Container.Update(%s)"%(addon.build_plugin_url({'mode':'addonlist','url':aurthorUrl}))])
    CMi.append(['Visit Page',"XBMC.Container.Update(plugin://%s/?mode=BrowseUrl&url=%s)"%(addon_id,urllib.quote_plus(url))])
    if len(forumUrl) > 0: CMi.append(['Visit Forum',"XBMC.Container.Update(plugin://%s/?mode=BrowseUrl&url=%s)"%(addon_id,urllib.quote_plus(forumUrl))])
    #print CMi
    addHELPDir('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]%s[/COLOR][COLOR FF0077D7] (v%s) [%s][/COLOR] [COLOR FF0077D7][I]by[/I][/COLOR]  [COLOR FFFFFFFF]%s[/COLOR]'%(name,version,releaseddate,author),addonurl,'addoninstall',iconimage,ifanart,description,'addon',repourl,version,author,CMi,True);
    AUTO_VIEW('addons')
#****************************************************************
def Note(header="",message="",sleep=5000): xbmc.executebuiltin("XBMC.Notification(%s,%s,%i)" % (header,message,sleep))
def File_Save(path,data): file=open(path,'w'); file.write(data); file.close()
def File_Open(path):
    if os.path.isfile(path): file=open(path, 'r'); contents=file.read(); file.close(); return contents ## File found.
    else: return '' ## File not found.
def OPEN_URL(url):
    try: req=urllib2.Request(url); req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'); response=urllib2.urlopen(req); link=response.read(); response.close(); return link
    except: return ""
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
        try: url=FireDrive(url)
        except: print "error in FireDrive() function."
        path=xbmc.translatePath(os.path.join('special://home','addons','packages')); dp=xbmcgui.DialogProgress();
        dp.create("First Launch:","Creating Database ",'','Only Shown on First Launch');
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url,lib,dp)
        if filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
        time.sleep(2)
        #dp.update(0,"","Installing selections.....")
        print '======================================='; print addonfolder; print '=======================================';
        extract.all(lib,addonfolder,'')
#****************************************************************
def DEPENDINSTALL(name,url,description,filetype,repourl):
        #Split Script Depends============================
        files=url.split('/'); dependname=files[-1:]; dependname=str(dependname);
        dependname=dependname.replace('[','').replace(']','').replace('"','').replace('[','').replace("'",'').replace(".zip",'');
        #StoprSplit======================================
        path=xbmc.translatePath(os.path.join('special://home','addons','packages')); dp=xbmcgui.DialogProgress();
        dp.create("Configuring Requirments:","Downloading and ",'','Installing '+name);
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
                print 'Script Requires --- '+requires;
                dependspath=xbmc.translatePath(os.path.join('special://home','addons',requires))
                #if not os.path.exists(dependspath): DEPENDINSTALL(requires,'http://addonrepo.com/xbmchub/depends/'+requires+'.zip','','addon','none')
                if not os.path.exists(dependspath): DEPENDINSTALL(requires,tribeca_url2+'maintenance/modules/'+requires+'.zip','','addon','none')
        #End Script Depend Search======================================================================
def ADDONINSTALL(name,url,description,filetype,repourl,Auto=False,v='',vO=''):
  print ['name',name,'url',url,'description',description,'filetype',filetype,'repourl',repourl,'Auto',Auto,'v',v,'vO',vO];
  try: name=name.split('[COLOR FF0077D7]Install [/COLOR][COLOR FFFFFFFF]')[1].split('[/COLOR][COLOR FF0077D7] (v')[0]
  except: pass
  #Start Depend Setup================================================================================
  print 'Installing Url is '+url; ##addonfile=url.split('-');
  newfile='-'.join(url.split('/')[-1].split('-')[:-1]); ##folder=newfile.split('/');
  addonname=str(newfile).replace('[','').replace(']','').replace('"','').replace('[','').replace("'",'');
  print ['newfile',newfile,'addonname',addonname];

  print 'SOURCE FILE IS '+addonname;
  #End of Depend Setup==================================================================================
  path=xbmc.translatePath(os.path.join('special://home','addons','packages')); vTag='';
  if len(v)  > 0: vTag+=" v"+v
  if len(vO) > 0: vTag+=" [local v"+vO+"]"
  confirm=xbmcgui.Dialog().yesno("Please Confirm","                Do you wish to install the chosen add-on and","                        its respective repository if needed?              ","              "+name+vTag,"Cancel","Install")
  #if Auto==True: confirm=True
  if confirm:
        dp=xbmcgui.DialogProgress(); dp.create("Download Progress:","Downloading your selection ",'','Please Wait');
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url,lib,dp)
        if   filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
        elif filetype=='media': addonfolder=xbmc.translatePath(os.path.join('special://','home'))
        elif filetype=='main':  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        #dp.update(0,"","Installing selections.....")
        print '======================================='; print addonfolder; print '=======================================';
        extract.all(lib,addonfolder,dp)
        try:
            #Start Addon Depend Search==================================================================
            depends=xbmc.translatePath(os.path.join('special://home','addons',addonname,'addon.xml'));
            source=open(depends,mode='r'); link=source.read(); source.close();
            dmatch=re.compile('import addon="(.+?)"').findall(link)
            for requires in dmatch:
                if not 'xbmc.python' in requires:
                    print 'Requires --- '+requires; dependspath=xbmc.translatePath(os.path.join('special://home/addons',requires));
                    #if not os.path.exists(dependspath): DEPENDINSTALL(requires,'http://addonrepo.com/xbmchub/depends/'+requires+'.zip','','addon','none')
                    print dependspath
                    if not os.path.exists(dependspath): DEPENDINSTALL(requires,tribeca_url2+'maintenance/modules/'+requires+'.zip','','addon','none')
        except: traceback.print_exc(file=sys.stdout)
            #End Addon Depend Search======================================================================
        #dialog=xbmcgui.Dialog()
        #dialog.ok("Success!","Please Reboot To Take Effect","    Brought To You By %s "% siteTitle)
        ## #start repo dl# ##
        if  'none' not in repourl:
            path=xbmc.translatePath(os.path.join('special://home/addons','packages')); dp=xbmcgui.DialogProgress();
            dp.create("Updating Repo if needed:","Configuring Installation ",'',' ');
            lib=os.path.join(path,name+'.zip')
            try: os.remove(lib)
            except: pass
            downloader.download(repourl, lib, '')
            if   filetype=='addon': addonfolder=xbmc.translatePath(os.path.join('special://','home/addons'))
            elif filetype=='media': addonfolder=xbmc.translatePath(os.path.join('special://','home'))
            elif filetype=='main':  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(2)
            #dp.update(0,"","Checking Installation......")
            print '======================================='; print addonfolder; print '======================================='
            extract.all(lib,addonfolder,dp);
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()");
            dialog=xbmcgui.Dialog();
            if Auto==True: Note("Success!",name+" "+v+" Installed")
            else: dialog.ok("Success!","    Your Selection(s) Have Been Installed.","    Brought To You By %s "% siteTitle)
        else:
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()");
            dialog=xbmcgui.Dialog();
            if Auto==True: Note("Success!",name+" "+v+" Installed")
            else: dialog.ok("Success!","     Your Selections Have Been Installed","    Brought To You By %s "% siteTitle)
        '''confirm=xbmcgui.Dialog().yesno("Success!","                Please Restart To Take Effect","                        Brought To You By %s              "% siteTitle,"                    ","Later","Restart")
        if confirm: xbmc.executebuiltin('Quit')
        else: pass'''
  else: return
#****************************************************************
def AUTO_VIEW(content='',viewmode=''): # Set View
     viewmode=str(viewmode); content=str(content);
     if len(viewmode)==0:
         if settings.getSetting('auto-view')=='true':
             if content=='addons':  viewmode=settings.getSetting('addon-view')
             if content=='list':  viewmode=settings.getSetting('list-view')
             else:                  viewmode=settings.getSetting('default-view')
         else: viewmode='500'
     if len(content) > 0: xbmcplugin.setContent(int(sys.argv[1]),str(content))
     #if settings.getSetting('auto-view')=='true': xbmc.executebuiltin("Container.SetViewMode(%s)" % str(viewmode))
     if len(viewmode) > 0: xbmc.executebuiltin("Container.SetViewMode(%s)" % str(viewmode))
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
	title=urllib.quote_plus(vq); searchUrl+=title+'&criteria=title'; print "Searching URL: "+searchUrl; List_Addons(searchUrl); AUTO_VIEW('list') # we need to set the title to our query
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
if mode==None or url==None or len(url)<1: MAININDEX()
try:
	if url: print url
except: pass
if   mode=='settings':  			addon.show_settings()																		# Settings
elif mode=='autoupdate': 			items=AutoUpdate(url) 																	#
elif mode=='autoupdate2': 		 																												# Featured
	AutoUpdate(tribeca_url+'featured-addons.php')
	AutoUpdate(tribeca_url+'featured-repos.php')
elif mode=='interrepolist': 			items=List_Inter_Addons(url)
elif mode=='interlist': 			items=INTERNATIONAL(url)
elif mode=='innertabs': 			items=List_Addons_Inner_Tabs(name,url)									# Newest / Updated
elif mode=='addonlist': 			items=List_Addons(url)																	# List Addons
elif mode=='worldlist': 			items=List_Tribeca_WorldList(url)												# World Addons - Temp
elif mode=='toprepolist': 		items=List_Repo_Top_Developers(url)											# Top Devs
elif mode=='searchaddon': 		SEARCHADDON(url)																				# Search
elif mode=='addonindex': 			ADDONINDEX(name,url,filetype)														# Right Before Installing Addon(s)
elif mode=='addoninstall': 		ADDONINSTALL(name,url,description,filetype,repourl)			# Installing Addon(s)
elif mode=='adultlist': 			items=List_Tribeca_Adult(url)														# Adult Addons - Temp
elif mode=='WizardTypeInstaller': 	WizardTypeInstaller(name,url)											#
elif mode=='AddonTypeInstaller': 		AddonTypeInstaller(name,url)											#
elif mode=='dependinstall': 	DEPENDINSTALL(name,url,description,filetype,repourl)		# Dependancies
elif mode=='BrowseUrl': 			xbmc.executebuiltin("XBMC.System.Exec(%s)" % url)				#
xbmcplugin.endOfDirectory(int(sys.argv[1]))
