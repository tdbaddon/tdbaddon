# -*- coding: utf-8 -*-

import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import xml.etree.ElementTree as ET
import urllib,urllib2,time,os,re

def iplaList(iplaid,contentupdatets,newsid,name):
    iplaidlist = []
    elems = get_data()
    cats = elems.findall("cat")
    for cat in cats:
        val = cat.attrib
        try:
            pid = val['pid']
            if pid == str(iplaid):
                iplaidlist.append(val)
        except:
            pass
    if not iplaidlist:
        iplaVOD(iplaid,contentupdatets,newsid,name) 
    else:
        for item in iplaidlist:
            iplaid = item['id']
            newsid = item['pid']
            title = item.get('title','')
            iconimage = item.get('thumbnail_big','')
            descr = item.get('descr','')
            publishts = float(item.get('publishts',time.time()))
            contentupdatets = float(item.get('contentupdatets',time.time()))
            if iplaid != '5000296':
                addDir(iplaid,newsid,title,iconimage,descr,publishts,contentupdatets)
        xbmcplugin.addSortMethod( int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def iplaVOD(iplaid,contentupdatets,newsid,name):
    darmolist = []
    elems = get_VOD_data(iplaid,contentupdatets,newsid)
    vods = elems.find("VoDs").findall("vod")    
    for vod in vods:
        val = vod.attrib
        links = vod.findall("srcreq")
        maxquality = 0
        for link in links:
            ell = link.attrib
            drm = ell['drmtype']
            quality = ell['quality']
            if drm == '0' :
                if int(quality) > maxquality:
                    maxquality = int(quality)
        for link in links:
            ell = link.attrib
            drm = ell['drmtype']
            iquality = int(ell['quality'])
            if drm == '0' and iquality == maxquality:
                val['url'] = ell['url']
                darmolist.append(val)
                break
    if not darmolist:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('ipla.tv','Niestety, nie ma darmowej zawartości') 
    else:
        for item in darmolist:
            title = item.get('title','')
            if not title:
                title = item.get('descr','')
            iconimage = item.get('thumbnail_big','')
            descr = item.get('descr','')
            vcnt = item.get('vcnt','') 
            vote = item.get('vote','')
            dur = int(item.get('dur','0'))
            url = item.get('url','')
            timestamp = float(item.get('timestamp',time.time()))
            addLink(title,url,iconimage,descr,timestamp,vcnt,vote,dur,name)
        xbmcplugin.addSortMethod( int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE )
        xbmcplugin.addSortMethod( int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        xbmcplugin.addSortMethod( int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addLink(name,url,iconimage,descr,timestamp,vcnt,vote,dur,tvshowtitle):
        ok=True
        m, s = divmod(dur, 60)
        h, m = divmod(m, 60)
        odcinek = 0
        matched = re.match(u'(.*)\\s?[-\u2013]\\s[Oo]dcinek\\s+(\\d+)',name)
        if matched:
            name, odcinek = matched.group(1), int(matched.group(2))
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="video",  infoLabels = {
                'title' : name ,
                'tvshowtitle' : tvshowtitle ,
                'aired' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)) ,
                'date' : time.strftime("%d.%m.%Y", time.localtime(timestamp)) ,
                'votes' : vcnt ,
                'rating' : float(vote) ,
                'episode' : odcinek ,
                'duration' : "%d:%02d:%02d" % (h, m, s) ,
                'plot': descr
        })
        liz.setProperty('fanart_image', __settings__.getAddonInfo('fanart') )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(iplaid,newsid,title,iconimage,descr,publishts,contentupdatets):
    u=sys.argv[0]+"?iplaid="+str(iplaid)+"&newsid="+str(newsid)+"&contentupdatets="+str(contentupdatets)+"&name="+title
    ok=True
    liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="video",  infoLabels = {
                'title' : title ,
                'aired' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publishts)) ,
                'year' : int(time.strftime("%Y", time.localtime(publishts))) , 
                'genre' : 'ipla.tv' , 
                'plot': descr
    })
    liz.setProperty('fanart_image', __settings__.getAddonInfo('fanart') )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

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

def request(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'ipla/344 (Windows NT 6.1)')
	response = urllib2.urlopen(req)
	data = response.read()
	response.close()
	return data

def download_listfile(dest):
        data = request(URL_CATEGORIES)
        f = open(dest,'w')
        f.write(unicode(data,'UTF-8').encode('UTF-8'))
        f.close()

def get_data():
	local = xbmc.translatePath(__settings__.getAddonInfo('profile'))
	if not os.path.exists(local):
		os.makedirs(local)
	local = os.path.join(local,'list.xml')
	if os.path.exists(local):
		if (time.time() - os.path.getctime(local)) > (3600*24):
			download_listfile(local)
	else:
		download_listfile(local)
	return ET.parse(local).getroot()

def download_VODfile(dest,iplaid):
        data = request(URL_MOVIE + str(iplaid))
        f = open(dest,'w')
        f.write(unicode(data,'UTF-8').encode('UTF-8'))
        f.close()

def get_VOD_data(iplaid,contentupdatets,newsid):
    local = xbmc.translatePath(__settings__.getAddonInfo('profile'))
    local = os.path.join(local,str(iplaid)+'.xml')
    if os.path.exists(local):
        if contentupdatets > os.path.getctime(local):
            download_VODfile(local,iplaid)
        elif (time.time() - os.path.getctime(local)) > (3600*4):
            download_VODfile(local,iplaid)
    else:
        download_VODfile(local,iplaid)  
    return ET.parse(local).getroot()

__settings__ = xbmcaddon.Addon(id='plugin.video.ipla.pl')
URL_IPLA = 'http://getmedia.redefine.pl'
IDENTITY = 'login=common_user&passwdmd5=&ver=281&cuid=-8939960'
URL_CATEGORIES = URL_IPLA + '/r/l_x_35_ipla/categories/list/?' + IDENTITY
URL_MOVIE = URL_IPLA + '/action/2.0/vod/list/?' + IDENTITY + '&category='
params=get_params()
newsid=None
contentupdatets=None
try:
        iplaid=int(params["iplaid"])
except:
        iplaid=0
        pass
try:
        newsid=int(params["newsid"])
except:
        pass
try:
        contentupdatets=float(params["contentupdatets"])
except:
        pass
try:
        name=params["name"]
except:
        name='ipla.tv'
        pass

iplaList(iplaid,contentupdatets,newsid,name)



