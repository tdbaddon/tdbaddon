# -*- coding: utf-8 -*-

"""
    Greek TV Add-on
    Author: Thgiliwt

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
"""

import re, os, sys, random
import urlparse
import xbmcaddon, xbmcgui, xbmcplugin, xbmc
from resources.lib import ordereddict, client, thgiliwt

addon = xbmcaddon.Addon()
localisedstr = addon.getLocalizedString
addonname = addon.getAddonInfo("name")
addonpath = addon.getAddonInfo("path").decode('utf-8')
addonfanart = addon.getAddonInfo("fanart")
addonicon = addon.getAddonInfo("icon")
addonid = addon.getAddonInfo("id")

dialog = xbmcgui.Dialog()

addDirItems = xbmcplugin.addDirectoryItems
addDirItem = xbmcplugin.addDirectoryItem
endDir = xbmcplugin.endOfDirectory

execute = xbmc.executebuiltin

join = os.path.join
addonmedia = join(addonpath, 'resources', 'media')

addon_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urlparse.parse_qsl(sys.argv[2][1:]))
action = params.get('action', None)


def constructor():

    compiled_list = []
    groups = []

    text = client.request(thgiliwt.thgiliwt('==Qdz0mLkl2byRmbh9SbvNmLkFWbtgnL2R3LvoDc0RHa'))

    result = text.replace('\r\n', '\n')
    items = re.compile('group-title="(.*?)".*?tvg-logo="(.*?)",(.*?)$\n(.*?)$', re.U + re.M).findall(result)

    for group, icon, title, url in items:

        title = title.strip()

        item_data = ({'title': title, 'icon': icon, 'group': group.decode('utf-8'), 'url': url})
        compiled_list.append(item_data)
        groups.append(group.decode('utf-8'))

    trimmed_groups = list(ordereddict.OrderedDict.fromkeys(groups))

    alt_strings = [' BUP']

    no_bup = [item for item in compiled_list if not any(alt in item['title'] for alt in alt_strings)]

    if addon.getSetting('show-bup') == 'true':
        return compiled_list, trimmed_groups
    else:
        return no_bup, trimmed_groups


def switcher():

    groups = [localisedstr(30016)] + constructor()[1]

    choices = dialog.select(heading=localisedstr(30017), list_=groups)

    if choices == 0:
        addon.setSetting('group', 'ΟΛΑ'.decode('utf-8'))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(50)
        execute('Container.Refresh')
    elif choices <= len(groups) and not choices == -1:
        addon.setSetting('group', (groups.pop(choices)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(50)
        execute('Container.Refresh')
    else:
        execute('Dialog.Close(busydialog)')
        dialog.notification(heading=addonname, message=localisedstr(30019), icon=addonicon, sound=False)


def list_items():

    item_list = []

    root_menu = [
        {
            'title': localisedstr(30011),
            'icon': join(addonmedia, 'settings.png'),
            'url': '{0}?action={1}'.format(addon_url, 'settings')
        }
        ,
        {
            'title': localisedstr(30015).format(localisedstr(30016) if addon.getSetting('group') == 'ΟΛΑ' else addon.getSetting('group').decode('utf-8')),
            'icon': join(addonmedia, 'switcher.png'),
            'url': '{0}?action={1}'.format(addon_url, 'switcher')
        }
    ]

    null = [
        {
            'title': localisedstr(30013),
            'icon': join(addonmedia, 'null.png'),
            'url': '{0}?action={1}'.format(addon_url, 'null')
        }
    ]

    try:
        if not constructor()[0] == []:
            filtered = [item for item in constructor()[0] if any(item['group'] == selected for selected in [addon.getSetting('group').decode('utf-8')])] if not addon.getSetting('group') == 'ΟΛΑ' else constructor()[0]
            items = root_menu + filtered
            if addon.getSetting('sort') == 'true':
                if addon.getSetting('method') == '0':
                    items = root_menu + sorted(items[2:], key=lambda k: k['group'].lower())
                elif addon.getSetting('method') == '1':
                    items = root_menu + sorted(items[2:], key=lambda k: k['title'].lower())
            else:
                pass
        else:
            items = root_menu + null
            del items[1]
    except ValueError:
        items = root_menu + null
        del items[1]

    for item in items:

        list_item = xbmcgui.ListItem(label=item['title'], iconImage=item['icon'])
        list_item.setInfo('video', {'title': item['title']})
        list_item.setArt({'thumb': item['icon'], 'fanart': addonfanart})
        list_item.setProperty('IsPlayable', 'true')
        list_item.addContextMenuItems([(localisedstr(30012), 'RunPlugin({0}?action=refresh)'.format(addon_url))])
        _url_ = '{0}?action=play&url={1}'.format(addon_url, item['url'])
        if item['url'].startswith('https://www.youtube.com/watch?v='):
            _url_ = item['url'].replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=')
        if item['url'].endswith(('switcher','settings','null')):
            list_item.setProperty('IsPlayable', 'false')
            _url_ = item['url']
        isFolder = False
        item_list.append((_url_, list_item, isFolder))

    addDirItems(handle=addon_handle, items=item_list)
    endDir(addon_handle, cacheToDisc=False)


def play_item(path):

    list_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=list_item)


if action is None:

    list_items()

elif action == 'play':

    play_item(params['url'])

elif action == 'settings':

    execute('Dialog.Close(busydialog)')
    addon.openSettings()

elif action == 'refresh':

    execute('Container.Refresh')

elif action == 'switcher':
    dialog.notification(heading=addonname, message=localisedstr(30020), time=1000, sound=False)
    execute('ActivateWindow(busydialog)')
    switcher()
