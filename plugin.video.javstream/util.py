#-*- coding: utf-8 -*-

import sys, urllib, urllib2, re, cookielib, os.path, json, base64, tempfile, time, threading
from bs4 import BeautifulSoup
from jsbeautifier import beautify
import xml.etree.ElementTree as ET
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import urlresolver
from jsunpack import unpack
import search

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)

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

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

globalURLS=[]
statusDialog=""  
updateCounter=0  
updateBy=0 
updateTotal=0

if xbmcplugin.getSetting(int(sysarg), "proxy")=="true":
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
            if (len(nameValuePair) > 0):
                pair = nameValuePair.split('=')
                key = pair[0]
                value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                parameters[key] = value
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

def getURL(url, header=hdr):
    try:
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req)
        if response and response.getcode() == 200:
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO( response.read())
                gzip_f = gzip.GzipFile(fileobj=buf)
                content = gzip_f.read()
            else:
                content = response.read()
            content = content.decode('utf-8', 'ignore')
            return content
    except:
        xbmc.log('Error Loading URL : '+url.encode("utf-8"), xbmc.LOGERROR)
        try:
            xbmc.log("Error Code: "+str(response.getcode())+' Content: '+response.read(), xbmc.LOGERROR)
        except:
            pass
    
    return False

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
    
def addMenuItems(details, show=True):
    changed=False
    for detail in details:
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].decode("utf-8"), iconImage=detail['icon'])
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
        if detail['mode']==5:
            changed=True
            view = (sys.argv[0] +
                "?url=set-default-view" +
                "&mode=" + str(10) +
                "&poster="+detail['poster']+
                "&fanart="+detail['fanart']+
                "&extras="+sysarg+
                "&name=" + "set-default-view")
            liz.addContextMenuItems([('Set Default View', 'xbmc.RunPlugin('+view+')')])
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    if show:
        if changed==True:
            xbmc.executebuiltin('Container.SetViewMode(%d)' % int(xbmcplugin.getSetting(int(sysarg), "vidview")))
        xbmcplugin.endOfDirectory(int(sysarg))

def alert(alertText):
    dialog = xbmcgui.Dialog()
    ret = dialog.ok("JAVStream", alertText.title())
        
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

def progressStart(title, status):
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(title, status)
    progressUpdate(pDialog, 1, status)
    return pDialog

def progressStop(pDialog):
    pDialog.close
    
def progressCancelled(pDialog):
    if pDialog.iscanceled():
        return True
    return False

def progressUpdate(pDialog, progress, status):
    pDialog.update(progress, status)

def customDialog(imgW, imgH, img):
    cDialog=xbmcgui.WindowDialog()
    cWindow=xbmcgui.Window()
    #logError(cWindow.getResolution())
    cDialog.addControl(xbmcgui.ControlImage(x=cWindow.getWidth()/2, y=30, width=imgW, height=imgH, filename=img))
    cDialog.show()
    return cDialog

