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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,base64,xmltosrt,os
from BeautifulSoup import BeautifulSoup
h = HTMLParser.HTMLParser()


versao = '1.1.9'
addon_id = 'plugin.video.roggerstream'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.png'
 

###################################################MENUS############################################

	
def  menus():        		
	dialog = xbmcgui.Dialog()
	dialog.ok("ROGGER STREAM", "          Assistam a vários canais IPTV do Brasil e do mundo !!!")
	addDir('ROGGER STREAM','-',3,'http://i.imgur.com/y22MB94.jpg')
	
	
	

def  categorias():
	addDir('CANAIS ABERTOS DO BRASIL','https://copy.com/Nlyj6xxWlRFKdinh?download=1',6,'https://copy.com/JvvK4Iw39ofK1rPF')
	addDir('FUTEBOL AO VIVO','https://copy.com/xUo6eMRYOiVevL2h?download=1',6,'https://copy.com/NPRaZORymdG0FxJ1')
	addDir('TV PAGA BRASIL','-',5,'https://copy.com/VVF8ouCl1Ghkjum8')
	addDir('STREAMS DO YOUTUBE','https://copy.com/8QZD9AQuv4Lchd2M?download=1',10,'http://i.imgur.com/fKCIAxx.jpg')
	addDir('SÉRIES E DESENHOS 24 HORAS','https://copy.com/nEagWXhOC1s7dlyO?download=1',6,'https://copy.com/SzKOJlBKxIfEuHnp')
	addDir('CAÇA E PESCA','https://copy.com/b6uCi8jKTmq24wLy?download=1',6,'https://copy.com/Igk8UorSxdbG4xnE')
	addDir('CANAIS LATINOS','https://copy.com/tapliy8nIaKSLDQq?download=1',6,'https://copy.com/wPVtPygtxuY0P1xl')
	addDir('CANAIS DE PORTUGAL','https://copy.com/unoGFK2bL8ZJ0iHD?download=1',6,'https://copy.com/HwP6Xpia6GNQvWsi')
	addDir('WEBCAMS','https://copy.com/Ywh4MnZQqy2R7M8P?download=1',6,'https://copy.com/dPj2J9AzaExumsnE')
	addDir('CANAIS HD','https://copy.com/VMoOgU8UDvAgfjv0?download=1',6,'https://copy.com/WB68NrrmvjxdH1pJ')
	addDir('MÚSICAS E VIDEOCLIPES','https://copy.com/1cvRyOdMSOCSBH70?download=1',6,'https://copy.com/stpjErgehf9hPtwW')
	addDir('ESPORTES INTERNACIONAIS','https://copy.com/bIIpBHwFbXMXOBBB?download=1',6,'https://copy.com/pUGvpVMDpoY09PcA')
	addDir('RÁDIOS','https://copy.com/znUclLey0qF30gSd?download=1',6,'https://copy.com/fuDnLrM1Am7VNtmT')
	
	


def  categorias_tv_paga_brasil():
	addDir('DOCUMENTÁRIOS','https://copy.com/u3fZuJaCSqXQUNuk?download=1',6,'https://copy.com/9KLabSgitalsvYkg')
	addDir('ESPORTES','https://copy.com/342Ys8apG9i2Ar9J?download=1',6,'https://copy.com/qJfijQo0kIyxhgsc')	
	addDir('FILMES E SÉRIES','https://copy.com/qaC2wr0YHQ3cWgN3?download=1',6,'https://copy.com/9b1kFz9GVNs2CVEg')
	addDir('INFANTIL','https://copy.com/FH28QXuLwrJY9cXS?download=1',6,'https://copy.com/AAJrU1yDtryoKeqt')	
	addDir('NOTÍCIAS','https://copy.com/r19WdvfFW4xP7h7Q?download=1',6,'https://copy.com/9wy1vGvZAAbP2Gus')
	addDir('RELIGIOSOS','https://copy.com/S6Jm2vh2DYJDTEwJ?download=1',6,'https://copy.com/uzJEAXOCWzCUv2up')
	addDir('VARIEDADES','https://copy.com/DUKhtoZqYdjklcOa?download=1',6,'https://copy.com/pqAXz2FWGHwAIAfU')	

	
###############################################################FKav####################################################
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup

def player_youtube(url):
    #mera correção feita por Cleiton Leonel Creton!!!
	xbmcPlayer = xbmc.Player()
        xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +url)
		
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
                  addDir(nome,rtmp,11,img,False)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(500)")
		
##########################################################################################################################	
	
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
	  
	  
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

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

def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

	
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
	
elif mode==3:
	print ""
	categorias()

elif mode==5:
	print ""
	categorias_tv_paga_brasil()	
	
elif mode==6: 
	print ""
	listar_canais(url)

elif mode==10: 
	listar_videostxt(url)
elif mode==11:
	player_youtube(url)	


	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
