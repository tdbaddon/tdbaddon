import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net,xbmc
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.channels import *
from resources.lib.modules.common import *
from resources.lib.modules.plugintools import *
from resources.lib.vod.blaze import *
from resources.lib.vod.quest import *
from resources.lib.vod.tvplayer import *
from resources.lib.vod.trutv import *
from resources.lib.vod.uktv_play import *

net       = net.Net()
ADDON     = xbmcaddon.Addon(id='plugin.video.freeview')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.freeview'), '')
addon_id  = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
icon      = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeview', 'icon.jpg'))
fanart    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeview', 'fanart.jpg'))
logos     = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeview/resources/logos', ''))
logos_tvp = 'https://assets.tvplayer.com/common/logos/256/Inverted/'

def CATEGORIES():
	addDir('Live TV','url',5,logos+'menu_live.png')
	addDir('Catch Up TV','url',6,logos+'menu_vod.png')
	
def getVOD():
	addDir('Blaze','url',8,logos+'blaze.png')
	addDir('Dave','http://uktvplay.uktv.co.uk/shows/channel/dave/',10,logos_tvp+'300.png')
	addDir('Drama','http://uktvplay.uktv.co.uk/shows/channel/drama/',10,logos_tvp+'346.png')
	addDir('Quest','url',9,logos_tvp+'327.png')
	addDir('Really','http://uktvplay.uktv.co.uk/shows/channel/really/',10,logos_tvp+'306.png')
	addDir('Yesterday','http://uktvplay.uktv.co.uk/shows/channel/yesterday/',10,logos_tvp+'308.png')
		
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

print "Mode: "+str(mode)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
	
elif mode==1: play(url)
elif mode==2: tvplayer(url)
elif mode==3: vod_trutv()
elif mode==4: vod_play(url)
elif mode==5: getChannels()
elif mode==6: getVOD()
elif mode==8: vod_blaze()
elif mode==9: vod_quest()
elif mode==10: vod_uktv(url)
elif mode==11: vod_uktvEp(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
