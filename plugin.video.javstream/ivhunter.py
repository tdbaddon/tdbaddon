import urllib2, re, urllib, base64, difflib, time, json, base64, HTMLParser, time, sys
import xbmcaddon, xbmcplugin, xbmcgui
import util, goslate

sysarg=str(sys.argv[1]) 

def showVideos(url, hdr):
    content=util.getURL(url, hdr)
    toReturn=[]
    
    if content!=False:
        gs = goslate.Goslate()
        
        allfilms=util.extract(content, '<div class="nag cf">', '<!-- end .loop-content -->')
        if allfilms!=None:
            films=util.extractAll(allfilms, '<div id="post-', '<!-- end #post-')
            for film in films:
                details=util.extract(film, '<div class="thumb">', '</div>')
                title=util.replaceHTMLCodes(util.extract(details, 'title="', '"'))
                
                
                plot="no plot"
                starring="no starring"
                studio="no studio"
                date="no date"
                url=util.extract(film, 'href="', '"')
                poster=util.extract(film, '<img src="', '" alt').replace("pl.jpg", "ps.jpg")
                fanart=poster.replace("ps.jpg", "pl.jpg")
                toReturn.append([title, plot, starring, studio, date, url, poster, fanart])
        
            checkNext=util.extract(content, '<a class="nextpostslink" rel="next" href="', '"')
            if checkNext!=None:
                toReturn.append(['next', checkNext])
    return toReturn
    
def getStudios(url, hdr):
    content=util.getURL(url, hdr)
    
    if content!=False:
        studios=util.extractAll(content, '<a href="http://ivhunter.com/studios', 'a>')
        for studio in studios:
            if util.extract(studio, '">', '</')!="Studios":
                util.addDir(util.extract(studio, '">', '</'), "http://ivhunter.com/studios/"+util.extract(studio, '/', '/'), 1, "")
        xbmcplugin.endOfDirectory(int(sysarg))

def getIdols(url, hdr):
    content=util.getURL(url, hdr)
    
    if content!=False:
        alphabet=util.extractAll(content, '<ul class="links">', '</ul>')
        for letter in alphabet:
            idols=util.extractAll(letter, '<li>', '</li>')
            for idol in idols:
                if util.makeAscii(util.extract(idol, 'title="', '"'))!="":
                    util.addDir(util.makeAscii(util.extract(idol, 'title="', '"')), util.extract(idol, 'href="', '"').encode('utf-8'), 1, "")
        xbmcplugin.endOfDirectory(int(sysarg))
        
def getPopular(url, hdr):
    toReturn=[]
    
    content=util.getURL(url, hdr)
    if content!=False:
        gs = goslate.Goslate()
        
        popularFilms=util.extract(content, '<div id="dp-widget-posts-2" class="widget widget-posts">', '<!--end #sidebar-->')
        films=util.extractAll(popularFilms, '<div class="thumb">', '</div>')
        for film in films:
            title=util.extract(film, 'title="', 'href')
            if '[' in title and ']' in title:
                videoCode=util.extract(title.encode("utf-8"), "[", "]")
                videoTitle=gs.translate(util.extract(title.encode('utf-8'), "]", '"'), 'en').title()
                title=util.makeAscii("["+videoCode+"] ")+videoTitle.encode('utf-8')
            else:
                title=gs.translate(title.encode('utf-8').replace('"', ""), 'en').title()
                
            plot="no plot"
            starring="no starring"
            studio="no studio"
            date="no date"
            url=util.extract(film, 'href="', '"')
            poster=util.extract(film, '<img src="', '" alt')
            fanart=poster.replace("ps.jpg", "pl.jpg")
            toReturn.append([title, plot, starring, studio, date, url, poster, fanart])
            
        return toReturn  