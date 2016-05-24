import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.movies4me')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.movies4me'), '')

def addon():
    return ADDON
	
def quality():
    delay = ADDON.getSetting('quality')
    if delay == '0':
        return 'HD'
    else:
        return 'SD'
		
def enable_meta():
    if ADDON.getSetting('enable_meta') == "true":
        return True
    else:
        return False
		
def cache_path():
    return create_directory(DATA_PATH, "cache")
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
		
def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")
	
def restrict_trailer():
    if ADDON.getSetting('restrict_trailer') == "true":
        return True
    else:
        return False
		
def trailer_quality():
    quality = ADDON.getSetting('trailer_quality')
    if quality == '0':
        return '480p'
    elif quality == '1':
        return '720p'
    else:
        return '1080p'
		
def trailer_one_click():
    if ADDON.getSetting('trailer_one_click') == "true":
        return True
    else:
        return False
		
def movie_directory():
    if ADDON.getSetting('movie_directory')=='set':
        return create_directory(DATA_PATH, "movies")
    else:
        return ADDON.getSetting('movie_directory')
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
create_directory(DATA_PATH, "")

		
