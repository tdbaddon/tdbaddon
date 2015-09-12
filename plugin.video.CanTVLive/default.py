import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,base64


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = '[B]P2P-Streams[/B] addon required for sports channels'
line2 = 'More Info: http://tinyurl.com/p2pstreamsconfig'
line3 = 'CTV Channels require Filmon.TV from kinkin repo'

 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)

plugin_handle = int(sys.argv[1])

_id = 'plugin.video.CanTVLive'
_icondir = "special://home/addons/" + _id + "/icons/"
_resources = "special://home/addons/" + _id + "/resources/"

fanart = "special://home/addons/" + _id + '/fanart.jpg'
icon = xbmc.translatePath(os.path.join('special://home/addons/' + _id, 'TSN_icon.png'))

def add_video_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=False)
	
def add_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'False')
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=True)


# Test

add_video_item('http://t2.llcdn.quickplay.com/live/hls/3505/s/livech3713/004.m3u8',{ 'title': 'INFO'}, '%s/links.png'% _icondir)

# Bonus

add_video_item('https://raw.githubusercontent.com/podgod/podgod/master/resources/Canada.m3u',{ 'title': 'Bonus Channels - DOWN'}, '%s/canada.png'% _icondir)

	
# Entertainment
add_video_item('http://link.theplatform.com/s/dtjsEC/77l1KA_G_5P1?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Halifax HD'}, '%s/GlobalHalifax.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/EqBPGYLY6fEx?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Vancouver HD'}, '%s/GlobalBC.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/hdSH3iztz_j_?feed=DEV%20Live%20Stream%20Feed',{ 'title': 'Global TV Toronto HD'}, '%s/GlobalToronto.png'% _icondir)
add_video_item('plugin://plugin.video.F.T.V/?url=http%3A%2F%2Fwww.filmon.com%2Fchannel%2Fcfcn-5-ctv-lethbridge&mode=125&name=CFCN-5+CTV+Lethbridge&iconimage=http%3A%2F%2Fstatic.filmon.com%2Fcouch%2Fchannels%2F2059%2Fextra_big_logo.png&start=cfcn-5-ctv-lethbridge&ch_fanart=2059',{ 'title': 'CFCN CTV Lethbridge'}, '%s/CTV_Lethbridge.png'% _icondir)
add_video_item('plugin://plugin.video.F.T.V/?url=http%3A%2F%2Fwww.filmon.com%2Fchannel%2Fcfrn-ctv-edmonton&mode=125&name=CFRN+CTV+Edmonton&iconimage=http%3A%2F%2Fstatic.filmon.com%2Fcouch%2Fchannels%2F2053%2Fextra_big_logo.png&start=cfrn-ctv-edmonton&ch_fanart=2053',{ 'title': 'CFRN CTV Edmonton'}, '%s/CTV_Edmonton.png'% _icondir)
add_video_item('plugin://plugin.video.F.T.V/?url=http%3A%2F%2Fwww.filmon.com%2Fchannel%2Fcicc-ctv-yorkton&mode=125&name=CICC+CTV+Yorkton&iconimage=http%3A%2F%2Fstatic.filmon.com%2Fcouch%2Fchannels%2F2062%2Fextra_big_logo.png&start=cicc-ctv-yorkton&ch_fanart=2062',{ 'title': 'CICC CTV Yorkton'}, '%s/CTV_Yorkton.png'% _icondir)
add_video_item('plugin://plugin.video.F.T.V/?url=http%3A%2F%2Fwww.filmon.com%2Fchannel%2Fckck-ctv-regina&mode=125&name=CKCK+CTV+Regina&iconimage=http%3A%2F%2Fstatic.filmon.com%2Fcouch%2Fchannels%2F2056%2Fextra_big_logo.png&start=ckck-ctv-regina&ch_fanart=2056',{ 'title': 'CKCK CTV Regina'}, '%s/CTV_Regina.png'% _icondir)
add_video_item('rtmp://54.85.197.21:1935/live/news live=1 timeout=15',{ 'title': '[COLOR yellow]CHCH Hamilton HD[/COLOR]'}, '%s/CHCH_.png'% _icondir)
add_video_item('http://link.theplatform.com/s/dtjsEC/chjdYJxKb44V?manifest=m3u&feed=History%20Live%20Stream%20Feed',{ 'title': 'History (Canada) HD'}, '%s/history.png'% _icondir)
add_video_item('http://bcoveliveios-i.akamaihd.net/hls/live/207737/1942203455001/nat/master_Layer5.m3u8',{ 'title': 'Weather Network National HD'}, '%s/twn.png' % _icondir)
#DOWN add_video_item('http://bcoveliveios-i.akamaihd.net/hls/live/207737/1942203455001/atl/master.m3u8',{ 'title': 'Weather Network Atlantic HD'}, '%s/twn.png' % _icondir)
add_video_item('http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-p.m3u8',{ 'title': 'The Shopping Channel HD'}, '%s/tsc.png'% _icondir)
add_video_item('http://tscstreaming-lh.akamaihd.net/i/TSCLiveStreaming_1@91031/index_3_av-b.m3u8',{ 'title': 'The Shopping Channel HD Alternate Link'}, '%s/tsc.png'% _icondir)
add_video_item('http://btflash-lh.akamaihd.net/i/BTTOFLASH_live@120219/master.m3u8',{ 'title': '[COLOR yellow]City TV Toronto HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTMTLFLASH_live@120220/master.m3u8',{ 'title': '[COLOR yellow]City TV Montreal HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTVANFLASH_live@120224/master.m3u8',{ 'title': '[COLOR yellow]City TV Vancouver HD[/COLOR]'}, '%s/CityTV.png'% _icondir)	
add_video_item('http://btflash-lh.akamaihd.net/i/BTCALFLASH_live@120221/master.m3u8',{ 'title': '[COLOR yellow]City TV Calgary HD[/COLOR]'}, '%s/CityTV.png'% _icondir)
add_video_item('http://supertv.gq/toonf/2620.m3u8',{ 'title': '[COLOR red]Teletoon[/COLOR]'}, '%s/teletoon.png'% _icondir)

# News
add_video_item('http://bcliveuniv-lh.akamaihd.net/i/cpac1eng2014_01@119330/index_2000_av-p.m3u8',{ 'title': 'CPAC HD'}, '%s/cpac-english.png'% _icondir)
add_video_item('http://bcliveuniv-lh.akamaihd.net/i/cpac1flr2014_01@51230/index_2000_av-p.m3u8',{ 'title': 'CPAC HD Alternate Link'}, '%s/cpac-english.png'% _icondir)
add_video_item('rtmp://c.cdn.newschat.tv/edge playpath=cbc_live swfUrl=http://newschat.tv/player.swf live=1 live=true pageUrl=http://www.livenewschat.eu/canada/',{ 'title': 'CBC News'}, '%s/cbcnewsnetwork.png' % _icondir)
#DOWN add_video_item('http://ams-lp3.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/cp24Open8.m3u8',{ 'title': 'CP24 News HD'}, '%s/CP24.png' % _icondir)
add_video_item('http://66.51.129.171:8080/demo/index.m3u8',{ 'title': 'CTV News HD'}, '%s/ctv_news.png' % _icondir)
add_video_item('http://ams-lp10.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News18.m3u8',{ 'title': 'CTV News Live Feed 1 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp7.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News28.m3u8',{ 'title': 'CTV News Live Feed 2 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp6.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News38.m3u8',{ 'title': 'CTV News Live Feed 3 HD'}, '%s/CTVNews.png' % _icondir)
add_video_item('http://ams-lp5.9c9media.com/hls-live/livepkgr/_definst_/liveNews/News48.m3u8',{ 'title': 'CTV News Live Feed 4 HD'}, '%s/CTVNews.png' % _icondir)

#Sports
add_video_item('http://nlds187.cdnak.neulion.com/nlds/sportsnetnow/sn_360/as/live/sn_360_hd_ipad.m3u8',{ 'title': '[COLOR red]SportsNet 360 HD[/COLOR]'}, '%s/sportsnet_360.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13094.acelive&mode=1&name=SportsNet+HD',{ 'title': 'SportsNet HD'}, '%s/sportsnet_one.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13028.acelive&mode=1&name=SportsNet+World+HD',{ 'title': 'SportsNet World HD'}, '%s/sportsnet_world.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13091.acelive&mode=1&name=TSN+1+HD',{ 'title': 'TSN 1 HD'}, '%s/tsn_1.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13092.acelive&mode=1&name=TSN+2+HD',{ 'title': 'TSN 2 HD'}, '%s/tsn_2.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13093.acelive&mode=1&name=TSN+3+HD',{ 'title': 'TSN 3 HD'}, '%s/tsn_3.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13096.acelive&mode=1&name=TSN+4+HD',{ 'title': 'TSN 4 HD'}, '%s/tsn_4.png' % _icondir)
add_video_item('plugin://plugin.video.p2p-streams/?url=http://content.torrent-tv.ru/13097.acelive&mode=1&name=TSN+5+HD',{ 'title': 'TSN 5 HD'}, '%s/tsn_5.png' % _icondir)

# French
add_video_item('http://hdflash_1-lh.akamaihd.net/i/cancbft_1@95875/index_1200_av-p.m3u8',{ 'title': 'CANCBFT (CBC French) HD'}, '%s/CBFT.png' % _icondir)
add_video_item('http://hdflash_1-lh.akamaihd.net/i/cancbft_1@95875/index_1200_av-b.m3u8',{ 'title': 'CANCBFT (CBC French) HD Alternate Link'}, '%s/CBFT.png' % _icondir)
add_video_item('rtmp://cp39414.live.edgefcs.net:443/live playpath=argent@9751 swfUrl=http://fpdownload.adobe.com/strobe/FlashMediaPlayback_101.swf/[[DYNAMIC]]/1 live=1 pageUrl=http://tele-en-direct.blogspot.com/2014/05/argent-tv-canada-en-direct.html',{ 'title': 'Argent (French)'}, '%s/argent.png' % _icondir)
add_video_item('rtmp://cp39414.live.edgefcs.net/live/ playpath=lcn2@9754 swfUrl=http://www.centraltv.fr/jwplayer/jwplayer.flash.swf live=1 pageUrl=http://www.centraltv.fr/canada-television/lcn-news',{ 'title': 'LCN News (French)'}, '%s/lcn.png' % _icondir)
add_video_item('http://frlive.artestras.cshls.lldns.net/artestras/contrib/frlive/frlive_925.m3u8',{ 'title': 'ARTE (French)'}, '%s/arte.png' % _icondir)




xbmcplugin.endOfDirectory(int(sys.argv[1]))

xbmc.executebuiltin("Container.SetViewMode(500)")

