# -*- coding: utf-8 -*-

'''
    Bob Add-on
    Copyright (C) 2016 Bob

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

import random
import urllib

import nanscrapers
import urlparse
import xbmc

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database


class sources:
    @staticmethod
    def getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, timeout=30,
                   progress=True, preset="search", dialog=None, exclude=None, scraper_title=False):

        year = str(year)

        content = 'movie' if tvshowtitle == None else 'episode'

        if content == 'movie':
            title = cleantitle.normalize(title)
            links_scraper = nanscrapers.scrape_movie(title, year, imdb, timeout=timeout, exclude=exclude)
        elif content == 'episode':
            if scraper_title:
                tvshowtitle = title
            tvshowtitle = cleantitle.normalize(tvshowtitle)
            links_scraper = nanscrapers.scrape_episode(tvshowtitle, year, premiered, season, episode, imdb, tvdb,
                                                       timeout=timeout, exclude=exclude)
        else:
            return

        allow_debrid = bool(control.setting('allow_debrid'))

        if control.setting('use_link_dialog') == 'true':
            if content == 'movie':
                link = nanscrapers.scrape_movie_with_dialog(title, year, imdb, timeout=timeout, exclude=exclude, sort_function=sources.sort_function)
            elif content == "episode":
                link = nanscrapers.scrape_episode_with_dialog(tvshowtitle, year, premiered, season, episode, imdb, tvdb,
                                                       timeout=timeout, exclude=exclude, sort_function=sources.sort_function)
            else:
                return

            url = link['url']
            import urlresolver9
            hmf = urlresolver9.HostedMediaFile(url=url, include_disabled=False,
                                               include_universal=allow_debrid)
            if hmf.valid_url() == True:
                resolved_url = hmf.resolve()
            else:
                resolved_url = None
            if resolved_url and sources().check_playable(resolved_url) is not None:
                url = resolved_url
            return url




        sd_links = []
        non_direct = []
        sd_non_direct = []
        links_scraper = links_scraper()
        for scraper_links in links_scraper:
            if scraper_links is not None:
                random.shuffle(scraper_links)
                for scraper_link in scraper_links:
                    if dialog is not None and dialog.iscanceled():
                        return

                    if (not control.setting('allow_openload') == 'true' and 'openload' in scraper_link['url']) or (
                                not control.setting('allow_the_video_me') == 'true' and 'thevideo.me' in scraper_link[
                                'url']):
                        continue
                    if preset.lower() == 'searchsd':
                        try:
                            quality = int(scraper_link['quality'])
                            if quality > 576:
                                continue
                        except:
                            if scraper_link['quality'] not in ["SD", "CAM", "SCR"]:
                                continue
                    elif preset.lower() == 'search':
                        try:
                            quality = int(scraper_link['quality'])
                            if quality <= 576:
                                sd_links.append(scraper_link)
                                continue
                        except:
                            if scraper_link['quality'] in ["SD", "CAM", "SCR"]:
                                sd_links.append(scraper_link)
                                continue

                    if "m4u" in scraper_link['url']:
                        if sources().check_playable(scraper_link['url']) is not None:
                            return scraper_link['url']

                    else:
                        try:
                            if scraper_link['direct']:
                                import urlresolver9
                                hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                                   include_universal=allow_debrid)
                                if hmf.valid_url() == True: resolved_url = hmf.resolve()
                                # resolved_url = urlresolver9.resolve(scraper_link['url'])
                                if resolved_url and sources().check_playable(resolved_url) is not None:
                                    url = resolved_url
                                    return url
                                else:
                                    if sources().check_playable(scraper_link['url']):
                                        return scraper_link['url']
                            else:
                                non_direct.append(scraper_link)
                        except:
                            if scraper_link['direct']:
                                url = scraper_link['url']
                                if sources().check_playable(url) is not None:
                                    return url
                            else:
                                non_direct.append(scraper_link)

        for scraper_link in non_direct:
            if dialog is not None and dialog.iscanceled():
                return

            if (not control.setting('allow_openload') == 'true' and 'openload' in scraper_link['url']) or (
                        not control.setting('allow_the_video_me') == 'true' and 'thevideo.me' in scraper_link[
                        'url']):
                continue
            if preset.lower() == 'searchsd':
                try:
                    quality = int(scraper_link['quality'])
                    if quality > 576:
                        continue
                except:
                    if scraper_link['quality'] not in ["SD", "CAM", "SCR"]:
                        continue
            elif preset.lower() == 'search':
                try:
                    quality = int(scraper_link['quality'])
                    if quality <= 576:
                        sd_non_direct.append(scraper_link)
                        continue
                except:
                    if scraper_link['quality'] in ["SD", "CAM", "SCR"]:
                        sd_non_direct.append(scraper_link)
                        continue

            try:
                hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                   include_universal=allow_debrid)
                if hmf.valid_url() == True: resolved_url = hmf.resolve()
                # resolved_url = urlresolver9.resolve(scraper_link['url'])
            except:
                continue
            if resolved_url and (
                        resolved_url.startswith("plugin://") or sources().check_playable(resolved_url) is not None):
                url = resolved_url
                return url

        for scraper_link in sd_links:

            if dialog is not None and dialog.iscanceled():
                return

            if "m4u" in scraper_link['url']:
                return scraper_link['url']

            else:
                try:
                    if scraper_link['direct']:
                        import urlresolver9
                        hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                           include_universal=allow_debrid)
                        if hmf.valid_url() == True: resolved_url = hmf.resolve()
                        # resolved_url = urlresolver9.resolve(scraper_link['url'])
                        if resolved_url and sources().check_playable(resolved_url) is not None:
                            url = resolved_url
                            return url
                        else:
                            if sources().check_playable(scraper_link['url']):
                                return scraper_link['url']
                    else:
                        non_direct.append(scraper_link)
                except:
                    if scraper_link['direct']:
                        url = scraper_link['url']
                        if sources().check_playable(url) is not None:
                            return url
                    else:
                        non_direct.append(scraper_link)

        try:
            import urlresolver9
        except:
            control.dialog.ok("Dependency missing",
                              "please install script.mrknow.urlresolver to resolve non-direct links")
            return

        for scraper_link in sd_non_direct:
            if dialog is not None and dialog.iscanceled():
                return

            try:
                hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                   include_universal=allow_debrid)
                if hmf.valid_url() == True: resolved_url = hmf.resolve()
                # resolved_url = urlresolver9.resolve(scraper_link['url'])
            except:
                continue
            if resolved_url and (
                        resolved_url.startswith("plugin://") or sources().check_playable(resolved_url) is not None):
                url = resolved_url
                return url

    @staticmethod
    def getMusicSources(title, artist, timeout=30, progress=True, preset="search", dialog=None, exclude=None):
        title = cleantitle.normalize(title)
        links_scraper = nanscrapers.scrape_song(title, artist, timeout=timeout, exclude=exclude)

        sd_links = []
        non_direct = []
        sd_non_direct = []
        allow_debrid = bool(control.setting('allow_debrid'))

        for scraper_links in links_scraper():
            if scraper_links is not None:
                random.shuffle(scraper_links)
                for scraper_link in scraper_links:
                    if dialog is not None and dialog.iscanceled():
                        return

                    if (not control.setting('allow_openload') == 'true' and 'openload' in scraper_link['url']) or (
                                not control.setting('allow_the_video_me') == 'true' and 'thevideo.me' in scraper_link[
                                'url']):
                        continue
                    if preset.lower() == 'searchsd':
                        if scraper_link['quality'] not in ["SD"]:
                            continue
                    elif preset.lower() == 'search':
                        if scraper_link['quality'] in ["SD"]:
                            sd_links.append(scraper_link)
                            continue

                    if scraper_link['direct']:
                        url = scraper_link['url']
                        if sources().check_playable(url) is not None:
                            return url
                        else:
                            non_direct.append(scraper_link)

                for scraper_link in sd_links:
                    if dialog is not None and dialog.iscanceled():
                        return
                    if scraper_link['direct']:
                        url = scraper_link['url']
                        if sources().check_playable(url) is not None:
                            return url
                        else:
                            non_direct.append(scraper_link)

                try:
                    import urlresolver9
                except:
                    control.dialog.ok("Dependency missing",
                                      "please install script.mrknow.urlresolver to resolve non-direct links")
                    return

                for scraper_link in non_direct:
                    if dialog is not None and dialog.iscanceled():
                        return

                    if preset.lower() == 'searchsd':
                        if scraper_link['quality'] not in ["SD"]:
                            continue
                    elif preset.lower() == 'search':
                        if scraper_link['quality'] in ["SD"]:
                            sd_non_direct.append(scraper_link)
                            continue
                    try:
                        hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                           include_universal=allow_debrid)
                        if hmf.valid_url() == True: resolved_url = hmf.resolve()
                        # resolved_url = urlresolver9.resolve(scraper_link['url'])
                    except:
                        continue
                    if resolved_url and (
                                resolved_url.startswith("plugin://") or sources().check_playable(
                                resolved_url) is not None):
                        url = resolved_url
                        return url

                for scraper_link in sd_non_direct:
                    if dialog is not None and dialog.iscanceled():
                        return

                    try:
                        hmf = urlresolver9.HostedMediaFile(url=scraper_link['url'], include_disabled=False,
                                                           include_universal=allow_debrid)
                        if hmf.valid_url() == True: resolved_url = hmf.resolve()
                        # resolved_url = urlresolver9.resolve(scraper_link['url'])
                    except:
                        continue
                    if resolved_url and (
                                resolved_url.startswith("plugin://") or sources().check_playable(
                                resolved_url) is not None):
                        url = resolved_url
                        return url

    @staticmethod
    def direct_resolve(url):
        try:
            import urlresolver9
        except:
            control.dialog.ok("Dependency missing",
                              "please install script.mrknow.urlresolver to resolve non-direct links")
        try:
            allow_debrid = bool(control.setting('allow_debrid'))
            hmf = urlresolver9.HostedMediaFile(url=url, include_disabled=False,
                                               include_universal=allow_debrid)
            if hmf.valid_url() == True: resolved_url = hmf.resolve()
            # resolved_url = urlresolver9.resolve(url)
            if resolved_url and sources().check_playable(resolved_url) is not None:
                return resolved_url
        except:
            return False

    @staticmethod
    def check_playable(url):
        try:
            headers = url.rsplit('|', 1)[1]
        except:
            headers = ''
        headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
        headers = dict(urlparse.parse_qsl(headers))

        result = None

        if url.startswith('http') and '.m3u8' in url:
            result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout=5)
            if result == None: return None

        elif url.startswith('http'):
            result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout=5)
            if result == None: return None

        return result

    @staticmethod
    def sort_function(item):
        quality = item[1][0]["quality"]
        if quality == "1080": quality = "HDa"
        if quality == "720": quality = "HDb"
        if quality == "560": quality = "HDc"
        if quality == "HD": quality = "HDd"
        if quality == "480": quality = "SDa"
        if quality == "360": quality = "SDb"
        if quality == "SD": quality = "SDc"

        return quality

    @staticmethod
    def get_vk_token():
        import xbmcgui
        import xbmcaddon
        from resources.lib.modules import vkAuth

        if not bool(control.setting("enable_vk")):
            return False

        # flag if a vk.com token is valid
        validVKToken = False

        # if empty vk.com email xor password
        if bool(control.setting('vk_email') == "") ^ bool(control.setting('vk_password') == ""):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok("VK", "Please enter your VK.com credentials")
            control.setSetting('vk_token', '')
            xbmcaddon.Addon().openSettings()
            return False
            # if empty vk.com email and password
        elif control.setting('vk_email') == "" and control.setting('vk_password') == "":
            control.setSetting('vk_token_email', '')
            control.setSetting('vk_token_password', '')
            control.setSetting('vk_token', '')
            # display vk.com account need message
            dialog = xbmcgui.Dialog()
            ok = dialog.ok("VK", "Please Enter your VK.com credentials")
            xbmcaddon.Addon().openSettings()
            return False
        # if credentials are given
        else:
            # check if user changed vk_email/vk_password or if vk_token_email/vk_token_password is empty (need reauth)
            if control.setting('vk_token_email') != control.setting('vk_email') or control.setting(
                    'vk_token_password') != control.setting('vk_password'):
                control.setSetting('vk_token_email', '')
                control.setSetting('vk_token_password', '')
                control.setSetting('vk_token', '')
            # check current token
            if control.setting('vk_token'): validVKToken = vkAuth.isTokenValid(control.setting('vk_token'))
            # if the token provided is not valid, login and generate a new one
            if validVKToken != True:
                # login in vk.com - get the token
                email = control.setting('vk_email')
                passw = control.setting('vk_password')
                try:
                    token = vkAuth.auth(email, passw, 2648691, 'audio,offline,video')
                except:
                    token = False
                # check login status
                if token == False:
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok("VK Log in Failed", "Please enter your VK.com credentials")
                    xbmcaddon.Addon().openSettings()
                    return False
                else:
                    # test the new token
                    validVKToken = vkAuth.isTokenValid(token)
                    # if there was an error, inform the user
                    if validVKToken != True:
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("VK Log in Failed", "Reason" + validVKToken)
                        xbmcaddon.Addon().openSettings()
                        return False
                    else:
                        control.setSetting('vk_token_email', email)
                        control.setSetting('vk_token_password', passw)
                        control.setSetting('vk_token', token)
                        return token
            else:
                return control.setting('vk_token')
