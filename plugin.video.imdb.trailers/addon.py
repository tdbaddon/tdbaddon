# -*- coding: utf-8 -*-
"""
    IMDB Trailers Kodi Addon
    Copyright (C) 2013 queep
    Copyright (C) 2016 gujal
    
    Add-on originally written by queep for XBMC Frodo (except Android)
    Code modified by Gujal to run on Kodi 15 and above on all platforms
    
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
# Imports
import hashlib
import os
import re
import time
import errno
import sys
import urlparse
import urllib
import urllib2
if sys.version_info >= (2, 7):
  import json as _json
else:
  import simplejson as _json
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# DEBUG
DEBUG = False

_addon = xbmcaddon.Addon()
_plugin = _addon.getAddonInfo('name')
_version = _addon.getAddonInfo('version')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_language = _addon.getLocalizedString
_settings = _addon.getSetting


CACHE_1HOUR = 1
CACHE_4HOUR = 4
CACHE_1DAY = 24


CACHE_TIME = CACHE_4HOUR

cache = StorageServer.StorageServer("imdbtrailers", CACHE_TIME)

MAIN_URL = 'http://www.imdb.com'
CONTENT_URL = 'http://www.imdb.com/video/trailers/data/_ajax/adapter/shoveler?list=%s&debug=0'
OLD_DETAILS_PAGE = "http://www.imdb.com/video/imdb/%s/html5?format=%s"
DETAILS_PAGE = "http://www.imdb.com/video/imdb/%s/imdbvideo?format=%s"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'

# disable fanarts for speed on raspberry
try:
  if os.uname()[4].startswith('armv6'):
    FANART = False
    poster_res = ['_V1._SY256_.jpg', 'medium']
  else:
    FANART = True
    poster_res = ['_V1._SY512_.jpg', 'large']
except:
  FANART = True
  poster_res = ['_V1._SY512_.jpg', 'large']

# Fanart
if FANART:
  xbmcplugin.setPluginFanart(int(sys.argv[1]), _fanart)


# Main
class Main:
  def __init__(self):
    if ("action=list" in sys.argv[2]):
      self.list_contents()
    elif ("action=play" in sys.argv[2]):
      self.play()
    elif ("action=couchpotato" in sys.argv[2]):
      self.couchpotato()
    else:
      self.main_menu()

  def main_menu(self):
    if DEBUG:
      self.log('main_menu()')
    category = [{'title':_language(30201), 'key':'recent'},
                {'title':_language(30202), 'key':'top_hd'},
                {'title':_language(30203), 'key':'popular'}]
    for i in category:
      listitem = xbmcgui.ListItem(i['title'])
      listitem.setArt({ 'thumb': _icon })
      listitem.setIconImage('DefaultFolder.png')
      if FANART:
        listitem.setArt({'fanart': _fanart })
      url = sys.argv[0] + '?' + urllib.urlencode({'action': 'list',
                                                  'key': i['key']})
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, True)])
    # Sort methods and content type...
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def list_contents(self):
    if DEBUG:
      self.log('content_list()')
    try:
      contentUrl = self.parameters('next_page')
    except:
      contentUrl = CONTENT_URL % self.parameters('key')
    content = _json.loads(cache.cacheFunction(fetch,contentUrl))
    try:
      next_page_url = MAIN_URL + content['model']['next']
      next_page = True
    except:
      next_page = False
    for video in content['model']['items']:
      plot = video['overview']['plot']
      if not plot:
        plot = ''
      genrelist = video['overview']['genres']
      if genrelist is not None:
        genres = ', '.join(map(str, genrelist))
      else:
        genres = ''
      mpaa = video['overview']['certificate']
      if not mpaa:
        mpaa = ''
      rating = video['overview']['user_rating']
      if not rating:
        rating = 0
      # TODO: Check empty and list director list
      directors = video['overview']['directors']
      if len(directors) > 1:
        directors = '%s, %s' % (directors[0], directors[1])
      elif len(directors) < 1:
        directors = ''
      else:
        directors = directors[0]
      stars = video['overview']['stars']
      # duration = video['video']['duration']['string']
      # art = video['video']['slateUrl']
      videoId = video['video']['videoId']
      title = video['display']['text'].replace('&#x26;', '&').replace('&#x27;', "'")
      year = video['display']['year']
      if not year:
        year = '1900'
      imdbID = video['display']['titleId']
      try:
        poster = video['display']['poster']['url'].split('_V1._')[0] + poster_res[0]
      except:
        poster = 'http://i.media-imdb.com/images/nopicture/%s/film_hd-gallery.png' % poster_res[1]

      listitem = xbmcgui.ListItem(title)
      listitem.setArt({ 'thumb': poster,
                        'poster': poster})
      listitem.setIconImage('DefaultVideo.png')
      if FANART:
        listitem.setArt({'fanart': _fanart})
      listitem.setInfo(type='video',
                       infoLabels={'title': title,
                                   'plot': plot,
                                   'genre': genres,
                                   'year': int(year),
                                   'rating': float(rating),
                                   'mpaa': mpaa,
                                   # 'duration': str(duration),
                                   'director': directors.encode('utf-8', 'ignore'),
                                   'cast': stars})
      # dummy context menu variable
      contextmenu = []
      if _settings('couchpotato') == 'true':
        contextmenu += [(_language(30108), 'XBMC.RunPlugin(%s?action=couchpotato&imdbid=%s)' % (sys.argv[0], imdbID))]
      listitem.addContextMenuItems(contextmenu, replaceItems=False)
      url = sys.argv[0] + '?' + urllib.urlencode({'action': 'play',
                                                  'videoid': videoId})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, False)
    # next page listitem
    if next_page:
      listitem = xbmcgui.ListItem(_language(30204))
      listitem.setArt({ 'thumb': _icon })
      listitem.setIconImage('DefaultVideo.png')
      if FANART:
       listitem.setArt({'fanart': _fanart})
      url = sys.argv[0] + '?' + urllib.urlencode({'action': 'list',
                                                  'next_page': next_page_url})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)
    # Sort methods and content type...
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def get_video_url(self):
    if DEBUG:
      self.log('get_video_url()')
    quality = _settings("video_quality")
    detailsUrl = DETAILS_PAGE % (self.parameters('videoid'), quality)
    if DEBUG:
      self.log('detailsURL: %s' % detailsUrl)
    headers = {'User-Agent': USER_AGENT}
    req = urllib2.Request(detailsUrl, None, headers)
    details = urllib2.urlopen(req).read()
    videoUrl = re.findall('"url":"(.+?)"', details)[0]
    if DEBUG:
      self.log('videoURL: %s' % videoUrl)
    return videoUrl

  def play(self):
    if DEBUG:
      self.log('play()')
    title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
    thumbnail = xbmc.getInfoImage("ListItem.Thumb")
    plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
    # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
    listitem = xbmcgui.ListItem(title)
    listitem.setArt({ 'thumb': thumbnail })
    listitem.setIconImage('DefaultVideo.png')
    # set the key information
    listitem.setInfo('video', {'title': title,
                               'label': title,
                               'plot': plot,
                               'plotOutline': plot})
    xbmc.Player().play(self.get_video_url(), listitem)

  def couchpotato(self):
    if DEBUG:
      self.log('couchpotato(): Adding to CouchPotato')

    ip = _settings('cpIP')
    port = _settings('cpPort')
    u = _settings('cpUser')
    p = _settings('cpPass')
    imdbID = self.parameters('imdbid')

    def md5(_string):
      return hashlib.md5(str(_string)).hexdigest()

    def get_api_key():
      if u and p:
        apikey_url = 'http://%s:%s/getkey/?p=%s&u=%s' % (ip, port, md5(p), md5(u))
      else:
        apikey_url = 'http://%s:%s/getkey/' % (ip, port)
      get_apikey = _json.load(urllib.urlopen(apikey_url))
      if get_apikey['success']:
        return get_apikey['api_key']
      else:
        self.log('Error on geting apikey!')

    query_args = {'identifier': imdbID}
    encoded_query_args = urllib.urlencode(query_args)
    request = urllib2.Request('http://%s:%s/api/%s/movie.add/?%s' % (ip, port, get_api_key(), encoded_query_args))
    add = urllib2.urlopen(request)
    if _json.load(add)['success']:
      self.notification(_language(30108).encode('utf-8', 'ignore'), _language(30109).encode('utf-8', 'ignore'))
    else:
      self.notification(_language(30108).encode('utf-8', 'ignore'), _language(30110).encode('utf-8', 'ignore'), displaytime=6000)

  def notification(self, title, message, image=_icon, displaytime=5000):
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": {"title": "%s", "message": "%s", "image": "%s", "displaytime": %i}, "id": "%s"}' % \
                        (title, message, image, displaytime, _addon.getAddonInfo('id')))

  def parameters(self, arg):
    _parameters = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    return _parameters[arg][0]

  def log(self, description):
    xbmc.log("[ADD-ON] '%s v%s': %s" % (_plugin, _version, description), xbmc.LOGNOTICE)

def fetch(url):

    headers = {'User-Agent': USER_AGENT}
    req = urllib2.Request(url, None, headers)
    data = urllib2.urlopen(req).read()
    return data
    

if __name__ == '__main__':
  Main()
