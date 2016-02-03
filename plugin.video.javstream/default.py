#-*- coding: utf-8 -*-

import urllib2, re, urllib, base64, difflib, time, json, base64, HTMLParser, time, sys, cookielib, os.path, urlparse, httplib
import xbmcaddon,xbmcplugin,xbmcgui
from jsbeautifier import beautify
import util, sexloading, ivhunter

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
           
sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.javstream'
addon = xbmcaddon.Addon(id=ADDON_ID)

rootDir = addon.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)
resDir = os.path.join(rootDir, 'resources')
imgDir = os.path.join(resDir, 'images')

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")
cookiePath = os.path.join(profileDir, 'cookies.lwp')

if not os.path.exists(profileDir):
    os.makedirs(profileDir)

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

if cj != None:
    if os.path.isfile(xbmc.translatePath(cookiePath)):
        cj.load(xbmc.translatePath(cookiePath))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
else:
    opener = urllib2.build_opener()

urllib2.install_opener(opener)

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
 
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

def getVids(urls) :
    for url in urls:
        if "sexloading" in url:
            param=sexloading.showVideos(url, hdr)
        elif "ivhunter" in url:
            param=ivhunter.showVideos(url, hdr)
        buildVideoMenu(param)
    xbmcplugin.endOfDirectory(int(sysarg))
   
def buildVideoMenu(param):
    loadNext=[]
    for video in param:
        if video[0]=='next':
            loadNext.append(video[1])
        else:
            u=sys.argv[0]+"?url="+video[5]+"&play="+str(4)+"&name="+urllib.quote_plus(video[0].encode("utf-8"))+"&poster="+video[6]
            liz=xbmcgui.ListItem(video[0].encode("utf-8"), iconImage="DefaultVideo.png", thumbnailImage=video[6])
            liz.setInfo( type="Video", infoLabels={ "Title": video[0].encode("utf-8"),"Plot": video[1]} )
            liz.setProperty("Fanart_Image", video[7])
            liz.setProperty("Landscape_Image", video[7])
            liz.setProperty("Poster_Image", video[6])
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    if len(loadNext)>0:
        if len(loadNext)==1:
            util.addDir("Next Page >", loadNext[0], 1, "")
        else:
            util.addDir("Next Page >", "<split>".join(loadNext), 4, "")            
        
def buildMainMenu():
    util.addDir("JAV","JAV", 2, "")
    util.addDir("Gravure", "Gravure", 2, "")
    util.addDir("Latest JAV", "http://sexloading.com/", 1, "")
    util.addDir("Latest Gravure", "http://ivhunter.com", 1, "")
    util.addDir("Search","http://sexloading.com/?s=<split>http://ivhunter.com/?s=", 3, "")
    xbmcplugin.endOfDirectory(int(sysarg))

def buildSubMenu(params):
    if params['url']=='JAV':
        util.addDir("Genres", "http://sexloading.com/faq/", 5, "")
        util.addDir("Censored", "http://sexloading.com/censored/", 1, "")
        util.addDir("Uncensored", "http://sexloading.com/uncensored/", 1, "")
        util.addDir("Most Popular JAV", "http://sexloading.com/", 6, "")
        util.addDir("Latest JAV", "http://sexloading.com/", 1, "")
        util.addDir("Search", "http://sexloading.com/?s=", 3, "")
    elif params['url']=="Gravure":
        util.addDir("Studios", "http://ivhunter.com/note/", 7, "")
        util.addDir("Idols", "http://ivhunter.com/idols-library/", 8, "")
        util.addDir("Most Popular Gravure", "http://ivhunter.com/", 9, "")
        util.addDir("Latest Gravure", "http://ivhunter.com", 1, "")
        util.addDir("Search", "http://ivhunter.com/?s=", 3, "")
    xbmcplugin.endOfDirectory(int(sysarg))
        
def search(urls):
    toSend=[]
    term=util.searchBox()
    for url in urls:
        xbmc.log(url+term, xbmc.LOGERROR)
        toSend.append(url+term)
    getVids(toSend)

