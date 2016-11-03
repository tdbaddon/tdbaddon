#-*- coding: utf-8 -*-

import sys, urllib, urllib2, re, cookielib, os.path, json, base64, tempfile, time, threading, png, math, socket
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs
from jsunpack import unpack
import search
import urlresolver
from packer import cPacker

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)
ADDON_VER="0.92.3"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
           'Accept': '*/*',
           'Connection': 'keep-alive'}

      
profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')       

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

libraryDir=xbmc.translatePath(xbmcaddon.Addon().getSetting('library_path'))
if not os.path.exists(libraryDir):
    os.makedirs(libraryDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

globalURLS=[]
statusDialog=""  
updateCounter=0  
updateBy=0 
updateTotal=0

if xbmcaddon.Addon().getSetting('proxy')=="true":
    siteURL="http://javstream.club/repress/javpop.com"
else:
    siteURL="http://javpop.com"
if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        try:
            cj.load(xbmc.translatePath(cookiePath))
        except:
            try:
                os.remove(xbmc.translatePath(cookiePath))
                pass
            except:
                dialog.ok('Oh oh','The Cookie file is locked, please restart Kodi')
                pass
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))


                                                       
                                                       
def parseParameters(inputString=sys.argv[2]):
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    inputString: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    
    
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            try:
                if (len(nameValuePair) > 0):
                    pair = nameValuePair.split('=')
                    key = pair[0]
                    value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                    parameters[key] = value
                    #logError(value)
            except:
                pass
    return parameters

def extractAll(text, startText, endText):
    """
    Extract all occurences of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns an array containing all occurences found, with tabs and newlines removed and leading whitespace removed
    """
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        pos = text.find(startText, end)
    return result

def extract(text, startText, endText):
    """
    Extract the first occurence of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns the string found between startText and endText, or None if the startText or endText is not found
    """
    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None      

def getURL(url, header=headers):
    try:
        req = urllib2.Request(url, headers=header)
            
        response = urllib2.urlopen(req, timeout=int(xbmcaddon.Addon().getSetting("timeout")))
        
        if response and response.getcode() == 200:
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO( response.read())
                gzip_f = gzip.GzipFile(fileobj=buf)
                content = gzip_f.read()
            else:
                content = response.read()
            content = content.decode('utf-8', 'ignore')
            return content
        else:
            xbmc.log('Error Loading URL : '+str(response.getcode()), xbmc.LOGERROR)
    except urllib2.HTTPError as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    except urllib2.URLError as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    except socket.timeout as err:
        logError('Error Loading URL : '+url.encode("utf-8"))
        logError(str(err))
    #    xbmc.log('Error Loading URL : '+url.encode("utf-8"), xbmc.LOGERROR)
    #    try:
    #        xbmc.log("Error Code: "+str(response.getcode())+' Content: '+response.read(), xbmc.LOGERROR)
    #    except:
    #        xbmc.log(str(response))
    
    return False

def postURL(url, payload):
    data = urllib.urlencode(payload)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    return response.read

    
def getHtml(url, referer, hdr=None, NoCookie=None, data=None):
    if not hdr:
        req = Request(url, data, headers)
    else:
        req = Request(url, data, hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    if data:
        req.add_header('Content-Length', len(data))
    response = urlopen(req, timeout=60)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        f.close()
    else:
        data = response.read()    
    if not NoCookie:
        # Cope with problematic timestamp values on RPi on OpenElec 4.2.1
        try:
            cj.save(cookiePath)
        except: pass
    response.close()
    return data
    
def addMenuItems(details, show=True, isFolder=True):
    changed=False
    for detail in details:
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].decode("utf-8"),"Plot": detail['plot']} )
        
        try:
            u=u+"&extras="+detail["extras"]
        except:
            pass
        try:
            u=u+"&extras2="+detail["extras2"]
        except:
            pass
        try:
            liz.setProperty("Fanart_Image", detail['fanart'])
            u=u+"&fanart="+detail['fanart']
        except:
            pass
        try:
            liz.setProperty("Landscape_Image", detail['landscape'])
            u=u+"&landscape="+detail['landscape']
        except:
            pass
        try:
            liz.setProperty("Poster_Image", detail['poster'])
            u=u+"&poster="+detail['poster']
        except:
            pass
        try:
            if detail['mode']==6:
                dwnld = (sys.argv[0] +
                    "?url=" + urllib.quote_plus(detail['url']) +
                    "&mode=" + str(9) +
                    "&poster="+detail['poster']+
                    "&extras="+detail['extras']+
                    "&download=" + str(1) +
                    "&fanart="+detail['fanart']+
                    "&name=" + urllib.quote_plus(detail['extras2'].encode('utf-8')))
                
                liz.addContextMenuItems([('Download Video', 'xbmc.RunPlugin('+dwnld+')')])
            if detail['mode']==5 and detail['extras']!="44":
                changed=True
                view = (sys.argv[0] +
                    "?url=set-default-view" +
                    "&mode=" + str(10) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+sysarg+
                    "&name=" + "set-default-view")
                #liz.addContextMenuItems([('Set Default View', 'xbmc.RunPlugin('+view+')')])
                save2library = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(11) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                save2bookmarks = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(12) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                liz.addContextMenuItems([('Set default view', 'xbmc.RunPlugin('+view+')'), ('Add to library', 'xbmc.RunPlugin('+save2library+')'), ('Add to JAVStream favourites', 'xbmc.RunPlugin('+save2bookmarks+')')])
            elif detail['mode']==5 and detail['extras']=="44":
                changed=True
                view = (sys.argv[0] +
                    "?url=set-default-view" +
                    "&mode=" + str(10) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+sysarg+
                    "&name=" + "set-default-view")
                #liz.addContextMenuItems([('Set Default View', 'xbmc.RunPlugin('+view+')')])
                save2library = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(11) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                deletebookmarks = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(14) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+"single-delete"+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                liz.addContextMenuItems([('Set default view', 'xbmc.RunPlugin('+view+')'), ('Add to library', 'xbmc.RunPlugin('+save2library+')'), ('Remove from JAVStream favourites', 'xbmc.RunPlugin('+deletebookmarks+')')])
        except:
            pass
        try:
            if detail["extras"]=="force-search" and detail["extras2"]=="db-search":
                dwnld = (sys.argv[0] +
                    "?url=" + urllib.quote_plus(detail['url']) +
                    "&mode=" + str(31) +
                    "&poster="+detail['poster']+
                    "&extras="+"single-delete"+
                    "&fanart="+detail['fanart']+
                    "&name=" + urllib.quote_plus(detail['title'].encode('utf-8')))
                liz.addContextMenuItems([('Delete Search Term', 'xbmc.RunPlugin('+dwnld+')')])
        except:
            pass
        #addContextItem(liz, "Add to favourites","special://home/addons/plugin.video.javstream2/addFavourite.py", "id=909722")
        #addContextItem(liz, "Add idol to favourites","special://home/addons/plugin.video.javstream2/addFavouriteIdol.py", "id=909722")
        if isFolder:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty('IsPlayable', 'true')
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    if show:
        if changed==True:
            xbmc.executebuiltin('Container.SetViewMode(%d)' % int(xbmcplugin.getSetting(int(sysarg), "vidview")))
        xbmcplugin.endOfDirectory(int(sysarg))

def alert(alertText):
    dialog = xbmcgui.Dialog()
    ret = dialog.ok("JAVStream", alertText)
    
def select(list):
    dialog = xbmcgui.Dialog()
    ret = dialog.select("JAVStream", list)
    return ret
        
def notify(addonId, message, reportError=False, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))
    if reportError:
        logError(message)

def logError(error):
    try:
        xbmc.log("JAVStream Error - "+str(error.encode("utf-8")), xbmc.LOGERROR)
    except:
        xbmc.log("JAVStream Error - "+str(error), xbmc.LOGERROR)
    
def searchDialog(searchText="Please enter search text") :    
    keyb=xbmc.Keyboard('', searchText)
    keyb.doModal()
    searchText=''
    
    if (keyb.isConfirmed()) :
        searchText = keyb.getText()
    if searchText!='':
        return searchText
    return False

def progressStart(title, status):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create(title, status)
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )
    progressUpdate(pDialog, 1, status)
    return pDialog

def progressStop(pDialog):
    pDialog.close
    
def progressCancelled(pDialog):
    if pDialog.iscanceled():
        pDialog.close
        return True
    return False

def progressUpdate(pDialog, progress, status):
    pDialog.update(int(progress), status)

def customDialog(imgW, imgH, img):
    cDialog=xbmcgui.WindowDialog()
    cWindow=xbmcgui.Window()
    #logError(cWindow.getResolution())
    cDialog.addControl(xbmcgui.ControlImage(x=cWindow.getWidth()/2, y=30, width=imgW, height=imgH, filename=img))
    cDialog.show()
    return cDialog

def customDialogClose(cDialog):
    cDialog.close()

def getIMAGE(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    try:
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req)
        if response and response.getcode() == 200:
            return response
    except:
        return "failed"
    
    return False
    
