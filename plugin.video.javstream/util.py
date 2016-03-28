#-*- coding: utf-8 -*-

import sys, urllib, urllib2, re, cookielib, os.path, json, base64
from bs4 import BeautifulSoup
from jsbeautifier import beautify
import xml.etree.ElementTree as ET
import azure_translate_api
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import urlresolver
from jsunpack import unpack
#import favourites

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
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

client = azure_translate_api.MicrosoftTranslatorClient('javstream',  # make sure to replace client_id with your client id
                                                       'npMjGpvt+346wdkiYD+sNteGdIvWvJWmEQYmVpIYA68=') # replace the client secret with the client secret for you app.


                                                       
                                                       
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

def getURL(url, header):
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

def getHtml(url, referer, hdr2=None):
    if not hdr2:
        req = Request(url.encode("utf-8"), '', hdr)
    else:
        req = Request(url.encode("utf-8"), '', hdr2)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
    cj.save(cookiePath)
    response.close()
    return data
    
def addMenuItems(details, show=True):
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
        
        
        #addContextItem(liz, "Add to favourites","special://home/addons/plugin.video.javstream2/addFavourite.py", "id=909722")
        #addContextItem(liz, "Add idol to favourites","special://home/addons/plugin.video.javstream2/addFavouriteIdol.py", "id=909722")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    if show:
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
    logError(cWindow.getResolution())
    cDialog.addControl(xbmcgui.ControlImage(x=cWindow.getWidth()/2, y=30, width=imgW, height=imgH, filename=img))
    cDialog.show()
    return cDialog

def customDialogClose(cDialog):
    cDialog.close()
 
def findVideos(url):
    html=getURL(url, hdr)
    if html!=False:
        items=[]
        #try:
        bsObj=BeautifulSoup(html, "html.parser")
        for sibling in bsObj.find("div",{"class":"entry"}).ul.findChildren():
            if sibling.name=="li":
                items.append({
                    "title": translate(sibling.find("a")["title"]),
                    "url": sibling.find("a")["href"], 
                    "mode":5, 
                    "poster":sibling.find("img")["src"],
                    "icon":sibling.find("img")["src"], 
                    "fanart":sibling.find("img")["src"].replace("thumb", "poster"),
                    "type":"video", 
                    "plot":"",
                })
        try:
            p=re.compile("<a href=[\"|'](\S*)[\"|'] class=[\"|']nextpostslink[\"|']>")
            next=re.search(p, html).group(1)
            items.append({
                    "title": "Next >",
                    "url":next, 
                    "mode":4, 
                    "poster":"default.jpg",
                    "icon":"default.jpg",
                    "fanart":"default.jpg",
                    "type":"", 
                    "plot":"",
                })
        except:
            # no next page found
            pass
        addMenuItems(items)
        #except:
        #    logError("Couldnt create video list")
    else:
        notify(ADDON_ID, "Unable to load page.", True)

def whatPlayer(url, site, dvdCode):
    html=getURL(url, hdr)  
    found=[]
    try:
        if site=="javseen":
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
                        alert("http://jav4k.net/"+video.find("a")["href"])
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
                    a=1
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
    return found
   