def customDialogClose(cDialog):
    cDialog.close()
 
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
                        "icon":os.path.join(home, 'resources/media', 'next.jpg'),
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
    global updateCounter
    global updateString
    global updateTotal
    if "<javpage=" in url:
        parts=url.split("<")
        url=parts[0]
        parts=parts[1].replace("javpage=", "")
    html=getURL(url, hdr)  
    found=[]
    
    try:
        if site=="javstreams":
            p=re.compile("(javstreams\.com\/play\?v=\S.*?)\"")
            page="http://"+re.search(p,html).group(1)
        elif site=="javshow" or site=="eropoi" or site=="youpornjav" or site=="javabc" or site=="javhdvideo":
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
            #p=re.compile("<item>[\s|\S]*<link>([\S]*)<\/link>")
            p=re.compile("<guid[^>]+>(\S*)<\/guid>")
            page=re.search(p, html).group(1).replace("javseen.com/", "javseen.com/watch-");
            # need to add code to check for extra pages
        #elif site=="terlarang":
        #    page="http://terlarang.net/"+dvdCode+"-watch-online"
        elif site=="jav4k":
            dvdCode=dvdCode.replace("%22", "")
            if '<span class="sku"><span>'+dvdCode+'</span></span>' in html:
                bsObj=BeautifulSoup(html, "html.parser")
                videos=bsObj.findAll("div", {"class":"video_box_dvd"})
                for video in videos:
                    if dvdCode in str(video):
                        html=getURL("http://jav4k.net/"+video.find("a")["href"], hdr)
                        if html!=False:
                            p=re.compile('href="(watch-\S*)"')
                            page="http://jav4k.net/"+re.search(p, html).group(1)
        elif site=="javhub":
            dvdCode=dvdCode.replace("%22", "")
            if 'title="'+dvdCode in html:
                bsObj=BeautifulSoup(html, "html.parser")
                for sibling in bsObj.find("div",{"class":"section-main-content"}).ul.findChildren():
                    if sibling.name=="li" and dvdCode in str(sibling):
                        page="http://javhub.net/"+sibling.find("a")["href"]
                        break
        elif site=="jav-onlines":
            if "playerriz.com" in html:
                p=re.compile("<iframe src=\"https:\/\/(www.playerriz.com\/embed\?v=\S+)\"");
                page="http://"+re.search(p, html).group(1)
        else:
            #p=re.compile("<item>[\S\s]+<link>([^<]+)")
            p=re.compile("<guid[^>]+>(\S*)<\/guid>")
            page=re.search(p, html).group(1)
        
        html=getURL(page, hdr)
        found.append(page)
    except:
        html=False
        #logError(site+": Link not found in "+url.encode("utf-8"))
    
    if html!=False and site!="adult":
        if 'type="video/mp4" data-res="480"' in html:
            found.append("googlevideo (480)")
        if 'type="video/mp4" data-res="720"' in html:
            found.append("googlevideo (720)")
        if 'type="video/mp4" data-res="1080"' in html:
            found.append("googlevideo (1080)")
        if "googlevideo" in html or "googleusercontent" in html:
            p=re.compile('src=[\'|"](http[s]*:\/\/googleusercontent.[\S]*)[\'|"]')
            try: 
                link=urlresolver.resolve(re.search(p, html).group(1))
                found.append("googlevideo")
            except:
                p=re.compile('src=[\'|"](http[s]*:\/\/googlevideo.[\S]*)[\'|"]')
                try: 
                    link=urlresolver.resolve(re.search(p, html).group(1))
                    found.append("googlevideo")
                except:
                    p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?googlevideo.\S.*?)[\'|"]')
                    try: 
                        link=urlresolver.resolve(re.search(p, html).group(1))
                        found.append("googlevideo")
                    except:
                        pass
        if "videomega" in html:
            found.append("videomega")
        if "openload" in html:
            found.append("openload")
        if "flashx" in html: #to be added in the future
            found.append("flashx")
        if "videowood" in html:
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
            found.append("flashx")
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
    counter=0
    for page in found:
        if site=="adult":
            site="dodova"
        if counter==0:
            link=page
            counter=1
        else:
            globalURLS.append({"site":site, "source":page, "url":link})
    updateTotal=updateTotal+1
    updateString=updateString.replace(site, "")
    updateCounter=updateCounter+1
   
