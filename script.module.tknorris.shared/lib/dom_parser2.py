'''
   Based on Parsedom for XBMC plugins
   Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

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
import re
import log_utils
from collections import namedtuple

DomMatch = namedtuple('DOMMatch', ['attrs', 'content'])

def __get_dom_content(html, name, match):
    end_str = "</%s" % (name)
    start_str = '<%s' % (name)

    start = html.find(match)
    end = html.find(end_str, start)
    pos = html.find(start_str, start + 1)

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(end_str, end + len(end_str))
        if tend != -1:
            end = tend
        pos = html.find(start_str, pos + 1)

    if start == -1 and end == -1:
        result = ''
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]
    else:
        result = ''

    return result

def __get_dom_elements(item, name, attrs):
    if not attrs:
        pattern = '(<%s(?:\s[^>]*>|/?>))' % (name)
        this_list = re.findall(pattern, item, re.M | re.S | re.I)
    else:
        last_list = None
        for key, value in attrs.iteritems():
            pattern = '''(<%s\s[^>]*%s=['"]%s['"][^>]*>)''' % (name, key, value)
            this_list = re.findall(pattern, item, re.M | re. S | re.I)
            if not this_list and ' ' not in value:
                pattern = '''(<%s\s[^>]*%s=%s[^>]*>)''' % (name, key, value)
                this_list = re.findall(pattern, item, re.M | re. S | re.I)
    
            if last_list is None:
                last_list = this_list
            else:
                last_list = [item for item in this_list if item in last_list]
        this_list = last_list
    
    return this_list

def __get_attribs(element):
    attribs = {}
    for match in re.finditer('''\s+(?P<key>[^=]+)=(?:(?P<delim>["'])(?P<value1>.*?)(?P=delim)|(?P<value2>[^"'][^>\s]*))''', element):
        match = match.groupdict()
        attribs[match['key']] = match.get('value1') or match.get('value2')
    return attribs

def parse_dom(html, name='', attrs=None, req=False):
    if attrs is None: attrs = {}
    name = name.strip()
    # log_utils.log('parse_dom: Name: |%s| Attrs: |%s| Ret: |%s| - HTML: %s' % (name, attrs, req, type(html)), log_utils.LOGDEBUG)
    if isinstance(html, unicode):
        html = [html]
    elif isinstance(html, str):
        try:
            html = [html.decode("utf-8")]  # Replace with chardet thingy
        except:
            log_utils.log("HTML Decode Failed. Data length: %d" % len(html), log_utils.LOGWARNING)
            try:
                html = [html.decode("utf-8", "replace")]
            except:
                log_utils.log("HTML Decode Failed (Replace). Data length: %d" % len(html), log_utils.LOGWARNING)
                html = [html]
    elif not isinstance(html, list):
        log_utils.log("Input isn't list or string/unicode.", log_utils.LOGWARNING)
        return ''

    if not name:
        log_utils.log("Missing tag name", log_utils.LOGWARNING)
        return ''
    
    if not isinstance(attrs, dict):
        log_utils.log("Attrs must be dictionary", log_utils.LOGWARNING)
        return ''

    if req:
        if not isinstance(req, list):
            req = [req]
        req = set(req)
        
    all_results = []
    for item in html:
        results = []
        for element in __get_dom_elements(item, name, attrs):
            attribs = __get_attribs(element)
            if req and not req <= set(attribs.keys()): continue
            temp = __get_dom_content(item, name, element).strip()
            results.append(DomMatch(attribs, temp))
            item = item[item.find(temp, item.find(element)):]
        all_results += results

    # log_utils.log("Done: %s" + (all_results), xbmc.LOGDEBUG)
    return all_results
