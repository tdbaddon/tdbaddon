import util, urllib2, re, urllib, base64, difflib, time, json, base64, HTMLParser
import xbmcaddon,xbmcplugin,xbmcgui

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
ADDON_ID='plugin.video.likuoo'

sysarg=str(sys.argv[1]) 

# This function implements a horrible hack related to python 2.4's terrible unicode handling.
def makeAscii(data):
    #log(repr(data), 5)
    #if sys.hexversion >= 0x02050000:
    #        return data

    try:
        return data.encode('ascii', "ignore")
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.encode("ascii", "ignore")
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i

        #log(repr(s), 5)
        return s

def replaceHTMLCodes(txt):
    #log(repr(txt), 5)

    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    #log(repr(txt), 5)
    return txt

# This function handles stupid utf handling in python.
def makeUTF8(data):
    #log(repr(data), 5)
    return data
    try:
        return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.decode("utf8", "xmlcharrefreplace") 
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i
        #log(repr(s), 5)
        return s
        
def getVids(params) :
    param={'play':1}
    
    content=util.getURL(params['url'], hdr)
    if content!=False:
        films=util.extractAll(content, '<div class="item">', '<div class="item">')
        for film in films:
            param['title']=makeAscii(util.extract(film, 'title="', '"'))
            param['url']=util.extract(film, '<a href="', '" title="')
            param['poster']=util.extract(film, 'src="', '" title="')
            param['fanart']=param['poster']
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&play="+str(4)+"&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": ""} )
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        next=util.extract(content, '<span class="current">', '</span>')
        #xbmc.log(">>>>>"+str(next), xbmc.LOGERROR)
        if next!=None:
            next=int(next)+1
            #xbmc.log('http://www.likuoo.com/new/'+str(next), xbmc.LOGERROR)
            if 'http://www.likuoo.com/new/'+str(next) in content:
                util.addDir("Next >", 'http://www.likuoo.com/new/'+str(next), 2, "","")
        xbmcplugin.endOfDirectory(int(sysarg))

def buildMainMenu():
    util.addDir("Latest","http://www.likuoo.com/", 2, "","")
    util.addDir("Categories","http://www.likuoo.com/", 3, "","")
    util.addDir("Search","Search", 4, "","")
    xbmcplugin.endOfDirectory(int(sysarg))
    
def search():
    term=util.searchBox()
    params={'search':1}
    params['url']="http://www.likuoo.com/search/?s="+term
    getVids(params)

def getCategories(url):
    param={'category':1}
    content=util.getURL(url, hdr)
    if content!=False:
        cats=util.extractAll(content, '<div class="item">', '<div class="item">')
        for film in cats:
            param['title']=makeAscii(util.extract(film, 'title="', '"'))
            param['url']='http://www.likuoo.com'+util.extract(film, '<a href="', '" title="')
            param['poster']=util.extract(film, 'src="', '" title="')
            param['fanart']=param['poster']
            xbmc.log("Play URL:"+param['url'], xbmc.LOGERROR)
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&mode=2&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": ""} )
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmcplugin.endOfDirectory(int(sysarg))
                
def playVideo(params):
    content=util.getURL(params['url'], hdr)
    xbmc.log("0", xbmc.LOGERROR)
    if content!=False:
        video=util.extract(content, '<div id="post_in">', '</div>')
        url=util.extract(video, '<iframe src="', '"')
        xbmc.log("0.5 URL > "+url, xbmc.LOGERROR)
        content2=util.getURL(url, hdr)
        xbmc.log("1", xbmc.LOGERROR)
        if content2!=False:
            if '<iframe src="' in content2 :
                url=util.extract(content2, '<iframe src="', '"')
                xbmc.log("2", xbmc.LOGERROR)
                content3=util.getURL(url, hdr)
                if content3!=False:
                    if '<iframe src="' in content3 :
                        url=util.extract(content3, '<iframe src="', '"')
                        xbmc.log("3", xbmc.LOGERROR)
                        content4=util.getURL(url, hdr)
                        if content4!=False:
                            xbmc.log("4", xbmc.LOGERROR)
                            url=util.extract(content4, "script.setAttribute('src', '", "'")
                            content5=util.getURL(url.decode('string_escape'), hdr)
                            if content5!=False:
                                mp4_240=util.extract(content5, '"mp4_240":"', '"')
                                mp4_360=util.extract(content5, '"mp4_360":"', '"')
                                mp4_720=util.extract(content5, '"mp4_720":"', '"')
                                mp4_1080=util.extract(content5, '"mp4_1080":"', '"')
                                
                                if mp4_1080!=None:
                                    url=mp4_1080.replace("\\", "")
                                elif mp4_720!=None:
                                    url=mp4_720.replace("\\", "")
                                elif mp4_360!=None:
                                    url=mp4_360.replace("\\", "")
                                elif mp4_240!=None:
                                    url=mp4_240.replace("\\", "")
                            xbmc.log("FINAL: "+makeAscii(url), xbmc.LOGERROR)
            else:
                xbmc.log("1.5", xbmc.LOGERROR)
                if '<source src="' in content2:
                    url=util.extract(content2, '<source src="', '"')
                elif "file: '" in content2:
                    url=util.extract(content2, "file: '", "'")
        else:
            url=util.extract(content2, '<source src="', '"')
            
        util.playMedia(params['name'], params['poster'], url, "Video")

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None

if mode==2:
    getVids(parameters)
elif mode==3:
    getCategories('http://www.likuoo.com/all-channels/')
elif mode==4:
    # search code goes here!!
    search()
elif 'play' in parameters:
    playVideo(parameters)
else :
    buildMainMenu()
