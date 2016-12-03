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

import re, os, sys, base64, random
import urlparse
import xbmcaddon, xbmcgui, xbmcplugin, xbmc
from resources.lib import ordereddict, client

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


def random_agent():

    BR_VERS = [['%s.0' % i for i in xrange(18, 43)],
               ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101',
                '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95',
                '39.0.2171.99', '40.0.2214.93', '40.0.2214.111', '40.0.2214.115',
                '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81',
                '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101',
                '45.0.2454.85', '46.0.2490.71', '46.0.2490.80', '46.0.2490.86',
                '47.0.2526.73', '47.0.2526.80'], ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))


# def opener(url, user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'):
#
#     req = urllib2.Request(url)
#     req.add_header('User-Agent', user_agent)
#     response = urllib2.urlopen(req)
#     result = response.read()
#     response.close()
#
#     return result


def ant1cy_resolver():

    return client.request('http://www.ant1iwo.com/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL=http://l2.cloudskep.com/antl2/abr/playlist.m3u8')


def constructor():

    compiled_list = []
    groups = []

    text = client.request('https://raw.githubusercontent.com/free-greek-iptv/greek-iptv/master/android.m3u')

    result = text.replace('\r\n', '\n')
    items = re.compile('group-title="(.*?)".*?tvg-logo="(.*?)",(.*?)$\n(.*?)$', re.U + re.M).findall(result)

    for group, icon, title, url in items:

        title = title.strip()

        if title == 'ANT1 CY':
            url = ant1cy_resolver()

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