def addToLibrary(params):
    name=' '.join(params['name'].replace("'", " ").replace('"', " ").replace("/", "-").replace("\\", "-").encode('utf-8').split())
    toAdd=os.path.join(libraryDir, name.decode('utf-8'))
    if not os.path.isdir(toAdd.encode('utf-8')):
        #try:
        xbmcvfs.mkdir(toAdd.encode('utf-8'))
        file=os.path.join(toAdd.encode('utf-8'), "movie.strm")
        #f = open(file,'w')
        f =xbmcvfs.File (file, 'w')
        f.write(str('plugin://plugin.video.javstream/?extras='+params['extras']+'&fanart='+params['fanart']+'&icon='+params['poster']+'&mode=5&name='+urllib.quote_plus(params['name'].encode("utf-8"))+'&poster='+params['poster']+'&url='+params['url']+'&fromlibrary=true'))
        f.close() # you can omit in most cases as the destructor will call it
        
        genre=""
        if params['extras']=="40":
            genre="\n<genre>Censored</genre>"
        elif params['extras']=="41":
            genre="\n<genre>Uncensored</genre>"
        elif params['extras']=="42":
            genre="\n<genre>Gravure</genre>"
        
        nfo=os.path.join(toAdd.encode('utf-8'), "movie.nfo")
        #f = open(nfo,'w')
        f=xbmcvfs.File (nfo, 'w')
        f.write(str('<?xml version="1.0" encoding="utf-8"?>\n<movie>\n<title>'+params['name'].encode('utf-8')+'</title>\n<genre>JAV</genre>'+genre.encode('utf-8')+'\n</movie>'))
        f.close()
        
        
        #f = open(os.path.join(toAdd, "fanart.jpg"),'wb')
        f =xbmcvfs.File (os.path.join(toAdd.encode('utf-8'), "fanart.jpg"), 'w')
        f.write(getIMAGE(params['fanart']).read())
        
        #f = open(os.path.join(toAdd, "poster.jpg"),'wb')
        f =xbmcvfs.File (os.path.join(toAdd.encode('utf-8'), "poster.jpg"), 'w')
        f.write(getIMAGE(params['poster']).read())
        
        notify(ADDON_ID, "Video added to library", True, 2000)
        #except:
        #    notify(ADDON_ID, "Unable to add video to library")
        #    logError('Unable to add '+name)
        if xbmcaddon.Addon().getSetting('library_update')=='true':
            xbmc.executebuiltin('updateLibrary(video, %s)' % (libraryDir))
    else:
        notify(ADDON_ID, "Video already added to library", True, 2000)
        logError('Folder '+toAdd+' already exists')

def addToBookmarks(params):
    search.addBookmark(params['name'], params['poster'], params['fanart'], params['url'])
    notify(ADDON_ID, "Video added to bookmarks", True, 2000)

def showBookmarks(params):
    bookmarks=search.getBookmarks()
    #logError(bookmarks)
    items=[]
    if bookmarks:
        
        for bookmark in bookmarks:
            items.append({
                "title": bookmark[0],
                "url": bookmark[3], 
                "mode":5, 
                "poster":bookmark[1],
                "icon":bookmark[1], 
                "fanart":bookmark[2],
                "type":"video", 
                "plot":"",
                "extras":"44"
            })
    addMenuItems(items)
        
def findVideos(url, refresh=False):
    searching="0"
    if "category/censored" in url:
        searching="40"
    elif "category/uncensored" in url:
        searching="41"
    elif "category/idol" in url:
        searching="42"
    else:
        searching="43"
    
    html=getURL(url, hdr)
    if html!=False:
        if "No posts found" in html:
            notify(ADDON_ID, "No videos found.", True)
        else :
            items=[]
            bsObj=BeautifulSoup(html, "html.parser")
            
            for sibling in bsObj.find("div",{"class":"entry"}).ul.findChildren():
                try:
                    if "http://javpop.com" not in sibling.find("img")["src"]:
                        image="http://javstream.club"+sibling.find("img")["src"]
                    else:
                        image=sibling.find("img")["src"]
                except:
                    pass
                    
                    
                if sibling.name=="li":
                    items.append({
                        "title": translate(sibling.find("a")["title"]),
                        "url": sibling.find("a")["href"], 
                        "mode":5, 
                        "poster":image,
                        "icon":image, 
                        "fanart":image.replace("thumb", "poster"),
                        "type":"video", 
                        "plot":"",
                        "extras":searching
                    })
            try:
                p=re.compile("<a href=[\"|'](\S*)[\"|'] class=[\"|']nextpostslink[\"|']>")
                next=re.search(p, html).group(1)
                if "repress" in next:
                    next=siteURL+(next.replace("/repress/javpop.com", ""))
                items.append({
                        "title": "Next >",
                        "url":next, 
                        "mode":4, 
                        "poster":"default.jpg",
                        "icon":os.path.join(home, 'resources/media', str(searching)+'next.jpg'),
                        "fanart":"default.jpg",
                        "type":"", 
                        "plot":"",
                    })
            except:
                # no next page found
                pass
            addMenuItems(items)
                
    else:
        notify(ADDON_ID, "Unable to load page. If problem persist turn on Proxy within Settings", True)

