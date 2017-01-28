'''
@author: kinkin
'''
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
from common import create_directory, create_file

ADDON = xbmcaddon.Addon(id='plugin.video.gachecker')
DATA_PATH = os.path.join(ADDON.getAddonInfo('path'), '')

def addon():
    return ADDON

def plugin_list():
    return create_file(DATA_PATH, "plugins.list")

