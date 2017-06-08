# -*- coding: utf-8 -*-
#------------------------------------------------------------
# FutureMusic Magazine from YouTube by Slim
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import re
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.FutureMusic'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')
fanart = local.getAddonInfo('fanart')

YOUTUBE_CHANNEL_ID = "UC4hni3O2-HrgbAyY9QduJdg"

# Entry point
def run():
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    textfile = "http://pastebin.com/raw/gDxH2AQr"
    word = plugintools.read(textfile)
    names = re.compile('.+?ame="(.+?)"').findall(word)
    urls = re.compile('.+?youtube.com/playlist/(.+?)"').findall(word)
    icons = re.compile('.+?con="(.+?)"').findall(word)
    fanarts = re.compile('.+?anart="(.+?)"').findall(word)
    for name,url,icon,fanart in zip(names,urls,icons,fanarts):
        xbmc.log(name)
        xbmc.log(url)
        xbmc.log(icon)
        xbmc.log(fanart)
        plugintools.add_item(
            title=name,
            url="plugin://plugin.video.youtube/playlist/"+url+"/",
            thumbnail=icon,
            fanart=fanart,
            folder=True)
run()