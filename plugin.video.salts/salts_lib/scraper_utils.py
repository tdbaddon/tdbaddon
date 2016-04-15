"""
    SALTS XBMC Addon
    Copyright (C) 2016 tknorris

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
import base64
import random
import re
import sys
import time
import urllib
import urlparse
import json
import htmlentitydefs
from salts_lib import kodi
from salts_lib import pyaes
from salts_lib import log_utils
from salts_lib.constants import *

def disable_sub_check(settings):
    for i in reversed(xrange(len(settings))):
        if 'sub_check' in settings[i]:
            settings[i] = settings[i].replace('default="true"', 'default="false"')
    return settings

def get_ua():
    try: last_gen = int(kodi.get_setting('last_ua_create'))
    except: last_gen = 0
    if not kodi.get_setting('current_ua') or last_gen < (time.time() - (7 * 24 * 60 * 60)):
        index = random.randrange(len(RAND_UAS))
        user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
        log_utils.log('Creating New User Agent: %s' % (user_agent), log_utils.LOGDEBUG)
        kodi.set_setting('current_ua', user_agent)
        kodi.set_setting('last_ua_create', str(int(time.time())))
    else:
        user_agent = kodi.get_setting('current_ua')
    return user_agent

def cookies_as_str(cj):
    s = ''
    c = cj._cookies
    for domain in c:
        s += '{%s: ' % (domain)
        for path in c[domain]:
            s += '{%s: ' % (path)
            for cookie in c[domain][path]:
                s += '{%s=%s}' % (cookie, c[domain][path][cookie].value)
            s += '}'
        s += '} '
    return s
                
# TODO: Test with CJ
def fix_bad_cookies(cookies):
    for domain in cookies:
        for path in cookies[domain]:
            for key in cookies[domain][path]:
                cookie = cookies[domain][path][key]
                if cookie.expires > sys.maxint:
                    log_utils.log('Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint), log_utils.LOGDEBUG)
                    cookie.expires = sys.maxint
    return cookies

def force_title(video):
        trakt_str = kodi.get_setting('force_title_match')
        trakt_list = trakt_str.split('|') if trakt_str else []
        return str(video.trakt_id) in trakt_list

def normalize_title(title):
    if title is None: title = ''
    title = cleanse_title(title)
    new_title = title.upper()
    new_title = re.sub('[^A-Za-z0-9]', '', new_title)
    # log_utils.log('In title: |%s| Out title: |%s|' % (title,new_title), log_utils.LOGDEBUG)
    return new_title

def blog_get_quality(video, q_str, host):
    """
    Use the q_str to determine the post quality; then use the host to determine host quality
    allow the host to drop the quality but not increase it
    """
    q_str.replace(video.title, '')
    q_str.replace(str(video.year), '')
    q_str = q_str.upper()

    post_quality = None
    for key in [item[0] for item in sorted(Q_ORDER.items(), key=lambda x:x[1])]:
        if any(q in q_str for q in BLOG_Q_MAP[key]):
            post_quality = key

    return get_quality(video, host, post_quality)

def get_quality(video, host, base_quality=None):
    if host is None: host = ''
    host = host.lower()
    # Assume movies are low quality, tv shows are high quality
    if base_quality is None:
        if video.video_type == VIDEO_TYPES.MOVIE:
            quality = QUALITIES.LOW
        else:
            quality = QUALITIES.HIGH
    else:
        quality = base_quality

    host_quality = None
    if host:
        for key in HOST_Q:
            if any(hostname in host for hostname in HOST_Q[key]):
                host_quality = key
                break

    # log_utils.log('q_str: %s, host: %s, post q: %s, host q: %s' % (q_str, host, post_quality, host_quality), log_utils.LOGDEBUG)
    if host_quality is not None and Q_ORDER[host_quality] < Q_ORDER[quality]:
        quality = host_quality

    return quality

def width_get_quality(width):
    try: width = int(width)
    except: width = 320
    if width > 1280:
        quality = QUALITIES.HD1080
    elif width > 800:
        quality = QUALITIES.HD720
    elif width > 640:
        quality = QUALITIES.HIGH
    elif width > 320:
        quality = QUALITIES.MEDIUM
    else:
        quality = QUALITIES.LOW
    return quality

def height_get_quality(height):
    if str(height)[-1] in ['p', 'P']:
        height = str(height)[:-1]
        
    try: height = int(height)
    except: height = 200
    if height >= 800:
        quality = QUALITIES.HD1080
    elif height > 480:
        quality = QUALITIES.HD720
    elif height >= 400:
        quality = QUALITIES.HIGH
    elif height > 200:
        quality = QUALITIES.MEDIUM
    else:
        quality = QUALITIES.LOW
    return quality

def gv_get_quality(stream_url):
    stream_url = urllib.unquote(stream_url)
    if 'itag=18' in stream_url or '=m18' in stream_url:
        return QUALITIES.MEDIUM
    elif 'itag=22' in stream_url or '=m22' in stream_url:
        return QUALITIES.HD720
    elif 'itag=34' in stream_url or '=m34' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=35' in stream_url or '=m35' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=37' in stream_url or '=m37' in stream_url:
        return QUALITIES.HD1080
    elif 'itag=43' in stream_url or '=m43' in stream_url:
        return QUALITIES.MEDIUM
    else:
        return QUALITIES.HIGH

def get_sucuri_cookie(html):
    if 'sucuri_cloudproxy_js' in html:
        match = re.search("S\s*=\s*'([^']+)", html)
        if match:
            s = base64.b64decode(match.group(1))
            s = s.replace(' ', '')
            s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
            s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
            s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
            s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
            s = re.sub(';location.reload\(\);', '', s)
            s = re.sub(r'\n', '', s)
            s = re.sub(r'document\.cookie', 'cookie', s)
            try:
                cookie = ''
                exec(s)
                match = re.match('([^=]+)=(.*)', cookie)
                if match:
                    return {match.group(1): match.group(2)}
            except Exception as e:
                log_utils.log('Exception during sucuri js: %s' % (e), log_utils.LOGWARNING)
    
    return {}
    
def gk_decrypt(name, key, cipher_link):
    try:
        key += (24 - len(key)) * '\0'
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
        plain_text = decrypter.feed(cipher_link.decode('hex'))
        plain_text += decrypter.feed()
        plain_text = plain_text.split('\0', 1)[0]
    except Exception as e:
        log_utils.log('Exception (%s) during %s gk decrypt: cipher_link: %s' % (e, name, cipher_link), log_utils.LOGWARNING)
        plain_text = ''

    return plain_text

def parse_episode_link(link):
    link = urllib.unquote(link)
    file_name = link.split('/')[-1]
    match = re.match('(.*?)[._ ]S(\d+)[._ ]?E(\d+)(?:E\d+)*.*?(?:[._ ](\d+)p[._ ])(.*)', file_name, re.I)
    if match:
        return match.groups()
    else:
        match = re.match('(.*?)[._ ]S(\d+)[._ ]?E(\d+)(?:E\d+)*(.*)', file_name, re.I)
        if match:
            return match.groups()[:-1] + ('480', ) + (match.groups()[-1],)  # assume no height = 480
        else:
            match = re.search('[._ ](\d{3,})p[._ ]', file_name)
            if match:
                return ('', '-1', '-1', match.group(1), '')
            else:
                return ('', '-1', '-1', '480', '')

def parse_movie_link(link):
    file_name = link.split('/')[-1]
    match = re.match('(.*?)(?:[._ ](\d{4})(?:[._ ].*?)*)?[._ ](\d+)p[._ ](.*)', file_name)
    if match:
        return match.groups()
    else:
        match = re.match('(.*?)(?:[._ ](\d{4})(?:[._ ].*?)*)(.*)', file_name)
        if match:
            title, year, extra = match.groups()
            return (title, year, '480', extra)
        else:
            return ('', '', '480', '')  # make 480p when unknown

def title_check(video, title):
    title = normalize_title(title)
    if video.video_type == VIDEO_TYPES.MOVIE:
        return normalize_title(video.title) in title and (not video.year or video.year in title)
    else:
        sxe = 'S%02dE%02d' % (int(video.season), int(video.episode))
        se = '%d%02d' % (int(video.season), int(video.episode))
        try:
            air_date = video.ep_airdate.strftime('%Y%m%d')
        except:
            air_date = ''
            
        if sxe in title:
            show_title = title.split(sxe)[0]
        elif air_date and air_date in title:
            show_title = title.split(air_date)[0]
        elif se in title:
            show_title = title.split(se)[0]
        else:
            show_title = title
        # log_utils.log('%s - %s - %s - %s - %s' % (scraper_utils.normalize_title(video.title), show_title, title, sxe, air_date), log_utils.LOGDEBUG)
        return normalize_title(video.title) in show_title and (sxe in title or se in title or air_date in title)

def pathify_url(url):
    url = url.replace('\/', '/')
    pieces = urlparse.urlparse(url)
    if pieces.scheme:
        strip = pieces.scheme + ':'
    else:
        strip = ''
    strip += '//' + pieces.netloc
    url = url.replace(strip, '')
    if url.startswith('..'): url = url[2:]
    if not url.startswith('/'): url = '/' + url
    url = url.replace('/./', '/')
    url = url.replace('&amp;', '&')
    url = url.replace('//', '/')
    return url

def parse_json(html, url=''):
    if html:
        try:
            js_data = json.loads(html)
            if js_data is None:
                return {}
            else:
                return js_data
        except ValueError:
            log_utils.log('Invalid JSON returned: %s: %s' % (html, url), log_utils.LOGWARNING)
            return {}
    else:
        log_utils.log('Empty JSON object: %s: %s' % (html, url), log_utils.LOGDEBUG)
        return {}

def format_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def cleanse_title(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fixup, text.strip())
