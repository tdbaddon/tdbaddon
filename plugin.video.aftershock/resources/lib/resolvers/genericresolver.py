# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import re, urllib

from urlparse import urlparse
from ashock.modules import client
from ashock.modules import jsunpack
from ashock.modules import logger



def resolve(url):
    try:
        headers = {'User-Agent': client.randomagent()}

        result, response_code, response_headers, headers, cookie = client.request(url, headers=headers, output='extended')
        headers.update({'Referer': url})
        headers.update({'Cookie': cookie})

        scheme = urlparse(url).scheme
        result_blacklist = []
        source_list = scrape_sources(result, result_blacklist, scheme)
        source = pick_source(source_list)
        url = source + append_headers(headers)
        logger.debug('URL [%s]' % url, __name__)
        return url
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False

def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])

def pick_source(sources, auto_pick=True):

    if len(sources) == 1:
        return sources[0][1]
    elif len(sources) > 1:
        if auto_pick:
            return sources[0][1]

def scrape_sources(html, result_blacklist=None, scheme='http'):
    def __parse_to_list(_html, regex):
        _blacklist = ['.jpg', '.jpeg', '.gif', '.png', '.js', '.css', '.htm', '.html', '.php', '.srt', '.sub', '.xml', '.swf', '.vtt']
        _blacklist = set(_blacklist + result_blacklist)
        streams = []
        labels = []
        for r in re.finditer(regex, _html, re.DOTALL):
            match = r.groupdict()
            stream_url = match['url']
            file_name = urlparse(stream_url).path.split('/')[-1]
            blocked = not file_name or any(item in file_name.lower() for item in _blacklist)
            if stream_url.startswith('//'): stream_url = scheme + ':' + stream_url
            if '://' not in stream_url or blocked or (stream_url in streams) or any(stream_url == t[1] for t in source_list):
                continue

            label = match.get('label', file_name)
            if label is None: label = file_name
            labels.append(label)
            streams.append(stream_url)

        matches = zip(labels, streams)
        return matches

    if result_blacklist is None:
        result_blacklist = []
    elif isinstance(result_blacklist, str):
        result_blacklist = [result_blacklist]

    html = add_packed_data(html)

    source_list = []
    source_list += __parse_to_list(html, '''["']?label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)''')
    source_list += __parse_to_list(html, '''["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)''')
    source_list += __parse_to_list(html, '''video[^><]+src\s*[=:]\s*['"](?P<url>[^'"]+)''')
    source_list += __parse_to_list(html, '''source\s+src\s*=\s*['"](?P<url>[^'"]+)['"](?:.*?data-res\s*=\s*['"](?P<label>[^'"]+))?''')
    source_list += __parse_to_list(html, '''["']?\s*(?:file|url)\s*["']?\s*[:=]\s*["'](?P<url>[^"']+)''')
    source_list += __parse_to_list(html, '''param\s+name\s*=\s*"src"\s*value\s*=\s*"(?P<url>[^"]+)''')

    if len(source_list) > 1:
        try: source_list.sort(key=lambda x: int(x[0]), reverse=True)
        except:
            try: source_list.sort(key=lambda x: int(x[0][:-1]), reverse=True)
            except:
                pass

    return source_list

def add_packed_data(html):
    for match in re.finditer('(eval\(function.*?)</script>', html, re.DOTALL):
        try:
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            html += js_data
        except:
            pass

    return html