# -*- coding: utf-8 -*-

# Imports
import hashlib
import os
import re
import shutil
import tempfile
import time
import errno
import sys
import urlparse
import urllib
import urllib2
import simplejson
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# DEBUG
DEBUG = False

__addon__ = xbmcaddon.Addon()
__plugin__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')
__fanart__ = __addon__.getAddonInfo('fanart')
__cachedir__ = __addon__.getAddonInfo('profile')
__language__ = __addon__.getLocalizedString
__settings__ = __addon__.getSetting

CACHE_1MINUTE = 60
CACHE_1HOUR = 3600
CACHE_1DAY = 86400
CACHE_1WEEK = 604800
CACHE_1MONTH = 2592000

CACHE_TIME = CACHE_1HOUR

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
  xbmcplugin.setPluginFanart(int(sys.argv[1]), __fanart__)


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
    category = [{'title':__language__(30201), 'key':'recent'},
                {'title':__language__(30202), 'key':'top_hd'},
                {'title':__language__(30203), 'key':'popular'}]
    for i in category:
      listitem = xbmcgui.ListItem(i['title'], iconImage='DefaultFolder.png', thumbnailImage=__icon__)
      if FANART:
        listitem.setProperty('fanart_image', __fanart__)
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
    content = simplejson.loads(fetcher.fetch(contentUrl, CACHE_TIME))
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
      art = video['video']['slateUrl']
      videoId = video['video']['videoId']
      title = video['display']['text'].replace('&#x26;', '&').replace('&#x27;', "'")
      year = video['display']['year']
      imdbID = video['display']['titleId']
      try:
        poster = video['display']['poster']['url'].split('_V1._')[0] + poster_res[0]
      except:
        poster = 'http://i.media-imdb.com/images/nopicture/%s/film_hd-gallery.png' % poster_res[1]

      listitem = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=poster)
      if FANART:
        listitem.setProperty('fanart_image', art)
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
      if __settings__('couchpotato') == 'true':
        contextmenu += [(__language__(30108), 'XBMC.RunPlugin(%s?action=couchpotato&imdbid=%s)' % (sys.argv[0], imdbID))]
      listitem.addContextMenuItems(contextmenu, replaceItems=False)
      url = sys.argv[0] + '?' + urllib.urlencode({'action': 'play',
                                                  'videoid': videoId})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, False)
    # next page listitem
    if next_page:
      listitem = xbmcgui.ListItem(__language__(30204), iconImage='DefaultVideo.png', thumbnailImage=__icon__)
      if FANART:
        listitem.setProperty('fanart_image', __fanart__)
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
    quality = __settings__("video_quality")
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
    listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    # set the key information
    listitem.setInfo('video', {'title': title,
                               'label': title,
                               'plot': plot,
                               'plotOutline': plot})
    xbmc.Player().play(self.get_video_url(), listitem)

  def couchpotato(self):
    if DEBUG:
      self.log('couchpotato(): Adding to CouchPotato')

    ip = __settings__('cpIP')
    port = __settings__('cpPort')
    u = __settings__('cpUser')
    p = __settings__('cpPass')
    imdbID = self.parameters('imdbid')

    def md5(_string):
      return hashlib.md5(str(_string)).hexdigest()

    def get_api_key():
      if u and p:
        apikey_url = 'http://%s:%s/getkey/?p=%s&u=%s' % (ip, port, md5(p), md5(u))
      else:
        apikey_url = 'http://%s:%s/getkey/' % (ip, port)
      get_apikey = simplejson.load(urllib.urlopen(apikey_url))
      if get_apikey['success']:
        return get_apikey['api_key']
      else:
        self.log('Error on geting apikey!')

    query_args = {'identifier': imdbID}
    encoded_query_args = urllib.urlencode(query_args)
    request = urllib2.Request('http://%s:%s/api/%s/movie.add/?%s' % (ip, port, get_api_key(), encoded_query_args))
    add = urllib2.urlopen(request)
    if simplejson.load(add)['success']:
      self.notification(__language__(30108).encode('utf-8', 'ignore'), __language__(30109).encode('utf-8', 'ignore'))
    else:
      self.notification(__language__(30108).encode('utf-8', 'ignore'), __language__(30110).encode('utf-8', 'ignore'), displaytime=6000)

  def notification(self, title, message, image=__icon__, displaytime=5000):
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": {"title": "%s", "message": "%s", "image": "%s", "displaytime": %i}, "id": "%s"}' % \
                        (title, message, image, displaytime, __addon__.getAddonInfo('id')))

  def parameters(self, arg):
    _parameters = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    return _parameters[arg][0]

  def log(self, description):
    xbmc.log("[ADD-ON] '%s v%s': %s" % (__plugin__, __version__, description), xbmc.LOGNOTICE)


class DiskCacheFetcher:
  def __init__(self, cache_dir=None):
    # If no cache directory specified, use system temp directory
    if cache_dir is None:
      cache_dir = tempfile.gettempdir()
    if not os.path.exists(cache_dir):
      try:
        os.mkdir(cache_dir)
      except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(cache_dir):
          # File exists, and it's a directory,
          # another process beat us to creating this dir, that's OK.
          pass
        else:
          # Our target dir is already a file, or different error,
          # relay the error!
          raise
    self.cache_dir = cache_dir

  def fetch(self, url, max_age=CACHE_TIME):
    # Use MD5 hash of the URL as the filename
    filename = hashlib.md5(url).hexdigest()
    filepath = os.path.join(self.cache_dir, filename)
    if os.path.exists(filepath):
      if int(time.time()) - os.path.getmtime(filepath) < max_age:
        if DEBUG:
          print 'file exists and reading from cache.'
        return open(filepath).read()
    # Retrieve over HTTP and cache, using rename to avoid collisions
    if DEBUG:
      print 'file not yet cached or cache time expired. File reading from URL and try to cache to disk'
    headers = {'User-Agent': USER_AGENT}
    req = urllib2.Request(url, None, headers)
    data = urllib2.urlopen(req).read()
    fd, temppath = tempfile.mkstemp()
    fp = os.fdopen(fd, 'w')
    fp.write(data)
    fp.close()
    shutil.move(temppath, filepath)
    return data

fetcher = DiskCacheFetcher(xbmc.translatePath(__cachedir__))

if __name__ == '__main__':
  Main()
