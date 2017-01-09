# -*- coding: utf-8 -*-

#      Copyright (C) 2017 Mucky Duck
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
import os,re,shutil,sys,urllib

from metahandler import metahandlers
from common import Addon

metaget = metahandlers.MetaData()


class md:



	def __init__(self, addon_id, argv=None):

		self.addon = Addon(addon_id, sys.argv)




	def regex_from_to(self, text, from_string, to_string, excluding=True):
		if excluding:
			try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
			except: r = ''
		else:
			try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
			except: r = ''
		return r




	def regex_get_all(self, text, start_with, end_with):
		r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
		return r




	def PT(self, url):
		#currently not workng
		self.addon.log('Play Trailer %s' % url)
		notification(self.addon.get_name(), 'fetching trailer', self.addon.get_icon())
		xbmc.executebuiltin("PlayMedia(%s)"%url)




	def notification(self, title, message, icon):
		self.addon.show_small_popup(self.addon.get_name(), message.title(), 5000, self.addon.get_icon)
		return




	def User_Agent(self):
		return 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'




	def addLink(self, name,url,mode,iconimage,fanart,description=''):
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
		return ok




	def addDir(self, name, url, mode, iconimage, fanart, title, season,
		   episode, description, type='', is_folder=True, item_count=0):

		metaset = self.addon.get_setting('enable_meta')

		splitName = title.partition('(')
		simplename = ""
		simpleyear = ""

		if len(splitName)>0:
			simplename=splitName[0]
			simpleyear=splitName[2].partition(')')

		if len(simpleyear)>0:
				simpleyear=simpleyear[0]

		u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+ \
		    "&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+ \
		    "&title="+urllib.quote_plus(title)+"&season="+urllib.quote_plus(season)+"&episode="+urllib.quote_plus(episode)
		ok=True
		
		if type == '':
			
			name = name.replace('()','')
			liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
			liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
			liz.setProperty('fanart_image', fanart)

		else:
			if metaset == 'true':
				
				if type == 'movie':

					try:
						meta = metaget.get_meta(type,simplename,simpleyear)
					except:
						meta = metaget.get_meta(type,simplename)

				elif type == 'tvshow':
					meta = metaget.get_meta(type,simplename)

				elif type == 'season':
					if not season == '' or season == None:
						if '0' in season[0]:
							season = season[1:].strip()
						meta.get_season_meta(title,len(season))
					else:
						meta = metaget.get_meta('tvshow',simplename)

				elif type == 'episode':
					if not episode == '' or episode == None:
						if '0' in episode[0]:
							episode = episode[1:].strip()
						if '0' in season[0]:
							season = season[1:].strip()
						meta = metaget.get_episode_meta(simplename,'',season,episode)
					else:
						meta = metaget.get_meta('tvshow',simplename)

				if meta['cover_url']=='':
					try:
						meta['cover_url']=iconimage
					except:
						meta['cover_url']=icon

				#if meta['title'] == '':
				meta['title'] = name
				#else:
					#meta['title'] = '[B][COLOR white]%s[/COLOR][/B]' %meta['title']

				contextMenuItems = []
				contextMenuItems.append(('Plot Information', 'XBMC.Action(Info)'))

				liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
				liz.setInfo( type="Video", infoLabels=meta )
				liz.addContextMenuItems(contextMenuItems, replaceItems=False)

				if not meta['backdrop_url'] == '':
					liz.setProperty('fanart_image', meta['backdrop_url'])

				else:
					liz.setProperty('fanart_image', fanart)
			else:
				name = name.replace('()','')
				liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
				liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
				liz.setProperty('fanart_image', fanart)
		

		if not is_folder == True:
			liz.setProperty("IsPlayable","true")
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=item_count)

		else:
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=item_count)

		return ok




	def get_params(self):
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



	def check_source(self):
		if xbmcvfs.exists(xbmc.translatePath('special://home/userdata/sources.xml')):
			with open(xbmc.translatePath('special://home/userdata/sources.xml'), 'r+') as f:
				my_file = f.read()
				if re.search(r'http://muckys.mediaportal4kodi.ml', my_file):
					self.addon.log('Muckys Source Found in sources.xml, Not Deleting.')
				else:
					line1 = "you have Installed The MDrepo From An"
					line2 = "Unofficial Source And Will Now Delete Please"
					line3 = "Install From [COLOR red]http://muckys.mediaportal4kodi.ml[/COLOR]"
					line4 = "Removed Repo And Addon"
					line5 = "successfully"
					self.addon.show_ok_dialog(addon_name, line1, line2, line3)
					delete_addon = self.addon.get_path()
					delete_repo = xbmc.translatePath('special://home/addons/repository.mdrepo')
					shutil.rmtree(delete_addon, ignore_errors=True)
					shutil.rmtree(delete_repo, ignore_errors=True)
					self.addon.log('===DELETING===ADDON===+===REPO===')
					self.addon.show_ok_dialog(self.addon.get_name(), line4, line5)
