import sys
import os
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import logging
from operator import itemgetter

def show_tags():
  tag_handle = int(sys.argv[1])
  xbmcplugin.setContent(tag_handle, 'tags')

  for tag in tags:
    iconPath = os.path.join(home, 'resources', 'media', tag['icon'])
    li = xbmcgui.ListItem(tag['name'], iconImage=iconPath)
    url = sys.argv[0] + '?tag=' + str(tag['id'])
    xbmcplugin.addDirectoryItem(handle=tag_handle, url=url, listitem=li, isFolder=True)

  xbmcplugin.endOfDirectory(tag_handle)


def show_streams(tag):
  stream_handle = int(sys.argv[1])
  xbmcplugin.setContent(stream_handle, 'streams')
  logging.warning('TAG show_streams!!!! %s', tag)
  for stream in streams[str(tag)]:
    logging.debug('STREAM HERE!!! %s', stream['name'])
    iconPath = os.path.join(home, 'resources', 'media', stream['icon'])
    li = xbmcgui.ListItem(stream['name'], iconImage=iconPath)
    xbmcplugin.addDirectoryItem(handle=stream_handle, url=stream['url'], listitem=li)

  xbmcplugin.endOfDirectory(stream_handle)


def get_params():
  """
  Retrieves the current existing parameters from XBMC.
  """
  param = []
  paramstring = sys.argv[2]
  if len(paramstring) >= 2:
    params = sys.argv[2]
    cleanedparams = params.replace('?', '')
    if params[len(params) - 1] == '/':
      params = params[0:len(params) - 2]
    pairsofparams = cleanedparams.split('&')
    param = {}
    for i in range(len(pairsofparams)):
      splitparams = {}
      splitparams = pairsofparams[i].split('=')
      if (len(splitparams)) == 2:
        param[splitparams[0]] = splitparams[1]
  return param


def lower_getter(field):
  def _getter(obj):
    return obj[field].lower()

  return _getter


addon = xbmcaddon.Addon()
username = addon.getSetting('username')
password = addon.getSetting('password')
home = xbmc.translatePath(addon.getAddonInfo('path'))

tags = [
{
    'name': 'DISCLAIMER',
    'id': 'DISCLAIMER',
    'icon': 'icon.png'
  }, {
    'name': 'Motivation',
    'id': 'Motivation',
    'icon': 'icon.png'
  }, {
    'name': 'Channels',
    'id': 'Channels',
    'icon': 'icon.png'
  }
]

DISCLAIMER = [{
  'name': '1. Disclaimer: These free links are not ours. We just try to keep them current as a courtesy to the community',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '2. There are no media files hosted by us for this free video add-on',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '3. Any issues with these Channels are out of our control.',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '4. For quality HD IPTV, visit www.rasp.tv and get premium',
  'url': '',
  'icon': 'icon.png',
  'disabled': False
}]

Motivation = [{
  'name': '1. Buy me a beer? PayPal rasp@rasp.tv',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '2. Maintaining these lists takes time and effort.',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '3. Visit us www.rasp.tv',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '4. Like Rasp /rasptv on Facebook',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '5. Follow @watchrasp on Twitter',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': '6. Report dead links to rasp@rasp.tv',
  'url': 'http://',
  'icon': 'icon.png',
  'disabled': False
}]

Channels = [{
  'name': 'ALL',
  'url': 'https://www.rasp.tv/freem3u/all.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'NEWS',
  'url': 'https://www.rasp.tv/freem3u/news.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'DOCUMENTARY/EDUCATIONAL',
  'url': 'https://www.rasp.tv/freem3u/documentary.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'ENTERTAINMENT',
  'url': 'https://www.rasp.tv/freem3u/entertainment.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'SPORTS/GAMES',
  'url': 'https://www.rasp.tv/freem3u/sport.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'MUSIC',
  'url': 'https://www.rasp.tv/freem3u/music.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'SHOPPING',
  'url': 'https://www.rasp.tv/freem3u/shopping.m3u',
  'icon': 'icon.png',
  'disabled': False
  }, {
  'name': 'TESTING',
  'url': 'https://www.rasp.tv/freem3u/untested.m3u',
  'icon': 'icon.png',
  'disabled': False
  }]

streams = {
  'DISCLAIMER': sorted((i for i in DISCLAIMER if not i.get('disabled', False)), key=lower_getter('name')),
  'Motivation': sorted((i for i in Motivation if not i.get('disabled', False)), key=lower_getter('name')),
  'Channels': sorted((i for i in Channels if not i.get('disabled', False)), key=lower_getter('name')),
  
  # 'DISCLAIMER': sorted(DISCLAIMER, key=lower_getter('name')),
  # 'Motivation': sorted(Motivation, key=lower_getter('name')),
  # 'Channels': sorted(Channels, key=lower_getter('name')),

}

PARAMS = get_params()
TAG = None
logging.warning('PARAMS!!!! %s', PARAMS)

try:
  TAG = PARAMS['tag']
except:
  pass

logging.warning('ARGS!!!! sys.argv %s', sys.argv)

if TAG == None:
  show_tags()
else:
  show_streams(TAG)
