#-*- coding: utf-8 -*-

import sys, urllib, urllib2, re, cookielib, os.path, json, base64, tempfile, time
import xml.etree.ElementTree as ET
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
from jsunpack import unpack
#import favourites

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.jamo68'
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
    #logError(cWindow.getResolution())
    cDialog.addControl(xbmcgui.ControlImage(x=cWindow.getWidth()/2, y=30, width=imgW, height=imgH, filename=img))
    cDialog.show()
    return cDialog

def customDialogClose(cDialog):
    cDialog.close()

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

def jamoMenu(start, end):
    html=getURL("http://jamo.tv/contact.html")
    if html!=False:
        categories=extract(html, start, end)
        category=extractAll(categories, '<b>', '</b>')
        items=[]
        
        for cat in category:
            items.append({
                "title": extract(cat, '>', '<'),
                "url": "http://jamo.tv/"+extract(cat, '"', '"'), 
                "mode":111, 
                "poster":"none",
                "icon":"none", 
                "fanart":os.path.join(home, '', 'fanart.jpg'),
                "type":"video", 
                "plot":"none",
            })
        addMenuItems(items)

def jamoVideos(params):
    html=getURL(params["url"])
    if html!=False:
        movies=extractAll(html, '<div class="movie">', '</a>')
        items=[]
        for movie in movies:
            items.append({
                "title": extract(movie, 'title="', '"'),
                "url": extract(movie, 'href="', '"'), 
                "mode":120, 
                "poster":extract(movie, 'src="', '"'),
                "icon":extract(movie, 'src="', '"'), 
                "fanart":extract(movie, 'src="', '"').replace("thumb", "big"),
                "type":"video", 
                "plot":"none",
            })
        commands=extractAll(html, 'class="command"', '>')
        for next in commands:
            if 'Next' in next:
                logError(next)
                items.append({
                    "title": "Next Page >",
                    "url": "http://jamo.tv/"+extract(next, 'href="', '"'), 
                    "mode":111, 
                    "poster":"default.jpg",
                    "icon":"default.jpg", 
                    "fanart":os.path.join(home, '', 'fanart.jpg'),
                    "type":"video", 
                    "plot":"none",
                })
                break
        addMenuItems(items)
        
def jamoModels(url):
    if url=="model-link":
        html=getURL('http://jamo.tv/top-models-page-1.html')
        if html!=False:
            alphabet=extract(html, '<div style="margin-left:10px;  font: bold 14px Arial, Helvetica; color:#F60;">', '</div>')
            letters=extractAll(alphabet, '<a', 'a>')
            items=[]
            for letter in letters:
                items.append({
                    "title": extract(letter, '>', '<'),
                    "url": extract(letter, 'href="', '"'), 
                    "mode":13, 
                    "poster":"default.jpg",
                    "icon":"default.jpg", 
                    "fanart":os.path.join(home, '', 'fanart.jpg'),
                    "type":"video", 
                    "plot":"none",
                })
            addMenuItems(items)
    else:
        html=getURL(url)
        if html!=False:
            models=extractAll(html, '<div class="poster">', '</div>')
            items=[]
            for model in models:
                items.append({
                    "title": extract(model, 'title="', '"'),
                    "url": "http://jamo.tv/"+extract(model, 'href="', '"'), 
                    "mode":13, 
                    "poster":extract(model, 'src="', '"'),
                    "icon":extract(model, 'src="', '"'), 
                    "fanart":os.path.join(home, '', 'fanart.jpg'),
                    "type":"video", 
                    "plot":"none",
                })
            commands=extractAll(html, 'class="command"', '>')
            for next in commands:
                if 'Next' in next:
                    logError(next)
                    items.append({
                        "title": "Next Page >",
                        "url": "http://jamo.tv/"+extract(next, 'href="', '"'), 
                        "mode":111, 
                        "poster":"default.jpg",
                        "icon":"default.jpg", 
                        "fanart":os.path.join(home, '', 'fanart.jpg'),
                        "type":"video", 
                        "plot":"none",
                    })
                    break
            addMenuItems(items)
        
