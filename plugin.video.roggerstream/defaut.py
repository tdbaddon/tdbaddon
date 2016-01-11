#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,base64
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from BeautifulSoup import BeautifulSoup
h = HTMLParser.HTMLParser()

versao = '3.0.6'
addon_id = 'plugin.video.roggerstream'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.png'
url_base = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')
url_base2 = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vY2FuYWlzLmh0bWw=')
url_base3 = base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')
url_base4 = base64.b64decode('aHR0cHM6Ly9jb3B5LmNvbS9oWjJFbU1YZnROdTRSV3oxP2Rvd25sb2FkPTE=')
url_base5 = base64.b64decode('aHR0cDovL3d3dy5hb3Zpdm9icmFzaWwuY29tL3R2YW1pZ29zMi8=')
url_base6 = base64.b64decode('aHR0cDovL3d3dy5jYXJvbGluZW9saXZlaXJhLmNvbS5ici9zd2YvcGxheWVyLnN3Zg==')
 
###################################################MENUS############################################

def  menus():        		
	dialog = xbmcgui.Dialog()
	dialog.ok("[B]ROGGER STREAM[/B]", "                       Assistam a vários canais de TV no Kodi.")
	addDir('[B]ROGGER STREAM[/B]','-',2,'http://i.imgur.com/y22MB94.jpg')	
	
def  categorias():
	addDir('[B]CANAIS ABERTOS DO BRASIL[/B]','https://copy.com/Nlyj6xxWlRFKdinh?download=1',4,'https://copy.com/JvvK4Iw39ofK1rPF')
	addDir('[B]FUTEBOL AO VIVO[/B]','https://copy.com/xUo6eMRYOiVevL2h?download=1',4,'https://copy.com/NPRaZORymdG0FxJ1')
	addDir('[B]FUTEBOL AO VIVO [COLOR red] (YOUTUBE) [/COLOR][/B]','https://copy.com/8QZD9AQuv4Lchd2M?download=1',5,'http://i.imgur.com/SAEuWPw.jpg')
	addDir('[B]BRTV[/B]','-',7,'http://i.imgur.com/GgDmzDO.jpg')
	addDir('[B]SERIES E DESENHOS [COLOR blue] 24hrs [/COLOR][/B]','-',9,'https://copy.com/KwIFEqNxxBlnSEjL?download=1')	
	addDir('[B]TV PAGA BRASIL[/B]','-',3,'https://copy.com/VVF8ouCl1Ghkjum8')
	addDir('[B]PROGRAMAS DA BAND AO VIVO[/B]','https://copy.com/LUbu11FOacRUEw4O?download=1',4,'http://i.imgur.com/Mxyc9jj.png')
	addDir('[B]WEBCAMS BRASIL[/B]','https://copy.com/nEagWXhOC1s7dlyO?download=1',4,'https://copy.com/dPj2J9AzaExumsnE')
	addDir('[B]CAÇA E PESCA[/B]','https://copy.com/b6uCi8jKTmq24wLy?download=1',4,'https://copy.com/Igk8UorSxdbG4xnE')
	addDir('[B]CANAIS LATINOS[/B]','https://copy.com/tapliy8nIaKSLDQq?download=1',4,'https://copy.com/wPVtPygtxuY0P1xl')
	addDir('[B]CANAIS DE PORTUGAL[/B]','https://copy.com/unoGFK2bL8ZJ0iHD?download=1',4,'https://copy.com/HwP6Xpia6GNQvWsi')
	addDir('[B]WEBCAMS MUNDO[/B]','https://copy.com/Ywh4MnZQqy2R7M8P?download=1',4,'https://copy.com/dPj2J9AzaExumsnE')
	addDir('[B]CANAIS [COLOR blue] HD [/COLOR][/B]','https://copy.com/VMoOgU8UDvAgfjv0?download=1',4,'https://copy.com/WB68NrrmvjxdH1pJ')
	addDir('[B]MÚSICAS E VIDEOCLIPES[/B]','https://copy.com/1cvRyOdMSOCSBH70?download=1',4,'https://copy.com/stpjErgehf9hPtwW')
	addDir('[B]ESPORTES INTERNACIONAIS[/B]','https://copy.com/bIIpBHwFbXMXOBBB?download=1',4,'https://copy.com/pUGvpVMDpoY09PcA')
	addDir('[B]RÁDIOS[/B]','https://copy.com/znUclLey0qF30gSd?download=1',4,'https://copy.com/fuDnLrM1Am7VNtmT')
	addDir('[B]CANAIS ITALIANOS[/B]','https://copy.com/8HphQbrUevxz2OgR?download=1',4,'https://copy.com/61JSYlrWYxnSosTJ')
	
