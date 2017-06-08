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
from resources.lib.modules import debrid

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database


class sources:
    @staticmethod
    def getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, timeout=30,
                   progress=True, preset="search", dialog=None, exclude=None, scraper_title=False, queueing=False):

        year = str(year)
        content = 'movie' if tvshowtitle == None else 'episode'
        allow_debrid = control.setting('allow_debrid') == "true"

        if content == 'movie':
            title = cleantitle.normalize(title)
            links_scraper = nanscrapers.scrape_movie(title, year, imdb, timeout=timeout, exclude=exclude,
                                                     enable_debrid=allow_debrid)
        elif content == 'episode':
            if scraper_title:
                tvshowtitle = title
            tvshowtitle = cleantitle.normalize(tvshowtitle)
            links_scraper = nanscrapers.scrape_episode(tvshowtitle, year, premiered, season, episode, imdb, tvdb,
                                                       timeout=timeout, exclude=exclude, enable_debrid=allow_debrid)
        else:
            return

        if not queueing and control.setting('use_link_dialog') == 'true':
            if control.setting('check_url') == "true":
                check_url = True
            else:
                check_url = False
            if content == 'movie':
                link, items = nanscrapers.scrape_movie_with_dialog(title, year, imdb, timeout=timeout, exclude=exclude,
                                                                   sort_function=sources.sort_function,
                                                                   check_url=check_url, extended=True,
                                                                   enable_debrid=allow_debrid)
            elif content == "episode":
                link, items = nanscrapers.scrape_episode_with_dialog(tvshowtitle, year, premiered, season, episode,
                                                                     imdb, tvdb,
                                                                     timeout=timeout, exclude=exclude,
                                                                     sort_function=sources.sort_function,
                                                                     check_url=check_url, extended=True,
                                                                     enable_debrid=allow_debrid)
            else:
                return

            if link is None:
                return False

            if type(link) == dict and "path" in link:
                link = link["path"]
            url = link['url']
            if allow_debrid:
                new_url = debrid.resolve(url)
                if new_url:
                    url = new_url
            import urlresolver9
            try:
                hmf = urlresolver9.HostedMediaFile(url=url, include_disabled=False,
                                                   include_universal=allow_debrid)
                if hmf.valid_url() == True:
                    resolved_url = hmf.resolve()
                else:
                    resolved_url = url
            except:
                resolved_url = None

            if resolved_url and sources().check_playable(resolved_url) is not None:
                url = resolved_url
            else:
                if control.setting('link_fallthtough') == 'true':
                    try:
                        links = []
                        for item in items:
                            if type(item) == dict and "path" in item:
                                links.extend(item["path"][1])
                            else:
                                links.extend(item[1])
                        index = links.index(link)
                        links = links[index + 1:]
                        for link in links:
                            try:
                                hmf = urlresolver9.HostedMediaFile(url=link["url"], include_disabled=False,
                                                                   include_universal=allow_debrid)
                                if hmf.valid_url() == True:
                                    resolved_url = hmf.resolve()
                                else:
                                    resolved_url = None
                            except:
                                resolved_url = None

                            if resolved_url and sources().check_playable(resolved_url) is not None:
                                url = resolved_url
                                return url
                        url = None
                    except:
                        pass
                else:
                    url = None
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

                    if allow_debrid:
                        new_url = debrid.resolve(scraper_link['url'])
                        if new_url:
                            scraper_link['url'] = new_url

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
                                if scraper_link["direct"]:
                                    sd_links.append(scraper_link)
                                else:
                                    sd_non_direct.append(scraper_link)
                                continue
                        except:
                            if scraper_link['quality'] in ["SD", "CAM", "SCR"]:
                                if scraper_link["direct"]:
                                    sd_links.append(scraper_link)
                                else:
                                    sd_non_direct.append(scraper_link)
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
    def getMusicSources(title, artist, timeout=30, progress=True, preset="search", dialog=None, exclude=None,
                        queueing=False):
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
        if 'quality' in item[1][0]:
            quality = item[1][0]["quality"]
        else:
            quality = item[1][0]["path"]["quality"]
        if quality.startswith("1080"): quality = "HDa"
        if quality.startswith("720"): quality = "HDb"
        if quality.startswith("560"): quality = "HDc"
        if quality == "HD": quality = "HDd"
        if quality.startswith("480"): quality = "SDa"
        if quality.startswith("360"): quality = "SDb"
        if quality.startswith("SD"): quality = "SDc"
        return quality

    @staticmethod
    def format_function(scraper_array):
        results_array = []
        if scraper_array:
            labels = {}
            for link in scraper_array:
                quality = ""
                try:
                    quality = str(int(link['quality'])) + "p"
                except:
                    quality = link['quality']
                if link.get("debridonly", ""):
                    label = link["source"] + " (debrid) " + link["scraper"] + " (" + quality + ")"
                else:
                    label = link["source"] + " " + link["scraper"] + " (" + quality + ")"
                results_array.append((label, [link]))
            return results_array
