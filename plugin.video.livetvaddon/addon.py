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
    iconPath = os.path.join(home, 'logos', tag['icon'])
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
    iconPath = os.path.join(home, 'logos', stream['icon'])
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
home = xbmc.translatePath(addon.getAddonInfo('path'))

tags = [
  {
    'name': 'Live TV',
    'id': 'LiveTV',
    'icon': 'livetv.png'
  }, {
    'name': 'Movies',
    'id': 'Movies',
    'icon': 'ukmovies.png'
  }
]


LiveTV = [{
  'name': 'US: Voice Clips Usa 1',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2034.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 2',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2035.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 3',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2036.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 4',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2037.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 5',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2038.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 6',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2039.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 7',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2040.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 8',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2041.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 9',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2042.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 10',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2043.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 11',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2044.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 12',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2045.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 13',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2046.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 14',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2047.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 15',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2048.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 16',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2049.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 17',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2050.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 18',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2051.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 19',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2052.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 20',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2053.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 21',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2054.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 22',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2055.mp4',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'US: Voice Clips Usa 23',
  'url': 'http://ipsatpro.com:8000/movie/156/156/2056.mp4',
  'icon': 'uk.png',
  'disabled': False  
}, {
  'name': 'Vevo 2',
  'url': 'http://pro-unibox.com:8000/live/bali/bali/59.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'SHOWTIME HD',
  'url': 'http://185.59.222.49:8000/live/D3KUeZI4CB/oQik1d8k5f/6346.ts',
  'icon': 'uk.png',
  'disabled': False  
}, {
  'name': 'Vevo 3',
  'url': 'http://pro-unibox.com:8000/live/bali/bali/60.ts',
  'icon': 'uk.png',
  'disabled': False  
}, {
  'name': 'ABC',
  'url': 'http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8?sd=10&b=1200&rebase=on',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'FOX SPORT',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/58.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'HISTORY 2',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/36.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'MLB NETWORK',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/48.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'MLS SOCCER',
  'url': 'http://208.92.36.158/ipad/live/nba_ipad_1240.m3u8',
  'icon': 'uk.png',
  'disabled': False  
}, {
  'name': 'NBA SPORTS',
  'url': 'http://208.92.36.158/ipad/live/nba_ipad_1240.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NBA TV',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/47.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'SN',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/57.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'SNWL',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/59.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'TS 1',
  'url': 'http://btv-i.akamaihd.net/hls/live/202760/btvusa_ios/P1/M18K.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'TS 3',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/54.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'TS 4',
  'url': 'http://46.166.162.35:9090/load/b0922f3fa8aa/55.m3u8',
  'icon': 'uk.png',
  'disabled': False  
}, {
  'name': 'CBS News HD',
  'url': 'http://cbsnews-linear.mdialog.com/video_assets/cbsnews.m3u8?api_key=563b80c1ae4ce359830f572d2496a947&iu=/8264/vaw-can/mobile_web/cbsnews_mobile',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CHICAGO POLICE-live audio feeds',
  'url': 'http://audio4.broadcastify.com/il_chicago_police2.mp3',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CTV News Live Events Feed 1 HD',
  'url': 'http://ams-lp10.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News18.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Euronews',
  'url': 'http://fr-par-iphone-2.cdn.hexaglobe.net/streaming/euronews_ewns/ipad_en.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'France24',
  'url': 'http://static.france24.com/live/F24_EN_LO_HLS/live_web.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NHK World',
  'url': 'http://nhkwglobal-i.akamaihd.net/hls/live/222714/nhkwglobal/index_1180.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'RTE NEWS NOW',
  'url': 'http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': '360 North Alaska',
  'url': 'http://state.ak.tvwmedia.net:1935/ktoo-live/_definst_/360north/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NASA TV HD',
  'url': 'http://nasatv-lh.akamaihd.net/i/NASA_101@319270/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': '_International Space Station Live 1',
  'url': 'http://iphone-streaming.ustream.tv/uhls/17074538/streams/live/iphone/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'International Space Station Live 2',
  'url': 'http://iphone-streaming.ustream.tv/uhls/9408562/streams/live/iphone/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'H2 USA',
  'url': 'http://fluvod1.giniko.com/all-documentaries/all-documentaries/tracks-5,6/index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Hunting Channel',
  'url': 'http://fluvod1.giniko.com/all-hunting/all-hunting/tracks-5,6/index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NDR HD',
  'url': 'http://ndr_fs-lh.akamaihd.net/i/ndrfs_nds@119224/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': ',AMG',
  'url': 'http://telvuehls_t02027-i.akamaihd.net/hls/live/213119/T02027-amgtv2/playlist_2.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Arirang',
  'url': 'http://amdlive.ctnd.com.edgesuite.net/arirang_1ch/smil:arirang_1ch.smil/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Comedy Central HD',
  'url': 'http://216.31.255.235/hlsl/1/COMEDY/COMEDY.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'E/I',
  'url': 'http://acaooyalahd2-lh.akamaihd.net/i/TBN04_delivery@186242/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'FXX HD',
  'url': 'http://216.31.255.235/hlsl/4/FXX/FXX.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'TVA Montreal',
  'url': 'http://tva_chaine_uls-lh.akamaihd.net/i/chaine_tva_1@125892/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 National HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12netw_delivery@132840/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Arizona HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12ariz_delivery@132836/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Bay Area HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12baya_delivery@132837/index_2328_av-p.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Los Angeles HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12losa_delivery@132838/index_2328_av-p.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Mountain HD',
  'url': 'http://xrxs.net/video/live-p12moun-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Oregon HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12oreg_delivery@132835/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC 12 Washington HD',
  'url': 'http://pac12hd2-lh.akamaihd.net/i/p12wash_delivery@132841/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Poker Central',
  'url': 'http://ooyalahd2-f.akamaihd.net/i/crtv01_delivery@329705/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
 }, {
  'name': 'REAL MADRID CHANNEL',
  'url': 'http://rmtvlive-lh.akamaihd.net/i/rmtv_1@154306/index_1000_av-b.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'VERSUS',
  'url': 'http://208.92.36.158/ipad/live/nba_ipad_1240.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'QVC HD',
  'url': 'http://qvclvp2.mmdlive.lldns.net/qvclvp2/9aa645c89c5447a8937537011e8f8d0d/manifest.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'The Shopping Channel HD',
  'url': 'http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-p.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'DJING ANIMATION',
  'url': 'http://djing.com/tv/a-05.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'DJING UNDERGROUND',
  'url': 'http://djing.com/tv/u-05.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'HEART TV',
  'url': 'http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/index_656_av-b.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': '_m2o TV',
  'url': 'http://m2otv-lh.akamaihd.net/i/m2oTv_1@186074/index_600_av-b.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': '_Spirit Television',
  'url': 'http://cdn.rbm.tv/rightbrainmedia-live-109/_definst_/smil:spirit_all.smil/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Dream TV',
  'url': 'http://live.netd.com.tr/S1/HLS_LIVE/dreamtv/1000/prog_index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Power Turk',
  'url': 'http://185.28.3.10/powertv/powerturktvh.stream/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'ABC News',
  'url': 'http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'AMG TV',
  'url': 'http://telvuehls_t02027-i.akamaihd.net/hls/live/213119/T02027-amgtv2/playlist_2.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Bloomberg',
  'url': 'http://cdn3.videos.bloomberg.com/btv/us/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Capital TV',
  'url': 'http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CBSN News',
  'url': 'http://cbsnews-linear.mdialog.com/video_assets/cbsnews.m3u8?api_key=563b80c1ae4ce359830f572d2496a947&iu=/8264/vaw-can/mobile_web/cbsnews_mobile',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Cinestream TV',
  'url': 'http://68.71.42.179/live/livestream1/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'France24',
  'url': 'http://f24hls-i.akamaihd.net/hls/live/221193/F24_EN_LO_HLS/master_500.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Heartv',
  'url': 'http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/index_656_av-p.m3u8?sd=10&rebase=on',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'HSN 1',
  'url': 'http://hsn.mpl.miisolutions.net:1935/hsn-live01/_definst_/mp4:420p500kB31/mp4:420p500kB31.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'London Live',
  'url': 'http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Mystery Science Theater 3000',
  'url': 'http://goo.gl/B2UPYd',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NASA TV',
  'url': 'http://nasatv-lh.akamaihd.net/i/NASA_101@319270/master.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'NHK World',
  'url': 'http://web-cache.stream.ne.jp/www11/nhkworld-tv/global/222714/live.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Arizona)',
  'url': 'http://xrxs.net/video/live-p12ariz-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Bay Area)',
  'url': 'http://xrxs.net/video/live-p12baya-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Los Angeles)',
  'url': 'http://xrxs.net/video/live-p12losa-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Mountain)',
  'url': 'http://xrxs.net/video/live-p12moun-2328.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (National)',
  'url': 'http://xrxs.net/video/live-p12netw-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Oregon)',
  'url': 'http://xrxs.net/video/live-p12oreg-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'PAC-12 Net. (Washington)',
  'url': 'http://xrxs.net/video/live-p12wash-4728.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Poker Central',
  'url': 'http://ooyalahd2-f.akamaihd.net/i/crtv01_delivery@329705/index_1164_av-b.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'QVC 1',
  'url': 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi5/1/prog_index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'QVC 2',
  'url': 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi1/1/prog_index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'QVC Beauty',
  'url': 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi6/1/prog_index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'QVC Style',
  'url': 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi8/3/prog_index.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Toonami Aftermath',
  'url': 'http://iphone-streaming.ustream.tv/uhls/19964352/streams/live/iphone/playlist.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'TSC',
  'url': 'http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-p.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'Versus',
  'url': 'http://208.92.36.158/ipad/live/nba_ipad_1240.m3u8',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'WGN News Chicago',
  'url': 'http://wgntribune-lh.akamaihd.net/i/WGNPrimary_1@304622/index_350_av-p.m3u8?',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TSN 1',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/2299.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TSN 2',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/2298.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TSN 3',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/2297.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TSN 4',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/2296.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TSN 5',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/2295.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Astro Supersport 1',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/3876.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Astro Supersport 2',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/3877.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Astro Supersport 3',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/3878.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: FOX SPORTS HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8215.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: SportsNet World',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7824.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Sportnet East',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7368.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Sportnet West',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8155.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: ESPN HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8707.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: ESPN 1',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8470.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: NHL Network',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7418.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: NFL',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6812.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: US WWE HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/4270.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: PAG HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7416.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: DIY Network HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7366.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: UFC Fight Night 88 US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10688.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Food Network',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7434.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: FX HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9674.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: FXX HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9673.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CBS HD USA',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9668.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: NBC HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9669.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HALLMARK',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6827.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: AMC HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9676.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Showtime HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6623.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: SHOWTIME HD 2',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8866.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: SHOWTIME WEST',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9670.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: SHOWTIME SHOWCASE',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9671.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HBO 2 HD US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7758.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HBO plus HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6825.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HBO East',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8069.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HBO Comedy',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7426.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HBO Signature HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6830.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Comedy Central HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8871.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Cinemax ActionMax',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7438.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Cinemax MoreMax',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7643.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Cinemax East',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7462.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz West US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10684.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz Kids US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10683.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz Encore US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10681.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz Edge US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10680.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz East US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10679.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz Comedy US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10678.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Starz Cinema US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10677.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Bravo',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6807.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: FOX 43',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10239.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: MBL HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10140.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: A&E',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10726.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: TWiT',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7424.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Fox News',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6831.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: HIFI',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6810.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: SPACE',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6806.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: byu tv',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8157.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: BLOOMBERG',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7903.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CNN US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/6814.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CNBC',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/3860.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CAPITAL TV',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7443.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: WGN',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7425.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: Poker Central',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7439.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: NASA TV',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7367.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CNBC HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7414.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CBSN US',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7820.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: PAG',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/7413.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: VH1 Classic',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/9675.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'USA: CN HD',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/8869.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CA: TVS Sports',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10240.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CA: TeleQub',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10241.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CA: Supercrun1',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10242.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'CA: SERIES',
  'url': 'http://dmtn-iptv.com:8080/live/189nad1604/189nad1604/10244.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport 1 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2964.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport 2 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2965.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport 3 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2966.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport 4 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2967.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport 5 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2968.ts',
  'icon': 'uk.png',
  'disabled': False
}, {
  'name': 'UK: Sky Sport F1 HD',
  'url': 'http://orbit-iptv.com:2500/live/mZlyLxAxAH/yPVYvQdeKh/2969.ts',
  'icon': 'uk.png',
  'disabled': False  
  
  
  
}]


