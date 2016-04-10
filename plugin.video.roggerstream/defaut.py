#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################################################################################################
#                                         Atualizado em 05/04/2016                                         #
#                   Desenvolvedores:Rogger Henrique,Cleiton Leonel Creton e Filipe Carvalho                #
############################################################################################################

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

############################################################################################################
#                                     BIBLIOTECAS A IMPORTAR DEFINIÇÕES                                    #
############################################################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,base64
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from BeautifulSoup import BeautifulSoup
h = HTMLParser.HTMLParser()
versao = '4.0.0'
addon_id = 'plugin.video.roggerstream'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.png'
fav = addonfolder + '/fav'
addonname = 'Rogger stream'
line1 = "Lista de Favoritos limpa com sucesso"
line2 = "Favorito adicionado com sucesso"
line3 = "Favorito removido com sucesso"
icon = addonfolder + '/icon.png'
time = 2
url_base = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')
url_base2 = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vY2FuYWlzLmh0bWw=')
url_base3 = base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')
url_base4 = base64.b64decode('aHR0cDovL3Bhc3RlYmluLmNvbS9yYXcvNmJ2Njh5N20=')
url_base5 = base64.b64decode('aHR0cDovL3d3dy5hb3Zpdm9icmFzaWwuY29tL3R2YW1pZ29zMi8=')
url_base6 = base64.b64decode('aHR0cDovL3d3dy5jYXJvbGluZW9saXZlaXJhLmNvbS5ici9zd2YvcGxheWVyLnN3Zg==')
url_base7 = 'http://pastebin.com/raw/'
txt_regex = '(.*?), (.*?), (.*?),\s*'
master_regex = '<li><a href="(.*?)" title="(.*?)"><img src="(.*?)">'
############################################################################################################
#                                                 CATEGORIAS                                               #
############################################################################################################	
	
def  categorias():
	addDir('[B]CANAIS ABERTOS DO BRASIL[/B]','http://pastebin.com/raw/bXZL7m2L',4,'http://s17.postimg.org/fg7t8j31n/century.png')
	addDir('[B]FUTEBOL AO VIVO[/B]','http://pastebin.com/raw/ZDDMswjx',4,'http://s20.postimg.org/9nskrfnix/futebol_ao_vivo.png')
	addDir('[B]FUTEBOL AO VIVO [COLOR red] (YOUTUBE) [/COLOR][/B]','http://pastebin.com/raw/Q8gvAVw1',5,'http://s9.postimg.org/w9zx1n4wv/you.png')
	addDir('[B]BRTV[/B]','-',7,'http://s20.postimg.org/hj3468x5l/brtv.png')
	addDir('[B]SERIES E DESENHOS [COLOR blue] 24hrs [/COLOR][/B]','-',9,'http://s20.postimg.org/ha5jgbkd5/S_ries_e_desenhos.png')	
	addDir('[B]TV PAGA BRASIL[/B]','-',3,'http://i.imgur.com/flYnDUu.png')
	addDir('[B]PROGRAMAS DA BAND AO VIVO[/B]','http://pastebin.com/raw/kXBnNSbN',4,'http://s21.postimg.org/cxcndd31v/android_marshmallow.png')
	addDir('[B]WEBCAMS BRASIL[/B]','http://pastebin.com/raw/Vu4LWBuf',4,'http://s20.postimg.org/scamereft/webcam_02_1.png')
	addDir('[B]CANAIS LATINOS[/B]','http://pastebin.com/raw/uHGmiy37',4,'http://i.imgur.com/ODnHvr9.png')
	addDir('[B]CANAIS DE PORTUGAL[/B]','http://pastebin.com/raw/3HgXnWcw',4,'http://i.imgur.com/zrN35DO.png')
	addDir('[B]WEBCAMS MUNDO[/B]','http://pastebin.com/raw/GHkJUUA2',4,'http://s20.postimg.org/scamereft/webcam_02_1.png')
	addDir('[B]CANAIS [COLOR blue] HD [/COLOR][/B]','http://pastebin.com/raw/v7eFd3LJ',4,'http://i.imgur.com/A2ZUwkE.png')
	addDir('[B]MÚSICAS E VIDEOCLIPES[/B]','http://pastebin.com/raw/CkTi4k2A',4,'http://i.imgur.com/mMaRel5.png')
	addDir('[B]ESPORTES INTERNACIONAIS[/B]','http://pastebin.com/raw/B0V8Y108',4,'http://i.imgur.com/Wu97a7U.png')
	addDir('[B]RÁDIOS[/B]','http://pastebin.com/raw/YprHSXUx',4,'http://i.imgur.com/EQFgXqj.png')
	addDir('[B]CANAIS ITALIANOS[/B]','http://pastebin.com/raw/Ep6YLc6Z',4,'http://i.imgur.com/2E2QDf1.png')
	addDir('[B]CANAIS DA FRANÇA[/B]','http://pastebin.com/raw/JQy0QZpu',4,'http://i.imgur.com/5oK0sUi.png')
	addDir("[B]SEARCH[/B]",'-',16,'http://s29.postimg.org/xg55o044z/busca.png')
	addDir("[B]FAVORITOS[/B]",'-',12,'http://s24.postimg.org/t22vlu68h/favorites.png')	
	xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	
