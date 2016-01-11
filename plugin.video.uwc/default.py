'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils, hdporn, porntrex, nudeflix, hentaicraving, watchxxxfree, xtheatre, pornhive, beeg, todayporn, nltubes
import elreyx, thepornnation, xvideospanish, pelisxporno, hqporner, videomegaporn, streamxxx, javhdonline, yourfreetube
import xtasie, streampleasure, chaturbate, playporn, pornkino, justporn, hdzog, cat3movie, tubepornclassic, paradisehill

socket.setdefaulttimeout(60)

xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)

progress = utils.progress
dialog = utils.dialog

imgDir = utils.imgDir


def INDEX():
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Scenes[/COLOR]','',2,'','')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Movies[/COLOR]','',3,'','')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Hentai[/COLOR]','http://www.hentaicraving.com/?genre=Uncensored',30,os.path.join(imgDir, 'hc.jpg'),'')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Tubes[/COLOR]','',6,'','')
    utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Webcams & Streams[/COLOR]','',7,'','')
    download_path = addon.getSetting('download_path')
    if download_path != '' and os.path.exists(download_path):
        utils.addDir('[COLOR white]Whitecream[/COLOR] [COLOR yellow]Download Folder[/COLOR]',download_path,4,'','')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def INDEXS():
    utils.addDir('[COLOR yellow]WatchXXXFree[/COLOR]','http://www.watchxxxfree.com/page/1/',10,os.path.join(imgDir, 'wxf.png'),'')
    utils.addDir('[COLOR yellow]PornTrex[/COLOR]','http://www.porntrex.com/videos?o=mr&page=1',50,os.path.join(imgDir, 'pt.png'),'')
    utils.addDir('[COLOR yellow]PornAQ[/COLOR]','http://www.pornaq.com/page/1/',60,os.path.join(imgDir, 'paq.png'),'')
    utils.addDir('[COLOR yellow]Porn00[/COLOR]','http://www.porn00.com/page/1/',64,os.path.join(imgDir, 'p00.png'),'')
    utils.addDir('[COLOR yellow]Beeg[/COLOR]','http://beeg.com/page-1',80,os.path.join(imgDir, 'bg.png'),'')
    utils.addDir('[COLOR yellow]ElReyX[/COLOR]','http://elreyx.com/index1.html',110,os.path.join(imgDir, 'elreyx.png'),'')
    utils.addDir('[COLOR yellow]Thepornnation[/COLOR]','http://thepornnation.com/category/videos/',120,os.path.join(imgDir, 'thepornnation.png'),'')
    utils.addDir('[COLOR yellow]XvideoSpanish[/COLOR]','http://www.xvideospanish.com/',130,os.path.join(imgDir, 'xvideospanish.png'),'')
    utils.addDir('[COLOR yellow]HQPorner[/COLOR]','http://hqporner.com/hdporn/1',150,os.path.join(imgDir, 'hqporner.png'),'')
    utils.addDir('[COLOR yellow]VideoMegaPorn[/COLOR]','http://www.videomegaporn.com/index.html',160,os.path.join(imgDir, 'videomegaporn.png'),'')
    utils.addDir('[COLOR yellow]StreamXXX[/COLOR]','http://streamxxx.tv/category/clips/',170,os.path.join(imgDir, 'streamxxx.png'),'')
    utils.addDir('[COLOR yellow]JustPorn[/COLOR]','http://justporn.to/category/scenes/',240,os.path.join(imgDir, 'justporn.png'),'')
    utils.addDir('[COLOR yellow]JavHDonline[/COLOR]','http://javhdonline.com/watch/category/jav-uncensored/',180,os.path.join(imgDir, 'javhdonline.png'),'')
    utils.addDir('[COLOR yellow]YourFreeTube[/COLOR]','http://www.yourfreetube.net/newvideos.html',190,'','')
    utils.addDir('[COLOR yellow]Xtasie[/COLOR]','http://xtasie.com/porn-video-list/page/1/',200,os.path.join(imgDir, 'xtasie.png'),'')
    utils.addDir('[COLOR yellow]StreamPleasure[/COLOR]','http://streampleasure.com/page/1/?filtre=date&cat=0',210,os.path.join(imgDir, 'streampleasure.png'),'')    
    utils.addDir('[COLOR yellow]Playporn[/COLOR]','http://playporn.to/category/xxx-clips-scenes-stream/',230,os.path.join(imgDir, 'playporn.png'),'')
    utils.addDir('[COLOR yellow]HD Zog[/COLOR]','http://www.hdzog.com/new/',340,os.path.join(imgDir, 'hdzog.png'),'')    
    utils.addDir('[COLOR yellow]One list, to watch them all[/COLOR]','',5,'',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

def INDEXM():    
    utils.addDir('[COLOR yellow]Xtheatre[/COLOR]','http://xtheatre.net/page/1/',20,os.path.join(imgDir, 'xt.png'),'')
    utils.addDir('[COLOR yellow]Nudeflix[/COLOR]','http://www.nudeflix.com/browse?order=released&page=1',40,os.path.join(imgDir, 'nf.png'),'')
    utils.addDir('[COLOR yellow]PornHive[/COLOR]','http://www.pornhive.tv/en/movies/all',70,os.path.join(imgDir, 'ph.png'),'')
    utils.addDir('[COLOR yellow]JustPorn[/COLOR]','http://justporn.to/category/dvdrips-full-movies/',245,os.path.join(imgDir, 'justporn.png'),'')
    utils.addDir('[COLOR yellow]ElReyX[/COLOR]','http://elreyx.com/index1.html',116,os.path.join(imgDir, 'elreyx.png'),'')
    utils.addDir('[COLOR yellow]Thepornnation[/COLOR]','http://thepornnation.com//category/movies/',125,os.path.join(imgDir, 'thepornnation.png'),'')
    utils.addDir('[COLOR yellow]PelisxPorno[/COLOR]','http://www.pelisxporno.com/',140,os.path.join(imgDir, 'pelisxporno.png'),'')
    utils.addDir('[COLOR yellow]StreamXXX[/COLOR]','http://streamxxx.tv/category/movies/',175,os.path.join(imgDir, 'streamxxx.png'),'')
    utils.addDir('[COLOR yellow]Playporn[/COLOR]','http://playporn.to/category/xxx-movie-stream/',231,os.path.join(imgDir, 'playporn.png'),'')
    utils.addDir('[COLOR yellow]Pornkino[/COLOR]','http://pornkino.to/',330,os.path.join(imgDir, 'pornkino.png'),'')
    utils.addDir('[COLOR yellow]Cat3Movie[/COLOR]','http://cat3movie.us',350,os.path.join(imgDir, 'cat3movie.png'),'')
    utils.addDir('[COLOR yellow]ParadiseHill[/COLOR]','http://www.paradisehill.tv/en/',250,os.path.join(imgDir, 'paradisehill.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def INDEXT():    
    utils.addDir('[COLOR yellow]TodayPorn[/COLOR]','http://www.todayporn.com/page1.html',90,os.path.join(imgDir, 'tp.png'),'')
    utils.addDir('[COLOR yellow]Poldertube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.poldertube.nl/pornofilms/nieuw',100,os.path.join(imgDir, 'poldertube.png'),0)
    utils.addDir('[COLOR yellow]Milf.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.milf.nl/videos/nieuw',100,os.path.join(imgDir, 'milfnl.png'),1)
    utils.addDir('[COLOR yellow]Sextube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.sextube.nl/videos/nieuw',100,os.path.join(imgDir, 'sextube.png'),2)
    utils.addDir('[COLOR yellow]TubePornClassic[/COLOR]','http://www.tubepornclassic.com/latest-updates/',360,os.path.join(imgDir, 'tubepornclassic.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def INDEXW():
    utils.addDir('[COLOR yellow]Chaturbate[/COLOR] - webcams','https://chaturbate.com/?page=1',220,os.path.join(imgDir, 'chaturbate.png'),'')
    utils.addDir('[COLOR yellow]Streams[/COLOR] - beta','',8,'','')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def STREAMS():
    streamurl = 'https://github.com/whitecream01/WhiteCream-V0.0.1/raw/master/plugin.video.uwc/streamlist.m3u'
    streamlist = utils.getHtml(streamurl, '')
    match = re.compile('#.+,(.+?)\n(.+?)\n').findall(streamlist)
    for name, url in match:
        utils.addDownLink(name, url, 9, '', '', True)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def ONELIST(page):
    print page
    watchxxxfree.WXFList('http://www.watchxxxfree.com/page/1/',page, True)
    hdporn.PAQList('http://www.pornaq.com/page/1/',page, True)
    hdporn.PAQList('http://www.porn00.org/page/1/',page, True)
    porntrex.PTList('http://www.porntrex.com/videos?o=mr&page=1',page, True)
    streampleasure.SPList('http://streampleasure.com/page/1/?filtre=date&cat=0',page, True)
    npage = page + 1
    utils.addDir('[COLOR yellow]Next page ('+ str(npage) +')[/COLOR]','',5,'',npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)
    

def getParams():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = getParams()
url = None
name = None
mode = None
img = None
page = 1
download = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    page = int(params["page"])
except:
    pass
try:
    img = urllib.unquote_plus(params["img"])
except:
    pass
try:
    download = int(params["download"])
except:
    pass

if mode is None: INDEX()
elif mode == 2: INDEXS()
elif mode == 3: INDEXM()
elif mode == 4: xbmc.executebuiltin('ActivateWindow(Videos, '+url+')')
elif mode == 5: ONELIST(page)
elif mode == 6: INDEXT()
elif mode == 7: INDEXW()
elif mode == 8: STREAMS()
elif mode == 9: utils.PlayStream(name, url)
elif mode == 10: watchxxxfree.WXFMain()
elif mode == 11: watchxxxfree.WXFList(url, page)
elif mode == 12: watchxxxfree.WXFCat(url)
elif mode == 13: watchxxxfree.WXFVideo(url, name, download)
elif mode == 14: watchxxxfree.WXFSearch(url) 
elif mode == 15: watchxxxfree.WXFTPS(url)
elif mode == 16:
    addon.openSettings()
    watchxxxfree.WXFMain()
elif mode == 20: xtheatre.XTMain()
elif mode == 21: xtheatre.XTList(url, page)
elif mode == 22: xtheatre.XTCat(url)
elif mode == 23: xtheatre.XTVideo(url, name, download)
elif mode == 24: xtheatre.XTSearch(url)
elif mode == 25:
    addon.openSettings()
    xtheatre.XTMain()
elif mode == 30: hentaicraving.HCList(url)
elif mode == 31: hentaicraving.HCEpisodes(url, name, img)
elif mode == 32: hentaicraving.HCPlayvid(url, name, download)
elif mode == 33: hentaicraving.HCA2Z(url)
elif mode == 40: nudeflix.NFMain()
elif mode == 41: nudeflix.NFList(url, page)
elif mode == 42: nudeflix.NFScenes(url)
elif mode == 43: nudeflix.NFPlayvid(url, name, download)
elif mode == 44: nudeflix.NFCat(url)
elif mode == 50: porntrex.PTMain()
elif mode == 51: porntrex.PTList(url, page)
elif mode == 52: porntrex.PTPlayvid(url, name, download)
elif mode == 53: porntrex.PTCat(url)
elif mode == 54: porntrex.PTSearch(url)
elif mode == 60: hdporn.PAQMain()
elif mode == 61: hdporn.PAQList(url, page)
elif mode == 62: hdporn.PPlayvid(url, name, 1, download)
elif mode == 63: hdporn.PCat(url)
elif mode == 64: hdporn.P00Main()
elif mode == 68: hdporn.PSearch(url)
elif mode == 70: pornhive.PHMain()
elif mode == 71: pornhive.PHList(url)
elif mode == 72: pornhive.PHVideo(url, name, download)
elif mode == 73: pornhive.PHCat(url)
elif mode == 74: pornhive.PHSearch(url)
elif mode == 80: beeg.BGMain()
elif mode == 81: beeg.BGList(url)
elif mode == 82: beeg.BGPlayvid(url, name, download)
elif mode == 83: beeg.BGCat(url)
elif mode == 84: beeg.BGSearch(url)
elif mode == 90: todayporn.TPMain()
elif mode == 91: todayporn.TPList(url,page)
elif mode == 92: todayporn.TPPlayvid(url, name, download)
elif mode == 93: todayporn.TPCat(url)
elif mode == 94: todayporn.TPSearch(url)
elif mode == 95: todayporn.TPPornstars(url, page)
elif mode == 100: nltubes.NLTUBES(url, page)
elif mode == 101: nltubes.NLVIDEOLIST(url, page)
elif mode == 102: nltubes.NLPLAYVID(url, name, download)
elif mode == 103: nltubes.NLCAT(url, page)
elif mode == 104: nltubes.NLSEARCH(url, page)
elif mode == 110: elreyx.EXMain()
elif mode == 111: elreyx.EXList(url)
elif mode == 112: elreyx.EXPlayvid(url, name, download)
elif mode == 113: elreyx.EXCat(url)
elif mode == 114: elreyx.EXSearch(url)
elif mode == 115: elreyx.EXPornstars(url)
elif mode == 116: elreyx.EXMovies(url)
elif mode == 117: elreyx.EXMoviesList(url)
elif mode == 120: thepornnation.TPNMain(url)
elif mode == 121: thepornnation.TPNList(url)
elif mode == 122: thepornnation.TPNPlayvid(url, name, download)
elif mode == 123: thepornnation.TPNCat(url, 1)
elif mode == 124: thepornnation.TPNSearch(url)
elif mode == 125: thepornnation.TPNMainMovies(url)
elif mode == 126: thepornnation.TPNCat(url, 0)
elif mode == 127: thepornnation.TPNSearchList(url)
elif mode == 130: xvideospanish.Main()
elif mode == 131: xvideospanish.List(url)
elif mode == 132: xvideospanish.Playvid(url, name, download)
elif mode == 133: xvideospanish.Categories(url)
elif mode == 134: xvideospanish.Search(url)
elif mode == 140: pelisxporno.Main()
elif mode == 141: pelisxporno.List(url)
elif mode == 142: pelisxporno.Playvid(url, name, download)
elif mode == 143: pelisxporno.Categories(url)
elif mode == 144: pelisxporno.Search(url)
elif mode == 150: hqporner.HQMAIN()
elif mode == 151: hqporner.HQLIST(url)
elif mode == 152: hqporner.HQPLAY(url, name, download)
elif mode == 153: hqporner.HQCAT(url)
elif mode == 154: hqporner.HQSEARCH(url)
elif mode == 160: videomegaporn.Main()
elif mode == 161: videomegaporn.List(url)
elif mode == 162: videomegaporn.Playvid(url, name, download)
elif mode == 163: videomegaporn.Categories(url)
elif mode == 164: videomegaporn.Search(url)
elif mode == 170: streamxxx.Main()
elif mode == 171: streamxxx.List(url)
elif mode == 172: streamxxx.Playvid(url, name, download)
elif mode == 173: streamxxx.Tags(url)
elif mode == 174: streamxxx.Search(url)
elif mode == 175: streamxxx.MainMovies()
elif mode == 176: streamxxx.MainInternationalMovies()
elif mode == 177: streamxxx.Categories(url)
elif mode == 180: javhdonline.Main()
elif mode == 181: javhdonline.List(url)
elif mode == 182: javhdonline.Playvid(url, name, download)
elif mode == 183: javhdonline.Tags(url)
elif mode == 184: javhdonline.Search(url)
elif mode == 190: yourfreetube.YFTMain()
elif mode == 191: yourfreetube.YFTList(url)
elif mode == 192: yourfreetube.YFTPlayvid(url, name, download)
elif mode == 193: yourfreetube.YFTCat(url)
elif mode == 194: yourfreetube.YFTSearch(url)
elif mode == 200: xtasie.XTCMain()
elif mode == 201: xtasie.XTCList(url)
elif mode == 202: xtasie.XTCPlayvid(url, name, download)
elif mode == 203: xtasie.XTCCat(url)
elif mode == 204: xtasie.XTCSearch(url)
elif mode == 210: streampleasure.SPMain()
elif mode == 211: streampleasure.SPList(url,page)
elif mode == 212: streampleasure.SPPlayvid(url, name, download)
elif mode == 213: streampleasure.SPSearch(url)
elif mode == 220: chaturbate.Main()
elif mode == 221: chaturbate.List(url)
elif mode == 222: chaturbate.Playvid(url, name)
elif mode == 230: playporn.Main()
elif mode == 231: playporn.MainMovies()
elif mode == 232: playporn.List(url)
elif mode == 233: playporn.Playvid(url, name, download)
elif mode == 234: playporn.Search(url)
elif mode == 235: playporn.Categories(url, 0)
elif mode == 236: playporn.Categories(url, 1)
elif mode == 240: justporn.Main()
elif mode == 241: justporn.List(url)
elif mode == 242: justporn.Playvid(url, name, download)
elif mode == 244: justporn.Search(url)
elif mode == 245: justporn.MainMovies()
elif mode == 250: paradisehill.Main()
elif mode == 251: paradisehill.List(url, page)
elif mode == 252: paradisehill.Playvid(url, name, download)
elif mode == 253: paradisehill.Cat(url)
elif mode == 254: paradisehill.Search(url)
elif mode == 330: pornkino.Main()
elif mode == 331: pornkino.List(url)
elif mode == 332: pornkino.Playvid(url, name, download)
elif mode == 333: pornkino.Search(url)
elif mode == 334: pornkino.Categories(url)
elif mode == 340: hdzog.Main()
elif mode == 341: hdzog.List(url)
elif mode == 342: hdzog.Playvid(url, name, download)
elif mode == 343: hdzog.Search(url)
elif mode == 344: hdzog.Categories(url)
elif mode == 345: hdzog.Channels(url)
elif mode == 346: hdzog.Models(url)
elif mode == 350: cat3movie.Main()
elif mode == 351: cat3movie.List(url)
elif mode == 352: cat3movie.Playvid(url, name, download)
elif mode == 353: cat3movie.Search(url)
elif mode == 354: cat3movie.Categories(url)
elif mode == 360: tubepornclassic.Main()
elif mode == 361: tubepornclassic.List(url)
elif mode == 362: tubepornclassic.Playvid(url, name, download)
elif mode == 363: tubepornclassic.Cat(url)
elif mode == 364: tubepornclassic.Search(url)

xbmcplugin.endOfDirectory(utils.addon_handle)
