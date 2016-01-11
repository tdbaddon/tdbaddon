import os
import re
import sys
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcgui


from addon.common.net import Net
from addon.common.addon import Addon

net = Net()

addon_id = 'plugin.video.xxtrucoxx'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()

newsurl = 'http://xxtrucoxx.googlecode.com/svn/trunk/list/_latestnews.xml'

try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)
               
def TWITTER(url):
    #test = net.http_GET(newsurl).content
    #r = re.search(r'<message>(.*?)</message>', test, re.I|re.DOTALL)

    #print r.groups()
    

    #print latestnews
    try:
      latestnews = re.sub(r'\r|\n', ' ', re.search('<message>(.*?)</message>', net.http_GET(newsurl).content, re.I|re.DOTALL).group(1))
      html = net.http_GET(url).content
    except:
      error()

    l = []
    r = re.findall('tem\>.*?title\>(.*?)\<\/tit.*?Date\>(.*?)\s+\d+\:', html, re.I|re.DOTALL)
    for text, date in r:

        text = re.sub(r'(?i)(\#\w+)\s', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(\#\w+)$', r'[COLOR blue]\1[/COLOR] ', text)
        text = re.sub(r'(?i)(pic\.twitter.*?)$', r'', text)
        text = re.sub(r'(?i)^(white\w+)\:', r'[B][COLOR green]<<<[/B][/COLOR]\1:',text)
        text = re.sub(r'(?i)^(\w+)(?!white\w+)\:', r'[B][COLOR yellow]>>>[/B][/COLOR]\1:',text)
        
        final = date+'\n'+text+'\n'+'\n'
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (latestnews,tt)
      
    
    
def SetViewType(viewtype):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % viewtype)


def Announce(date,announce):
    date = re.sub(r'/','-', date)

    if addon.get_setting('seen_anounce') == 'true':
        seen_date = addon.get_setting('seen_date')
        if date > seen_date:
            pass
        else:
            return

    from pyxbmct.addonwindow import *
    Addon.setSetting('seen_anounce', value='true')
    
    window = AddonDialogWindow('XxTRUCOxX [COLOR red]*ANNOUNCEMENT*[/COLOR] %s'%date)
    window.setGeometry(850, 600, 12, 8)
    textBox = TextBox(textColor='0xFFFFFFFF')
    window.placeControl(textBox, 0, 0, columnspan=7, rowspan=11)
    textBox.setText(announce)

    button = Button('Close')
    window.placeControl(button, 11, 3, columnspan=2)
    window.setFocus(button)
    window.connect(button, window.close)
    window.connect(ACTION_NAV_BACK, window.close)
    window.doModal()

    Addon.setSetting(id='seen_date', value=date)
    


        