def huntVideo(params):
    global updateString
    global updateTotal
    urls=[]
    items=[]
    found=[]
    search=str(params["extras"])
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
    
    udvdCode=dvdCode.replace("-", "%20")
    
    search=search.split(",")
    titles=[]
    for searching in search:
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
        if xbmcplugin.getSetting(int(sysarg), searching+"jav69")=="true":
            titles.append("jav69")
            huntSites.append("http://jav69.biz/search/"+dvdCode+"/feed/rss2/")
        if xbmcplugin.getSetting(int(sysarg), searching+"streamingjav")=="true":
            titles.append("streamjav")
            huntSites.append("http://streamjav.org/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"phimsexjav")=="true":
            titles.append("phimsexjav")
            huntSites.append("http://phimsexjav.net/search/"+dvdCode+"/feed/rss2") # description
        if xbmcplugin.getSetting(int(sysarg), searching+"javwest")=="true":
            titles.append("javwest")
            huntSites.append("http://javwest.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"dinojav")=="true":
            titles.append("dinojav")
            huntSites.append("http://www.dinojav.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"top1porn")=="true":
            titles.append("top1porn")
            huntSites.append("http://top1porn.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jav-stream")=="true":
            titles.append("jav-search")
            huntSites.append("http://jav-stream.net/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javseen")=="true":
            titles.append("javseen")
            huntSites.append("http://javseen.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"ikujav")=="true":
            titles.append("ikujav")
            huntSites.append("http://www.ikujav.com/search/"+dvdCode+"/feed/rss2")
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
            huntSites.append("http://javhub.net/search/"+dvdCodeClean)
        if xbmcplugin.getSetting(int(sysarg), searching+"jav-onlines")=="true":
            titles.append("jav-onlines")
            huntSites.append("http://jav-onlines.com/search/"+dvdCode+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javeu")=="true":
            titles.append("javeu")
            huntSites.append("http://javeu.com/search/"+dvdCodeClean+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"yebbun90")=="true":
            titles.append("yebbun90")
            huntSites.append("http://yebbun90.com/search/"+dvdCodeClean+"/feed/rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"youpornjav")=="true":   
            titles.append("youpornjav")
            huntSites.append("http://www.youpornjav.com/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"javshow")=="true":
            titles.append("javshow")
            huntSites.append("http://javshow.net/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"eropoi")=="true":
            titles.append("eropoi")
            huntSites.append("http://eropoi.com/post-sitemap.xml")
            huntSites.append("http://eropoi.com/post-sitemap.xml<javpage=2")
            huntSites.append("http://eropoi.com/post-sitemap.xml<javpage=3")
            # needs new sources adding
        if xbmcplugin.getSetting(int(sysarg), searching+"jav720p")=="true":
            titles.append("jav720p")
            huntSites.append("http://jav720p.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"korean720")=="true":
            titles.append("korean720")
            huntSites.append("http://korean720.com/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javstreams")=="true": 
            titles.append("javstreams")
            huntSites.append("http://javstreams.com/?s="+dvdCode+"&feed=rss2")
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
            titles.append("havhdvideo")
            huntSites.append("http://javhdvideo.net/sitemap.xml")
        if xbmcplugin.getSetting(int(sysarg), searching+"javsex")=="true":
            titles.append("javsex")
            huntSites.append("http://javsex.net/?s="+dvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"jpidols")=="true":
            titles.append("jpidols")
            huntSites.append("http://jpidols.tv/?s="+dvdCode+"&feed=rss2")
            huntSites.append("http://jpidols.tv/?s="+udvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"javfree")=="true":
            titles.append("javhdfree")
            huntSites.append("http://javhdfree.net/?s="+dvdCode+"&feed=rss2")
            huntSites.append("http://javhdfree.net/?s="+udvdCode+"&feed=rss2")
        if xbmcplugin.getSetting(int(sysarg), searching+"dojav69")=="true":
            titles.append("dojav69")
            huntSites.append("http://doojav69.com/?s="+dvdCode+"&feed=rss2")
            huntSites.append("http://doojav69.com//?s="+udvdCode+"&feed=rss2")
            
    huntSites=unique(huntSites)  
    updateString=" ".join(titles)
    # to be added in the future
    # -------------------------
    # javchan.com
    # javcenso.com
    # javuncen.me
    
    
    #p1=re.compile("http:\/\/(www.)?([a-zA-Z0-9-]*.[a-z]*)")
    p=re.compile("[http|https]*:\/\/(www.)?([a-zA-Z0-9-]*).")
    updateBy=100/len(huntSites)
    
    statusDialog=progressStart("Searching for streams", "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")
    progressUpdate(statusDialog, updateCounter*updateBy, "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")
    
    threads=[threading.Thread(target=whatPlayer, args=(url, re.search(p, url).group(2), dvdCode,)) for url in huntSites]
    for thread in threads:
        thread.start()

    while updateTotal<len(huntSites):
        progressUpdate(statusDialog, updateCounter*updateBy, "Searching: "+str(updateTotal)+" out of "+str(len(huntSites))+" sites searched, please wait...")
        if len(globalURLS)>0 and xbmcplugin.getSetting(int(sysarg), "autoplay")=="true":
            progressCancelled(statusDialog)
            break
    
    for thread in threads:
        try:
            thread.exit()
        except:
            pass
    
    counter=0
    if len(globalURLS)>0:
        for url in globalURLS:
            counter=counter+1
            items.append({
                "title": str(counter).zfill(2)+" | [B]"+url["site"]+"[/B] | "+url["source"],
                "url": url["url"], 
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
                myurl=getVideoURL(items[0])
                playMedia(params["name"], params["poster"], myurl, "Video")
                return False
        progressStop(statusDialog)
        addMenuItems(items)
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
    
def playMedia(title, thumbnail, link, mediaType='Video') :
    """Plays a video

    Arguments:
    title: the title to be displayed
    thumbnail: the thumnail to be used as an icon and thumbnail
    link: the link to the media to be played
    mediaType: the type of media to play, defaults to Video. Known values are Video, Pictures, Music and Programs
    """
    try:
        li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
        li.setInfo(type=mediaType, infoLabels={ "Title": title })
        xbmc.Player().play(item=link, listitem=li)
    except:
        if link!=False:
            notify(ADDON_ID, "Unable to play stream. "+str(link))
    
def getVideoURL(params):
    #logError("getting "+params["url"].encode("utf-8"))
    videosource=getURL(params["url"].encode("utf-8"), hdr)
    if "javeu.com" in params["url"]:
        
        p=re.compile('<td>'+params["extras"]+'[\S\s]*?href="([\S\s]*?)"')
        videosource=getURL(re.search(p, videosource).group(1).encode("utf-8"), hdr)
        p=re.compile('document\.write\(doit\("([\s\S]*?)"\)')
        videosource=base64.b64decode(base64.b64decode(re.search(p, videosource).group(1)))
    else:
        videosource=getURL(params["url"].encode("utf-8"), hdr)
    
    link=False
    if params["extras"]=="googlevideo (1080)" or  params["extras"]=="googlevideo (720)" or params["extras"]=="googlevideo (480)":
        res=params["extras"].replace("googlevideo (", "").replace(")", "")
        p=re.compile('<source src="([\S]*)" type="video\S*" data-res="'+res+'"\/>')
        link=re.search(p, videosource).group(1)
    if params["extras"]=="openload":
        openloadurl = re.compile(r"//(?:www\.)?openload\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadlist = list(set(openloadurl))
        if len(openloadlist) > 1:
            i = 1
            hashlist = []
            for x in openloadlist:
                hashlist.append('Video ' + str(i))
                i += 1
            openloadurl = openloadlist[olvideo]
        else: openloadurl = openloadurl[0]
        
        openloadurl1 = 'http://openload.co/embed/%s/' % openloadurl

        #try:
        openloadsrc = getHtml(openloadurl1, '', hdr)
        link = decodeOpenLoad(openloadsrc)
        #except:
        #    return
    elif params["extras"]=="videomega":
        if ".mp4" in videosource:
            p=re.compile("SRC='([\s\S]*?)'")
            link=re.search(p, videosource).group(1)
        elif re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile("""javascript["']>ref=['"]([^'"]+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/iframe.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r"iframe\.php\?ref=([^&]+)&", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/view.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'view\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/cdn.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'cdn\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/\?ref=", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'videomega.tv/\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        else:
            hashkey = re.compile("""hashkey=([^"']+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
            if not hashkey:
                dialog.ok('Oh oh','Couldn\'t find playable videomega link')
                return
            if len(hashkey) > 1:
                i = 1
                hashlist = []
                for x in hashkey:
                    hashlist.append('Video ' + str(i))
                    i += 1
                vmvideo = dialog.select('Multiple videos found', hashlist)
                hashkey = hashkey[vmvideo]
            else: hashkey = hashkey[0]
            hashpage = getHtml('http://videomega.tv/validatehash.php?hashkey='+hashkey, params['url'])
            hashref = re.compile('ref="([^"]+)', re.DOTALL | re.IGNORECASE).findall(hashpage)
        #progress.update( 80, "", "Getting video file from Videomega", "" )
        vmhost = 'http://videomega.tv/view.php?ref=' + hashref[0]
        videopage = getHtml(vmhost, params['url'])
        vmpacked = re.compile(r"(eval\(.*\))\s+</", re.DOTALL | re.IGNORECASE).findall(videopage)
        vmunpacked = unpack(vmpacked[0])
        videourl = re.compile('src",\s?"([^"]+)', re.DOTALL | re.IGNORECASE).findall(vmunpacked)
        videourl = videourl[0]
        videourl = videourl + '|Referer=' + vmhost + '&User-Agent:%20Mozilla/5.0%20(Windows%20NT%206.1;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/46.0.2490.86%20Safari/537.36'

        link = videourl
    elif params["extras"]=="videowood":
        vwurl = re.compile(r"//(?:www\.)?videowood\.tv/(?:embed|video)/([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        vwurl = 'http://www.videowood.tv/embed/' + vwurl[0]
        vwsrc = getHtml(vwurl, params['url'])
        link = videowood(vwsrc)
    elif params["extras"]=="flashx":
        flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        flashxlist = list(set(flashxurl))
        if len(flashxlist) > 1:
            i = 1
            hashlist = []
            for x in flashxlist:
                hashlist.append('Video ' + str(i))
                i += 1
            flashxurl = flashxlist[fxvideo]
        else: flashxurl = flashxurl[0]        
        flashxurl = 'http://flashx.tv/embed-%s-670x400.html' % flashxurl
        
        flashxsrc = getURL(flashxurl, hdr)
        flashxurl2 = re.compile('<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(flashxsrc)
        flashxsrc2 = getURL(flashxurl2[0], hdr)
        flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc2)
        try: flashxujs = unpack(flashxjs[0])
        except: flashxujs = flashxjs[0]
        
        videourl = re.compile(r'\[{\s?file:\s?"([^"]+)",', re.DOTALL | re.IGNORECASE).findall(flashxujs)
        link = videourl[0]
    elif params["extras"]=="googlevideo":
        try: 
            p=re.compile('src=[\'|"](http[s]*:\/\/googlevideo.[\S]*)[\'|"]')
            link=re.search(p, videosource).group(1)
        except:
            try: 
                p=re.compile('file: [\'|"](http[s]*:\/\/\S.*?googlevideo.\S.*?)[\'|"]')
                link=re.search(p, videosource).group(1)
            except:
                logError("Failed getting google video")
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
    
def decodeOpenLoad(html):
    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html,
                         re.DOTALL | re.IGNORECASE).group(1)

    aastring = aastring.replace(
        "(\xef\xbe\x9f\xd0\x94\xef\xbe\x9f)[\xef\xbe\x9f\xce\xb5\xef\xbe\x9f]+(o\xef\xbe\x9f\xef\xbd\xb0\xef\xbe\x9fo)+ ((c^_^o)-(c^_^o))+ (-~0)+ (\xef\xbe\x9f\xd0\x94\xef\xbe\x9f) ['c']+ (-~-~1)+",
        "")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))", "8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))", "7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))", "6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))", "5")
    aastring = aastring.replace("(ﾟｰﾟ)", "4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))", "2")
    aastring = aastring.replace("(o^_^o)", "3")
    aastring = aastring.replace("(ﾟΘﾟ)", "1")
    aastring = aastring.replace("(+!+[])", "1")
    aastring = aastring.replace("(c^_^o)", "0")
    aastring = aastring.replace("(0+0)", "0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]", "\\")
    aastring = aastring.replace("(3 +3 +0)", "6")
    aastring = aastring.replace("(3 - 1 +0)", "2")
    aastring = aastring.replace("(!+[]+!+[])", "2")
    aastring = aastring.replace("(-~-~2)", "4")
    aastring = aastring.replace("(-~-~1)", "3")
    aastring = aastring.replace("(-~0)", "1")
    aastring = aastring.replace("(-~1)", "2")
    aastring = aastring.replace("(-~3)", "4")
    aastring = aastring.replace("(0-0)", "0")

    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+" + decodestring
    decodestring = decodestring.replace("+", "")
    decodestring = decodestring.replace(" ", "")

    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/", "/")

    if 'toString' in decodestring:
        base = int(re.compile('toString\\(a\\+(\\d+)', re.DOTALL | re.IGNORECASE).findall(decodestring)[0])
        match = re.compile('(\\(\\d[^)]+\\))', re.DOTALL | re.IGNORECASE).findall(decodestring)
        for rep1 in match:
            match1 = re.compile('(\\d+),(\\d+)', re.DOTALL | re.IGNORECASE).findall(rep1)
            base2 = base + int(match1[0][0])
            rep12 = base10toN(int(match1[0][1]), base2)
            decodestring = decodestring.replace(rep1, rep12)
        decodestring = decodestring.replace('+', '')
        decodestring = decodestring.replace('"', '')
        videourl = re.search('(http[^\\}]+)', decodestring, re.DOTALL | re.IGNORECASE).group(1)
    else:
        videourl = re.search(r"vr\s?=\s?\"|'([^\"']+)", decodestring, re.DOTALL | re.IGNORECASE).group(1)
    return videourl


def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')


def base10toN(num, n):
    num_rep = {10: 'a',
               11: 'b',
               12: 'c',
               13: 'd',
               14: 'e',
               15: 'f',
               16: 'g',
               17: 'h',
               18: 'i',
               19: 'j',
               20: 'k',
               21: 'l',
               22: 'm',
               23: 'n',
               24: 'o',
               25: 'p',
               26: 'q',
               27: 'r',
               28: 's',
               29: 't',
               30: 'u',
               31: 'v',
               32: 'w',
               33: 'x',
               34: 'y',
               35: 'z'}
    new_num_string = ''
    current = num
    while current != 0:
        remainder = current % n
        if 36 > remainder > 9:
            remainder_string = num_rep[remainder]
        elif remainder >= 36:
            remainder_string = '(' + str(remainder) + ')'
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
        current = current / n
    return new_num_string

    
def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')

def searchFilms(parameters):
    find=searchDialog()
    if search.inDatabase(find)==False:
        search.addSearch(find)
        xbmc.executebuiltin('Container.Refresh')
    findVideos(parameters['url']+"?s="+find, True)

def deleteSearch(params):
    try:
        if "single-delete" in params["extras"]:
            runDelete=True
    except:
        runDelete= xbmcgui.Dialog().yesno("Confirm Delete","Are you sure you want to delete ALL search terms?")
    if runDelete==True:
        search.removeSearch(params)
        xbmc.executebuiltin('Container.Refresh')
    
def searchMenu():
    items=[]
    items.append({
        "title":"New Search", 
        "url":siteURL+"/index.php", 
        "mode":3, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'search-main.jpg'), 
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
        "icon":os.path.join(home, 'resources/media', 'search-main.jpg'), 
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
                    "icon":os.path.join(home, 'resources/media', 'search-main.jpg'), 
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

def unpackjs(texto,tipoclaves=1):
    
    patron = "return p\}(.*?)\.split"
    matches = re.compile(patron,re.DOTALL).findall(texto)
    if len(matches)>0:
        data = matches[0]
    else:
        patron = "return p; }(.*?)\.split"
        matches = re.compile(patron,re.DOTALL).findall(texto)
        if len(matches)>0:
            data = matches[0]
        else:
            return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    descifrado = ""
    
    # Crea el dicionario con la tabla de conversion
    claves = []
    if tipoclaves==1:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    else:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
        claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
        claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
        
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:
        #logger.info("i=%d" % i)
        #logger.info("claves_i="+claves[i])
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

    # Sustituye las palabras de la tabla de conversion
    # Obtenido de http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

    #lista = map(re.escape, diccionario)
    # Invierte las claves, para que tengan prioridad las más largas
    claves.reverse()
    cadenapatron = '|'.join(claves)
    #logger.info("[unpackerjs.py] cadenapatron="+cadenapatron)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)
    descifrado = descifrado.replace("\\","")

    return descifrado