def  categorias_tv_paga_brasil():
	addDir('[B]DOCUMENTÁRIOS[/B]','http://pastebin.com/raw/SqkdckbS',4,'http://i.imgur.com/BxnySNs.png')
	addDir('[B]ESPORTES[/B]','http://pastebin.com/raw/YxdiprDU',4,'http://i.imgur.com/Wu97a7U.png')	
	addDir('[B]FILMES E SÉRIES[/B]','http://pastebin.com/raw/jc3mzrAi',4,'http://i.imgur.com/rbqNruK.png')
	addDir('[B]INFANTIL[/B]','http://pastebin.com/raw/1bixerQr',4,'http://i.imgur.com/fEsWrJW.png')	
	addDir('[B]NOTÍCIAS[/B]','http://pastebin.com/raw/VetY05Gn',4,'http://i.imgur.com/0o9xWHw.png')
	addDir('[B]RELIGIOSOS[/B]','http://pastebin.com/raw/1KRPeQbK',4,'http://i.imgur.com/LS2KYQF.png')
	addDir('[B]VARIEDADES[/B]','http://pastebin.com/raw.php?i=DY2kby4s',4,'http://i.imgur.com/F7QVSL5.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'episodies')

############################################################################################################
#                                                 CÓDIGO                                                   #
############################################################################################################

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
                  addDirfav(nome,rtmp,14,img,False)
            except:
                pass
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')	
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
                  addDirfav(nome,rtmp,6,img,False)
            except:
                pass
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')	
		xbmc.executebuiltin("Container.SetViewMode(500)")

def player_youtube(url):
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
		addDirfav("[B]"+titulo.encode('utf-8')+"[/B]",url,10,iconimage,False)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
		
def series_e_desenhos_24hrs():
	html = gethtml(base64.b64decode('aHR0cDovL3Bhc3RlYmluLmNvbS9yYXcvYzBHZmI5aGo='))
	soup = html.find("div",{"class":"canais"})
	items = soup.findAll("li")
	for item in items:
		titulo = item.a.text
		url = item.a["href"]
		iconimage = item.img["src"]
		addDirfav("[B]"+titulo.encode('utf-8')+"[/B]",url,11,iconimage,False)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def player(name,url,iconimage):
	pl=xbmc.PlayList(1)
	pl.clear()
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	xbmc.PlayList(1).add(url, listitem)
	xbmc.Player().play(pl)	
	
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
		link = 'rtmp://'+ip+'/live?wmsAuthSign='+get_wms() +' playpath='+playpath+' swfUrl='+url_base3+' live=1 pageUrl='+url_base+' token='+get_token() +''
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
	
	
############################################################################################################
#                                                   FUNÇÕES                                                #
############################################################################################################

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
	
def addDirfav(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))	
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addDirfavs(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR orange]Remover um Favorito do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))	
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
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

def get_token():
    req = urllib2.Request(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvdG9rZW4ucGhw'))
    print req
    response = urllib2.urlopen(req)
    print response
    token = response.read()
    print token
    response.close()
    return token

def adicionar_favoritos(url):
	arquivo = open(fav, 'r')
	texto = arquivo.readlines()
	texto.append(name+'#'+url+'#'+iconimage+'#'+'\n') 
	arquivo = open(fav, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line2, time, icon))

def favoritos():
	arquivo = open(fav, 'r').readlines()
	for line in arquivo:
		params = line.split('#')
		try:
			nome = params[0]
			rtmp = params[1]
			img = params[2]			
			addDirfavs(nome,rtmp,30,img,False)
			
		except:
			pass
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')	
		xbmc.executebuiltin("Container.SetViewMode(500)")			
	
