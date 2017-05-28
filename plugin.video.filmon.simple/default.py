'''
    FilmOn Simple Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, sys, re, xbmcplugin, xbmcgui, xbmcaddon, xbmc, os, urllib2
import json, string, random
import datetime
from resources.modules import net
net = net.Net()

plugin='plugin.video.filmon.simple'
addon = xbmcaddon.Addon(id=plugin)
addonname = addon.getAddonInfo('name')
addonid = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addonid).getAddonInfo('path')
addon_logo = xbmc.translatePath(os.path.join(plugin_path,'tvaddons_logo.png'))

dlg = xbmcgui.Dialog()

datapath = xbmc.translatePath(addon.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')

if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)

cookie_jar = os.path.join(cookie_path, "FilmOn.lwp")
    
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Magic Browser')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def categories():
    url='http://www.filmon.com/group'
    net.set_cookies(cookie_jar)
    html = net.http_GET(url).content
    link = html.encode('ascii', 'ignore')
    match=re.compile('<li class="group-item">.+?<a href="(.+?)">.+?"logo" src="(.+?)" title="(.+?)"',re.DOTALL).findall(link)
    for url, iconimage , name in match:
        if name == "ENTERTAINMENT" or name == "MUSIC" or name == "COMEDY" or name == "KIDS" or name == "BUSINESS TV" or name == "DOCUMENTARY" or name == "NEWS TV" or name == "EXTREME SPORTS" or name == "URBAN" or name == "PARTY TV" or name == "LIFESTYLE" or name == "BODY &amp; SOUL" or name == "FILMON EXCLUSIVE" or name == "FASHION" or name == "SCIENCE &amp; TECHNOLOGY TV" or name == "GERMAN TV" or name == "RUSSIAN TV" or name == "INDIAN TV" or name == "ITALIAN TV" or name == "MIDDLE EASTERN TV" or name == "SWISS TV" or name == "HUNGARIAN TV" or name == "LATINO TV" or name == "CLASSIC TV" or name == "SHORT FILMS" or name == "OUTDOORS" or name == "TRAVEL" or name == "SOMALI TV" or name == "GREEK LIVE TV" or name == "RELIGION" or name == "CELEBRITY TV" or name == "FOOD AND WINE" or name == "CARS &amp; AUTO" or name == "EDUCATION" or name == "SHOPPING TV" or name == "CARIBBEAN CHANNELS" or name == "ASIAN TV" or name == "AFRICAN TV" or name == "KAZAKH TV":
            xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
            addDir(name.title().replace('Tv','TV').replace('Uk','UK').replace('Uk','UK').replace('&Amp;','&'),url,3,iconimage,'',name)
                
def channels(url,name,group):
    r='<li class="channel i-box-sizing".+?channel_id="(.+?)">.+?"channel_logo" src="(.+?)" title="(.+?)"'
    net.set_cookies(cookie_jar)
    html = open_url('http://www.filmon.com'+url)
    match=re.compile(r,re.DOTALL).findall(html)
    for id , iconimage , name in match:
        if id != '1240' and id != '1078' and id != '1426' and id != '2146'and id != '2230' and id != '2236' and id != '2206' and id != '2233' and id != '4463' and id != '4931' and id != '2188' and id != '2152' and id != '2170' and id != '1426' and id != '1367' and id != '1310' and id != '1325' and id != '1336' and id != '1114' and id != '1111' and id != '1108' and id != '1099' and id != '1198' and id != '1102' and id != '1285' and id != '1287' and id != '3191' and id != '29' and id != '1289' and id != '1282' and id != '1286' and id != '1281' and id != '1172' and id != '2786' and id != '5672' and id != '93' and id != '1759' and id != '2218' and id != '1483' and id != '1254' and id != '1487' and id != '1345' and id != '1358' and id != '5366' and id != '1753' and id != '1536' and id != '1248' and id != '1266' and id != '1255' and id != '1258' and id != '1271' and id != '1256' and id != '2086' and id != '1272' and id != '1257' and id != '1262' and id != '1976' and id != '2044' and id != '2119' and id != '2128' and id != '2134' and id != '1129' and id != '1535' and id != '1507' and id != '1429' and id != '1524' and id != '1410' and id != '1526' and id != '1500' and id != '1505' and id != '1424' and id != '2245' and id != '1546' and id != '1506' and id != '2756' and id != '1738' and id != '1981' and id != '1735' and id != '1741' and id != '1744' and id != '3704' and id != '445' and id != '379' and id != '1778' and id != '1781' and id != '1796' and id != '1775' and id != '1772' and id != '79' and id != '1565' and id != '1558' and id != '1559' and id != '1561' and id != '1563' and id != '1562' and id != '1732' and id != '1213' and id != '1212' and id != '1217' and id != '1218' and id != '1219' and id != '1179' and id != '1238' and id != '1221' and id != '1237' and id != '1239' and id != '1233' and id != '1232' and id != '1222' and id != '1223' and id != '1224' and id != '1225' and id != '1226' and id != '1419' and id != '2242' and id != '1459' and id != '1461' and id != '1451' and id != '1793':
            addDir(name.replace(' New','New'),'http://www.filmon.com'+url.replace('channel','tv').replace('tvs','channels'),2,iconimage,id,group)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r
        
def play_stream(name,url,iconimage,description):
    streamerlink = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    swfplay = 'http://www.filmon.com' + regex_from_to(streamerlink, '"streamer":"', '",').replace("\/", "/")

    name = name.replace('[COLOR cyan]','').replace('[/COLOR]','')
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    utc_now = datetime.datetime.now()
    channel_name=name
    net.set_cookies(cookie_jar)
    url='http://www.filmon.com/channel/%s' % (description)
    link = net.http_GET(url,headers={'Accept':'application/json, text/javascript, */*; q=0.01'}).content
    link = json.loads(link)
    link = str(link)
	
    next_p = regex_from_to(link, "next_playing'", "u'title")
    try:
        n_start_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "startdatetime': u'", "',")))
        n_end_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "enddatetime': u'", "',")))
        n_programme_name = regex_from_to(next_p, "programme_name': u'", "',")
        n_start_t = n_start_time.strftime('%H:%M')
        n_end_t = n_end_time.strftime('%H:%M')
        n_p_name = "[COLOR cyan]Next: %s (%s-%s)[/COLOR]" % (n_programme_name, n_start_t, n_end_t)
    except:
        n_p_name = ""
		
    now_p = regex_from_to(link, "now_playing':", "u'tvguide")
    try:
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "startdatetime': u'", "',")))
        end_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "enddatetime': u'", "',")))
        programme_name = regex_from_to(now_p, "programme_name': u'", "',")
        description = ""
        start_t = start_time.strftime('%H:%M')
        end_t = end_time.strftime('%H:%M')
        p_name = "%s (%s-%s)" % (programme_name, start_t, end_t)
        dp.update(50, p_name)
    except:
        try:
            p_name = programme_name
        except:
            p_name = name
    streams = regex_from_to(link, "streams'", "u'tvguide")
    hl_streams = regex_get_all(streams, '{', '}')
    url = regex_from_to(hl_streams[1], "url': u'", "',")
    name = regex_from_to(hl_streams[1], "name': u'", "',")

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    try:
        listitem = xbmcgui.ListItem(p_name + ' ' + n_p_name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        if handle != "-1":	
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(url,listitem)
    except:
        listitem = xbmcgui.ListItem(channel_name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(url,listitem)
    dp.close()

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
           
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
            
def addDir(name,url,mode,iconimage,description,group):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&group="+urllib.quote_plus(group)+"&rand=" + random_generator()
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    if mode==2:
        liz.setProperty("IsPlayable", "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
                                 
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_setting(setting):
    return addon.getSetting(setting)
    
def set_setting(setting, string):
    return addon.setSetting(setting, string) 
                                               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
group=None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:        
    mode = int(params["mode"])
except:
    pass
try:        
    description = urllib.unquote_plus(params["description"])
except:
    pass
try:        
    group=urllib.unquote_plus(params["group"])
except:
    pass

if mode == None or url == None or len(url) < 1:
    categories()
    if len(get_setting('notify')) > 0:
        set_setting('notify', str(int(get_setting('notify')) + 1))  
    else:
        set_setting('notify', "1")        
    if int(get_setting('notify')) == 1:
        xbmcgui.Dialog().notification(addonname + ' is provided by:','www.tvaddons.ag',addon_logo,5000,False)
    elif int(get_setting('notify')) == 9:
        set_setting('notify', "0")             

elif mode == 2:
    play_stream(name,url,iconimage,description)
                
elif mode == 3:
    channels(url,name,group)
                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