def huntVideo(params):
    urls=[]
    items=[]
    found=[]
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
    
    if xbmcplugin.getSetting(int(sysarg), "sexloading")=="true":
        huntSites.append("http://sexloading.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "ivhunter")=="true":
        huntSites.append("http://ivhunter.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javhdonline")=="true":
        huntSites.append("http://javhdonline.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "watchjavonline")=="true":
        huntSites.append("http://watchjavonline.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javlinks")=="true":
        huntSites.append("http://javlinks.com/search/"+dvdCode+"/feed/rss2/")
    if xbmcplugin.getSetting(int(sysarg), "dodova")=="true":
        huntSites.append("http://adult.dodova.com/search/"+dvdCode+"/feed/rss2/")
    if xbmcplugin.getSetting(int(sysarg), "hentaidream")=="true":
        huntSites.append("http://hentaidream.me/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "jav69")=="true":
        huntSites.append("http://jav69.biz/search/"+dvdCode+"/feed/rss2/")
    if xbmcplugin.getSetting(int(sysarg), "streamingjav")=="true":
        huntSites.append("http://streamjav.org/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "phimsexjav")=="true":
        huntSites.append("http://phimsexjav.net/search/"+dvdCode+"/feed/rss2") # description
    if xbmcplugin.getSetting(int(sysarg), "javwest")=="true":
        huntSites.append("http://javwest.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "dinojav")=="true":
        huntSites.append("http://www.dinojav.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "top1porn")=="true":
        huntSites.append("http://top1porn.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "jav-stream")=="true":
        huntSites.append("http://jav-stream.net/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javseen")=="true":
        huntSites.append("http://javseen.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "ikujav")=="true":
        huntSites.append("http://www.ikujav.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javst")=="true":
        huntSites.append("http://javst.net/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javlabels")=="true":
        huntSites.append("http://javlabels.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "terlarang")=="true":
        huntSites.append("http://terlarang.net/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "jav4k")=="true":
        huntSites.append("http://jav4k.net/moviesearch/"+dvdCode)
    if xbmcplugin.getSetting(int(sysarg), "javhub")=="true":
        huntSites.append("http://javhub.net/search/"+dvdCodeClean)
    if xbmcplugin.getSetting(int(sysarg), "jav-onlines")=="true":
        huntSites.append("http://jav-onlines.com/search/"+dvdCode+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "javeu")=="true":
        huntSites.append("http://javeu.com/search/"+dvdCodeClean+"/feed/rss2")
    if xbmcplugin.getSetting(int(sysarg), "yebbun90")=="true":
        huntSites.append("http://yebbun90.com/search/"+dvdCodeClean+"/feed/rss2")
    # to be added in the future
    # -------------------------
    # http://freenung-x.com
    # http://javch.com
    # http://javso.com
    # http://jav68.tv/
    # http://javpub.com/
    # http://sexiz.net/
    # http://sexvidx.tv/
    # http://jporn4u.com/
    # http://jav720p.com/
    # http://javstreaming.net/
    # http://javbabe.com/
    # http://www.jav24.us/
    # http://jamo.tv/
    # http://vk.com/wall-55136440
    # http://vk.com/videos-83300719?section=all
    # http://vk.com/videos-69328374?section=all
    # http://vk.com/videos-63032622?section=all
    # http://newpornhome.com/
    # http://playporn.to/
    
    p=re.compile("[http|https]*:\/\/(www.)?([a-zA-Z0-9-]*).")
    p1=re.compile("http:\/\/(www.)?([a-zA-Z0-9-]*.[a-z]*)")
    updateCounter=1
    updateBy=100/len(huntSites)
    statusDialog=progressStart("Searching for streams", "Searching: "+re.search(p1, huntSites[0]).group(2))
    # progressUpdate(pDialog, progress, status)
    for site in huntSites:        
        name=re.search(p, site).group(2)
        progressUpdate(statusDialog, updateCounter*updateBy, "Searching: "+re.search(p1, site).group(2))
        
        found=whatPlayer(site, name, dvdCode)
        counter=0
        for page in found:
            if name=="adult":
                name="dodova"
            if counter==0:
                link=page
                counter=1
            else:
                urls.append({"site":name, "source":page, "url":link})
        updateCounter=updateCounter+1
        if progressCancelled(statusDialog):
            return False
    
    counter=0
    if len(urls)>0:
        for url in urls:
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
        progressStop(statusDialog)
        addMenuItems(items)
    else:
        notify(ADDON_ID, "No Streams Found")
        
def translate(toTranslate):
    p1=re.compile(ur"[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]+ (?=[A-Za-z ]+–)", re.UNICODE)
    toTranslate=p1.sub("", toTranslate)
    
    if xbmcplugin.getSetting(int(sysarg), "translation")=="true":
        p=re.compile("(\[[A-Za-z0-9-_\ ]+\])")  
        dvdCode=p.match(toTranslate.encode("utf-8")).group(1)

        translated=client.TranslateText(toTranslate.replace(dvdCode, "").encode("utf-8"), 'ja', xbmcplugin.getSetting(int(sysarg), "language"))

        return dvdCode+" "+translated.title().replace('"', '')
        
    return toTranslate
    
def playMedia(title, thumbnail, link, mediaType='Video') :
    #link = urlresolver.resolve("https://openload.co/embed/QjfigJGJKs8/")
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
    
    """if params["extras"]=="videomega":
        p=re.compile('src=[\'|"](http[s]*:\/\/videomega.[\S]*)[\'|"]')
        link=urlresolver.resolve(re.search(p, videosource).group(1))
        #link=re.compile(r"//(?:www\.)?openload\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        logError("resolvered url="+link)    
        return link """
    
    link=False
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
        if re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
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
        errorCounter=0
        if "embedlink.info/videowood.php" in videosource:
            try:
                p=re.compile("(http:\/\/embedlink\.info\/videowood\.php\?url=\S*)[\"|']")
                videosource2=getURL(re.search(p, videosource).group(1), hdr)
                if "Base64.decode" in videosource:
                    p=re.compile("Base64.decode\(\"(\S*)\"\)")
                    videosource2=base64.b64decode(re.search(p, videosource2).group(1))
                    p=re.compile('src=[\'|"](\S*)[\'|"]')
                    videosource2=getURL(re.search(p, videosource2).group(1), hdr)
            except:
                pass
        else:
            p=re.compile(ur"videowood.[a-z]*\/embed\/([a-zA-Z0-9]*)")
            videosource2=getURL("http://videowood.tv/embed/"+re.search(p, videosource).group(1), hdr)
            if videosource2==False:
                p=re.compile(ur"http[s]*:\/\/[w.]*videowood.tv\/video\/([a-zA-Z0-9]+)")
                videosource2=getURL("http://videowood.tv/embed/"+re.search(p, videosource).group(1), hdr)
            
            matches=re.findall("(eval.function.p,a,c,k,e,.*?)\s*</script>", videosource2, flags=re.DOTALL )
            data=unpackjs(matches[0])
            pattern = r'"file"\s*:\s*"([^"]+/video/[^"]+)'
            link=re.search(pattern, data, re.DOTALL).group(1)
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
    else:
        try:
            p=re.compile('src=[\'|"](http[s]*:\/\/'+params['extra']+'.[\S]*)[\'|"]')
            link=urlresolver.resolve(re.search(p, videosource).group(1))
        except:
            logError("EXTRA equals NULL")
    """elif params["extras"]=="streamin":
        p=re.compile("(https?:\/\/[www.|.]*flashx.[a-z]*\/embed[a-zA-Z0-9-]*.html)")
        url=re.search(p, videosource).group(1)
        logError(url)
        link=urlresolver.resolve(url)"""
    """    link="http://5.79.81.106:8777/tkipfe5o6huzcg3h5gscbfhe22nk4ll7jtlkj3gv24o5dirajilhtayxgkiq/v.mp4"
    elif params["extras"]=="googlevideo":
        try:
            p=re.compile('<source src="(\S*)"')
            link=re.search(p, videosource).group(1)
        except:
            try:
                quality=["360p", "720p", "1080p"]
                for q in quality:
                    p=re.compile('"file":"([a-zA-Z0-9:\/\.\-\=]*)","label":"'+q+'"')
                    link=re.search(p, videosource).group(1)
            except:
                pass"""
    logError(str(link))
    return link

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
"""
def decodeOpenLoad(html):

    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html, re.DOTALL | re.IGNORECASE).group(1)
    
    # decodeOpenLoad made by mortael, please leave this line for proper credit :)
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
    aastring = aastring.replace("(ﾟｰﾟ)","4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
    aastring = aastring.replace("(o^_^o)","3")
    aastring = aastring.replace("(ﾟΘﾟ)","1")
    aastring = aastring.replace("(+!+[])","1")
    aastring = aastring.replace("(c^_^o)","0")
    aastring = aastring.replace("(0+0)","0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
    aastring = aastring.replace("(3 +3 +0)","6")
    aastring = aastring.replace("(3 - 1 +0)","2")
    aastring = aastring.replace("(!+[]+!+[])","2")
    aastring = aastring.replace("(-~-~2)","4")
    aastring = aastring.replace("(-~-~1)","3")
    
    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+"+ decodestring
    decodestring = decodestring.replace("+","")
    decodestring = decodestring.replace(" ","")
    
    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/","/")`

    return videourl
    videourl = re.search(r"vr\s?=\s?\"|'([^\"']+)", decodestring, re.DOTALL | re.IGNORECASE).group(1)
"""
def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')

def getFavourites():
    return favourites.getFavourites()
    
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