Movies = [{
  'name': 'The Terminator',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/309.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Zootopia',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1986.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Winters Tale',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1988.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Independence Day',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1984.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Grimsby',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1985.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Batman: The Killing Joke',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1987.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Batman v Superman: Dawn of Justice',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1983.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Conjuring',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/1982.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Vijay',
  'url': 'http://mediaiptv.xyz:8000/live/cheesy/cheesy/1973.ts',
  'icon': 'ukmovies.png',
  'disabled': False  
}, {
  'name': 'Terminator Salvation',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/308.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Terminator Genisys',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/310.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Terminator 3: Rise of the Machines',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/307.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'X-Men: Days of Future Past',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/243.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Wrath of the Titans',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/298.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'TRON: Legacy',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/279.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Transformers: Age of Extinction',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/280.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Tooth Fairy',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/227.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Tinker Bell and the Great Fairy Rescue',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/253.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Nutty Professor (1996)',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/295.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Mummy (1999)',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/297.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Maze Runner',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/278.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Great Gatsby',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/246.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Day After Tomorrow',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/288.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'The Book of Eli',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/289.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Terminator 2: Judgment Day',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/259.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Star Trek',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/283.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Se7en',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/274.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Riddick',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/285.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Real Steel',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/258.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Quantum of Solace',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/270.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Point Break',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/249.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Ouija',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/303.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Now You See Me',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/275.mp4',
  'icon': 'ukmovies.png',
  'disabled': False
}, {
  'name': 'Mrs. Browns Boys DMovie',
  'url': 'http://mediaiptv.xyz:8000/movie/cheesy/cheesy/252.mp4',
  'icon': 'ukmovies.png',
  'disabled': False  
  
}]


streams = {
  'LiveTV': sorted((i for i in LiveTV if not i.get('disabled', False)), key=lower_getter('name')),
  'Movies': sorted((i for i in Movies if not i.get('disabled', False)), key=lower_getter('name')),
  # 'LiveTV': sorted(LiveTV, key=lower_getter('name')),
  # 'Movies': sorted(Movies, key=lower_getter('name')),
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
