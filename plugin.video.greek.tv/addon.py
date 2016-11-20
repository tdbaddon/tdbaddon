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

import re, os, sys, base64
import urlparse, urllib2, urllib
import xbmcaddon, xbmcgui, xbmcplugin, xbmc
from resources.lib import ordereddict

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
decode = base64.b64decode
addonmedia = join(addonpath, 'resources', 'media')

addon_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urlparse.parse_qsl(sys.argv[2][1:]))
action = params.get('action', None)


def opener(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    result = response.read()
    response.close()

    return result


def ant1cy_resolver():

    return opener('http://www.ant1iwo.com/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL=http://l2.cloudskep.com/antl2/abr/playlist.m3u8')


def constructor():

    compiled_list = []
    groups = []

    text = opener(decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2ZyZWUtZ3JlZWstaXB0di9ncmVlay1pcHR2L21hc3Rlci9hbmRyb2lkLm0zdQ=='))

    result = text.replace('\r\n', '\n')
    items = re.compile('group-title="(.*?)".*?tvg-logo="(.*?)",(.*?)$\n(.*?)$', re.U + re.M).findall(result)

    for group, icon, title, url in items:

        title = title.strip()

        if title == 'ANT1 CY':
            url = ant1cy_resolver() + '|User-Agent=' + urllib.quote_plus('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

        item_data = ({'title': title, 'icon': icon, 'group': group.decode('utf-8'), 'url': url})
        compiled_list.append(item_data)
        groups.append(group.decode('utf-8'))

    trimmed_groups = list(ordereddict.OrderedDict.fromkeys(groups))

    alt_strings = ['BUP']

    compiled_list_no_bup = [item for item in compiled_list if not any(alt in item['title'] for alt in alt_strings)]

    if addon.getSetting('show-bup') == 'true':
        return compiled_list, trimmed_groups
    else:
        return compiled_list_no_bup, trimmed_groups


def switcher():

    groups = [localisedstr(30016)] + constructor()[1]

    choices = dialog.select(heading=localisedstr(30017), list=groups)

    if choices == 0:
        addon.setSetting('group', 'ΟΛΑ'.decode('utf-8'))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 1:
        addon.setSetting('group', (groups.pop(1)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 2:
        addon.setSetting('group', (groups.pop(2)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 3:
        addon.setSetting('group', (groups.pop(3)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 4:
        addon.setSetting('group', (groups.pop(4)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 5:
        addon.setSetting('group', (groups.pop(5)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 6:
        addon.setSetting('group', (groups.pop(6)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 7:
        addon.setSetting('group', (groups.pop(7)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 8:
        addon.setSetting('group', (groups.pop(8)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 9:
        addon.setSetting('group', (groups.pop(9)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 10:
        addon.setSetting('group', (groups.pop(10)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 11:
        addon.setSetting('group', (groups.pop(11)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 12:
        addon.setSetting('group', (groups.pop(12)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 13:
        addon.setSetting('group', (groups.pop(13)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 14:
        addon.setSetting('group', (groups.pop(14)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 15:
        addon.setSetting('group', (groups.pop(15)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 16:
        addon.setSetting('group', (groups.pop(16)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 17:
        addon.setSetting('group', (groups.pop(17)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 18:
        addon.setSetting('group', (groups.pop(18)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 19:
        addon.setSetting('group', (groups.pop(19)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 20:
        addon.setSetting('group', (groups.pop(20)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 21:
        addon.setSetting('group', (groups.pop(21)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 22:
        addon.setSetting('group', (groups.pop(22)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 23:
        addon.setSetting('group', (groups.pop(23)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 24:
        addon.setSetting('group', (groups.pop(24)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 25:
        addon.setSetting('group', (groups.pop(25)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 26:
        addon.setSetting('group', (groups.pop(26)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 27:
        addon.setSetting('group', (groups.pop(27)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 28:
        addon.setSetting('group', (groups.pop(28)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 29:
        addon.setSetting('group', (groups.pop(29)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 30:
        addon.setSetting('group', (groups.pop(30)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 31:
        addon.setSetting('group', (groups.pop(31)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 32:
        addon.setSetting('group', (groups.pop(32)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 33:
        addon.setSetting('group', (groups.pop(33)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 34:
        addon.setSetting('group', (groups.pop(34)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 35:
        addon.setSetting('group', (groups.pop(35)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 36:
        addon.setSetting('group', (groups.pop(36)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 37:
        addon.setSetting('group', (groups.pop(37)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 38:
        addon.setSetting('group', (groups.pop(38)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 39:
        addon.setSetting('group', (groups.pop(39)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 40:
        addon.setSetting('group', (groups.pop(40)))
        execute('Dialog.Close(busydialog)')
        execute('Container.Refresh')
    elif choices == 41:
        addon.setSetting('group', (groups.pop(41)))
        execute('Dialog.Close(busydialog)')
        execute('Container.Refresh')
    elif choices == 42:
        addon.setSetting('group', (groups.pop(42)))
        execute('Dialog.Close(busydialog)')
        execute('Container.Refresh')
    elif choices == 43:
        addon.setSetting('group', (groups.pop(43)))
        execute('Dialog.Close(busydialog)')
        execute('Container.Refresh')
    elif choices == 44:
        addon.setSetting('group', (groups.pop(44)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 45:
        addon.setSetting('group', (groups.pop(45)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 46:
        addon.setSetting('group', (groups.pop(46)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 47:
        addon.setSetting('group', (groups.pop(47)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 48:
        addon.setSetting('group', (groups.pop(48)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 49:
        addon.setSetting('group', (groups.pop(49)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 50:
        addon.setSetting('group', (groups.pop(50)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 51:
        addon.setSetting('group', (groups.pop(51)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 52:
        addon.setSetting('group', (groups.pop(52)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 53:
        addon.setSetting('group', (groups.pop(53)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 54:
        addon.setSetting('group', (groups.pop(54)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 55:
        addon.setSetting('group', (groups.pop(55)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 56:
        addon.setSetting('group', (groups.pop(56)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 55:
        addon.setSetting('group', (groups.pop(57)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 58:
        addon.setSetting('group', (groups.pop(58)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 59:
        addon.setSetting('group', (groups.pop(59)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 60:
        addon.setSetting('group', (groups.pop(60)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 61:
        addon.setSetting('group', (groups.pop(61)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 62:
        addon.setSetting('group', (groups.pop(62)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 63:
        addon.setSetting('group', (groups.pop(63)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 64:
        addon.setSetting('group', (groups.pop(64)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 65:
        addon.setSetting('group', (groups.pop(65)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 66:
        addon.setSetting('group', (groups.pop(66)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 67:
        addon.setSetting('group', (groups.pop(67)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 68:
        addon.setSetting('group', (groups.pop(68)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 69:
        addon.setSetting('group', (groups.pop(69)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 70:
        addon.setSetting('group', (groups.pop(70)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 71:
        addon.setSetting('group', (groups.pop(71)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 72:
        addon.setSetting('group', (groups.pop(72)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 73:
        addon.setSetting('group', (groups.pop(73)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 74:
        addon.setSetting('group', (groups.pop(74)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
        execute('Container.Refresh')
    elif choices == 75:
        addon.setSetting('group', (groups.pop(75)))
        execute('Dialog.Close(busydialog)')
        xbmc.sleep(500)
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
            'title': localisedstr(30015).format(localisedstr(30016) if addon.getSetting('group') == 'ΟΛΑ'.decode('utf-8') else addon.getSetting('group').decode('utf-8')),
            'icon': join(addonmedia, 'switcher.png'),
            'url': '{0}?action={1}'.format(addon_url, 'switcher')
        }
    ]

    null = [
        {
            'title': localisedstr(30013),
            'icon': join(addonmedia, 'null.png'),
            'url': addon_url
        }
    ]

    try:
        if not constructor()[0] == []:
            filtered = [item for item in constructor()[0] if any(item['group'] == selected for selected in [addon.getSetting('group').decode('utf-8')])] if not addon.getSetting('group') == 'ΟΛΑ' else constructor()[0]
            items = root_menu + filtered
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
        if item['url'].endswith(('switcher','settings')):
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