def whatPlayer(url, site, dvdCode):
    try:
        global updateCounter
        global updateString
        global updateTotal
        
        if "<javpage=" in url:
            parts=url.split("<")
            url=parts[0]
            parts=parts[1].replace("javpage=", "")
            
        if "gaimup" in site:
            if "Caribbeancom" in dvdCode:
                url=url.replace("Caribbeancom", "Carib").replace("_", "-")
                dvdCode=dvdCode.replace("Caribbeancom", "Carib").replace("_", "-")
            elif "Heydouga" in dvdCode:
                url=url.replace("_", "-PPV")
                dvdCode=dvdCode.replace("_", "-PPV")
            elif "10musume" in dvdCode:
                url=url.replace("10musume", "10mu")
                dvdCode=dvdCode.replace("_", "-PPV")
            elif "Pacopacomama" in dvdCode:
                url=url.replace("Pacopacomama", "paco")
                dvdCode=dvdCodeurl.replace("Pacopacomama", "paco")
            elif "Muramura" in dvdCode:
                url=url.replace("Muremura", "Mura")
                dvdCode=dvdCode.replace("Muremura", "Mura")
        elif "streamingjav" in site:
            if "1Pondo" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20").replace("%22", "")
            elif "Real_diva" in dvdCode:
                url=url.replace("-", "_").replace("Real_diva", "Real-diva")
            elif "Muramura" in dvdCode or "1000Giri" in dvdCode or "Zipang" in dvdCode:
                url=url.replace("-", "_")
            elif "Heyzo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancom-" in dvdCode:
                url=url.replace("_", "-").replace("Caribbeancom-", "Caribbean_")
            elif "Tokyo_hot" in dvdCode:
                url=url.replace("-", "_").replace("Tokyo_Hot", "Tokyo-hot")
        elif "sexloading" in site:
            if "Heyzo" in dvdCode or "1Pondo" in dvdCode or "Caribbeancom" in dvdCode or "Zipang" in dvdCode or "Kin8tengoku" in dvdCode or "Gachinco" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            elif "Real_Diva" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
            elif "Heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-PPV")
        elif "jpav" in site:
            if "Heyzo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancom" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
        elif "javgo" in site:
            if "Caribbeancompr" in dvdCode:
                url=url.replace("Caribbeancompr-", "")
                dvdCode=dvdCode.replace("Caribbeancompr-", "")
            elif "Caribbeancom-" in dvdCode:
                url=url.replace("Caribbeancom-", "").replace("_", "-")
                dvdCode=dvdCode.replace("Caribbeancom-", "").replace("_", "-")
            elif "10musume" in dvdCode:
                url=url.replace("10musume-", "")
                dvdCode=dvdCode.replace("10musume-", "")
            elif "1Pondo" in dvdCode:
                url=url.replace("1Pondo-", "")
                dvdCode=dvdCode.replace("1Pondo-", "")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("Tokyo_Hot-", "")
                dvdCode=dvdCode.replace("Tokyo_Hot-", "")
            elif "Pacopacomama" in dvdCode:
                url=url.replace("Pacopacomama-", "")
                dvdCode=dvdCode.replace("Pacopacomama-", "")
            elif "Heydouga" in dvdCode:
                url=url.replace("Heydouga-", "").replace("_", "-")
                dvdCode=dvdCode.replace("Heydouga-", "").replace("_", "-")
            elif "Gachinco" in dvdCode:
                url=url.replace("Gachinco-", "")
                dvdCode=dvdCode.replace("Gachinco-", "")
            elif "H4610" in dvdCode:
                url=url.replace("-", "%20")
                dvdCode=dvdCode.replace("-", "%20")
            elif "Roselip" in dvdCode:
                url=url.replace("_fetish-", "%20")
                dvdCode=dvdCode.replace("_fetish-", "%20")
            elif "Muramura" in dvdCode:
                url=url.replace("Muramura-", "")
                dvdCode=dvdCode.replace("Muramura-", "")
        elif "jav-onlines" in site:
            url=url.replace("jav-onlines", "javonlines")
            if "Caribbeancom-" in dvdCode:
                url=url.replace("_", "-").replace("Caribbeancom-", "Caribbean_")
            elif "Kin8tengoku" in dvdCode or "Heyzo" in dvdCode or "Caribbeancompr" in dvdCode or "10musume" in dvdCode or "1Pondo" in dvdCode or "Pacopacomama" in dvdCode:
                url=url.replace("-", "%20")
            elif "Real_diva" in dvdCode:
                url=url.replace("Real_", "Real-").replace("diva-", "diva_")
            elif "Muramura" in dvdCode or "Zipang" in dvdCode or "H4610" in dvdCode:
                url=url.replace("-", "_")
            elif "Tokyo_Hot" in dvdCode or "Gachinco" in dvdCode or "Asiatengoku" in dvdCode or "C0930" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            url=url.replace("javonlines", "jav-onlines")
        elif "javlinks" in site:
            if "Gachinco" in dvdCode or "Pacopacomama" in dvdCode or "Nyoshin" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            elif "Caribbeancom" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
        elif "javleak" in site:
            if "Heyzo" in dvdCode or "Tokyo_Hot" in dvdCode or "1Pondo" in dvdCode or "Caribbeancom" in dvdCode or "10musume" in dvdCode or "Kin8tengoku" in dvdCode:
                url=url.replace("-", "%20")
        elif "javlabels" in site:
            if "Tokyo_Hot" in dvdCode or "Heyzo" in dvdCode or "Zipang" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            elif "Gachinco" in dvdCode:
                url=url.replace("Gachinco", "%E3%82%AC%E3%83%81%E3%82%93%E5%A8%98%21").replace("-", "%20")
            elif "heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-PPV")
            elif "Sm_" in dvdCode:
                url=url.replace("-", "%20e").replace("_", "-")
        elif "javus" in site:
            if "Tokyo_Hot" in dvdCode:
                url=url.replace("_", "%20").replace("-", "%20")
            elif "1Pondo" in dvdCode or "Heyzo" in dvdCode or "Pacopacomama" in dvdCode or "Gachinco" in dvdCode or "10Musume" in dvdCode or "H6410" in dvdCode or "C0390" in dvdCode or "H0930" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancom-" in dvdCode:
                url=url.replace("Caribbeancom-", "Caribbean%20").replace("_", "-")
            elif "Caribbeancompr" in dvdCode:
                url=url.replace("Caribbeancompr", "Caribbeanpr").replace("-", "%20").replace("-", "_")
            elif "Heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
        elif "jpidols" in url:
            if "10musume" in dvdCode or "Heyzo" in dvdCode or "Gachinco" in dvdCode or "Tokyo_Hot" in dvdCode or "Pacopaco" in dvdCode or "Caribbeancom" in dvdCode or "Asiatengoku" in dvdCode or "1Pondo" in dvdCode or "H610":
                url=url.replace("-", "%20")
                if "Tokyo_Hot" in dvdCode:
                    url=url.replace("_", "%20")
                elif "Caribbeancom" in dvdCode:
                    url=url.replace("_", "-")
        elif "jav18" in url:
            if "Caribbeancom-" in dvdCode:
                url=url.replace("Caribbeancom-", "carib").replace("_", "-")
            elif "10musume" in dvdCode:
                url=url.replace("10musume", "10mu").replace("_", "-")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            elif "Pacopacomama" in dvdCode:
                url=url.replace("Pacopacomama", "paco").replace("_", "-")
            elif "Heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
        elif "javhdfree" in url:
            if "1Pondo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancompr" in dvdCode:
                url=url.replace("-", "%20").replace("Caribbeancompr", "Caribbeancom Premium")
            elif "Caribbeancom" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
        elif "doojav69" in url:
            if "Caribbeancom-" in dvdCode:
                url=url.replace("Caribbeancom", "Caribbean").replace("_", "-")
        elif site=="freevideopornxxx":
            if "Real_diva" in dvdCode or "Caribbeancom-" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
            elif "Caribbeancompr" in dvdCode or "Gachinco" in dvdCode or "1Pondo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
        elif site=="hentaidream":
            if "1Pondo" in dvdCode or "Heyzo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancom-" in dvdCode or "Heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
            elif "Caribbeancompr" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("_", "%20").replace("-", "%20")
        elif site=="hjav5278":
            if "Heyzo" in dvdCode or "Pacopacomama" in dvdCode or "Kin8tengoku" in dvdCode or "Asiatengoku" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
            elif "Gachinco" in dvdCode:
                url=url.replace("Gachinco-", "")
            elif "1Pondo" in dvdCode:
                url=url.replace("1Pondo-", "%E4%B8%80%E6%9C%AC%E9%81%93%20")
        elif site=="jav4k":
            if "1pondo" in dvdCode.lower():
                dvdCode=dvdCode.replace("-", "%20")
                url=url.replace("-", "%20")
            elif "Caribbeancom-" in dvdCode:
                dvdCode=dvdCode.replace("Caribbeancom-", "Carib%20")
                url=url.replace("Caribbeancom-", "Carib%20")
        elif site=="javeu":
            if "Pacopacomama" in url or "10musume" in url or "1Pondo" in url or "Caribbeancompr" in dvdCode or "Heyzo" in dvdCode:
                url=url.replace("-", "%20")
            elif "Caribbeancom-" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
            elif "Heydouga" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-PPV")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("-", "%20").replace("_", "%20")
        elif site=="javhdonline":
            if "1Pondo" in url or "Pacopacomama" in url or "H0930" in url or "Asiatengoku" in url or "10musume" in dvdCode or "Caribbeancompr" in dvdCode or "Gachinco" in dvdCode:
                url=url.replace("-", "%20")
            elif "Tokyo_Hot" in dvdCode:
                url=url.replace("_", "%20").replace("-", "%20")
            elif "Heydouga" in dvdCode:   
                url=url.replace("-", "%20").replace("_", "-PPV")
            elif "Caribbeancom-" in dvdCode:
                url=url.replace("-", "%20").replace("_", "-")
        elif site=="javhub":#ガチん娘_gachi1054
            dvdCode=dvdCode.replace("%22", "")
            url=url.replace("%22", "")
            if "Caribbeancom" in dvdCode or "Caribbeancompr" in dvdCode:
                url=url.replace("-", "%20")
                dvdCode=dvdCode.replace("-", "%20")
            elif "Gachinco" in dvdCode:
                url=url.replace("-", "_").replace("Gachinco", "%E3%82%AC%E3%83%81%E3%82%93%E5%A8%98")
                dvdCode=dvdCode.replace("-", "_").replace("Gachinco", "ガチん娘")
        if "xonline" not in url:
            html=getURL(url, hdr)  
        found=[]
        
        try:
            if site=="javgo":
                items=extractAll(html, 'main-item">', '</div>')
                for item in items:
                    if dvdCode.replace("%22", "").replace("%20", " ").lower() in item.lower():
                        page=extract(item, 'href="', '"')
                        html=getURL(page)
                        p=re.compile("<a href=\"(.*?)\" class=\"lg-button\"")
                        page=re.search(p, html).group(1)
                        break
            elif site=="xonline":
                dvdCode=dvdCode.replace("%22", "").replace("-", "%20").replace("_", "%20")
                if "Pacopacomam" in dvdCode:
                    dvdCode=dvdCode.replace("Pacopacomama", "Paco")
                if "10musume" in dvdCode:
                    dvdCode=dvdCode.replace("10musume", "10mu")
                html=getURL(url+dvdCode+".html")
                items=extract(html, '<ul class="view-thumb-res">', '</ul>')
                items=extractAll(items, '<li', '</li')
                for item in items:
                    page=url+extract(item, '<a href="', '"')
                    page=page.replace("search/", "")
                    break
            elif site=="popjav":
                items=extractAll(html, '<li class="video"', '</li>')
                for item in items:
                    page=extract(item, '<a href="', '"')
                    break
                
            elif site=="freejav":
                html=extract(html, '<ul class="movies n_list">', '</ul>')
                items=extractAll(html, "<li>", "</li>")
                for item in items:
                    url=extract(item, '<span class="name"><a href="', '"')
                    break
                html=getURL(url)
                page=extract(html, '<p class="w_now"><a href="', '" class=\'btn-watch\'')
            elif site=="javstreams":
                p=re.compile("(javstreams\.tv\/play\?v=\S.*?)\"")
                page="http://"+re.search(p,html).group(1)
            elif site=="javshow" or site=="eropoi" or site=="youpornjav" or site=="javabc" or site=="javhdvideo" or site=="xonline":
                dvdCode=dvdCode.replace(" ", "-").replace("_", "-").replace("%20", "-").replace("%22", "").lower()
                if dvdCode in html:
                    p=re.compile("<loc>([\S]*.?"+dvdCode+"[\S]*.?)<\/loc>")
                    page=re.search(p,html).group(1)
                    if site=="javshow":
                        page=page+"watch.html"
                    elif 'parts' in locals():
                        if site=="eropoi":
                            page=page+str(parts)
                        elif site=="javabc":
                            page=page+"/watch-"+str(parts)
            elif site=="javseen":
                p=re.compile("<guid[^>]+>(\S*)<\/guid>")
                page=re.search(p, html).group(1)
            elif site=="jav4k":
                dvdCode=dvdCode.replace("%22", "").replace("%20", " ")
                phtml='<span class="sku"><span>'+dvdCode.lower()+'</span></span>'
                if phtml in html.lower():
                    page="http://jav4k.net/"+extract(html.lower(), phtml+'<a href="', '"' )
                    html=getURL(page)
                    page=extract(html, 'index_update_left', '</a>')
                    page="http://jav4k.net/"+extract(page, '<a href="', '"')
            elif site=="javhub":#http://javhub.net/search/1Pondo-092216_389
                dvdCode=dvdCode.replace("1Pondo-", "")
                pages=extractAll(html, '<div class="v-item">', '</div>')
                if pages:
                    for p in pages: 
                        if dvdCode.lower() in p.lower():
                            page="http://javhub.net"+extract(p, '<a href="', '"')
                            page=page.split("/")
                            page.pop()
                            page="/".join(page)
                            break
            elif site=="streamjav":
                p=re.compile("<link>(\S*)<\/link>")
                page=re.search(p, html).group(2)
            #elif site=="javtubehd":
            #    p=re.compile('<iframe src="(http:\/\/www\.riz1.info\S+)"')
            #    page=re.search(p, html).group(1)
            elif "blogspot" in url:
                p=re.compile(ur'<item>[\n\S\s]*?<link>(.*?)<\/link>')
                page=re.search(p, html).group(1)
            else:
                #p=re.compile("<item>[\S\s]+<link>([^<]+)")
                p=re.compile("<guid[^>]+>(\S*)<\/guid>")
                page=re.search(p, html).group(1)        
            
            try:
                html=getURL(page, hdr)
            except:
                html=getURL(page.encode('utf-8'), hdr)
                
            if site=="kodporn":
                p=re.compile('iframe src="(\S*\/tube\/xplay\S+)"')
                page="http://www.kodporn.co"+re.search(p, html).group(1)
                html=getURL(page, hdr)
            
            if site=="gaimup":
                if dvdCode.lower() not in html.lower():
                    html=False
            
            if "jav18"!=site:
                found.append(page)
        except:
            html=False
            #logError(site+": Link not found in "+url.encode("utf-8"))    
        """if html!=False and site=="freejav":
            html=base64.b64decode(extract(html, 'Base64.decode("', '"'))
            # add code to check for other sources, looks to be last character of url is the relevant server """
        
        if html!=False and site=="gaimup":
            servers=extractAll(html, 'class="btn-eps', '>')
            if servers:
                for server in servers:
                    page="http://gaimup.com/wp-admin/admin-ajax.php?action=ts-ajax&p="+extract(server, 'data-link="', '"')+"&n=something"
                    html=getURL(page)
                    if html!=False:
                        if "sources: [" in html:
                            sources=extract(html, 'sources: [', ']')
                            sources=extractAll(sources, '{' , '}')
                            for source in sources:
                                gv=str(extract(source, 'label:"', '"').upper())
                                globalURLS.append({"site":site, "source":"googlevideo ["+gv+"]", "url":urllib.quote_plus(page)})
            else:
                server="http://gaimup.com"+extract(html, "<iframe src='http://gaimup.com", "'")
                html=getURL(server)
                if html!=False:
                    if "sources: [" in html:
                        sources=extract(html, 'sources: [', ']')
                        sources=extractAll(sources, '{' , '}')
                        for source in sources:
                            gv=str(extract(source, 'label: "', '"').upper())
                            globalURLS.append({"site":site, "source":"googlevideo ["+gv+"]", "url":urllib.quote_plus(server)})
        elif html!=False and site=="javstreamclub":
            html=base64.b64decode(extract(html, '<div class="b64d"><!-- ', ' --></div>'))
            found=found+whatSource(html, site)
        elif html!=False and site=="jpav":
            if ".mp4" in html:
                globalURLS.append({"site":site, "source":"googlevideo", "url":server})
            else:
                server='http://content.jwplatform.com/players/'+extract(html, '<script src="//content.jwplatform.com/players/', '"')
                html=getURL(server)
                if '"file":' in html:
                    globalURLS.append({"site":site, "source":"googlevideo", "url":server})
        elif html!=False and site=="javtubehd":
            server='https://freejav.co/'+extract(html, 'https://freejav.co/', '"')
            html=getURL(server)
            if html!=False:
                if "sources: [" in html:
                    sources=extract(html, 'sources: [', ']')
                    sources=extractAll(sources, '{' , '}')
                    for source in sources:
                        gv=str(extract(source, 'label: "', '"').upper()).replace(" SD", "").replace(" HD", "").replace(" Full HD", "")
                        globalURLS.append({"site":site, "source":"googlevideo ["+gv+"]", "url":server})
        elif html!=False and site=="javgo":
            servers=extractAll(html, '<span class="server-name">', '</a>')
            if servers!=False:
                temp=[]
                temp2=[]
                temp3=[]
                for server in servers:
                    if "down." not in server:
                        try:
                            page2=extract(server, 'href="', '"')
                            if page!=page2:
                                html=getURL(page2)
                            page2=extract(base64.b64decode(extract(html, "tplugin.decode('", "'")), '<iframe src="', '"')
                            html=getURL(page2)
                            if '"sources":[' in html:
                                sources=extract(html, '"sources":[', ']')
                                sources=extractAll(sources, '{' , '}')
                                for source in sources:
                                    gv=str(extract(source, '"label":"', '"').upper())
                                    temp.append({"site":site, "source":"googlevideo ["+gv+"]", "url":page2})
                            elif 'qwertycdn.com' in html:
                                sources=extract(html, '"sources":', ',"image"')
                                sources=extractAll(sources, '{' , '}')
                                for source in sources:
                                    gv=str(extract(source, '"label":"', '"').upper())
                                    temp2.append({"site":site, "source":"qwertycdn ["+gv+"]", "url":page2})
                        except:
                            found=whatSource(html, site)
                            if found:
                                for f in found:
                                    temp3.append({"site":site, "source":f, "url":page2})
                temp.reverse()
                temp=temp+temp2+temp3
                for t in temp:
                    globalURLS.append(t)
        elif html!=False and site=="javeu":
            jetemp=[]
            servers=extractAll(html, '<script>document.write(doit("', '"')
            for server in servers:
                server=base64.b64decode(base64.b64decode(server))
                server=extract(server, 'src="', '"')
                found=whatSource(server, site)
                if found:
                    for page2 in found:
                        jetemp.append({"site":site, "source":page2, "url":server})
            jeurl=extract(html, 'embedaio.xyz/', '"')
            if jeurl:
                server="http://embedaio.xyz/"+jeurl
                html2=getURL(server)
                found=whatSource(html2, site)
                if found:
                    for page2 in found:
                        jetemp.append({"site":site, "source":page2, "url":server})
            servers=extractAll(html, '<tr style="color: #0000ff;">', '</tr>')
            if servers:
                for html2 in servers:
                    #logError(html2)
                    if "flashx" in html2 or "vidto" in html2:
                        #server=extract(html2, 'href="', '"')
                        logError(server)
                        if "aiolinks" in server:
                            #logError("aio")
                            server=base64.b64decode(base64.b64decode(server.replace('http://aiolinks.com/watch.php?url=', '')))
                        else:
                            html3=getURL(server)
                            server=base64.b64decode(base64.b64decode(extract(html3, '<script>document.write(doit("', '"')))
                            server=extract(server, "SRC='", "'")
                        found=whatSource(server, site)
                        if found:
                            for page2 in found:
                                jetemp.append({"site":site, "source":page2, "url":server})
            for j in jetemp:
                globalURLS.append(j)
        elif html!=False and site=="jav4k":
            servers=extractAll(html, '<div class="wep">', '</div>')
            for server in servers: 
                page="http://jav4k.net/"+extract(server, 'a href="', '"')
                html=getURL(page)
                found=whatSource(html, site)
                for page2 in found:
                    globalURLS.append({"site":site, "source":page2, "url":page})
        elif html!=False and site=="jav-onlines" or html!=False and site=="streamingjav":
            page="http://www.riz1.info"+extract(html, '<iframe src="http://www.riz1.info', '"')
            html=getURL(page)
            if html!=False:
                if "sources: [" in html:
                    sources=extract(html, 'sources: [', ']')
                    sources=extractAll(sources, '{' , '}')
                    for source in sources:
                        gv=str(extract(source, 'label: "', '"').upper()).replace("/LOWSD", "").replace("/SD", "").replace("/MINIHD", "").replace("/FULLHD", "")
                        globalURLS.append({"site":site, "source":"googlevideo ["+gv+"]", "url":page})
        elif html!=False and site=="9xxx":
            servers=extractAll(html, '<div class="movieplay">', '</div>')
            for server in servers:
                page="http:"+extract(server, '<iframe src="', '"')
                html=getURL(page)
                if html!=False:
                    if "googlevideo" in html:
                        sources=extract(html, 'sources: [', ']')
                        sources=extractAll(sources, '{' , '}')
                        for source in sources:
                            gv=str(extract(source, 'label: "', '"').upper()).replace("/SD", "").replace("/HD", "").replace("/FHD", "")
                            globalURLS.append({"site":site, "source":"googlevideo ["+gv+"]", "url":page})
        elif html!=False and site=="xonline":
            p=re.compile(ur'window\.atob\(\"(.*?)\"\),label: \"(.*?)\"')
            matches = re.finditer(p, html)
            for matchNum, match in enumerate(matches):
                found.append("googlevideo ["+match.group(2)+"]")
        elif html!=False and site=="jpidols":
            servers=extract(html, '<div class="list_video">', '</div>')
            servers=extractAll(servers, '<a href="', '"')
            counter=0
            jplink=[]
            jppage=[]
            for page in servers:
                link=[]
                if counter>0:
                    html=getURL(page)
                counter=counter+1
                link=whatSource(html, site)
                if link:
                    jplink.append(link[0])
                    jppage.append(page)
            for x in range(0, len(jplink)):
                globalURLS.append({"site":site, "source":jplink[x], "url":jppage[x]})
        elif html!=False and site=="freejav":
            servers=extract(html, "class='list-episode'", '</table>')
            servers=extractAll(servers, "href='", "'")
            counter=0
            jplink=[]
            jppage=[]
            for page in servers:
                link=[]
                html=getURL(page)
                html=base64.b64decode(extract(html, 'Base64.decode("', '"'))
                link=whatSource(html, site)
                if link:
                    jplink.append(link[0])
                    jppage.append(page)
            for x in range(0, len(jplink)):
                globalURLS.append({"site":site, "source":jplink[x], "url":jppage[x]})
        elif html!=False and site=="popjav":
            pjurl=extract(html, 'src="http://popjav.com/images/loading-bert.gif"> </div> </div> <input type="hidden" value="', '"')
            pjid=extract(html, 'value="'+pjurl+'" id="', '"')
            url="http://popjav.com/video/?url="+pjurl+"&cid="+extract(html, "$('#"+pjid+"').val()+\"&cid=", '"')
            html=getURL(url)
            sources=extract(html, 'sources:[', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                found.append("googlevideo ["+str(extract(source, '"label":"', '"').upper())+"]")
        elif html!=False and site=="javhdfree" and "googlevideo" in html:
            sources=extract(html, 'sources: [', ']')
            sources=extractAll(sources, "{", "}")
            if sources:
                for source in sources:
                    found.append("googlevideo ["+str(extract(source, 'label:"', '"').upper())+"]")
        elif html!=False and site=="jav18":
            j18=[]
            servers=extract(html, '<!-- Streaming Panel & Video -->', '<ul id="panel-control"')
            servers=extractAll(servers, 'src="', '"')
            for server in servers:
                url2=server
                if "http" not in url2:
                    url2="http:"+url2
                if "jav18" in url2:
                    #logError(url2)
                    html2=getURL(url2)
                    if html2!=False:
                        j18.append({"site":site, "source":"googlevideo", "url":url2})
            if "openload" in html:
                j18.append({"site":site, "source":"openload", "url":page})
            for t in j18:
                globalURLS.append(t)
        elif html!=False:
            found=found+whatSource(html, site)
        
        if site!="jav18":
            counter=0
            for page in found:
                if site=="adult":
                    site="dodova"
                if site=="xxxx":
                    site="hjav5278"
                if counter==0:
                    link=page
                    counter=1
                elif "jpidols" not in site:
                    globalURLS.append({"site":site, "source":page, "url":link})
        """updateTotal=updateTotal+1
        updateString=updateString.replace(*/site, "")
        updateCounter=updateCounter+1"""
    except:
        # dont want to get into inifinite loop
        logError("some sort of error")
    updateTotal=updateTotal+1
    updateString=updateString.replace(site, "")
    updateCounter=updateCounter+1

def whatSource(html, site):
    try:
        found=[]
        if html!=False and site!="adult":
            if "rapidvideo.com" in html:
                found.append("rapidvideo")
            if "vidto.me" in html:
                found.append("vidtome")
            if site=='javpop' and "diskname hdsinglelink" in html:
                found.append("wushare [HD]")
            if site=='javpop' and "diskname singlelink" in html:
                found.append("wushare [SD]")    
            if 'type="video/mp4" data-res="480"' in html:
                found.append("googlevideo [480P]")
            if 'type="video/mp4" data-res="720"' in html:
                found.append("googlevideo [720P]")
            if 'type="video/mp4" data-res="1080"' in html:
                found.append("googlevideo [1080P]")
            """if "rapidgator" in html:
                found.append("rapidgator")"""
            if "bigfile.to" in html:
                try:
                    p=re.compile(r"['|\"](http[s]?:\/\/www\.bigfile\.to\/[\bfile\b|\bev\b]+\/[a-zA-Z0-9]*?)['|\"]")
                    link=re.search(p, html).group(1)
                    found.append("bigfile")
                except:
                    pass
            if "googlevideo" in html or "googleusercontent" in html or "docs.google" in html or "drive.google" in html:
                p=re.compile('src=[\'|"](http[s]*:\/\/googleusercontent.[\S]*)[\'|"]')
                try: 
                    link=urlresolver.resolve(re.search(p, html).group(1))
                    found.append("googlevideo")
                except:
                    p=re.compile('src=[\'|"](.*?googlevideo.*?)[\'|"]')
                    try: 
                        link=re.search(p, html).group(1)
                        found.append("googlevideo")
                    except:
                        p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?googlevideo.\S.*?)[\'|"]')
                        try: 
                            link=urlresolver.resolve(re.search(p, html).group(1))
                            found.append("googlevideo")
                        except:
                            p=re.compile('[\'|\"]([http|https]\S*googleusercontent\S*)[\'|\"]')
                            try: 
                                link=urlresolver.resolve(re.search(p, html).group(1))
                                found.append("googlevideo")
                            except:
                                p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?docs.google.com.\S.*?)[\'|"]')
                                try: 
                                    link=urlresolver.resolve(re.search(p, html).group(1))
                                    found.append("googlevideo")
                                except:
                                    p=re.compile('<video[\S\s].*src="(.*)"')
                                    try:
                                        link=urlresolver.resolve(re.search(p, html).group(1))
                                        found.append("googlevideo")
                                    except:
                                        try:
                                            if "drive.google.com" in html:
                                                found.append("googlevideo")
                                        except:
                                            pass
            if "openload" in html or "oload" in html:
                found.append("openload")
            if "flashx.tv" in html: #to be added in the future
                found.append("flashx")
            if "videowood.tv" in html:
                found.append("videowood")
            if "thevideome" in html: #to be added in the future
                found.append("thevideome")
            if "filehoot" in html: #to be added in the future
                found.append("filehoot")
            if "streamin.to" in html: #to be added in the future
                found.append("streamin")
            if "mega3x" in html: #to be added in the future
                found.append("mega3x")
            if "uptostream" in html: #to be added in the future
                found.append("uptostream")
            if "vodlocker" in html: #to be added in the future
                found.append("vodlocker")
            if "nowvideo" in html: #to be added in the future
                found.append("nowvideo")
            if "dropvideo" in html: #to be added in the future
                found.append("dropvideo")
            if "vidbull" in html: #to be added in the future
                found.append("vidbull")
            if "vid.bz" in html: #to be added in the future
                found.append("vid.bz")
        elif html!=False and site=="adult":
            if "Flash Video chanel</button>" in html: # to be added in the future
                found.append("flashx.tv")
            if "videomega Video chanel</button>" in html:
                found.append("videomega")
            if "videowood Video chanel</button>" in html:
                found.append("videowood")
            if "thevideome Video chanel</button>" in html: # to be added in the future
                found.append("thevideome")
            if "filehoot Video chanel</button>" in html: # to be added in the future
                found.append("filehoot")
            if "streamin Video chanel</button>" in html:  #to be added in the future
                found.append("streamin")
        return found
    except:
        return False
    