def  categorias_tv_paga_brasil():
	addDir('[B]DOCUMENTÁRIOS[/B]','https://copy.com/u3fZuJaCSqXQUNuk?download=1',4,'https://copy.com/9KLabSgitalsvYkg')
	addDir('[B]ESPORTES[/B]','https://copy.com/342Ys8apG9i2Ar9J?download=1',4,'https://copy.com/qJfijQo0kIyxhgsc')	
	addDir('[B]FILMES E SÉRIES[/B]','https://copy.com/qaC2wr0YHQ3cWgN3?download=1',4,'https://copy.com/9b1kFz9GVNs2CVEg')
	addDir('[B]INFANTIL[/B]','https://copy.com/FH28QXuLwrJY9cXS?download=1',4,'https://copy.com/AAJrU1yDtryoKeqt')	
	addDir('[B]NOTÍCIAS[/B]','https://copy.com/r19WdvfFW4xP7h7Q?download=1',4,'https://copy.com/9wy1vGvZAAbP2Gus')
	addDir('[B]RELIGIOSOS[/B]','https://copy.com/S6Jm2vh2DYJDTEwJ?download=1',4,'https://copy.com/uzJEAXOCWzCUv2up')
	addDir('[B]VARIEDADES[/B]','https://copy.com/DUKhtoZqYdjklcOa?download=1',4,'https://copy.com/pqAXz2FWGHwAIAfU')	

###############################################################FKav####################################################

def listar_canais(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  img = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
                  print 'Img: ' + img
                  rtmp = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
                  print 'Link: ' + rtmp
                  addLink(nome,rtmp,img)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(500)")		
		
def listar_videostxt(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  img = params[1].replace(' http','http')
                  print 'Img: ' + img
                  rtmp = params[2]
                  print 'Link: ' + rtmp
                  addDir(nome,rtmp,6,img,False)
            except:
                pass
		xbmc.executebuiltin("Container.SetViewMode(500)")

def player_youtube(url):
    #mera correção feita por Cleiton Leonel Creton!!!
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +url)

def listar_categorias():
	html = gethtml(url_base4)
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,8,iconimage)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')	
	
def canais_master(name,url,iconimage):
	html = gethtml(url)
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,10,iconimage,False)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
		
def series_e_desenhos_24hrs():
	html = gethtml(base64.b64decode('aHR0cHM6Ly9jb3B5LmNvbS82Y1ZYMmJQR0xzOFBjQ0xqP2Rvd25sb2FkPTE='))
	soup = html.find("div",{"class":"canais"})
	items = soup.findAll("li")
	for item in items:
		titulo = item.a.text
		url = item.a["href"]
		iconimage = item.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,11,iconimage,False)
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def player_master(name,url,iconimage):
	status = xbmcgui.DialogProgress()
	status.create('ROGGER STREAM', 'Resolvendo link...','Por favor aguarde...')
	playlist = xbmc.PlayList(1)
	playlist.clear()
	params = url.split(',')
	status.update(33)
	try:
		ip = params[0]
		playpath = params[1]
		link = 'rtmp://'+ip+'/live?wmsAuthSign='+get_wms() +' playpath='+playpath+' swfUrl='+url_base3+' live=1 pageUrl='+url_base+' token='+gettoken() +' '
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		status.update(66)
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		status.update(100)
		status.close()
	except:	
		xbmcgui.Dialog().ok('ROGGER STREAM', 'Canal temporariamente indisponivel,desculpe o transtorno.')

def	player_series_e_desenhos_24hrs(name,url,iconimage):
	status = xbmcgui.DialogProgress()
	status.create('ROGGER STREAM', 'Resolvendo link...','Por favor aguarde...')
	playlist = xbmc.PlayList(1)
	playlist.clear()
	params = url.split(',')
	status.update(33)
	try:
		ip = params[0]
		playpath = params[1]
		directory = params[2]
		html = abrir_url(url_base5+directory)
		wmsAuthSign = re.compile('tvamigos(.+?)&autostart').findall(html)[0]
		link = 'rtmp://'+ip+wmsAuthSign+' playpath='+playpath+' swfUrl='+url_base6+' live=1 pageUrl='+url_base5+directory
		status.update(66)
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		status.update(100)
		status.close()
	except:	
		xbmcgui.Dialog().ok('ROGGER STREAM', 'Conteudo temporariamente indisponivel,desculpe o transtorno.')	
	
##########################################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup	

def real_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.geturl()
	response.close()
	return link

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

#def addDir(name,url,mode,iconimage,pasta=True,total=1):
	#u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	#ok=True
	#liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setProperty('fanart_image', fanart)
	#ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	#return ok
	
def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	
	
def get_wms():
	req = urllib2.Request(url_base)
	req.add_header('referer', url_base2)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	wms = re.compile(r"AuthSign=(.+?)&auto").findall(link)[0]
	return wms	
	
def gettoken():
	req = urllib2.Request(base64.b64decode('aHR0cHM6Ly9jb3B5LmNvbS9LYjNSdnY4WnZIQmpOYVZsP2Rvd25sb2FkPTE='))
	response = urllib2.urlopen(req)
	token=response.read()
	response.close()
	return token	

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
 
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1:
    print ""
    menus()
	
elif mode==2:
	print ""
	categorias()

elif mode==3:
	print ""
	categorias_tv_paga_brasil()	
	
elif mode==4: 
	print ""
	listar_canais(url)

elif mode==5: 
	listar_videostxt(url)
	
elif mode==6:
	player_youtube(url)

elif mode==7:
    print ""
    listar_categorias()	
	
elif mode==8:
    print ""
    canais_master(name,url,iconimage)
	
elif mode==9:
    print ""
    series_e_desenhos_24hrs()	
	
elif mode==10:
    print ""
    player_master(name,url,iconimage)
	
elif mode==11:
    print ""
    player_series_e_desenhos_24hrs(name,url,iconimage)	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