def check(name,url,iconimage):
	xbmc.log("url = "+ url)
	if ',' in str(url):
		if 'ctv' in url:
			return player_series_e_desenhos_24hrs(name,url,iconimage)
		else:
			return player_master(name,url,iconimage)
	if 'http' in url:
		return player(name,url,iconimage)
	if 'rtmp' in url:
		return player(name,url,iconimage)
	else:
		player_youtube(url)
		
def remover_favorito():
	arquivo = open(fav, 'r')
	ref = url
	linhas = arquivo.readlines()
	arquivo.close()
	arquivo = open(fav, 'w')
	for linha in linhas:
		if ref in linha:
			linhas.remove(linha)
			arquivo.writelines(linhas)
			arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line3, time, icon))	
	xbmc.executebuiltin("Container.Refresh")
	sys.exit(0)

def search():
	try:
		keyb = xbmc.Keyboard('', 'Pesquisar')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ').capitalize()
		if len(url_base7+'c0Gfb9hj') > 0:		
			content = abrir_url(url_base7+'c0Gfb9hj')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,11,img,False)
		if len(url_base7+'1JazBri4') > 0:		
			content = abrir_url(url_base7+'1JazBri4')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,10,img,False)
		if len(url_base7+'1bMVw38i') > 0:		
			content = abrir_url(url_base7+'1bMVw38i')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,10,img,False)
		if len(url_base7+'SQDZWpDE') > 0:		
			content = abrir_url(url_base7+'SQDZWpDE')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,10,img,False)
		if len(url_base7+'wCFB1Skk') > 0:		
			content = abrir_url(url_base7+'wCFB1Skk')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,10,img,False)
		if len(url_base7+'Mix6xcKg') > 0:		
			content = abrir_url(url_base7+'Mix6xcKg')
			match = re.compile(master_regex).findall(content)
			for url, name, img in match:
				if searchText in name:
					addDirfav(name,url,10,img,False)
		if len(url_base7+'bXZL7m2L') > 0:		
			content = abrir_url(url_base7+'bXZL7m2L')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'kXBnNSbN') > 0:		
			content = abrir_url(url_base7+'kXBnNSbN')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'ZDDMswjx') > 0:		
			content = abrir_url(url_base7+'ZDDMswjx')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'Vu4LWBuf') > 0:		
			content = abrir_url(url_base7+'Vu4LWBuf')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'uHGmiy37') > 0:		
			content = abrir_url(url_base7+'uHGmiy37')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'3HgXnWcw') > 0:		
			content = abrir_url(url_base7+'3HgXnWcw')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'GHkJUUA2') > 0:		
			content = abrir_url(url_base7+'GHkJUUA2')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'v7eFd3LJ') > 0:		
			content = abrir_url(url_base7+'v7eFd3LJ')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'CkTi4k2A') > 0:		
			content = abrir_url(url_base7+'CkTi4k2A')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'B0V8Y108') > 0:		
			content = abrir_url(url_base7+'B0V8Y108')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'YprHSXUx') > 0:		
			content = abrir_url(url_base7+'YprHSXUx')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'Ep6YLc6Z') > 0:		
			content = abrir_url(url_base7+'Ep6YLc6Z')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)					
		if len(url_base7+'JQy0QZpu') > 0:		
			content = abrir_url(url_base7+'JQy0QZpu')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'SqkdckbS') > 0:		
			content = abrir_url(url_base7+'SqkdckbS')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'YxdiprDU') > 0:		
			content = abrir_url(url_base7+'YxdiprDU')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'jc3mzrAi') > 0:		
			content = abrir_url(url_base7+'jc3mzrAi')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'1bixerQr') > 0:		
			content = abrir_url(url_base7+'1bixerQr')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'VetY05Gn') > 0:		
			content = abrir_url(url_base7+'VetY05Gn')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'1KRPeQbK') > 0:		
			content = abrir_url(url_base7+'1KRPeQbK')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
		if len(url_base7+'DY2kby4s') > 0:		
			content = abrir_url(url_base7+'DY2kby4s')
			match = re.compile(txt_regex).findall(content)
			for name, img, url in match:
				if searchText in name:
					addDirfav(name,url,14,img,False)
	except:
		pass
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')

############################################################################################################
#                                              MAIS PARÂMETROS                                             #
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

elif mode==12:
    print ""
    favoritos()

elif mode==13:
    print ""
    adicionar_favoritos(url)

elif mode==14:
    print ""
    player(name,url,iconimage)

elif mode==15:
    print ""
    remover_favorito()

elif mode==16:
    print ""
    search()	
	
elif mode==30:
	check(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