def huntVideo(params):
    global updateString
    global updateTotal
    urls=[]
    items=[]
    javpophd=[]
    javpopsd=[]
    jsc=[]
    glinks=[]
    found=[]
    search=str(params["extras"])
    if search=="44":
        search="43"
    p=re.compile("(\[[A-Za-z0-9-_\ \.]+\])")  
    dvdCode=p.match(params['name'].encode("utf-8")).group(1).replace("[", "").replace("]", "").replace("_fetish-", "%20")
    dvdCodeClean=p.match(params['name'].encode("utf-8")).group(1).replace("[", "").replace("]", "").replace("_fetish-", "%20")
    
    dvdCodeClean=dvdCodeClean.replace("_", "%20")
    
    dvdCode="%22"+dvdCode+"%22"
    tempdvdCode=dvdCode.replace("-", " ").replace("_", " ").split(" ")
    splitdvdCode=""
    for part in tempdvdCode:
        splitdvdCode=dvdCode+"%22"+part+"%22"
    
    huntSites=[]
    
    udvdCode=dvdCode.replace("-", "%20").replace("%22", "")
    
    search=search.split(",")
    titles=[]
    for searching in search:
        if xbmcplugin.getSetting(int(sysarg), searching+"wushare")=="true":
            """if xbmcaddon.Addon().getSetting("wushare_username")=="" or xbmcaddon.Addon().getSetting("wushare_password")=="":
                alert("To use WuShare you must enter a Username and Password to a valid premium account.");
            else:
                titles.append("wushare")"""
            titles.append("javpop")
            huntSites.append("http://javpop.com/search/"+dvdCode.replace("%22", "")+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"sexloading")=="true":
            titles.append("sexloading")
            huntSites.append("http://sexloading.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"ivhunter")=="true":
            titles.append("ivhunter")
            huntSites.append("http://ivhunter.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javhdonline")=="true":
            titles.append("javhdonline")
            huntSites.append("http://javhdonline.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"watchjavonline")=="true":
            titles.append("watchjavonline")
            huntSites.append("http://watchjavonline.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javlinks")=="true":
            titles.append("javlinks")
            huntSites.append("http://javlinks.com/search/"+dvdCode+"/feed/rss2/")
        if xbmcplugin.getSetting(int(sysarg), searching+"dodova")=="true":
            titles.append("dodova")
            huntSites.append("http://adult.dodova.com/search/"+dvdCode+"/feed/rss2/")
        if xbmcplugin.getSetting(int(sysarg), searching+"hentaidream")=="true":
            titles.append("hentaidream")
            huntSites.append("http://hentaidream.me/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"streamjav")=="true":
            titles.append("streamjav")
            huntSites.append("http://streamjav.org/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"dinojav")=="true":
            titles.append("dinojav")
            huntSites.append("http://www.dinojav.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"top1porn")=="true":
            titles.append("top1porn")
            huntSites.append("http://top1porn.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jav-stream")=="true":
            titles.append("jav-stream")
            huntSites.append("http://jav-stream.net/search/"+dvdCode.replace("%22", "")+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javseen")=="true":
            titles.append("javseen")
            huntSites.append("http://javseen.com/search/"+dvdCode.replace("%22", "")+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javst")=="true":
            titles.append("javst")
            huntSites.append("http://javst.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javlabels")=="true":
            titles.append("javlabels")
            huntSites.append("http://javlabels.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"terlarang")=="true":
            titles.append("terlarang")
            huntSites.append("http://terlarang.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jav4k")=="true":
            titles.append("jav4k")
            huntSites.append("http://jav4k.net/moviesearch/"+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"javhub")=="true":
            titles.append("javhub")
            huntSites.append("http://javhub.net/search/"+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"jav-onlines")=="true":
            titles.append("jav-onlines")
            huntSites.append("http://jav-onlines.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javeu")=="true":
            titles.append("javeu")
            huntSites.append("http://javeu.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"yebbun90")=="true":
            titles.append("yebbun90")
            huntSites.append("http://yebbun90.com/search/"+dvdCodeClean+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"youpornjav")=="true":   
            titles.append("youpornjav")
            huntSites.append("http://www.youpornjav.com/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"jav720p")=="true":
            titles.append("jav720p")
            huntSites.append("http://jav720p.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javstreams")=="true": 
            titles.append("javstreams")
            huntSites.append("http://javstreams.tv/search/"+dvdCode+"/feed/rss")
        if xbmcplugin.getSetting(int(sysarg), searching+"javtv")=="true":
            titles.append("javtv")
            huntSites.append("http://javtv.org/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javstream365")=="true":
            titles.append("javstream365")
            #needs checking with uncensored
            #needs new sources adding
            huntSites.append("http://javstream365.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javabc")=="true":
            titles.append("javabc")
            huntSites.append("http://javabc.net/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"javhdvideo")=="true":
            titles.append("javhdvideo")
            huntSites.append("http://javhdvideo.net/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"javsex")=="true":
            titles.append("javsex")
            huntSites.append("http://javsex.net/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javhdfree")=="true":
            titles.append("javhdfree")
            huntSites.append("http://javhdfree.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"dojav69")=="true":
            titles.append("dojav69")
            huntSites.append("http://doojav69.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"dojav69")=="true":
            titles.append("javl")
            huntSites.append("http://javl.in/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jpav")=="true":
            titles.append("jpav")
            huntSites.append("http://jpav.site/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"hjav5278")=="true":
            titles.append("hjav5278")
            huntSites.append("http://xvideo.5278jav.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"tubebo")=="true":
            titles.append("tubebo")
            huntSites.append("http://tubebo.com/?s="+dvdCode+"&feed=rss2")
        """if xbmcplugin.getSetting(int(sysarg), searching+"javportal")=="true":
            titles.append("javportal")
            huntSites.append("http://javportal.net/?s="+dvdCode+"&feed=rss2")"""
        if xbmcplugin.getSetting(int(sysarg), searching+"freevideopornxxx")=="true":
            titles.append("freevideopornxxx")
            huntSites.append("http://freevideopornxxx.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javbest")=="true":
            titles.append("javbest")
            huntSites.append("http://javbest.co/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"gravuregirlz")=="true":
            titles.append("gravuregirlz")
            huntSites.append("http://gravuregirlz.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javleak")=="true":
            titles.append("javleak")
            huntSites.append("http://javleak.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"9XXX")=="true":
            titles.append("9xxx")
            huntSites.append("http://9xxx.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javtubehd")=="true":
            titles.append("javtubehd")
            huntSites.append("http://javtubehd.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"kodporn")=="true":
            titles.append("kodporn")
            huntSites.append("http://www.kodporn.co//search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"idolportal")=="true":
            titles.append("idolportal")
            huntSites.append("http://idolportal.blogspot.com/feeds/posts/default/?alt=rss&q="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"planetjav")=="true":
            titles.append("planetjav")
            huntSites.append("http://planetjav.blogspot.com/feeds/posts/default/?alt=rss&q="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"ytbsexclub")=="true":
            titles.append("ytbsexclub")
            huntSites.append("http://ytbsexclub.blogspot.com/feeds/posts/default/?alt=rss&q="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"streamjavporn")=="true":
            titles.append("streamjavporn")
            huntSites.append("http://streamjavporn.blogspot.com/feeds/posts/default/?alt=rss&q="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"javcuteonline")=="true":
            titles.append("javcuteonline")
            huntSites.append("http://javcuteonline.com/search/"+dvdCode.replace("%22", "")+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jav-720p")=="true":
            titles.append("jav-720p")
            huntSites.append("http://jav-720p.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"koleksijav")=="true":
            titles.append("koleksijav")
            huntSites.append("http://javkonyol.blogspot.com/feeds/posts/default/?alt=rss&q="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"javstreamclub")=="true":
            titles.append("javstreamclub")
            huntSites.append("http://javstream.club/search/"+dvdCode+"/feed/rss2")    
        if xbmcplugin.getSetting(int(sysarg), searching+"xonline")=="true":
            titles.append("xonline")
            huntSites.append("http://xonline.vip/search/")
        if xbmcplugin.getSetting(int(sysarg), searching+"freejav")=="true":
            titles.append("freejav")
            huntSites.append("http://freejav.us/search/?q="+dvdCode.replace("%22", ""))
        if xbmcplugin.getSetting(int(sysarg), searching+"javocado")=="true":
            titles.append("javocado")
            huntSites.append("http://www.javocado.com/search/"+dvdCode.replace("%22", "")+"/feed/rss2")  
        if xbmcplugin.getSetting(int(sysarg), searching+"jpidols")=="true":
            titles.append("jpidols")
            huntSites.append("http://jpidols.tv/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"popjav")=="true":
            titles.append("popjav")
            huntSites.append("http://popjav.com/?s="+dvdCode)
        if xbmcplugin.getSetting(int(sysarg), searching+"jav18")=="true":
            titles.append("jav18")
            huntSites.append("http://jav18.tv/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javus")=="true":
            titles.append("javus")
            huntSites.append("http://javus.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javgo")=="true":
            titles.append("javgo")
            huntSites.append("http://javgo.me/search?title="+dvdCode.replace("%22", ""))
        if xbmcplugin.getSetting(int(sysarg), searching+"streamingjav")=="true":
            titles.append("streamingjav")
            huntSites.append("http://streamingjav.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"gaimup")=="true":
            titles.append("gaimup")
            huntSites.append("http://gaimup.com/search/"+dvdCode+"/feed/rss2")
        #http://jav18.tv/search/%22kin8tengoku-1579%22/feed/rss2
        #titles.append("thepornsupremacy")
        #huntSites.append("http://thepornsupremacy.com/search/"+dvdCode.replace("%22", "")+"/feed/rss2")  
        #titles.append("dujav")
        #huntSites.append("http://dujav.com/search/"+dvdCode+"/feed/rss2")
        
    huntSites=unique(huntSites)  
    updateString=" ".join(titles)
    # to be fixed for new kodi
    # javtubehd
    # to be added in the future
    # -------------------------
    # javmovie.com
    # javuncen.me
    # rejav.com
    # xonline
    # openload2.appspot.com
    # --------------------------
    # wordpress sites
    # --------------------------
    # javdude.com
    # javchan.com
    # hdporn4us.com
    # jav18online.com
    # joojav.com
    # javholy.com
    # jav.one
    # javhdx.tv
    # --------------------------
    # blogspot (http://idolportal.blogspot.com/feeds/posts/default/?alt=rss&q=mmr)
    # --------------------------
    # planetjav.blogspot.com (added for censored not for uncensored)
    # ikibokep.blogspot.co.uk
    # --------------------------
    # realdebrid
    # --------------------------
    # javpop.com
    # javfilm.tk
    # javblog.me
    # nippondvd.com
    # acr700.biz
    # javfilm.ga
    # javarchive.com
    # maddawgjav.net
    # hdporn4us.com
    # vureness.com
    # japanidols.info
    # javgravureidols.info
    # japanesekayo.net
    
    #p1=re.compile("http:\/\/(www.)?([a-zA-Z0-9-]*.[a-z]*)")
    p=re.compile("[http|https]*:\/\/(www.)?([a-zA-Z0-9-]*).")
    updateBy=100/float(len(huntSites))
    
    statusDialog=progressStart("Searching for streams", "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")
    progressUpdate(statusDialog, updateCounter*updateBy, "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")

    
    threads=[]
    counter=0
    for url in huntSites:
        threads.append(threading.Thread(target=whatPlayer, args=(url, titles[counter], dvdCode,)) )
        counter=counter+1
    
    for thread in threads:
        thread.start()
    
    t_end = time.time() + int(xbmcaddon.Addon().getSetting("timeout"))+5 # prevent infinite loop that i cant find the cause of (run for length of page timeout+5)
    while updateTotal<len(huntSites):
        if statusDialog.iscanceled()==1:
            statusDialog.close()
            break
        else:
            progressUpdate(statusDialog, updateCounter*updateBy, "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")
            if len(globalURLS)>0 and xbmcplugin.getSetting(int(sysarg), "autoplay")=="true":
                progressCancelled(statusDialog)
                break
            if updateTotal+1==len(huntSites) and time.time()>t_end:
                logError("bump error")
                break
        
    for thread in threads:
        try:
            thread.exit()
        except:
            pass
    
    p1080=[]
    p720=[]
    p480=[]
    p360=[]
    jsc=[]
    
    counter=0
    if len(globalURLS)>0:
        for url in globalURLS:
            counter=counter+1
            if url["source"]=="googlevideo" and url["site"]=="javlinks":
                pass
            elif url["source"]=="wushare [HD]":
                javpophd.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[HD]", "| HD"),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif url["source"]=="wushare [SD]":
                javpopsd.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[SD]", "| SD"),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif url["site"]=="javstreamclub":
                jsc.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[SD]", "| SD"),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif "[1080P]" in url["source"]:
                p1080.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[", "| ").replace("]", ""),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif "[720P]" in url["source"]:
                p720.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[", "| ").replace("]", ""),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif "[480P]" in url["source"]:
                p480.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[", "| ").replace("]", ""),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            elif "[360P]" in url["source"]:
                p360.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"].replace("[", "| ").replace("]", ""),
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
            else:
                items.append({
                    "title": " | [B]"+url["site"]+"[/B] | "+url["source"],
                    "url": urllib.quote_plus(url["url"]), 
                    "mode":6, 
                    "poster":params["poster"],
                    "icon":params["poster"], 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":url["source"],
                    "extras2":params["name"]
                })
                
            
            
            if xbmcplugin.getSetting(int(sysarg), "autoplay")=="true":
                #logError(str(items))
                try:
                    myurl=getVideoURL(javpophd[0])
                except:
                    try:
                        myurl=getVideoURL(javpopsd[0])
                    except:
                        myurl=getVideoURL(items[0])
                playMedia(params["name"], params["poster"], myurl, "Video")
                return False
        
        counter=1
        items=javpophd+javpopsd+p1080+p720+p480+p360+jsc+items
        #items=javpophd+javpopsd+link1080+link720+link480+link360+gvid+openload+items
        for item in items:
            if "javpop" in item['title']:
                item['title']="[COLOR orange]"+str(counter).zfill(2)+item['title']+"[/COLOR]"
            else:
                item['title']=str(counter).zfill(2)+item['title']
            counter=counter+1
        
        progressStop(statusDialog)
        statusDialog.close()
        
        try:
            if params['fromlibrary']:
                librarySources=[]
                for item in items:
                    librarySources.append(item['title'])
                
                value=select(librarySources)
                url=getVideoURL({"url":items[value]['url'], "extras":items[value]['extras']})
                playMedia(items[value]['extras2'], items[value]['poster'], url, "Video")
        except:
            addMenuItems(items, isFolder=False)
    else:
        notify(ADDON_ID, "No Streams Found")

def unique(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result
   
def translate(toTranslate):
    try:
        p1=re.compile(ur"[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]+ (?=[A-Za-z ]+–)", re.UNICODE)
        toTranslate=p1.sub("", toTranslate)
        
        if xbmcplugin.getSetting(int(sysarg), "translation")=="true":
            p=re.compile("(\[[A-Za-z0-9-_\ ]+\])")  
            try:
                dvdCode=p.match(toTranslate.encode("utf-8")).group(1)
            except:
                dvdCode=""
            f={"to":xbmcplugin.getSetting(int(sysarg), "language"), "string": toTranslate.replace(dvdCode, "").encode("utf-8")}
            translated=getURL("http://javstream.club/translate/translate.php?"+urllib.urlencode(f))
            if translated==False:
                return toTranslate
            else:
                return dvdCode+" "+translated.replace('"', '').title()
    except:
        logError("Translation error")
    return toTranslate

def gravureIdols(params):
    html=getURL(params['url'])
    if html!=False:
        if "#" not in params['url']:
            all=extract(html, '<div id="mcTagMapNav">', '</div>')
            letters=extractAll(all, '<a', '/a>')
            items=[]
            for letter in letters:
                title=extract(letter, '>', '<')
                if title!=None:
                    items.append({
                        "title": title,
                        "url": params["url"]+"#"+title+"/0", 
                        "mode":1002, 
                        "poster":"default.jpg",
                        "icon":"default.jpg", 
                        "fanart":params["fanart"],
                        "type":"", 
                        "plot":"",
                    })
            addMenuItems(items) 
        else:
            details=params['url'].replace('http://ivhunter.com/idols-library/#', '')
            letter=details.split("/")
            page=letter[1]
            letter=letter[0]
            all=extract(html, '<h4 id="mctm-'+letter+'">'+letter+'</h4>', '</ul>')
            idols=extractAll(all, '<a', 'a>')
            items=[]
            counter=0
            pagination=0
            for idol in idols:
                if pagination>int(page)*20:
                    poster="default.jpg"
                    title=re.sub(r'([^\s\w]|_)+', '', extract(idol, 'title="', '"'))
                  
                    poster="default.png"
                    if ".not.found" in poster:
                        pass
                    else:
                        items.append({
                            "title": title,
                            "url": siteURL+'/category/idol', 
                            "mode": 3, 
                            "poster":poster,
                            "icon":poster, 
                            "fanart":params["fanart"],
                            "type":"", 
                            "plot":"",
                            "extras":"force-search"
                        })
                        counter=counter+1
                        if counter==20:
                            break
                pagination=pagination+1
            if len(idols)>int(page)*20+1:
                items.append({
                    "title": "Next >",
                    "url": 'http://ivhunter.com/idols-library/#'+letter+"/"+str(int(page)+1), 
                    "mode": 1002, 
                    "poster":os.path.join(home, 'resources/media', 'next.jpg'), 
                    "icon":os.path.join(home, 'resources/media', 'next.jpg'), 
                    "fanart":params["fanart"],
                    "type":"", 
                    "plot":"",
                    "extras":"force-search"
                })
            addMenuItems(items) 
    
def playMedia(title, thumbnail, link, mediaType='Video', library=True, title2="") :
    li = xbmcgui.ListItem(label=title2, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo( "video", { "Title" : title } )
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    
def getVideoURL(params):
    logError(str(params))
    #logError(params['url'])
    params['url']=urllib.unquote_plus(params['url'])
    if "vidto.me" in params['url']:
        # need to actually detect the embed for ones not passing in url
        return urlresolver.resolve(params['url'])
        
    videosource=getURL(params["url"].encode("utf-8"), hdr)
    
   
    
    if "javeu.com" in params["url"]:
        videosource=extract(videosource, "<td>"+params["extras"], "</tr>")
        videosource=extract(videosource, 'url=', '"')
        videosource=base64.b64decode(base64.b64decode(videosource))
    elif 'top1porn' in params['url']:
        videosource=extract(videosource, 'Watch online server '+params['extras']+"</p>", 'rel="nofollow"')
        videosource=getURL(extract(videosource, 'href="', '"'))
        videosource=base64.b64decode(extract(videosource, 'document.write(Base64.decode("', '"'))
    elif "javstream.club" in params['url']:
        videosource=base64.b64decode(extract(videosource, '<div class="b64d"><!-- ', ' --></div>'))
    link=False
    
    if "jwplatform" in params['url']:
        return urlresolver.resolve(extract(videosource, '"file": "', '"'))
    elif "jpav" in params['url']:
        return extract(videosource, '<meta itemprop="contentUrl" content="', '"')
    elif "javpop" in params['url']:
        if "HD" in params["extras"]:
            link=extract(videosource, "diskname hdsinglelink", "</a>")
            link=extract(link, '<a href="', '"')
        else:
            link=extract(videosource, "diskname singlelink", "</a>")
            link=extract(link, '<a href="', '"')
            
        cj2 = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj2))
        
        login_data = urllib.urlencode({'username_or_email' : xbmcaddon.Addon().getSetting("wushare_username"), 'password' : xbmcaddon.Addon().getSetting("wushare_password"), 'stay_login': '1', 'commit' : 'Login', 'referrer' : 'http://wushare.com/login'})
        opener.open('http://wushare.com/login', login_data)
        
        resp = opener.open(link)
        content=resp.read()
        if "Start download" not in content:
            alert("Unable to authenticate: Please check your WusShare account details.")
            #logError(content)
            return False;
        p=re.compile('dl_link">(\S+)<\/')
        try:
            link=re.search(p, content).group(1)
        except:
            pass
            #logError(resp.read())
    elif params['extras']=="bigfile":
        p=re.compile(r"['|\"]http[s]?:\/\/www\.bigfile\.to\/[\bfile\b|\bev\b]+\/([a-zA-Z0-9]*?)['|\"]")
        link=re.search(p, videosource).group(1)
        #logError("https://www.bigfile.to/ajax/video.php?action=201&shortenCode="+link)
        html=getURL("https://www.bigfile.to/ajax/video.php?action=201&shortenCode="+link)
        link=extract(html, 'url":"', '"').replace("\\", "")+"?downloadId="+extract(html, '"downloadId":"', '"')
        return link
    elif params['extras']=="rapidgator":
        pass # for the minute
    elif params["extras"]=="googlevideo [1080P]" or  params["extras"]=="googlevideo [720P]" or params["extras"]=="googlevideo [480P]" or params["extras"]=="googlevideo [360P]":
        if "gaimup" in params["url"]:
            sources=extract(videosource, 'sources: [', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                try:
                    if extract(source, 'label:"', '"').upper() in params["extras"]:
                        link=extract(source, 'file:"', '"').replace("\\", "")
                        break
                except:
                    if extract(source, 'label: "', '"').upper() in params["extras"]:
                        link=extract(source, 'file: "', '"').replace("\\", "")
                        break
            return link
        elif "javgo" in params['url']:
            sources=extract(videosource, '"sources":[', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                if extract(source, '"label":"', '"').upper() in params["extras"]:
                    link=extract(source, '"file":"', '"').replace("\\", "")
                    break
            return link
        elif "xonline" in params['url']:
            html=getURL(params['url'])
            p=re.compile(ur'window\.atob\(\"(.*?)\"\),label: \"(.*?)\"')
            matches = re.finditer(p, html)
            for matchNum, match in enumerate(matches):
                if "googlevideo ["+match.group(2)+"]" in params['extras']:
                    link=base64.b64decode(match.group(1))
            return link
        elif "popjav" in params['url']:
            pjurl=extract(videosource, 'src="http://popjav.com/images/loading-bert.gif"> </div> </div> <input type="hidden" value="', '"')
            pjid=extract(videosource, 'value="'+pjurl+'" id="', '"')
            url="http://popjav.com/video/?url="+pjurl+"&cid="+extract(videosource, "$('#"+pjid+"').val()+\"&cid=", '"')
            html=getURL(url)
            sources=extract(html, 'sources:[', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                if extract(source, '"label":"', '"').upper() in params["extras"]:
                    link=extract(source, '"file":"', '"')
                    break
            return link
        elif "javhdfree" in params['url']:
            sources=extract(videosource, 'sources: [', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                if extract(source, 'label:"', '"').upper() in params["extras"]:
                    link=extract(source, 'file:"', '"')
                    break
            return link
        elif "jav-onlines" in params['name'] or "streamingjav" in params['name']:
            sources=extract(videosource, 'sources: [', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                if extract(source, 'label: "', '"').upper().replace("/LOWSD", "").replace("/SD", "").replace("/MINIHD", "").replace("/FULLHD", "") in params["extras"]:
                    link=extract(source, 'file: "', '"')
                    break
            return link.replace("\u0026", "&").replace("\u003d", "=") 
        elif "9player" in params['url']:
            sources=extract(videosource, 'sources: [', ']')
            sources=extractAll(sources, "{", "}")
            for source in sources:
                if extract(source, 'label: "', '"').upper().replace("/SD", "").replace("/HD", "").replace("/FHD", "") in params["extras"]:
                    link=extract(source, 'file: "', '"')
                    break
            return link
        else:
            res=params["extras"].replace("googlevideo (", "").replace(")", "")
            p=re.compile('<source src="([\S]*)" type="video\S*" data-res="'+res+'"\/>')
            link=re.search(p, videosource).group(1)
        return urlresolver.resolve(link)
    if "qwertycdn" in params["extras"]:
        sources=extract(videosource, '"sources":', ',"image"')
        sources=extractAll(sources, "{", "}")
        for source in sources:
            if extract(source, '"label":"', '"').upper() in params["extras"]:
                link=extract(source, '"file":"', '"').replace("\\", "")
                break
        return link
    if params["extras"]=="openload":
        if "javcuteonline"  in params['url']:
            if "str='@" in videosource:
                encoded=extract(videosource, "str='", "';").replace("@", "%")
                videosource=urllib.unquote_plus(encoded)
        if "freejav" in params['url']:
            videosource=base64.b64decode(extract(videosource, 'Base64.decode("', '"'))
        openloadurl = re.compile(r"//(?:www\.)?o(?:pen)?load\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadlist = list(set(openloadurl))
        if len(openloadlist) > 1:
            i = 1
            hashlist = []
            for x in openloadlist:
                hashlist.append('Video ' + str(i))
                i += 1
            openloadurl = openloadlist[olvideo]
        else: openloadurl = openloadurl[0]
        
        openloadurl = 'http://openload.io/embed/%s/' % openloadurl
        #logError(openloadurl)
        link=urlresolver.resolve(openloadurl)
    elif params["extras"]=="videowood":
        vwurl = re.compile(r"//(?:www\.)?videowood\.tv/(?:embed|video)/([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        vwurl = 'http://www.videowood.tv/embed/' + vwurl[0]
        vwsrc = getHtml(vwurl, params['url'])
        link = videowood(vwsrc)
    elif params["extras"]=="flashx":
        if "flashx" in params['url']:
            if "embed" in params['url']:
                 link=params['url'].replace("embed", "playvid")
            if "embed" not in params["url"] and "playvide" not in params["url"]:
                link=params["url"].replace("flashx.tv/", "flashx.tv/playvid-")
        else:
            try:
                p=re.compile(r"([http|https]+:\/\/www.flashx.tv\/embed.*?.html)")
                link=re.search(p, videosource).group(1)
                link=link.replace("embed", "playvid")
                #logError(link)
                videosource=getURL(link)
            except:
                p=re.compile(r"([http|https]+:\/\/www.flashx.tv\/playvid.*?.html)")
                link=re.search(p, videosource).group(1)
        
        html=getHtml(link, params['url'], hdr)
        if "Your browser does not support JavaScript! Please enable JavaScript!" in html:
            logError("JS ERROR "+link)
        if "This is prohibited!" in html:
            html=getURL("http://www.flashx.tv/reloadit.php?w=e&c=8843274&i=n0h6gezvcc53")
            html=getURL("http://www.flashx.tv/playvid-"+extract(html, "http://www.flashx.tv/playvid-", '"'))
        p="(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        result = re.findall(p, html)
        unpacked = cPacker().unpack(result[0])
        p=r"{file:\"([^\",]+)\",label:\"([^\"<>,]+)\"}"
        result = re.findall(p, unpacked)
        #logError(result[0][0].replace("play.", ""))
        return result[0][0].replace("play.", "")
    elif params["extras"]=="googlevideo":
        if "jav18" in params['url']:
            link=extract(videosource, 'file:"', '"')
            return link
        try: 
            p=re.compile('src=[\'|"](http[s]*:\/\/googlevideo.[\S]*)[\'|"]')
            link=re.search(p, videosource).group(1)
        except:
            try: 
                p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?googlevideo.\S.*?)[\'|"]')
                link=re.search(p, videosource).group(1)
            except:
                try:
                    p=re.compile('content=[\'|"]([http|https]\S*googleusercontent\S*)[\'|"]')
                    link=re.search(p, videosource).group(1)
                except:
                    try:
                        p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?docs.google.com.\S.*?)[\'|"]')
                        link=re.search(p, videosource).group(1)
                        link=urlresolver.resolve(link)
                    except:
                        try:
                            p=re.compile('sources: \[{file: "(\S*drive.google.com.*?)"')
                            link=re.search(p, videosource).group(1)
                            return link
                        except:
                            logError("Failed to get Googe Video link")
        #logError(link)
    elif params["extras"]=='streamin':
        streaminurl = re.compile(r"//(?:www\.)?streamin\.to/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        #logError(streaminurl[0])
        streaminurl = 'http://streamin.to/embed-%s-670x400.html' % streaminurl[0]
        streaminsrc = getURL(streaminurl)
        videohash = re.compile('\?h=([^"]+)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        videourl = re.compile('image: "(http://[^/]+/)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        link = videourl[0] + videohash[0] + "/v.mp4"
    else:
        try:
            p=re.compile('src=[\'|"](http[s]*:\/\/'+params['extra']+'.[\S]*)[\'|"]')
            link=urlresolver.resolve(re.search(p, videosource).group(1))
        except:
            pass
    #logError(link)
    return link

# videowood decode copied from: https://github.com/schleichdi2/OpenNfr_E2_Gui-5.3/blob/4e3b5e967344c3ddc015bc67833a5935fc869fd4/lib/python/Plugins/Extensions/MediaPortal/resources/hosters/videowood.py    
def videowood(data):
    parse = re.search('(....ωﾟ.*?);</script>', data)
    if parse:
        todecode = parse.group(1).split(';')
        todecode = todecode[-1].replace(' ','')

        code = {
            "(ﾟДﾟ)[ﾟoﾟ]" : "o",
            "(ﾟДﾟ) [return]" : "\\",
            "(ﾟДﾟ) [ ﾟΘﾟ]" : "_",
            "(ﾟДﾟ) [ ﾟΘﾟﾉ]" : "b",
            "(ﾟДﾟ) [ﾟｰﾟﾉ]" : "d",
            "(ﾟДﾟ)[ﾟεﾟ]": "/",
            "(oﾟｰﾟo)": '(u)',
            "3ﾟｰﾟ3": "u",
            "(c^_^o)": "0",
            "(o^_^o)": "3",
            "ﾟεﾟ": "return",
            "ﾟωﾟﾉ": "undefined",
            "_": "3",
            "(ﾟДﾟ)['0']" : "c",
            "c": "0",
            "(ﾟΘﾟ)": "1",
            "o": "3",
            "(ﾟｰﾟ)": "4",
            }
        cryptnumbers = []
        for searchword,isword in code.iteritems():
            todecode = todecode.replace(searchword,isword)
        for i in range(len(todecode)):
            if todecode[i:i+2] == '/+':
                for j in range(i+2, len(todecode)):
                    if todecode[j:j+2] == '+/':
                        cryptnumbers.append(todecode[i+1:j])
                        i = j
                        break
                        break
        finalstring = ''
        for item in cryptnumbers:
            chrnumber = '\\'
            jcounter = 0
            while jcounter < len(item):
                clipcounter = 0
                if item[jcounter] == '(':
                    jcounter +=1
                    clipcounter += 1
                    for k in range(jcounter, len(item)):
                        if item[k] == '(':
                            clipcounter += 1
                        elif item[k] == ')':
                            clipcounter -= 1
                        if clipcounter == 0:
                            jcounter = 0
                            chrnumber = chrnumber + str(eval(item[:k+1]))
                            item = item[k+1:]
                            break
                else:
                    jcounter +=1
            finalstring = finalstring + chrnumber.decode('unicode-escape')
        stream_url = re.search('=\s*(\'|")(.*?)$', finalstring)
        if stream_url:
            return stream_url.group(2)
    else:
        return

def searchFilms(parameters):
    find=searchDialog()
    if find!=False:
        if search.inDatabase(find)==False:
            search.addSearch(find)
            xbmc.executebuiltin('Container.Refresh')
        xbmcplugin.setContent(int(sysarg), "movies")
        findVideos(parameters['url']+"?s="+find, True)
    else:
        return False

def deleteSearch(params):
    try:
        if "single-delete" in params["extras"]:
            runDelete=True
    except:
        runDelete= xbmcgui.Dialog().yesno("Confirm Delete","Are you sure you want to delete ALL search terms?")
    if runDelete==True:
        search.removeSearch(params)
        xbmc.executebuiltin('Container.Refresh')

def deleteBookmark(params):
    if "single-delete" in params["extras"]:
        runDelete=True
    if runDelete==True:
        search.removeBookmarks(params)
        xbmc.executebuiltin('Container.Refresh')
        
def searchMenu():
    items=[]
    items.append({
        "title":"New Search", 
        "url":siteURL+"/index.php", 
        "mode":3, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'new-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "extras":"true-search"
    })
    items.append({
        "title":"[COLOR yellow]Clear Search Terms[/COLOR]", 
        "url":"delete-all", 
        "mode":31, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'clear-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
    })
    savedSearch=search.getSearch()
    savedSearch.sort()
    for ss in savedSearch:
        try:
            if len(ss[0])>0:
                items.append({
                    "title":ss[0], 
                    "url":siteURL+"/index.php", 
                    "mode":3, 
                    "poster":"none",
                    "icon":os.path.join(home, 'resources/media', 'main-search.jpg'), 
                    "fanart":os.path.join(home, '', 'fanart.jpg'),
                    "type":"", 
                    "plot":"",
                    "extras":"force-search",
                    "extras2":"db-search"
                })
        except:
            pass
    addMenuItems(items)
    
def addContextItem(liz, name,script,arg):
    commands = []
    runner = "XBMC.RunScript(" + str(script)+ ", " + str(arg) + ")"
    commands.append(( str(name), runner, ))
    liz.addContextMenuItems( commands )

if search.checkVersion(ADDON_VER)==False:
    alert("Support for JAVStream has moved to the Addon Release Forum at forums.tvaddons.ag\nAlso follow @javstreamkodi on Twitter for news and updates")
    getURL('http://javstream.club/version/version.php?v='+ADDON_VER)
    
def postHtml(url, form_data={}, headers={}, compression=True, NoCookie=None):
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
    req = urllib2.Request(url)
    if form_data:
        form_data = urllib.urlencode(form_data)
        req = urllib2.Request(url, form_data)
    req.add_header('User-Agent', _user_agent)
    for k, v in headers.items():
        req.add_header(k, v)
    if compression:
        req.add_header('Accept-Encoding', 'gzip')
    response = urllib2.urlopen(req)
    data = response.read()
    if not NoCookie:
        try:
            cj.save(cookiePath)
        except: pass
    response.close()
    return data
