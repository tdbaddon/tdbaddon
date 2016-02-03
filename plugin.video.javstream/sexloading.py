import urllib2, re, urllib, base64, difflib, time, json, base64, HTMLParser, time, sys
import xbmcaddon, xbmcplugin, xbmcgui
import goslate, util

sysarg=str(sys.argv[1]) 

def showVideos(url, hdr):
    content=util.getURL(url, hdr)
    toReturn=[]
    
    if content!=False:
        gs = goslate.Goslate()
        
        allfilms=util.extract(content, '<div class="items">', '<div class="lateral">')
        films=util.extractAll(allfilms, '<div class="item">', '<div class="item">')
        for film in films:
            title=util.replaceHTMLCodes(util.extract(film, '<h2>', '</h2>'))
            
            plot="no plot"
            starring="no starring"
            studio="no studio"
            date="no date"
            url=util.extract(film, '<a href="', '"')
            poster=util.extract(film, '<img src="', '" alt')
            fanart=poster.replace("ps.jpg", "pl.jpg")
            toReturn.append([title, plot, starring, studio, date, url, poster, fanart])
            
        if '<link rel="next" href="' in content:
            toReturn.append(["next", util.extract(content, '<link rel="next" href="', '"')])
        return toReturn
        
def getGenres(url, hdr):
    content=util.getURL(url, hdr)
    
    if content!=False:
        allGenres=util.extract(content, '<ul class="scrolling cat">', '</ul>')
        genres=util.extractAll(allGenres, '<a href', 'a>')
        for genre in genres:
            util.addDir(util.extract(genre, '>', '</'), util.extract(genre, '="', '"'), 1, "")
        xbmcplugin.endOfDirectory(int(sysarg))

def getPopular(url, hdr):
    param={'play':1}
    toReturn=[]
    
    content=util.getURL(url, hdr)
    if content!=False:
        gs = goslate.Goslate()
        
        popularFilms=util.extract(content, '<div id="slider1"', '<div class="peliculas">')
        films=util.extractAll(popularFilms, '<a href', '</a>')
        for film in films:
            title=util.extract(film, 'alt="', 'width=')
            if '[' in title and ']' in title:
                videoCode=util.extract(title.encode("utf-8"), "[", "]")
                videoTitle=gs.translate(util.extract(title.encode('utf-8'), "]", '"'), 'en').title()
                title=util.makeAscii("["+videoCode+"] ")+videoTitle.encode('utf-8')
            else:
                title=gs.translate(title.encode('utf-8').replace("width=", ""), 'en').title()
                
            plot="no plot"
            starring="no starring"
            studio="no studio"
            date="no date"
            url=util.extract(film, '="', '"')
            poster=util.extract(film, '<img src="', '" alt')
            fanart=poster.replace("ps.jpg", "pl.jpg")
            toReturn.append([title, plot, starring, studio, date, url, poster, fanart])
            
        return toReturn  