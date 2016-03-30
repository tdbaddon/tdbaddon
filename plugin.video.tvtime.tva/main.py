'''
    TV Time Free Add-on

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

from resources.lib import Addon, tvtime
import sys, os, urllib, urllib2
import json
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonid   = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addonid).getAddonInfo('path')

Addon.plugin_url = sys.argv[0]
Addon.plugin_handle = int(sys.argv[1])
Addon.plugin_queries = Addon.parse_query(sys.argv[2][1:])

dlg = xbmcgui.Dialog()

Addon.log('plugin url: ' + Addon.plugin_url)
Addon.log('plugin queries: ' + str(Addon.plugin_queries))
Addon.log('plugin handle: ' + str(Addon.plugin_handle)) 

mode = Addon.plugin_queries['mode']

quality = int(Addon.get_setting('quality'))

if mode == 'main':
    channels = tvtime.TVtime().get_channels(quality)
    if channels:
        for c in channels:
            channel = c['channel'];
            rURL = "plugin://plugin.video.tvtime.tva/?channel=" + channel + "&mode=play&rand=" + Addon.random_generator()
            logo = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'logos', c['channel']+'.png'))
            title = c["title"].replace("&amp;", "&").replace('&quot;','"');
            title = title.replace("&amp;", "&");
            title = '%s - %s' % (Addon.cleanChannel(channel), title)
            cm_refresh = (Addon.get_string(40000), 
                      'XBMC.RunPlugin(%s/?mode=refresh)' % 
                           (Addon.plugin_url))
            cm_menu = [cm_refresh]
            if quality == 3 and channel != 'PBS' and channel != 'My9':
                quality_name = 'High';
            elif quality == 2 and channel != 'PBS' and channel != 'My9':
                quality_name = 'High';
            elif quality == 1 and channel != 'PBS' and channel != 'My9':
                quality_name = 'Medium';
            else:
                quality_name = 'Low';
            Addon.add_video_item(rURL,
                                 {'title': title},
                                 img=logo, playable=True, HD=quality_name, cm=cm_menu, cm_replace=False)
            xbmcplugin.setContent(Addon.plugin_handle, 'movie')

elif mode == 'refresh':
    xbmc.executebuiltin('Container.Refresh')

elif mode=='play':
    channel = Addon.plugin_queries['channel']
    Addon.log(channel)
    channels = []
    channels = tvtime.TVtime().get_link(quality)
    if channels:
        Addon.log(str(channels))
        for c in channels:
            if c['channel'] == channel:
                url = c['url']
                Addon.log(url)
                item = xbmcgui.ListItem(path=url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

Addon.end_of_directory()