def showVideoSources(params): 
    content=util.getURL(params['url'].encode('utf-8'), hdr)
    if content!=False: 
        counter=1
        if "videomega.tv" in content:
            videosource=content
            if re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
                hashref = re.compile("""javascript["']>ref=['"]([^'"]+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
            elif re.search("videomega.tv/iframe.php", videosource, re.DOTALL | re.IGNORECASE):
                hashref = re.compile(r"iframe\.php\?ref=([^&]+)&", re.DOTALL | re.IGNORECASE).findall(videosource)
            else:
                hashkey = re.compile("""hashkey=([^"']+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
                if len(hashkey) > 1:
                    i = 1
                    hashlist = []
                    for x in hashkey:
                        hashlist.append('Part ' + str(i))
                        i += 1
                    vmvideo = dialog.select('Multiple parts found', hashlist)
                    hashkey = hashkey[vmvideo]
                else: hashkey = hashkey[0]
                hashpage = getHtml('http://videomega.tv/validatehash.php?hashkey='+hashkey, params['url'].encode('utf-8'))
                hashref = re.compile('ref="([^"]+)', re.DOTALL | re.IGNORECASE).findall(hashpage)
            url='http://videomega.tv/view.php?ref='+hashref[0]
            videopage = getHtml('http://videomega.tv/view.php?ref='+hashref[0], params['url'].encode('utf-8'))
            vmpacked = re.compile(r"(eval\(.*\))\s+</", re.DOTALL | re.IGNORECASE).findall(videopage)
            vmunpacked = beautify(vmpacked[0])
            videourl = re.compile('src", "([^"]+)', re.DOTALL | re.IGNORECASE).findall(vmunpacked)
            videourl = videourl[0]
            #addDir(name,url,mode,iconimage,plot="",poster="",filename="")
            util.addDir("0"+str(counter)+" | VIDEOMEGA", videourl, 10, params['poster'], "", params['poster'], params['name'].encode("utf-8"))
            counter=counter+1
        if "http://videowood.tv/embed/" in content:
            download=util.extract(content, 'http://videowood.tv/embed/', '"')
            url='http://videowood.tv/embed/'+download
            xbmc.log("VIDEOWOOD: "+url, xbmc.LOGERROR)
            download=util.getURL(url, hdr)
            link=""
            if download!=False:
                xbmc.log("VIDEOWOOD: 1 ", xbmc.LOGERROR)
                errorCounter=0
                while True:
                    xbmc.log("VIDEOWOOD: 2", xbmc.LOGERROR)
                    p=re.compile("}\('\S={(\S*)};'\S*,'(\S*)'.split")
                    
                    packed=re.search(p, download)
                    vars=packed.group(2).split("|")
                    content=packed.group(1)
                    newcontent=""
                    
                    for index, letter in enumerate(content):
                        try:
                            int(letter)
                            newcontent=newcontent+vars[int(letter)]
                        except ValueError:
                            if letter.isalpha():
                                newcontent=newcontent+vars[ord(letter)-87]
                            else:
                                newcontent=newcontent+letter
                    newcontent=newcontent.replace("\\\\/", "/")
                    #logError(newcontent)
                    p=re.compile('"file":"(http[s]*:\/\/\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\/video\/\S*\/\S*.mp4)"')
                    try:
                        link=p.search(newcontent).group(1)
                        break
                    except:
                        errorCounter=errorCounter+1
                        xbmc.log("Cant find URL, try again ["+str(errorCounter)+"]", xbmc.LOGERROR)
                        #logError("Cant find URL, try again ["+str(errorCounter)+"]")
                    if errorCounter==10:
                        xbmc.log("Cant find URL, tried "+str(errorCounter)+" times, failing", xbmc.LOGERROR)
                        break
                        
            #url="http://"+ip+"/video/"+video+"/"+str(folder)+"/"+file+".mp4"
            xbmc.log("VIDEOWOOD: "+str(link), xbmc.LOGERROR)
            util.addDir("0"+str(counter)+" | VIDEOWOOD", link, 10, params['poster'], "", params['poster'], params['name'].encode("utf-8"))
        if "https://openload" in content:
            try:
                url="https://openload.co/embed/"+util.extract(content.encode('utf-8'), "https://openload.co/embed/", "/")+"/"
            except:
                url="https://openload.io/embed/"+util.extract(content.encode('utf-8'), "https://openload.io/embed/", "/")+"/"
            util.addDir("0"+str(counter)+" | OPENLOAD", url, 10, params['poster'], "", params['poster'], params['name'].encode("utf-8"))
        xbmcplugin.endOfDirectory(int(sysarg))
            
def fileInfo():
    return ((((((('&'+base64.b64decode(base64.b64decode('Ykc5bmFXND0=')))+'=')+base64.b64decode(base64.b64decode('WmpjMU1HSXlOalV4TTJZMk5EQXpOQT09')))+'&')+base64.b64decode(base64.b64decode('YTJWNQ==')))+'=')+base64.b64decode(base64.b64decode('YjJGQkxVMWlXbTg9')))
        
def playVideo(params):
    videourl=params['url']
    link=params['url']
    if 'openload' in videourl:
        download=util.extract(videourl, "https://openload.co/embed/", "/")
        openloadurl1 = 'http://openload.co/embed/%s/' % download
        try:
            openloadsrc = getHtml(openloadurl1, '', hdr)
            link = decodeOpenLoad(openloadsrc)
            util.playMedia(params['filename'], params['poster_file'], link, "Video")
        except:
            util.alert('Couldn\'t find playable OpenLoad link')
    else:
        util.playMedia(params['filename'], params['poster_file'], link, "Video")



def decodeOpenLoad(html):

    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html, re.DOTALL | re.IGNORECASE).group(1)
    
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
    aastring = aastring.replace("(ﾟｰﾟ)","4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
    aastring = aastring.replace("(o^_^o)","3")
    aastring = aastring.replace("(ﾟΘﾟ)","1")
    aastring = aastring.replace("(c^_^o)","0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
    aastring = aastring.replace("(3 +3 +0)","6")
    aastring = aastring.replace("(3 - 1 +0)","2")
    aastring = aastring.replace("(1 -0)","1")
    aastring = aastring.replace("(4 -0)","4")

    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+"+ decodestring
    decodestring = decodestring.replace("+","")
    decodestring = decodestring.replace(" ","")
    
    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/","/")
    
    videourl = re.search(r'vr\s?=\s?"([^"]+)', decodestring, re.DOTALL | re.IGNORECASE).group(1)
    return videourl

def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')    
    
    
def getHtml(url, referer, hdr=None):
    referer=urllib2.quote(referer).replace("%3A", ":")
    if not hdr:
        req = Request(url, '', headers)
    else:
        req = Request(url, '', hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
    cj.save(cookiePath)
    response.close()
    return data
        
parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None
    
if mode==1:
    getVids([parameters['url'].encode('utf-8')])
elif mode==2:
    buildSubMenu(parameters)
elif mode==3:
    search(parameters['url'].split('<split>'))
elif mode==4:
    getVids(parameters['url'].split('<split>'))
elif mode==5:
    sexloading.getGenres(parameters['url'], hdr)
elif mode==6:
    buildVideoMenu(sexloading.getPopular(parameters['url'], hdr))
    xbmcplugin.endOfDirectory(int(sysarg))
elif mode==7:
    ivhunter.getStudios(parameters['url'], hdr);
elif mode==8:
    ivhunter.getIdols(parameters['url'], hdr);
elif mode==9:
    buildVideoMenu(ivhunter.getPopular(parameters['url'], hdr))
    xbmcplugin.endOfDirectory(int(sysarg))
elif mode==10:
    playVideo(parameters)
elif 'play' in parameters:
    #playVideo(parameters)
    showVideoSources(parameters)
else:
    buildMainMenu()
