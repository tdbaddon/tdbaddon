# -*- coding: utf-8 -*-

'''
    zen Add-on
    Copyright (C) 2016 zen

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


import re,urllib,urlparse,random

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
# if not debridstatus == 'true': raise Exception()
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['ganool.cc']
        self.base_link = 'rlsarchive.com'
        self.search_link = 'http://www.rls-movies.com/?s='


    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			titlecheck = cleanmovie+year
			query = "http://www.rls-movies.com/?s=%s+%s" % (urllib.quote_plus(title),year)
			link = client.request(query, timeout="10")
			match = re.compile('<h2 class="post-box-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h2>').findall(link)
		
			for movielink,title in match:
				
				c_title = cleantitle_get_2(title)
				if titlecheck in c_title:
					self.zen_url.append([movielink,title])
			return self.zen_url
        except:
            return
			
    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return			

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []		
        try:
			if not debridstatus == 'true': raise Exception()
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)			
			episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(episodecheck)
			episodecheck = episodecheck.lower()
			titlecheck = cleanmovie+episodecheck
			query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(data['season']), int(data['episode']))
			movielink = self.search_link + str(query)
			link = client.request(movielink, timeout="10")
			match = re.compile('<h2 class="post-box-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h2>').findall(link)
			for movielink,title2 in match:
				c_title = cleantitle.get(title2)
				if titlecheck in c_title:
					self.zen_url.append([movielink,title])
			return self.zen_url
        except:
            return		

    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []


			for movielink,title in self.zen_url:
				
				
				
				mylink = client.request(movielink, timeout="5")

			
				if "1080" in title: quality = "1080p"
				elif "720" in title: quality = "HD"				
				else: quality = "SD"
				

				match2 = re.compile('<a href="(.+?)" class="external" rel="nofollow" target="_blank">').findall(mylink)
				for url in match2:
						myurl = str(url)
						if not any(value in myurl for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
							if ".avi" in url or ".mkv" in url or ".mp4" in url or ".divx" in url or ".mov" in url or "clicknupload" in url or "hugefiles" in url or "userscloud" in url:

								
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')															
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Videomega'
								
								sources.append({'source': host, 'quality': quality, 'provider': 'Rlsmovies', 'url': url, 'direct': False, 'debridonly': True})



	 

			return sources
        except:
            return sources


    def resolve(self, url):

            return url

def _getDOMContent(html, name, match, ret):
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

    if ret:
        endstr = html[end:html.find(">", html.find(end_str)) + 1]
        result = match + result + endstr

    return result

def _getDOMAttributes(match, name, ret):
    pattern = '''<%s[^>]* %s\s*=\s*(?:(['"])(.*?)\\1|([^'"].*?)(?:>|\s))''' % (name, ret)
    results = re.findall(pattern, match, re.I | re.M | re.S)
    return [result[1] if result[1] else result[2] for result in results]

def _getDOMElements(item, name, attrs):
    if not attrs:
        pattern = '(<%s(?: [^>]*>|/?>))' % (name)
        this_list = re.findall(pattern, item, re.M | re.S | re.I)
    else:
        last_list = None
        for key in attrs:
            pattern = '''(<%s [^>]*%s=['"]%s['"][^>]*>)''' % (name, key, attrs[key])
            this_list = re.findall(pattern, item, re.M | re. S | re.I)
            if not this_list and ' ' not in attrs[key]:
                pattern = '''(<%s [^>]*%s=%s[^>]*>)''' % (name, key, attrs[key])
                this_list = re.findall(pattern, item, re.M | re. S | re.I)
    
            if last_list is None:
                last_list = this_list
            else:
                last_list = [item for item in this_list if item in last_list]
        this_list = last_list
    
    return this_list

def parse_dom(html, name='', attrs=None, ret=False):
    if attrs is None: attrs = {}
    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")]  # Replace with chardet thingy
        except:
            print "none"
            try:
                html = [html.decode("utf-8", "replace")]
            except:
                
                html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):
        
        return ''

    if not name.strip():
        
        return ''
    
    if not isinstance(attrs, dict):
        
        return ''

    ret_lst = []
    for item in html:
        for match in re.findall('(<[^>]*\n[^>]*>)', item):
            item = item.replace(match, match.replace('\n', ' ').replace('\r', ' '))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    # log_utils.log("Done: " + repr(ret_lst), xbmc.LOGDEBUG)
    return ret_lst