def jamoGetSource(params):
    html=getURL(params['url'])
    if html!=False:
        link=extract(html, '<div class="index_update_left">', '>')
        page=extract(link, 'href="', '"')
        movieid=extract(page, "video-", "/")
        html=getURL("http://jamo.tv/?server_player="+movieid)
        logError(html)
        player=""
        if "videomega" in html:
            player="videomega"
        elif "flashx" in html:
            player="flashx"
        elif "openload" in html:
            player="openload"
        elif "videowood" in html:
            player="videowood"
        
        if player!="":
            url=getVideoURL({"url":"http://jamo.tv/?server_player="+movieid, "extras":player})
            playMedia(params['name'], params['poster'], url, "Video")   
        else:
            logError(html)

def jav68Menu(params):
    html=getURL('http://jav68.me')
    if html!=False:
        if params['url']=='category-link':
            content=extract(html, '<h2 class="filter-main-heading text-center">Categories</h2>', '</ul>')
        else:
            content=extract(html, '<h2 class="filter-main-heading text-center">Studios</h2>', '</ul>')
        links=extractAll(content, '<li>', '</li>')
        items=[]
        for link in links:
            items.append({
                "title": extract(link, 'title="', '"'),
                "url": extract(link, 'href="', '"'), 
                "mode":211, 
                "poster":'default.jpg',
                "icon":'default.jpg', 
                "fanart":os.path.join(home, '', 'fanart.jpg'),
                "type":"video", 
                "plot":"none",
            })
        addMenuItems(items)

def jav68GetVideos(params):
    html=getURL(params['url'])
    if html!=False:
        movies=extractAll(html, '<a class="main-thumb"', '</a>')
        items=[]
        for movie in movies:
            url=extract(movie, 'href="', '"')
            html2=getURL(url)
            content=extract(html2, '<div id="area_tx">', '</div>')
            fanart=extract(content, 'src="', '"')
            url=extract(html2, '<p class="clearfix wrap-btn">', '</a>')
            url=extract(url, 'href="', '"')
            
            items.append({
                "title": extract(movie, 'title="', '"'),
                "url": url, 
                "mode":220, 
                "poster":extract(movie, 'src="', '"'),
                "icon":extract(movie, 'src="', '"'), 
                "fanart":fanart,
                "type":"video", 
                "plot":"none",
            })
            
        commands=extract(html, '<ul class="episodes">', '</ul>')
        links=extractAll(commands, '<li>', '</li>')
        for next in links:
            if 'Next' in next:
                items.append({
                    "title": "Next Page >",
                    "url": extract(next, 'href="', '"'), 
                    "mode":211, 
                    "poster":"default.jpg",
                    "icon":"default.jpg", 
                    "fanart":os.path.join(home, '', 'fanart.jpg'),
                    "type":"video", 
                    "plot":"none",
                })
                break
        addMenuItems(items)

def jav68GetSource(params):
    html=getURL(params['url'])
    if html!=False:
        logError(params['url'])
        player=""
        if "codeplay" in html:
            f={}
            codePlay=extract(html, 'codeplay', ',"')
            f['string']=extract(codePlay, "'", "',")
            f['key']=extract(codePlay, "',", ')')
            url=getURL("http://www.asianteensfor.me/decrypt/?"+urllib.urlencode(f))
            playMedia(params['name'], params['poster'], url, "Video")
        elif "videomega" in html:
            player="videomega"
        elif "flashx" in html:
            player="flashx"
        elif "openload" in html:
            player="openload"
        elif "videowood" in html:
            player="videowood"
        if player!="":
            logError("Playing "+player)
            url=getVideoURL({"url":params['url'], "extras":player})
            playMedia(params['name'], params['poster'], url, "Video")  
    
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

    