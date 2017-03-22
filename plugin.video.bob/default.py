# -*- coding: utf-8 -*-

"""
    Bob Add-on

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

import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import koding

koding.User_Info()

ADDON_ID = 'plugin.video.bob'
HOME = xbmc.translatePath('special://home')
ADDON_DATA = xbmc.translatePath('special://profile/addon_data')
ADDONS = os.path.join(HOME, 'addons')
BOB_DATA = os.path.join(ADDON_DATA, ADDON_ID)
BOB_COOKIE = os.path.join(BOB_DATA, 'cookies')

if 'credits' in sys.argv[0]:
    try:
        f = xbmcvfs.File('special://home/addons/plugin.video.bob/credits.txt')
        text = f.read();
        f.close()
        if xbmc.getInfoLabel('System.ProfileName') != "Master user":
            you = xbmc.getInfoLabel('System.ProfileName')
        elif xbmc.getCondVisibility('System.Platform.Windows') == True or xbmc.getCondVisibility(
                'System.Platform.OSX') == True:
            if "Users\\" in HOME:
                proyou = str(HOME).split("Users\\")
                preyou = str(proyou[1]).split("\\")
                you = preyou[0]
            else:
                you = "You"
        else:
            you = "You"
        if you: newcredits = text + "\r\n\r\n\r\nSpecial thanks to:\r\n\r\n" + you + " for trying our new addon.\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nDo not be alarmed. \r\nNo personal data was gathered or stored in anyway.\r\nWe just used kodi's profile name or your OSX/Windows user-foldername to personalize this message on the fly..."
        label = '%s - %s' % (xbmc.getLocalizedString(470), xbmcaddon.Addon().getAddonInfo('name'))
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(100)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                win.getControl(1).setLabel(label)
                win.getControl(5).setText(newcredits)
                retry = 0
            except:
                retry -= 1
    except:
        pass

if not os.path.exists(BOB_DATA):
    os.makedirs(BOB_DATA)
    try:
        f = xbmcvfs.File(xbmcaddon.Addon().getAddonInfo('changelog'))
        text = f.read();
        f.close()
        label = '%s - %s' % (xbmc.getLocalizedString(24054), xbmcaddon.Addon().getAddonInfo('name'))
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(100)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                win.getControl(1).setLabel(label)
                win.getControl(5).setText(text)
                retry = 0
            except:
                retry -= 1
    except:
        pass

if not os.path.exists(BOB_COOKIE):
    os.makedirs(BOB_COOKIE)

import sys
import urlparse
import __builtin__

__builtin__.BOB_BASE_DOMAIN = str(koding.Check_Cookie('base'))

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
try:
    action = params['action']
except:
    action = None
try:
    content = params['content']
except:
    content = None
try:
    name = params['name']
except:
    name = None
try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    fanart = params['fanart']
except:
    fanart = None

try:
    uncached = params['uncached']
    if uncached == "true":
        uncached = True
    else:
        uncached = False
except:
    uncached = False

if action is None:
    xbmc.log('### user info initiated')
    from resources.lib.indexers import bob
    bob.Indexer().root()
elif action == 'directory':
    from resources.lib.indexers import bob
    bob.Indexer().get(url, uncached=uncached)
elif action == 'uncached':
    xbmc.executebuiltin('Container.Update(%s%s)' % (
    sys.argv[0], sys.argv[2].replace("action=uncached", "action=directory&uncached=true")))
elif action == 'get_all_episodes':
    from resources.lib.indexers import bob;

    bob.Indexer().get_all_episodes(url)
elif action == 'xdirectory':
    from resources.lib.indexers import bob;

    bob.Indexer().getx(url)
elif action == 'developer':
    from resources.lib.indexers import bob;

    bob.Indexer().developer()
elif action == 'play':
    from resources.lib.indexers import bob;

    bob.Player().play(url, content)
elif action == 'browser':
    from resources.lib.indexers import bob;

    bob.Resolver().browser(url)
elif action == 'search':
    from resources.lib.indexers import bob;

    bob.Indexer().search()
elif action == 'add_search':
    from resources.lib.indexers import bob;

    bob.Indexer().add_search(url)
elif action == 'delete_search':
    from resources.lib.indexers import bob;

    bob.Indexer().delete_search()
elif action == 'openSettings':
    from resources.lib.modules import control;

    control.openSettings()
elif action == 'addView':
    from resources.lib.modules import views;

    views.addView(content)
elif action == 'clearCache':
    from resources.lib.modules import cache;

    cache.clear()
elif action == 'trailer':
    from resources.lib.modules import trailer;

    trailer.trailer().play(name)
elif action == 'ScraperSettings':
    from resources.lib.modules import control

    control.openSettings(id='script.module.nanscrapers')
elif action == 'ResolverSettings':
    from resources.lib.modules import control

    control.openSettings(id='script.mrknow.urlresolver')
elif action == 'queueItem':
    from resources.lib.modules import control
    from resources.lib.indexers.bob import Resolver, Indexer, replace_url

    item_urls = []
    selected_link = None
    play_now = False
    already_played = False
    if not url.endswith(".xml"):
        item_urls.append({'url': url, 'name': name, 'image': image})
    else:
        if control.yesnoDialog('Select the quality to queue', '', '', yeslabel='HD', nolabel='SD'):
            selected_link = "HD"
        else:
            selected_link = "SD"
        indexer = Indexer()
        indexer.bob_list(replace_url(url))
        indexer.worker()
        list = indexer.list
        try:
            for item in list:
                if item['name'] == 'All Episodes':
                    continue
                if control.setting("include_watched_queue") == "false":
                    if "playcount" in item and int(item["playcount"]) >= 1:
                        continue
                if item['url'].endswith(".xml"):  # queueing tv show so need to get sublists
                    indexer.list = []
                    indexer.bob_list(replace_url(item['url']))
                    indexer.worker()
                    sublist = indexer.list
                    for subitem in sublist:
                        if control.setting("include_watched_queue") == "false":
                            if "playcount" in subitem and int(subitem["playcount"]) >= 1:
                                continue
                        if subitem['name'] == 'All Episodes':
                            continue
                        if not subitem['url'].endswith(".xml"):
                            item_urls.append(
                                {'url': subitem['url'], 'name': subitem['name'], 'image': subitem['poster']})
                else:
                    item_urls.append({'url': item['url'], 'name': item['name'], 'image': item['poster']})
        except:
            pass
    for item_url in item_urls:
        retrying = False
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        if playlist.size() > 0 and control.setting("background_list_queue") == "true" and len(item_urls) > 1:
            hide_progress = True
        else:
            hide_progress = False
        while True:
            if not hide_progress:
                control.execute('ActivateWindow(busydialog)')
            if retrying:
                resolved = Resolver().process(Resolver().get(item_url['url']), name=item_url['name'],
                                              hide_progress=hide_progress)
            else:
                link = Resolver().get(item_url['url'], link=selected_link)
                resolved = Resolver().process(link, name=item_url['name'], hide_progress=hide_progress)
            if not hide_progress:
                control.execute('Dialog.Close(busydialog)')
            if resolved:
                if playlist.size() == 0 and len(item_urls) > 1: play_now = True
                item = control.item(label=item_url['name'], iconImage=item_url['image'],
                                    thumbnailImage=item_url['image'])
                playlist.add(resolved, item)
                if play_now and not already_played and control.setting("background_list_queue") == "true":
                    play_now = False
                    already_played = True
                    control.player.play(playlist, item)
                    control.resolve(int(sys.argv[1]), True, item)
                break
            else:
                if not control.yesnoDialog(control.lang(30705).encode('utf-8'),
                                           "Would you like to try another stream?", ''):
                    break
                retrying = True
    xbmc.executebuiltin('Container.Refresh')
elif action == 'playQueue':
    from resources.lib.modules import control
    from resources.lib.indexers import bob

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    if playlist.size() > 0:
        item = playlist[0]
        control.player.play(playlist, item)
        control.resolve(int(sys.argv[1]), True, item)
    else:
        control.infoDialog("Queue is empty".encode('utf-8'))
elif action == 'clearQueue':
    from resources.lib.modules import control

    xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
    control.infoDialog("Queue cleared".encode('utf-8'))
    xbmc.executebuiltin('Container.Refresh')
elif action == "addToFavorites":
    from resources.lib.modules import favs

    fav_type = params['type']
    fav_link = params['link']
    fav_poster = params['poster']
    fav_fanart = params['fanart']
    result = favs.add_favorite(name, fav_type, fav_link, fav_poster, fav_fanart)
elif action == "removeFromFavorites":
    from resources.lib.modules import favs

    fav_type = params['type']
    fav_link = params['link']
    result = favs.remove_favorite(name, fav_type, fav_link)
    xbmc.executebuiltin("Container.Refresh")
elif action == "MoveFavorite":
    from resources.lib.modules import favs

    fav_type = params['type']
    fav_link = params['link']
    result = favs.move_favorite(name, fav_type, fav_link)
    xbmc.executebuiltin("Container.Refresh")
elif action == "getfavorites":
    from resources.lib.modules import favs

    favs.get_favorites_menu(url)
elif action.startswith("getfavorites_"):
    type = action.replace("getfavorites_", "")
    from resources.lib.modules import favs

    favs.get_favorites(type, url)
elif action == "markwatched":
    from resources.lib.modules import metacache
    from resources.lib.modules import control

    imdb = params["imdb"]
    tmdb = params["tmdb"]
    tvdb = params["tvdb"]
    season = params["season"]
    episode = params["episode"]
    mark_unwatched = params["unwatched"]
    content = params["content"]
    if mark_unwatched == "False":
        mark_unwatched = False
    else:
        mark_unwatched = True
    if content == "episode":
        metacache.episodes_set_watched(imdb, tmdb, tvdb, season, episode, mark_unwatched)
    elif content == "movie":
        metacache.movies_set_watched(imdb, tmdb, tvdb, mark_unwatched)
    control.refresh()
