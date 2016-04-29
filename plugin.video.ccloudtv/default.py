# -*- coding: utf-8 -*-

"""
Copyright (C) 2016 PodGod

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import urllib, urllib2, sys, re, os, random, unicodedata, cookielib, shutil
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, requests, base64

plugin_handle = int(sys.argv[1])
mysettings = xbmcaddon.Addon(id = 'plugin.video.ccloudtv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
enable_adult_section = mysettings.getSetting('enable_adult_section')

fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))
icon = xbmc.translatePath(os.path.join(home, 'resources/icons/icon.png'))
addonDir = mysettings.getAddonInfo('path').decode("utf-8")

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
group_title_regex = 'group-title=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
eng_regex = '#(.+?),English,(.+)\s*(.+)\s*'
adult_regex = '#(.+?)group-title="Adult",(.+)\s*(.+)\s*'
adult_regex2 = '#(.+?)group-title="Public-Adult",(.+)\s*(.+)\s*'
ondemand_regex = '[ON\'](.*?)[\'nd]'
yt = 'http://www.youtube.com'
m3u = 'WVVoU01HTkViM1pNTTBKb1l6TlNiRmx0YkhWTWJVNTJZbE01ZVZsWVkzVmpSMmgzVURKck9WUlViRWxTYXpWNVZGUmpQUT09'.decode('base64')
text = 'http://pastebin.com/raw.php?i=Zr0Hgrbw'
GuideDirectory = xbmc.translatePath('special://home/userdata/addon_data/script.renegadestv/')
GuideINI = xbmc.translatePath('special://home/userdata/addon_data/script.renegadestv/addons2.ini')
xbmcplugin.setContent(int(sys.argv[1]), 'movies')


					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass
		

def make_request():
	try:
		for server in shuffle(CCLOUDTV_SRV_URL):
			conn = GetHttpStatusAndData(server)
			if conn['valid']:
				links = conn['data'].encode('utf-8')
				return links
	except e:
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
	print 'All cCloud TV servers seem to be down. Please try again in a few minutes.'
	return None

			
def main():
	addDir('[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]', yt, 3, '%s/announcements.png'% iconpath, fanart)
	addDir('[COLOR red][B]Search[/B][/COLOR]', 'searchlink', 99, '%s/search.png'% iconpath, fanart)
	if len(CCLOUDTV_SRV_URL) > 0:	
		addDir('[COLOR yellow][B]All Channels[/B][/COLOR]', yt, 2, '%s/allchannels.png'% iconpath, fanart)
	if (len(CCLOUDTV_SRV_URL) < 1 ):		
		mysettings.openSettings()
		xbmc.executebuiltin("Container.Refresh")
	addDir('[COLOR yellow][B]TV Guide[/B][/COLOR]', 'guide', 97, '%s/guide.png'% iconpath, fanart)
	#addDir('Open TV Guide/Update Channels','INI',95,'%s/guide.png'% iconpath,fanart)
	addDir('[COLOR royalblue][B]English[/B][/COLOR]', 'english', 62, '%s/english.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Top 10[/B][/COLOR]', 'top10', 51, '%s/top10.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Sports[/B][/COLOR]', 'sports', 52, '%s/sports.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]News[/B][/COLOR]', 'news', 53, '%s/news.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Documentary[/B][/COLOR]', 'documentary', 54, '%s/documentary.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Entertainment[/B][/COLOR]', 'entertainment', 55, '%s/entertainment.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Family[/B][/COLOR]', 'family', 56, '%s/family.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Movies[/B][/COLOR]', 'movie', 57, '%s/movies.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Music[/B][/COLOR]', 'music', 58, '%s/music.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Lifestyle[/B][/COLOR]', 'lifestyle', 63, '%s/lifestyle.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]On Demand Movies[/B][/COLOR]', 'ondemandmovies', 59, '%s/ondemandmovies.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]On Demand Shows[/B][/COLOR]', 'ondemandshows', 65, '%s/ondemandshows.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]24/7 Channels[/B][/COLOR]', '24', 60, '%s/twentyfourseven.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Radio[/B][/COLOR]', 'radio', 61, '%s/radio.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Non-English/International[/B][/COLOR]', 'international', 64,'%s/international.png'% iconpath, fanart)
	if getSetting("enable_adult_section") == 'true':	
		addDir('[COLOR magenta][B]Adult(18+)[/B][/COLOR]', 'adult', 98, '%s/adult.png'% iconpath, fanart)

def createini():
	if not os.path.exists(GuideDirectory):
		dialog.ok(addon_id, 'Please make sure you have TV Guide installed and you have run it at least once then use this function to enable integration')
		dialog.notification(addonname, 'Please install and run TV Guide at least once', xbmcgui.NOTIFICATION_ERROR );
	
	if os.path.exists(GuideDirectory):
		addonsini = urllib.URLopener()
		addonsini.retrieve("https://raw.githubusercontent.com/podgod/podgod/master/cCloud_TV_Guide/XML/combined.ini", GuideINI)
        with open(GuideDirectory+"/addons2.ini", "a") as file:
            file.write('https://raw.githubusercontent.com/podgod/podgod/master/cCloud_TV_Guide/XML/combined.ini\n')
        shutil.rmtree(GuideDirectory , ignore_errors=True)
    	xbmc.executebuiltin("RunAddon(script.renegadestv)")
        sys.exit()
		
def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
		
def search(): 	
	try:
		keyb = xbmc.Keyboard('', 'Enter Channel Name')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def sports(): 	
	try:
		searchText = '(Sports)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

def top10(): 	
	try:
		searchText = '(Top10)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
def news(): 	
	try:
		searchText = '(News)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def documentary(): 	
	try:
		searchText = '(Document)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def entertainment(): 	
	try:
		searchText = '(Entertainment)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
	
def family(): 	
	try:
		searchText = '(Family)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass


		
def lifestyle(): 	
	try:
		searchText = '(Lifestyle)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass

		
	
def movie(): 	
	try:
		searchText = '(Movie Channels)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	


def music(): 	
	try:
		searchText = '(Music)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

def ondemandmovies(): 	
	try:
		searchText = '(OnDemandMovies)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass
	
def ondemandshows(): 	
	try:
		searchText = '(OnDemandShows)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass
		

	
def twentyfour7(): 	
	try:
		searchText = '(RandomAirTime 24/7)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

	
def radio(): 	
	try:
		searchText = '(Radio)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	

	
def adult(): 	
	try:
		searchText = ('(Adult)') or ('(Public-Adult)')
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(adult_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					adult_playlist(name, url, thumb)	
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(adult_regex2).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					adult_playlist(name, url, thumb)	

	except:
		pass
	
	
	
def english(): 	
	#addDir('[COLOR yellow][B]cCloud TV Guide[/B][/COLOR] - Click Here! Thanks to Renegades TV', 'guide', 97, '%s/guide.png'% iconpath, fanart)
	try:
		searchText = '(English)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content) 
			#file.write('\n'.join(match))
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
			#outfile.write("\n".join(addontest.ini))
	except:
		pass
	

def international(): 	
	try:
		searchGerman = '(German)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchGerman, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSpanish = '(Spanish)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSpanish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFrench = '(French)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFrench, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchHindi = '(Hindi)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchHindi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchArabic = '(Arabic)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchArabic, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchUrdu = '(Urdu)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchUrdu, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFarsi = '(Farsi)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFarsi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchPortuguese = '(Portuguese)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchPortuguese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchKurdish = '(Kurdish)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchKurdish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchChinese = '(Chinese)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchChinese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSomali = '(Somali)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSomali, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchRussian = '(Russian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchRussian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchAfrikaans = '(Afrikaans)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchAfrikaans, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchRomanian = '(Romanian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchRomanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchItalian = '(Italian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchItalian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchIsraeli = '(Israeli)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchIsraeli, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchGreek = '(Greek)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchGreek, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchhungarian = '(Hungarian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchHungarian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchTamil = '(Tamil)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchTamil, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMacedonian = '(Macedonian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchMacedonian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchIndian = '(Indian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchIndian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchCatalan = '(Catalan)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchCatalan, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchJamaica = '(Jamaica)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchJamaica, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchUkrainian = '(Ukrainian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchUkrainian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchVietamese = '(Vietamese)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchVietamese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMaltese = '(Maltese)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchMaltese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchLithuanian = '(Lithuanian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchLithuanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchPolish = '(Polish)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchPolish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchSlovenian = '(Slovenian)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchSlovenian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchDeutsch = '(Deutsch)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchDeutsch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchDutch = '(Dutch)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchDutch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchFilipino = '(Filipino)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	try:
		searchMandarin = '(Mandarin)'
		if len(CCLOUDTV_SRV_URL) > 0:		
			content = make_request()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
	except:
		pass
	
		
def text_online():		
	text = '[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]'
	newstext = 'http://pastebin.com/raw.php?i=7K3zDiZ2'
	req = urllib2.Request(newstext)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("<START>(.+?)<END>",re.DOTALL).findall(link)
	for status in match:
	    try:
			    status = status.decode('ascii', 'ignore')
	    except:
			    status = status.decode('utf-8','ignore')
	    status = status.replace('&amp;','')
	    text = status
	showText('[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]', text)

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass

def guide():
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('cCloud TV Guide', '[COLOR yellow]cCloud TV[/COLOR] is now integrated with your favourite TV Guides.','This is currently in beta and not all channels are supported.','[COLOR yellow]>>>>>>>>>>>>>  Choose Your Guide Below  <<<<<<<<<<<<<[/COLOR]','iVue TV Guide','Renegades TV Guide')
	if ret == 1:
			xbmc.executebuiltin("RunAddon(script.renegadestv)")
			sys.exit()
	if ret == 0:
			xbmc.executebuiltin("RunAddon(script.ivueguide)")
			sys.exit()
	else:
			sys.exit()
	
def m3u_online():		
	content = make_request()
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
		

def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			addDir(name, url, '', thumb, thumb)			
		else:	
			addDir(name, url, '', icon, fanart)
	else:
		if ('(Adult)' in name) or ('(Public-Adult)' in name):
			name = 'ADULTS ONLY'.url = 'http://ignoreme.com'
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		#elif 'dailymotion.com/video/' in url:
		#	url = url.split('/')[-1].split('_')[0]
		#	url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)			
		else:				
			addLink(name, url, 1, icon, fanart)	
			
			
def adult_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			addDir(name, url, '', thumb, thumb)		
		else:	
			addDir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		#elif 'dailymotion.com/video/' in url:
		#	url = url.split('/')[-1].split('_')[0]
		#	url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)			
		else:				
			addLink(name, url, 1, icon, fanart)	

def play_video(url):

	if 'parser.php?surl=' in url: # case for cCloudTv redirecting parser
		try:
			#print 'URL: ' + str(url)
			if '|' in url:
				urls = url.split('|')
				rurl = str(urls[0])
				purl = urls[1]
			else:
				rurl = url
			req = urllib2.Request(rurl)
			res = urllib2.urlopen(req)
			furl = res.geturl()
			if '|' in url:
				url = furl + '|' + purl
			else:
				url = furl
			#print 'RedirectorURL: ' + str(url)
		except:
			pass
			
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return
	
def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

ini = 'YUhSMGNEb3ZMMnR2WkdsbGNHY3VZMk5zWkM1cGJ3PT0='.decode('base64').decode('base64')
List1 = 'YUhSMGNEb3ZMM2d1WTI4dlpHSmphREF4'.decode('base64').decode('base64')
List2 = 'YUhSMGNEb3ZMMnR2WkdrdVkyTnNaQzVwYnc9PQ=='.decode('base64').decode('base64')
List3 = 'YUhSMGNEb3ZMMkZwYnk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVE9PQ=='.decode('base64').decode('base64')
List4 = 'YUhSMGNEb3ZMMmR2TW13dWFXNXJMMnR2WkdrPQ=='.decode('base64').decode('base64')
List5 = 'YUhSMGNEb3ZMM051YVhBdWJHa3ZhMjlrYVE9PQ=='.decode('base64').decode('base64')
List6 = 'YUhSMGNEb3ZMMk5rYmk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVRFPQ=='.decode('base64').decode('base64')
List7 = 'YUhSMGNEb3ZMMk5rYmk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVRJPQ=='.decode('base64').decode('base64')
List8 = 'YUhSMGNEb3ZMMk5rYmk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVRNPQ=='.decode('base64').decode('base64')
List9 = 'YUhSMGNEb3ZMMk5rYmk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVRRPQ=='.decode('base64').decode('base64')
List10 = 'YUhSMGNEb3ZMMk5rYmk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVRVPQ=='.decode('base64').decode('base64')
List11= 'YUhSMGNEb3ZMMkZwY2k1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVE9PQ=='.decode('base64').decode('base64')

CCLOUDTV_SRV_URL = [List1,List2,List3,List4,List5,List6,List7,List8,List9,List10,List11]

####################################################################################################
# Gets the data and tests for a valid M3U since a 200 response code can still lead to an empty file 
# or a different page but not our listing
def GetHttpStatusAndData(url):

	resp = {}
	resp['valid'] = False
	resp['data'] = ''
	try:
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
   
		req = urllib2.Request(url, headers=hdr)
		response = urllib2.urlopen(req)
		
		data = response.read()
		if '#EXTM3U' in data:
			resp['valid'] = True
			resp['data'] = data

	except urllib2.HTTPError, e:
		pass

	return resp

####################################################################################################
# Randomizes the order of items in a list
def shuffle(mlist):
	result = []
	cloneList = []
	for item in mlist:
		cloneList.append(item)
	for i in range(len(cloneList)):
		element = random.choice(cloneList)
		cloneList.remove(element)
		result.append(element)
	return result

def addDir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def addLink(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true') 
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
		
params = get_params()
url = None
name = None
mode = None
iconimage = None

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
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)		

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	play_video(url)

elif mode == 2:
	m3u_online()
	
elif mode == 3:
	text_online()
	
	
elif mode == 51:
	top10()
		
elif mode == 52:
	sports()
	
elif mode == 53:
	news()
	
elif mode == 54:
	documentary()
	
elif mode == 55:
	entertainment()
	
elif mode == 56:
	family()
	
elif mode == 57:
	movie()
	
elif mode == 58:
	music()
	
elif mode == 59:
	ondemandmovies()
	
elif mode == 65:
	ondemandshows()
	
elif mode == 60:
	twentyfour7()
	
elif mode == 61:
	radio()
	
elif mode == 62:
	english()

elif mode == 63:
	lifestyle()
	
elif mode == 64:
	international()
	
elif mode==95:
    createini()
		
elif mode == 97:
	guide()
	
elif mode == 98:
	adult()
	
elif mode == 99:
	search()
	
xbmcplugin.endOfDirectory(plugin_handle)