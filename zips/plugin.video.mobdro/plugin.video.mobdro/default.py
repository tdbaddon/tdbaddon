# -*- coding: utf-8 -*-
#------------------------------------------------------------
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import urllib
import urllib2
import json

from modules import VeetleProxyServer
from modules import resolver

__plugin__ = "Mobdro"
__author__ = "AddonHacker"
__image_path__ = ''
__settings__ = xbmcaddon.Addon(id='plugin.video.mobdro')
__language__ = "en"
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
addon_handle = int(sys.argv[1])

def add_cat(name, id):
	ADDON = xbmcaddon.Addon(id='plugin.video.mobdro')
	plugintools.add_item( action="channel_list" , title=name , url=id, folder=True )

# Entry point
def run():
	plugintools.log("Modbro.run")
	
	VeetleProxyServer.run()
    
    # Get params
	params = plugintools.get_params()
	
	if params.get("action") is None:
		category_list(params)
	elif params.get("action")=="channel_list":
		channel_list(params)
	else:
		plugintools.log("ACTION: " + params.get("action"))
		action = params.get("action")
		exec action + "(params)"
	
	plugintools.close_item_list()

def play_playlist(params):
	#plugintools.log("PLAYLSIT LENGTH: " + str(len(playlist)))
	xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)
	
	
# Categories
def category_list(params):
	add_cat("Channels", "channels")
	add_cat("News", "news")
	add_cat("Shows", "shows")
	add_cat("Movies", "movies")
	add_cat("Sports", "sports")
	add_cat("Music", "music")
	add_cat("Gaming", "gaming")
	add_cat("Animals", "animals")
	add_cat("Tech", "tech")
	add_cat("Podcasts", "podcasts")
	add_cat("Spiritual", "spiritual")
	add_cat("Others", "others")

playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
page_playlist = []
	
# Main menu
c_url = ""
c_data = ""
c_headers = ""
results = ""

def channel_list(params):
    global c_url
    global c_data
    global c_headers
    global results
    
    plugintools.log("mobdro.channel_list "+repr(params))
	
	# On first page, pagination parameters are fixed
    if params.get("url") is not None:
        c_url = "https://api.mobdro.sx/streambot/v3/show"
        c_headers = {"User-Agent":"Mobdro/5.0", "Referer":"api.mobdro.sx"}
        c_data = {'data':params.get("url"),'parental':0,'languages':'[]','alphabetical':0,'token':'XNZSGC]FSUQ]YP]D','signature':'1083937564'}
        c_data = urllib.urlencode(c_data)
        # Fetch channel list
        req = urllib2.Request(c_url, c_data, c_headers)
        response = urllib2.urlopen(req)
        response = response.read()

	results = json.loads(response)
	
	#results = parsed_json["items"]
	plugintools.log("LIST LENGTH: "+str(len(results)))

    c = 0
    for result in results:
        if resolver.display(result) == 1:
         c = c + 1
    plugintools.add_item( action="play" , title="Total: " + str(c), plot="", url="", folder=False )
	
def play(params):
	resolved_url = resolver.resolve(json.loads(params.get("url")))

	if resolved_url:
		plugintools.log("PLAYING: " + resolved_url)
        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(resolved_url)

    #liz = xbmcgui.ListItem(path=resolved_url)
    #liz.setInfo(type="Video", infoLabels={ "Title": params.get("title"), "Plot": urllib.unquote(params.get("plot")) })    
    #liz.setProperty('IsPlayable', 'true')
    #xbmcplugin.setResolvedUrl(handle=int(addon_handle), succeeded=True, listitem=liz)

run()