"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
from StringIO import StringIO
import abc
import cookielib
import datetime
import gzip
import os
import re
import threading
import time
import urllib
import urllib2
import urlparse

import xbmc
import xbmcgui

from salts_lib import cloudflare
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import Q_ORDER
from salts_lib.constants import SHORT_MONS
from salts_lib.constants import VIDEO_TYPES
from salts_lib.db_utils import DB_Connection
from salts_lib.kodi import i18n


BASE_URL = ''
CAPTCHA_BASE_URL = 'http://www.google.com/recaptcha/api'
COOKIEPATH = kodi.translate_path(kodi.get_profile())
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# Q_LIST = [item[0] for item in sorted(Q_ORDER.items(), key=lambda x:x[1])]
MAX_RESPONSE = 1024 * 1024 * 2

class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        log_utils.log('Stopping Redirect', log_utils.LOGDEBUG)
        return response

    https_response = http_response

abstractstaticmethod = abc.abstractmethod
class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)

DEFAULT_TIMEOUT = 30

class Scraper(object):
    __metaclass__ = abc.ABCMeta
    base_url = BASE_URL
    db_connection = None
    worker_id = None

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        pass

    @abstractclassmethod
    def provides(cls):
        """
        Must return a list/set/frozenset of VIDEO_TYPES that are supported by this scraper. Is a class method so that instances of the class
        don't have to be instantiated to determine they are not useful

        * Datatypes set or frozenset are preferred as existence checking is faster with sets
        """
        raise NotImplementedError

    @abstractclassmethod
    def get_name(cls):
        """
        Must return a string that is a name that will be used through out the UI and DB to refer to urls from this source
        Should be descriptive enough to be recognized but short enough to be presented in the UI
        """
        raise NotImplementedError

    @abc.abstractmethod
    def resolve_link(self, link):
        """
        Must return a string that is a urlresolver resolvable link given a link that this scraper supports

        link: a url fragment associated with this site that can be resolved to a hoster link

        * The purpose is many streaming sites provide the actual hoster link in a separate page from link
        on the video page.
        * This method is called for the user selected source before calling urlresolver on it.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def format_source_label(self, item):
        """
        Must return a string that is to be the label to be used for this source in the "Choose Source" dialog

        item: one element of the list that is returned from get_sources for this scraper
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_sources(self, video):
        """
        Must return a list of dictionaries that are potential link to hoster sites (or links to links to hoster sites)
        Each dictionary must contain elements of at least:
            * multi-part: True if this source is one part of a whole
            * class: a reference to an instance of the scraper itself
            * host: the hostname of the hoster
            * url: the url that is a link to a hoster, or a link to a page that this scraper can resolve to a link to a hoster
            * quality: one of the QUALITIES values, or None if unknown; users can sort sources by quality
            * views: count of the views from the site for this source or None is unknown; Users can sort sources by views
            * rating: a value between 0 and 100; 0 being worst, 100 the best, or None if unknown. Users can sort sources by rating.
            * direct: True if url is a direct link to a media file; False if not. If not present; assumption is direct
            * other keys are allowed as needed if they would be useful (e.g. for format_source_label)

        video is an object of type ScraperVideo:
            video_type: one of VIDEO_TYPES for whatever the sources should be for
            title: the title of the tv show or movie
            year: the year of the tv show or movie
            season: only present for tv shows; the season number of the video for which sources are requested
            episode: only present for tv shows; the episode number of the video for which sources are requested
            ep_title: only present for tv shows; the episode title if available
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_url(self, video):
        """
        Must return a url for the site this scraper is associated with that is related to this video.

        video is an object of type ScraperVideo:
            video_type: one of VIDEO_TYPES this url is for (e.g. EPISODE urls might be different than TVSHOW urls)
            title: the title of the tv show or movie
            year: the year of the tv show or movie
            season: only present for season or episode VIDEO_TYPES; the season number for the url being requested
            episode: only present for season or episode VIDEO_TYPES; the episode number for the url being requested
            ep_title: only present for tv shows; the episode title if available

        * Generally speaking, domain should not be included
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, video_type, title, year, season=''):
        """
        Must return a list of results returned from the site associated with this scraper when doing a search using the input parameters

        If it does return results, it must be a list of dictionaries. Each dictionary must contain at least the following:
            * title: title of the result
            * year: year of the result
            * url: a url fragment that is the url on the site associated with this scraper for this season result item

        video_type: one of the VIDEO_TYPES being searched for. Only tvshows and movies are expected generally
        title: the title being search for
        year: the year being search for
        season: the season being searched for (only required if video_type == VIDEO_TYPES.SEASON)

        * Method must be provided, but can raise NotImplementedError if search not available on the site
        """
        raise NotImplementedError

    @classmethod
    def get_settings(cls):
        """
        Returns a list of settings to be used for this scraper. Settings are automatically checked for updates every time scrapers are imported
        The list returned by each scraper is aggregated into a big settings.xml string, and then if it differs from the current settings xml in the Scrapers category
        the existing settings.xml fragment is removed and replaced by the new string
        """
        name = cls.get_name()
        return [
            '         <setting id="%s-enable" type="bool" label="%s %s" default="true" visible="true"/>' % (name, name, i18n('enabled')),
            '         <setting id="%s-base_url" type="text" label="    %s" default="%s" visible="eq(-1,true)"/>' % (name, i18n('base_url'), cls.base_url),
            '         <setting id="%s-sub_check" type="bool" label="    %s" default="true" visible="eq(-2,true)"/>' % (name, i18n('page_existence')),
            '         <setting id="%s_last_results" type="number" default="0" visible="false"/>' % (name),
        ]

    @classmethod
    def has_proxy(cls):
        return False
    
    def _default_get_url(self, video):
        url = None
        self.create_db_connection()
        if video.video_type == VIDEO_TYPES.EPISODE:
            if VIDEO_TYPES.TVSHOW in self.provides():
                temp_video_type = VIDEO_TYPES.TVSHOW
            else:
                temp_video_type = VIDEO_TYPES.SEASON
        else:
            temp_video_type = video.video_type

        if temp_video_type == VIDEO_TYPES.SEASON:
            season = video.season
        else:
            season = ''
            
        result = self.db_connection.get_related_url(temp_video_type, video.title, video.year, self.get_name(), season)
        if result:
            url = result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|%s|' % (temp_video_type, video.title, video.year, season, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            results = self.search(temp_video_type, video.title, video.year, season)
            if results:
                url = results[0]['url']
                self.db_connection.set_related_url(temp_video_type, video.title, video.year, self.get_name(), url, season)

        if video.video_type == VIDEO_TYPES.EPISODE:
            if url == FORCE_NO_MATCH:
                url = None
            elif url:
                result = self.db_connection.get_related_url(VIDEO_TYPES.EPISODE, video.title, video.year, self.get_name(), video.season, video.episode)
                if result:
                    url = result[0][0]
                    log_utils.log('Got local related url: |%s|%s|%s|' % (video, self.get_name(), url), log_utils.LOGDEBUG)
                else:
                    landing_url = url
                    url = self._get_episode_url(landing_url, video)
                    if url:
                        self.db_connection.set_related_url(VIDEO_TYPES.EPISODE, video.title, video.year, self.get_name(), url, video.season, video.episode)

        return url

    def _http_get(self, url, cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, method=None, cache_limit=8):
        return self._cached_http_get(url, self.base_url, self.timeout, cookies=cookies, data=data, multipart_data=multipart_data,
                                     headers=headers, allow_redirect=allow_redirect, method=method, cache_limit=cache_limit)
    
    def _cached_http_get(self, url, base_url, timeout, cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, method=None, cache_limit=8):
        if cookies is None: cookies = {}
        if timeout == 0: timeout = None
        if headers is None: headers = {}
        referer = headers['Referer'] if 'Referer' in headers else url
        log_utils.log('Getting Url: %s cookie=|%s| data=|%s| extra headers=|%s|' % (url, cookies, data, headers), log_utils.LOGDEBUG)
        if data is not None:
            if isinstance(data, basestring):
                data = data
            else:
                data = urllib.urlencode(data, True)

        if multipart_data is not None:
            headers['Content-Type'] = 'multipart/form-data; boundary=X-X-X'
            data = multipart_data

        self.create_db_connection()
        _created, _res_header, html = self.db_connection.get_cached_url(url, data, cache_limit)
        if html:
            log_utils.log('Returning cached result for: %s' % (url), log_utils.LOGDEBUG)
            return html

        try:
            self.cj = self._set_cookies(base_url, cookies)
            request = urllib2.Request(url, data=data)
            request.add_header('User-Agent', scraper_utils.get_ua())
            request.add_header('Accept', '*/*')
            request.add_unredirected_header('Host', request.get_host())
            request.add_unredirected_header('Referer', referer)
            for key in headers: request.add_header(key, headers[key])
            self.cj.add_cookie_header(request)
            if not allow_redirect:
                opener = urllib2.build_opener(NoRedirection)
                urllib2.install_opener(opener)
            else:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
                urllib2.install_opener(opener)
                opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
                urllib2.install_opener(opener2)

            if method is not None: request.get_method = lambda: method.upper()
            response = urllib2.urlopen(request, timeout=timeout)
            self.cj.extract_cookies(response, request)
            if kodi.get_setting('cookie_debug') == 'true':
                log_utils.log('Response Cookies: %s - %s' % (url, scraper_utils.cookies_as_str(self.cj)), log_utils.LOGDEBUG)
            self.cj._cookies = scraper_utils.fix_bad_cookies(self.cj._cookies)
            self.cj.save(ignore_discard=True)
            if not allow_redirect and (response.getcode() in [301, 302, 303, 307] or response.info().getheader('Refresh')):
                if response.info().getheader('Refresh') is not None:
                    refresh = response.info().getheader('Refresh')
                    return refresh.split(';')[-1].split('url=')[-1]
                else:
                    return response.info().getheader('Location')
            
            content_length = response.info().getheader('Content-Length', 0)
            if int(content_length) > MAX_RESPONSE:
                log_utils.log('Response exceeded allowed size. %s => %s / %s' % (url, content_length, MAX_RESPONSE), log_utils.LOGWARNING)
            
            if method == 'HEAD':
                return ''
            else:
                if response.info().get('Content-Encoding') == 'gzip':
                    buf = StringIO(response.read(MAX_RESPONSE))
                    f = gzip.GzipFile(fileobj=buf)
                    html = f.read()
                else:
                    html = response.read(MAX_RESPONSE)
        except urllib2.HTTPError as e:
            if e.code == 503 and 'cf-browser-verification' in e.read():
                html = cloudflare.solve(url, self.cj, scraper_utils.get_ua())
                if not html:
                    return ''
            else:
                log_utils.log('Error (%s) during scraper http get: %s' % (str(e), url), log_utils.LOGWARNING)
                return ''
        except Exception as e:
            log_utils.log('Error (%s) during scraper http get: %s' % (str(e), url), log_utils.LOGWARNING)
            return ''

        self.db_connection.cache_url(url, html, data)
        return html

    def _set_cookies(self, base_url, cookies):
        cookie_file = os.path.join(COOKIEPATH, '%s_cookies.lwp' % (self.get_name()))
        cj = cookielib.LWPCookieJar(cookie_file)
        try: cj.load(ignore_discard=True)
        except: pass
        if kodi.get_setting('cookie_debug') == 'true':
            log_utils.log('Before Cookies: %s - %s' % (self, scraper_utils.cookies_as_str(cj)), log_utils.LOGDEBUG)
        domain = urlparse.urlsplit(base_url).hostname
        for key in cookies:
            c = cookielib.Cookie(0, key, str(cookies[key]), port=None, port_specified=False, domain=domain, domain_specified=True,
                                 domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None,
                                 comment_url=None, rest={})
            cj.set_cookie(c)
        cj.save(ignore_discard=True)
        if kodi.get_setting('cookie_debug') == 'true':
            log_utils.log('After Cookies: %s - %s' % (self, scraper_utils.cookies_as_str(cj)), log_utils.LOGDEBUG)
        return cj

    def _do_recaptcha(self, key, tries=None, max_tries=None):
        challenge_url = CAPTCHA_BASE_URL + '/challenge?k=%s' % (key)
        html = self._cached_http_get(challenge_url, CAPTCHA_BASE_URL, timeout=DEFAULT_TIMEOUT, cache_limit=0)
        match = re.search("challenge\s+\:\s+'([^']+)", html)
        captchaimg = 'http://www.google.com/recaptcha/api/image?c=%s' % (match.group(1))
        img = xbmcgui.ControlImage(450, 0, 400, 130, captchaimg)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        header = 'Type the words in the image'
        if tries and max_tries:
            header += ' (Try: %s/%s)' % (tries, max_tries)
        kb = xbmc.Keyboard('', header, False)
        kb.doModal()
        solution = ''
        if kb.isConfirmed():
            solution = kb.getText()
            if not solution:
                raise Exception('You must enter text in the image to access video')
        wdlg.close()
        return {'recaptcha_challenge_field': match.group(1), 'recaptcha_response_field': solution}

    def _default_get_episode_url(self, show_url, video, episode_pattern, title_pattern='', airdate_pattern='', data=None, headers=None, method=None):
        log_utils.log('Default Episode Url: |%s|%s|%s|%s|' % (self.base_url, show_url, str(video), data), log_utils.LOGDEBUG)
        if not show_url.startswith('http'):
            url = urlparse.urljoin(self.base_url, show_url)
        else:
            url = show_url
        html = self._http_get(url, data=data, headers=headers, method=method, cache_limit=2)
        if html:
            force_title = scraper_utils.force_title(video)

            if not force_title:
                if episode_pattern:
                    match = re.search(episode_pattern, html, re.DOTALL)
                    if match:
                        return scraper_utils.pathify_url(match.group(1))

                if kodi.get_setting('airdate-fallback') == 'true' and airdate_pattern and video.ep_airdate:
                    airdate_pattern = airdate_pattern.replace('{year}', str(video.ep_airdate.year))
                    airdate_pattern = airdate_pattern.replace('{month}', str(video.ep_airdate.month))
                    airdate_pattern = airdate_pattern.replace('{p_month}', '%02d' % (video.ep_airdate.month))
                    airdate_pattern = airdate_pattern.replace('{month_name}', MONTHS[video.ep_airdate.month - 1])
                    airdate_pattern = airdate_pattern.replace('{short_month}', SHORT_MONS[video.ep_airdate.month - 1])
                    airdate_pattern = airdate_pattern.replace('{day}', str(video.ep_airdate.day))
                    airdate_pattern = airdate_pattern.replace('{p_day}', '%02d' % (video.ep_airdate.day))
                    log_utils.log('Air Date Pattern: %s' % (airdate_pattern), log_utils.LOGDEBUG)

                    match = re.search(airdate_pattern, html, re.DOTALL | re.I)
                    if match:
                        return scraper_utils.pathify_url(match.group(1))
            else:
                log_utils.log('Skipping S&E matching as title search is forced on: %s' % (video.trakt_id), log_utils.LOGDEBUG)

            if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title and title_pattern:
                norm_title = scraper_utils.normalize_title(video.ep_title)
                for match in re.finditer(title_pattern, html, re.DOTALL | re.I):
                    episode = match.groupdict()
                    if norm_title == scraper_utils.normalize_title(episode['title']):
                        return scraper_utils.pathify_url(episode['url'])

    def _blog_proc_results(self, html, post_pattern, date_format, video_type, title, year):
        results = []
        search_date = ''
        search_sxe = ''
        match = re.search('(.*?)\s*(S\d+E\d+)\s*', title)
        if match:
            show_title, search_sxe = match.groups()
        else:
            match = re.search('(.*?)\s*(\d{4})[ .]?(\d{2})[ .]?(\d{2})\s*', title)
            if match:
                show_title, search_year, search_month, search_day = match.groups()
                search_date = '%s%s%s' % (search_year, search_month, search_day)
            else:
                show_title = title
        norm_title = scraper_utils.normalize_title(show_title)

        today = datetime.date.today()
        for match in re.finditer(post_pattern, html, re.DOTALL):
            post_data = match.groupdict()
            post_title = post_data['post_title']
            if 'quality' in post_data:
                post_title += '- [%s]' % (post_data['quality'])

            try: filter_days = int(kodi.get_setting('%s-filter' % (self.get_name())))
            except ValueError: filter_days = 0
            if filter_days and date_format and 'date' in post_data:
                filter_days = datetime.timedelta(days=filter_days)
                try: post_date = datetime.datetime.strptime(post_data['date'], date_format).date()
                except TypeError: post_date = datetime.datetime(*(time.strptime(post_data['date'], date_format)[0:6])).date()
                if today - post_date > filter_days:
                    continue

            match_year = ''
            match_title = ''
            match_date = ''
            match_sxe = ''
            full_title = post_title
            if video_type == VIDEO_TYPES.MOVIE:
                match = re.search('(.*?)\s*[\[(]?(\d{4})[)\]]?\s*(.*)', post_title)
                if match:
                    match_title, match_year, extra_title = match.groups()
                    full_title = '%s [%s]' % (match_title, extra_title)
            else:
                match = re.search('(.*?)\s*(S\d+E\d+)\s*(.*)', post_title)
                if match:
                    match_title, match_sxe, extra_title = match.groups()
                    full_title = '%s [%s]' % (match_title, extra_title)
                else:
                    match = re.search('(.*?)\s*(\d{4})[ .]?(\d{2})[ .]?(\d{2})\s*(.*)', post_title)
                    if match:
                        match_title, match_year2, match_month, match_day, extra_title = match.groups()
                        match_date = '%s%s%s' % (match_year2, match_month, match_day)
                        full_title = '%s [%s]' % (match_title, extra_title)

            match_norm_title = scraper_utils.normalize_title(match_title)
            log_utils.log('Blog Results: |%s|%s| - |%s|%s| - |%s|%s| - |%s|%s|' % (match_norm_title, norm_title, year, match_year, search_date, match_date, search_sxe, match_sxe),
                          log_utils.LOGDEBUG)
            if (match_norm_title in norm_title or norm_title in match_norm_title) and (not year or not match_year or year == match_year) \
                    and (not search_date or (search_date == match_date)) and (not search_sxe or (search_sxe == match_sxe)):
                result = {'url': scraper_utils.pathify_url(post_data['url']), 'title': scraper_utils.cleanse_title(full_title), 'year': match_year}
                results.append(result)
        return results
    
    def _blog_get_url(self, video, delim='.'):
        url = None
        self.create_db_connection()
        result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            select = int(kodi.get_setting('%s-select' % (self.get_name())))
            if video.video_type == VIDEO_TYPES.EPISODE:
                temp_title = re.sub('[^A-Za-z0-9 ]', '', video.title)
                if not scraper_utils.force_title(video):
                    search_title = '%s S%02dE%02d' % (temp_title, int(video.season), int(video.episode))
                    if isinstance(video.ep_airdate, datetime.date):
                        fallback_search = '%s %s' % (temp_title, video.ep_airdate.strftime('%Y{0}%m{0}%d'.format(delim)))
                    else:
                        fallback_search = ''
                else:
                    if not video.ep_title: return None
                    search_title = '%s %s' % (temp_title, video.ep_title)
                    fallback_search = ''
            else:
                search_title = '%s %s' % (video.title, video.year)
                fallback_search = ''

            results = self.search(video.video_type, search_title, video.year)
            if not results and fallback_search:
                results = self.search(video.video_type, fallback_search, video.year)
            if results:
                # TODO: First result isn't always the most recent...
                best_result = results[0]
                if select != 0:
                    best_qorder = 0
                    for result in results:
                        match = re.search('\[(.*)\]$', result['title'])
                        if match:
                            q_str = match.group(1)
                            quality = scraper_utils.blog_get_quality(video, q_str, '')
                            log_utils.log('result: |%s|%s|%s|%s|' % (result, q_str, quality, Q_ORDER[quality]), log_utils.LOGDEBUG)
                            if Q_ORDER[quality] > best_qorder:
                                log_utils.log('Setting best as: |%s|%s|%s|%s|' % (result, q_str, quality, Q_ORDER[quality]), log_utils.LOGDEBUG)
                                best_result = result
                                best_qorder = Q_ORDER[quality]

                url = best_result['url']
                self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    def _get_direct_hostname(self, link):
        host = urlparse.urlparse(link).hostname
        if host and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            return 'gvideo'
        else:
            return self.get_name()
    
    def _parse_google(self, link):
        sources = []
        html = self._http_get(link, cache_limit=.5)
        match = re.search('pid=([^&]+)', link)
        if match:
            vid_id = match.group(1)
            sources = self.__parse_gplus(vid_id, html, link)
        else:
            if 'drive.google' in link or 'docs.google' in link:
                sources = self._parse_gdocs(link)
            if 'picasaweb' in link:
                i = link.rfind('#')
                if i > -1:
                    link_id = link[i + 1:]
                else:
                    link_id = ''
                match = re.search('feedPreload:\s*(.*}]}})},', html, re.DOTALL)
                if match:
                    js = scraper_utils.parse_json(match.group(1), link)
                    for item in js['feed']['entry']:
                        if not link_id or item['gphoto$id'] == link_id:
                            for media in item['media']['content']:
                                if media['type'].startswith('video'):
                                    sources.append(media['url'].replace('%3D', '='))
                else:
                    match = re.search('preload\'?:\s*(.*}})},', html, re.DOTALL)
                    if match:
                        js = scraper_utils.parse_json(match.group(1), link)
                        for media in js['feed']['media']['content']:
                            if media['type'].startswith('video'):
                                sources.append(media['url'].replace('%3D', '='))

        sources = list(set(sources))
        return sources

    def __parse_gplus(self, vid_id, html, link=''):
        sources = []
        match = re.search('return\s+(\[\[.*?)\s*}}', html, re.DOTALL)
        if match:
            try:
                js = scraper_utils.parse_json(match.group(1), link)
                for top_item in js:
                    if isinstance(top_item, list):
                        for item in top_item:
                            if isinstance(item, list):
                                for item2 in item:
                                    if isinstance(item2, list):
                                        for item3 in item2:
                                            if item3 == vid_id:
                                                sources = self.__extract_video(item2)
            except Exception as e:
                log_utils.log('Google Plus Parse failure: %s - %s' % (link, e), log_utils.LOGWARNING)
            return sources

    def __extract_video(self, item):
        sources = []
        for e in item:
            if isinstance(e, dict):
                for key in e:
                    for item2 in e[key]:
                        if isinstance(item2, list):
                            for item3 in item2:
                                if isinstance(item3, list):
                                    for item4 in item3:
                                        if isinstance(item4, basestring):
                                            s = urllib.unquote(item4).replace('\\0026', '&').replace('\\003D', '=')
                                            for match in re.finditer('url=([^&]+)', s):
                                                sources.append(match.group(1))
        return sources
        
    def _parse_gdocs(self, link):
        urls = []
        html = self._http_get(link, cache_limit=.5)
        for match in re.finditer('\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', html):
            key, value = match.groups()
            if key == 'fmt_stream_map':
                items = value.split(',')
                for item in items:
                    _source_fmt, source_url = item.split('|')
                    source_url = source_url.replace('\\u003d', '=').replace('\\u0026', '&')
                    source_url = urllib.unquote(source_url)
                    urls.append(source_url)
                    
        return urls

    def _get_stream_cookies(self):
        cj = self._set_cookies(self.base_url, {})
        cookies = []
        for cookie in cj:
            cookies.append('%s=%s' % (cookie.name, cookie.value))
        return urllib.quote(';'.join(cookies))

    def create_db_connection(self):
        worker_id = threading.current_thread().ident
        # create a connection if we don't have one or it was created in a different worker
        if self.db_connection is None or self.worker_id != worker_id:
            self.db_connection = DB_Connection()
            self.worker_id = worker_id

    def _parse_sources_list(self, html):
        sources = {}
        match = re.search('sources\s*:\s*\[(.*?)\]', html, re.DOTALL)
        if match:
            for match in re.finditer('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]+)''', match.group(1), re.DOTALL):
                stream_url, label = match.groups()
                stream_url = stream_url.replace('\/', '/')
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    sources[stream_url] = {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}
                elif re.search('\d+p?', label, re.I):
                    sources[stream_url] = {'quality': scraper_utils.height_get_quality(label), 'direct': True}
                else:
                    sources[stream_url] = {'quality': label, 'direct': True}
        return sources
