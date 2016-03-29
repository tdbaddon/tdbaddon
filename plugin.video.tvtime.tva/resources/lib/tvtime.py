'''
    TV Time Add-on

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

import sys, os, re
import urllib, urllib2
import json, random
import xbmcgui, xbmc, xbmcvfs
import Addon

class TVtime:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.mBASE_URL = 'http://mhancoc7.offshorepastebin.com/tvtime'
        self.uBASE_URL = 'http://m-api.ustvnow.com'

    def get_channels(self, quality):
        Addon.log('get_channels,' + str(quality))
	content = self._get_json('/playingnow.php')
	channels = []
	results = content['results'];
	for i in results:
	    channel = i['channel']
	    poster_url = i['img']
	    channels.append({
	        'channel': i['channel'],
	        'title': i['title'],
	        'image': i['img'],
	        })
	return channels 

    def get_link(self, quality):
        Addon.log('get_link,' + str(quality))
	content = self._get_json('/playingnow.php')
	channels = []
	results = content['results'];
	quality = (quality + 1)
	passkey = self._get_passkey()
	src = random.choice(['lv5', 'lv7', 'lv9'])
	stream_type = 'rtmp'
	for i in results:
	    if quality == 4 and i['channel'] == 'My9':
	        quality = (quality - 1)
	    channel = i['channel']
	    url = stream_type + '://' + str(src) + '.ustvnow.com:1935/dvrtest?key=' + passkey + '/mp4:' + i['stream'] + str(quality)
	    channels.append({
	        'channel': channel,
	        'url': url
	        })
	return channels
            
    def _build_url(self, path, queries={}):
        Addon.log('_build_url')
        if queries:
            query = Addon.build_query(queries)
            return '%s/%s?%s' % (self.mBASE_URL, path, query)
        else:
            return '%s/%s' % (self.mBASE_URL, path)

    def _build_json(self, path, queries={}):
        Addon.log('_build_json')
        if queries:
            query = urllib.urlencode(queries)
            return '%s/%s?%s' % (self.mBASE_URL, path, query)
        else:
            return '%s/%s' % (self.mBASE_URL, path)

    def _build_json_u(self, path, queries={}):
        Addon.log('_build_json_u')
        if queries:
            query = urllib.urlencode(queries)
            return '%s/%s?%s' % (self.uBASE_URL, path, query)
        else:
            return '%s/%s' % (self.mBASE_URL, path)

    def _fetch(self, url, form_data=False):
        Addon.log('_fetch')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        if form_data:
            req = urllib2.Request(url, form_data)
        else:
            req = url
        try:
            response = opener.open(req)
            return response
        except urllib2.URLError, e:
            return False

    def _get_json(self, path, queries={}):
        Addon.log('_get_json')
        content = False
        url = self._build_json(path, queries)
        response = self._fetch(url)
        if response:
            content = json.loads(response.read())
        else:
            content = False
        return content

    def _get_json_u(self, path, queries={}):
        Addon.log('_get_json_u')
        content = False
        url = self._build_json_u(path, queries)
        response = self._fetch(url)
        if response:
            content = json.loads(response.read())
        else:
            content = False
        return content

    def _get_html(self, path, queries={}):
        Addon.log('_get_html')
        html = False
        url = self._build_url(path, queries)
   
        response = self._fetch(url)
        if response:
            html = response.read()
        else:
            html = False
        return html

    def _get_passkey(self):
        token = self._get_json('/token.php')['token']
        passkey = self._get_json_u('/gtv/1/live/viewdvrlist', {'token': token})['globalparams']['passkey']
        return passkey
