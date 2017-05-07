import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net,xbmc
import xbmcaddon
import json
from cookielib import CookieJar
from resources.lib.modules.common import *
from resources.lib.modules.plugintools import *

addon_id  = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
fanart    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeview', 'fanart.jpg'))
logos     = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeview/resources/logos', ''))
logos_tvp = 'https://assets.tvplayer.com/common/logos/256/Inverted/'

def getChannels():
	addLink('4Music','128',2,logos_tvp+'128.png')
	#addLink('4seven','565',2,logos_tvp+'565.png')
	#addLink('5*','566',2,logos_tvp+'566.png')
	addLink('Al Jazeera','146',2,logos_tvp+'146.png')
	addLink('BBC Alba','236',2,logos_tvp+'236.png')
	addLink('BBC Four HD','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'110.png')
	addLink('BBC Four','110',2,logos_tvp+'110.png')
	addLink('BBC News HD','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'111.png')
	addLink('BBC News','111',2,logos_tvp+'111.png')
	addLink('BBC One HD','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
	addLink('BBC One','89',2,logos_tvp+'89.png')
	addLink('BBC One Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
	addLink('BBC One Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
	addLink('BBC One Wales','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
	addLink('BBC Two Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
	addLink('BBC Two Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
	addLink('BBC Two Wales','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
	addLink('BBC Parliament','345',2,logos_tvp+'345.png')
	addLink('BBC Two HD','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'90.png')
	addLink('BBC Two','90',2,logos_tvp+'90.png')
	#addLink('BET: Black Entertainment Television','572',2,logos_tvp+'572.png')
	addLink('Blaze','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1,logos+'blaze.png')
	addLink('Bloomberg','514',2,logos_tvp+'514.png')
	addLink('The Box','129',2,logos_tvp+'129.png')
	addLink('Box Hits','130',2,logos_tvp+'130.png')
	addLink('Box Upfront','158',2,logos_tvp+'158.png')
	addLink('Capital TV','157',2,logos_tvp+'157.png')
	addLink('CBBC HD','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'113.png')
	addLink('CBBC','113',2,logos_tvp+'113.png')
	addLink('CBeebies HD','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'114.png')
	addLink('CBeebies','114',2,logos_tvp+'114.png')
	addLink('Channel 4','92',2,logos_tvp+'92.png')
	addLink('Channel 5','574',2,logos_tvp+'574.png')
	addLink('Channel AKA','227',2,logos_tvp+'227.png')
	addLink('Chilled','226',2,logos_tvp+'226.png')
	addLink('CITV','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1,logos+'citv.png')
	addLink('Clubland','225',2,logos_tvp+'225.png')
	addLink('CNN International','286',2,logos_tvp+'286.png')
	addLink('Community Channel','259',2,logos_tvp+'259.png')
	#addLink('The Craft Channel','554',2,logos_tvp+'554.png')
	addLink('Dave','300',2,logos_tvp+'300.png')
	addLink('Dave ja vu','317',2,logos_tvp+'317.png')
	addLink('Drama','346',2,logos_tvp+'346.png')
	addLink('Food Network','125',2,logos_tvp+'125.png')
	addLink('Food Network+1','254',2,logos_tvp+'254.png')
	addLink('Forces TV','555',2,logos_tvp+'555.png')
	addLink('Heart TV','153',2,logos_tvp+'153.png')
	addLink('Home','512',2,logos_tvp+'512.png')
	addLink('ITV1','204',2,logos_tvp+'204.png')
	addLink('ITV2','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1,logos+'itv2.png')
	addLink('ITV3','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1,logos+'itv3.png')
	addLink('ITV4','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1,logos+'itv4.png')
	addLink('ITVBe','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1,logos+'itvbe.png')
	#addLink('The Jewellery Channel','545',2,logos_tvp+'545.png')
	#addLink('Keep It Country','569',2,logos_tvp+'569.png')
	addLink('Kerrang!','133',2,logos_tvp+'133.png')
	addLink('Kiss','131',2,logos_tvp+'131.png')
	addLink('London Live','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1,logos+'londonlive.png')
	addLink('Magic','132',2,logos_tvp+'132.png')
	#addLink('More4','563',2,logos_tvp+'563.png')
	addLink('NOW Music','228',2,logos_tvp+'228.png')
	addLink('QUEST','327',2,logos_tvp+'327.png')
	#addLink('QUEST+1','336',2,logos_tvp+'336.png')
	addLink('QVC Beauty','250',2,logos_tvp+'250.png')
	addLink('QVC Extra','248',2,logos_tvp+'248.png')
	addLink('QVC Plus','344',2,logos_tvp+'344.png')
	addLink('QVC Style','249',2,logos_tvp+'249.png')
	addLink('QVC','247',2,logos_tvp+'247.png')
	addLink('Really','306',2,logos_tvp+'306.png')
	addLink('S4C','251',2,logos_tvp+'251.png')
	addLink('Sky News','https://www.youtube.com/watch?v=y60wDzZt8yg',1,logos+'skynews.png')
	#addLink('Spike','568',2,logos_tvp+'568.png')
	addLink('Travel Channel','126',2,logos_tvp+'126.png')
	addLink('Travel Channel+1','255',2,logos_tvp+'255.png')
	addLink('Yesterday','308',2,logos_tvp+'308.png')
	addLink('Yesterday+1','318',2,logos_tvp+'318.png')
	#addLink('truTV','295',2,logos_tvp+'295.png')
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	
		

def getChannelsOld():
	if selfAddon.getSetting('list_all') == 'true':  
		addLink('4Music | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8',1,logos_tvp+'128.png')
		addLink('4Music | TVPlayer','128',2,logos_tvp+'128.png')
		addLink('5* | FilmOn','https://www.filmon.com/tv/5-star',1,logos_tvp+'566.png')
		addLink('5* | TVPlayer','566',2,logos_tvp+'566.png')
		addLink('Spike | TVPlayer','568',2,logos_tvp+'568.png')
		addLink('5USA | FilmOn','https://www.filmon.com/tv/5usa',1,logos+'5usa.png')
		addLink('Al Jazeera | TVPlayer','146',2,logos_tvp+'146.png')
		addLink('Al Jazeera | FilmOn','https://www.filmon.com/tv/al-jazeera',1,logos_tvp+'146.png')
		addLink('BBC Alba | TVPlayer','236',2,logos_tvp+'236.png')
		addLink('BBC Alba | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_alba/bbc_alba.isml/bbc_alba-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'236.png')
		addLink('BBC Four HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'110.png')
		addLink('BBC Four | TVPlayer','110',2,logos_tvp+'110.png')
		addLink('BBC Four | FilmOn','https://www.filmon.com/tv/cbeebiesbbc-four',1,logos_tvp+'110.png')
		addLink('BBC News HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'111.png')
		addLink('BBC News | TVPlayer','111',2,logos_tvp+'111.png')
		addLink('BBC News | FilmOn','https://www.filmon.com/tv/bbc-news',1,logos_tvp+'111.png')
		addLink('BBC One HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		addLink('BBC One | TVPlayer','89',2,logos_tvp+'89.png')
		addLink('BBC One | FilmOn','https://www.filmon.com/tv/bbc-one',1,logos_tvp+'89.png')
		addLink('BBC One Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		addLink('BBC One Northern Ireland | FilmOn','https://www.filmon.com/tv/bbc-1-north-ireland',1,logos_tvp+'89.png')
		addLink('BBC One Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		addLink('BBC One Scotland | FilmOn','https://www.filmon.com/tv/bbc-1-scotland',1,logos_tvp+'89.png')
		addLink('BBC One Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		addLink('BBC One Wales | FilmOn','https://www.filmon.com/tv/bbc-1-wales',1,logos_tvp+'89.png')
		addLink('BBC Two Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		addLink('BBC Two Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		addLink('BBC Two Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		addLink('BBC Parliament | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'345.png')
		addLink('BBC Parliament | TVPlayer','345',2,logos_tvp+'345.png')
		addLink('BBC Parliament | FilmOn','https://www.filmon.com/tv/bbc-parliament',1,logos_tvp+'345.png')
		addLink('BBC Two HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'90.png')
		addLink('BBC Two | TVPlayer','90',2,logos_tvp+'90.png')
		addLink('BBC Two | FilmOn','https://www.filmon.com/tv/bbc-two',1,logos_tvp+'90.png')
		addLink('Bloomberg | TVPlayer','514',2,logos_tvp+'514.png')
		addLink('Bloomberg | FilmOn','https://www.filmon.com/tv/bloomberg',1,logos_tvp+'514.png')
		addLink('The Box | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8',1,logos_tvp+'129.png')
		addLink('The Box | TVPlayer','129',2,logos_tvp+'129.png')
		addLink('Box Hits | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'158.png')
		addLink('Box Hits | TVPlayer','130',2,logos_tvp+'130.png')
		addLink('Box Upfront | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8',1,logos_tvp+'158.png')
		addLink('Box Upfront | TVPlayer','158',2,logos_tvp+'158.png')
		addLink('Capital TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',1,logos_tvp+'157.png')
		addLink('Capital TV | TVPlayer','157',2,logos_tvp+'157.png')
		addLink('CBBC HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'113.png')
		addLink('CBBC | TVPlayer','113',2,logos_tvp+'113.png')
		addLink('CBBC | FilmOn','https://www.filmon.com/tv/cbbc',1,logos_tvp+'113.png')
		addLink('CBeebies HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'114.png')
		addLink('CBeebies | TVPlayer','114',2,logos_tvp+'114.png')
		addLink('CBeebies | FilmOn','https://www.filmon.com/tv/cbeebies',1,logos_tvp+'114.png')
		addLink('CBS Action | FilmOn','https://www.filmon.com/tv/cbs-action',1,logos+'cbsaction.png')
		addLink('CBS Drama | FilmOn','https://www.filmon.com/tv/cbs-drama',1,logos+'cbsdrama.png')
		addLink('CBS Reality | FilmOn','https://www.filmon.com/tv/cbs-reality',1,logos+'cbsreality.png')
		addLink('CBS Reality+1 | FilmOn','https://www.filmon.com/tv/cbs-reality1',1,logos+'cbsreality.png')
		addLink('Channel 4 | TVPlayer','92',2,logos_tvp+'92.png')
		addLink('Channel 4 | FilmOn','https://www.filmon.com/tv/channel-4',1,logos_tvp+'92.png')
		addLink('Channel 5 | TVPlayer','574',2,logos_tvp+'574.png')
		addLink('Channel 5 | FilmOn','https://www.filmon.com/tv/channel-5',1,logos_tvp+'93.png')
		addLink('Channel AKA | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8',1,logos_tvp+'227.png')
		addLink('Channel AKA | TVPlayer','227',2,logos_tvp+'227.png')
		addLink('Chilled | TVPlayer','226',2,logos_tvp+'226.png')
		addLink('CITV | ITV Hub','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1,logos+'citv.png')
		addLink('Clubbing TV | FilmOn','https://www.filmon.com/tv/clubbing-tv',1,logos+'clubbingtv.png')
		addLink('Clubland | TVPlayer','225',2,logos_tvp+'225.png')
		addLink('CNN International | TVPlayer','286',2,logos_tvp+'286.png')
		addLink('Community Channel | TVPlayer','259',2,logos_tvp+'259.png')
		addLink('The Craft Channel | TVPlayer','554',2,logos_tvp+'554.png')
		addLink('Dave | TVPlayer','300',2,logos_tvp+'300.png')
		addLink('Dave ja vu | TVPlayer','317',2,logos_tvp+'317.png')
		addLink('Drama | TVPlayer','346',2,logos_tvp+'346.png')
		addLink('E4 | FilmOn','https://www.filmon.com/tv/e4',1,logos_tvp+'562.png')
		addLink('Film4 | FilmOn','https://www.filmon.com/tv/film-4',1,logos_tvp+'564.png')
		addLink('Food Network | TVPlayer','125',2,logos_tvp+'125.png')
		addLink('Food Network | FilmOn','http://www.filmon.com/tv/food-network',1,logos_tvp+'125.png')
		addLink('Food Network+1 | TVPlayer','254',2,logos_tvp+'254.png')
		addLink('Food Network+1 | FilmOn','http://www.filmon.com/tv/food-network-plus-1',1,logos_tvp+'254.png')
		addLink('Forces TV | TVPlayer','555',2,logos_tvp+'555.png')
		addLink('Heart TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8',1,logos_tvp+'153.png')
		addLink('Heart TV | TVPlayer','153',2,logos_tvp+'153.png')
		addLink('Home | TVPlayer','512',2,logos_tvp+'512.png')
		addLink('Horror Channel | FilmOn','https://www.filmon.com/tv/horror-channel',1,logos+'horrorchannel.png')
		addLink('ITV1 | ITV Hub','http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8',1,logos_tvp+'204.png')
		addLink('ITV1 | TVPlayer','204',2,logos_tvp+'204.png')
		addLink('ITV1 | FilmOn','http://www.filmon.com/tv/itv1',1,logos_tvp+'204.png')
		addLink('ITV1+1 | FilmOn','https://www.filmon.com/tv/itv-plus-1',1,logos_tvp+'204.png')
		addLink('ITV2 | ITV Hub','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1,logos+'itv2.png')
		addLink('ITV2 | FilmOn','http://www.filmon.com/tv/itv2',1,logos+'itv2.png')
		addLink('ITV2+1 | FilmOn','https://www.filmon.com/tv/itv2-plus-1',1,logos+'itv2.png')
		addLink('ITV3 | ITV Hub','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1,logos+'itv3.png')
		addLink('ITV3 | FilmOn','http://www.filmon.com/tv/itv3',1,logos+'itv3.png')
		addLink('ITV3+1 | FilmOn','https://www.filmon.com/tv/itv3-plus-1',1,logos+'itv3.png')
		addLink('ITV4 | ITV Hub','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1,logos+'itv4.png')
		addLink('ITV4 | FilmOn','http://www.filmon.com/tv/itv4',1,logos+'itv4.png')
		addLink('ITV4+1 | FilmOn','https://www.filmon.com/tv/itv4-plus-1',1,logos+'itv4.png')
		addLink('ITVBe | ITV Hub','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1,logos+'itvbe.png')
		addLink('ITVBe | FilmOn','http://www.filmon.com/tv/itvbe',1,logos+'itvbe.png')
		addLink('The Jewellery Channel | Direct','https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8',1,logos_tvp+'545.png')
		addLink('The Jewellery Channel | TVPlayer','545',2,logos_tvp+'545.png')
		addLink('Keep It Country | TVPlayer','569',2,logos_tvp+'569.png')
		addLink('Kerrang! | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8',1,logos_tvp+'133.png')
		addLink('Kerrang! | TVPlayer','133',2,logos_tvp+'133.png')
		addLink('Kiss | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8',1,logos_tvp+'131.png')
		addLink('Kiss | TVPlayer','131',2,logos_tvp+'131.png')
		addLink('Kix! | FilmOn','https://www.filmon.com/tv/kix',1,logos+'kix.png')
		addLink('London Live | Direct','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1,logos+'londonlive.png')
		addLink('Magic | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'132.png')
		addLink('Magic | TVPlayer','132',2,logos_tvp+'132.png')
		addLink('More4 | FilmOn','https://www.filmon.com/tv/more4',1,logos+'more4.png')
		addLink('NOW Music | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8',1,logos_tvp+'228.png')
		addLink('NOW Music | TVPlayer','228',2,logos_tvp+'228.png')
		addLink('POP | FilmOn','https://www.filmon.com/tv/pop',1,logos+'pop.png')
		addLink('Pick | FilmOn','https://www.filmon.com/tv/pick-tv',1,logos+'pick.png')
		addLink('QUEST | TVPlayer','327',2,logos_tvp+'327.png')
		addLink('QUEST | FilmOn','http://www.filmon.tv/tv/quest',1,logos_tvp+'327.png')
		addLink('QUEST+1 | TVPlayer','336',2,logos_tvp+'336.png')
		addLink('QVC Beauty | TVPlayer','250',2,logos_tvp+'250.png')
		addLink('QVC Extra | TVPlayer','248',2,logos_tvp+'248.png')
		addLink('QVC Plus | TVPlayer','344',2,logos_tvp+'344.png')
		addLink('QVC Style | TVPlayer','249',2,logos_tvp+'249.png')
		addLink('QVC | TVPlayer','247',2,logos_tvp+'247.png')
		addLink('Really | TVPlayer','306',2,logos_tvp+'306.png')
		addLink('Really | FilmOn','http://www.filmon.tv/tv/really',1,logos_tvp+'306.png')
		addLink('S4C | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_9/live/s4cpbs/s4cpbs.isml/s4cpbs-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'251.png')
		addLink('S4C | TVPlayer','251',2,logos_tvp+'251.png')
		addLink('Sky News | YouTube','https://www.youtube.com/watch?v=y60wDzZt8yg',1,logos+'skynews.png')
		addLink('Tiny Pop | FilmOn','https://www.filmon.com/tv/tiny-pop',1,logos+'tinypop.png')
		addLink('Travel Channel | TVPlayer','126',2,logos_tvp+'126.png')
		addLink('Travel Channel+1 | TVPlayer','255',2,logos_tvp+'255.png')
		addLink('Travel Channel+1 | FilmOn','http://www.filmon.tv/tv/travel-channel1',1,logos_tvp+'255.png')
		addLink('Yesterday | TVPlayer','308',2,logos_tvp+'308.png')
		addLink('Yesterday | FilmOn','http://www.filmon.tv/tv/yesterday',1,logos_tvp+'308.png')
		addLink('Yesterday+1 | TVPlayer','318',2,logos_tvp+'318.png')
		addLink('truTV | Direct','http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'295.png')
		addLink('truTV | TVPlayer','295',2,logos_tvp+'295.png')
		addLink('truTV | FilmOn','http://www.filmon.tv/tv/tru-tv',1,logos_tvp+'295.png')
		addLink('Blaze | Direct','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1,logos+'blaze.png')
		addLink('Bet | TVPlayer','572',2,logos_tvp+'572.png')
		addLink('ITVBe | TVPlayer','557',2,logos_tvp+'557.png')
		addLink('ITV2 | TVPlayer','556',2,logos_tvp+'556.png')
		addLink('ITV3 | TVPlayer','558',2,logos_tvp+'558.png')
		addLink('ITV4 | TVPlayer','559',2,logos_tvp+'559.png')
		addLink('CITV | TVPlayer','560',2,logos_tvp+'560.png')
		addLink('4seven | TVPlayer','565',2,logos_tvp+'565.png')
		addLink('More4 | TVPlayer','563',2,logos_tvp+'563.png')
		addLink('E4 | TVPlayer','562',2,logos_tvp+'562.png')
		addLink('Film4 | TVPlayer','564',2,logos_tvp+'564.png')
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

	else:	
		#4Music
		if selfAddon.getSetting('four_music') == 'Direct': addLink('4Music','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8',1,logos_tvp+'128.png')
		if selfAddon.getSetting('four_music') == 'TVPlayer': addLink('4Music','298',2,logos_tvp+'128.png')
		
		#4seven
		if selfAddon.getSetting('four_seven') == 'TVPlayer': addLink('4seven','565',2,logos_tvp+'565.png')
		
		#5*
		if selfAddon.getSetting('five_star') == 'FilmOn': addLink('5*','https://www.filmon.com/tv/5-star',1,logos_tvp+'566.png')
		if selfAddon.getSetting('five_star') == 'TVPlayer': addLink('5*','566',2,logos_tvp+'566.png')
		
		#5USA
		if selfAddon.getSetting('five_usa') == 'FilmOn': addLink('5USA','https://www.filmon.com/tv/5usa',1,logos+'5usa.png')
		
		#Al Jazeera
		if selfAddon.getSetting('al_jazeera') == 'TVPlayer': addLink('Al Jazeera','146',2,logos_tvp+'146.png')
		if selfAddon.getSetting('al_jazeera') == 'FilmOn': addLink('Al Jazeera','https://www.filmon.com/tv/al-jazeera',1,logos_tvp+'146.png')
		
		#BBC ALBA
		if selfAddon.getSetting('bbc_alba') == 'TVPlayer': addLink('BBC Alba','236',2,logos_tvp+'236.png')
		if selfAddon.getSetting('bbc_alba') == 'BBC iPlayer': addLink('BBC Alba','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_alba/bbc_alba.isml/bbc_alba-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'236.png')
		
		#BBC Four
		if selfAddon.getSetting('bbc_four') == 'BBC iPlayer': addLink('BBC Four HD','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'110.png')
		if selfAddon.getSetting('bbc_four') == 'TVPlayer': addLink('BBC Four','110',2,logos_tvp+'110.png')
		if selfAddon.getSetting('bbc_four') == 'FilmOn': addLink('BBC Four','https://www.filmon.com/tv/cbeebiesbbc-four',1,logos_tvp+'110.png')
		
		#BBC News
		if selfAddon.getSetting('bbc_news') == 'BBC iPlayer': addLink('BBC News HD','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'111.png')
		if selfAddon.getSetting('bbc_news') == 'TVPlayer': addLink('BBC News','111',2,logos_tvp+'111.png')
		if selfAddon.getSetting('bbc_news') == 'FilmOn': addLink('BBC News','https://www.filmon.com/tv/bbc-news',1,logos_tvp+'111.png')
		
		#BBC One
		if selfAddon.getSetting('bbc_one') == 'BBC iPlayer': addLink('BBC One HD','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one') == 'TVPlayer': addLink('BBC One','89',2,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one') == 'FilmOn': addLink('BBC One','https://www.filmon.com/tv/bbc-one',1,logos_tvp+'89.png')
		
		#BBC One Northern Ireland
		if selfAddon.getSetting('bbc_one_ni') == 'BBC iPlayer': addLink('BBC One Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_ni') == 'FilmOn': addLink('BBC One Northern Ireland','https://www.filmon.com/tv/bbc-1-north-ireland',1,logos_tvp+'89.png')
		
		#BBC Scotland
		if selfAddon.getSetting('bbc_one_scotland') == 'BBC iPlayer': addLink('BBC One Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_scotland') == 'FilmOn': addLink('BBC Scotland','https://www.filmon.com/tv/bbc-1-scotland',1,logos_tvp+'89.png')
		
		#BBC One Wales
		if selfAddon.getSetting('bbc_one_wales') == 'BBC iPlayer': addLink('BBC One Wales','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_wales') == 'FilmOn': addLink('BBC One Wales','https://www.filmon.com/tv/bbc-1-wales',1,logos_tvp+'89.png')
		
		#BBC Two Northern Ireland
		if selfAddon.getSetting('bbc_two_ni') == 'BBC iPlayer': addLink('BBC Two Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		
		#BBC Two Scotland
		if selfAddon.getSetting('bbc_two_scotland') == 'BBC iPlayer': addLink('BBC Two Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		
		#BBC Two Wales
		if selfAddon.getSetting('bbc_two_wales') == 'BBC iPlayer': addLink('BBC Two Wales','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'90.png')
		
		#BBC Parliament
		if selfAddon.getSetting('bbc_par') == 'BBC iPlayer': addLink('BBC Parliament','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'345.png')
		if selfAddon.getSetting('bbc_par') == 'TVPlayer': addLink('BBC Parliament','345',2,logos_tvp+'345.png')
		if selfAddon.getSetting('bbc_par') == 'FilmOn': addLink('BBC Parliament','https://www.filmon.com/tv/bbc-parliament',1,logos_tvp+'345.png')
		
		#BBC Two
		if selfAddon.getSetting('bbc_two') == 'BBC iPlayer': addLink('BBC Two HD','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'90.png')
		if selfAddon.getSetting('bbc_two') == 'TVPlayer': addLink('BBC Two','90',2,logos_tvp+'90.png')
		if selfAddon.getSetting('bbc_two') == 'FilmOn': addLink('BBC Two','https://www.filmon.com/tv/bbc-two',1,logos_tvp+'90.png')
		
        #BET
		if selfAddon.getSetting('bet') == 'TVPlayer': addLink('BET','572',2,logos_tvp+'572.png')
		
		
		#Blaze
		if selfAddon.getSetting('blaze') == 'Direct': addLink('Blaze','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1,logos+'blaze.png')

		#Bloomberg
		if selfAddon.getSetting('bloomberg') == 'TVPlayer': addLink('Bloomberg','514',2,logos_tvp+'514.png')
		if selfAddon.getSetting('bloomberg') == 'FilmOn': addLink('Bloomberg','https://www.filmon.com/tv/bloomberg',1,logos_tvp+'514.png')
		
		#The Box
		if selfAddon.getSetting('the_box') == 'Direct': addLink('The Box','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8',1,logos_tvp+'129.png')
		if selfAddon.getSetting('the_box') == 'TVPlayer': addLink('The Box','129',2,logos_tvp+'129.png')
		
		#Box Hits
		if selfAddon.getSetting('box_hits') == 'Direct': addLink('Box Hits','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'130.png')
		if selfAddon.getSetting('box_hits') == 'TVPlayer': addLink('Box Hits','130',2,logos_tvp+'130.png')
		
		#Box Upfront
		if selfAddon.getSetting('box_up') == 'Direct': addLink('Box Upfront','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8',1,logos_tvp+'158.png')
		if selfAddon.getSetting('box_up') == 'TVPlayer': addLink('Box Upfront','158',2,logos_tvp+'158.png')
		
		#Capital TV
		if selfAddon.getSetting('capital') == 'Direct': addLink('Capital TV','http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',1,logos_tvp+'157.png')
		if selfAddon.getSetting('capital') == 'TVPlayer': addLink('Capital TV','157',2,logos_tvp+'157.png')
		
		#CBBC
		if selfAddon.getSetting('cbbc') == 'BBC iPlayer': addLink('CBBC HD','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'113.png')
		if selfAddon.getSetting('cbbc') == 'TVPlayer': addLink('CBBC','113',2,logos_tvp+'113.png')
		if selfAddon.getSetting('cbbc') == 'FilmOn': addLink('CBBC','https://www.filmon.com/tv/cbbc',1,logos_tvp+'113.png')
		
		#CBeebies
		if selfAddon.getSetting('cbeebies') == 'BBC iPlayer': addLink('CBeebies HD','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1,logos_tvp+'114.png')
		if selfAddon.getSetting('cbeebies') == 'TVPlayer': addLink('CBeebies','114',2,logos_tvp+'114.png')
		if selfAddon.getSetting('cbeebies') == 'FilmOn': addLink('CBeebies','https://www.filmon.com/tv/cbeebies',1,logos_tvp+'114.png')
		
		#CBS Action
		if selfAddon.getSetting('cbs_a') == 'FilmOn': addLink('CBS Action','https://www.filmon.com/tv/cbs-action',1,logos+'cbsaction.png')
		
		#CBS Drama
		if selfAddon.getSetting('cbs_d') == 'FilmOn': addLink('CBS Drama','https://www.filmon.com/tv/cbs-drama',1,logos+'cbsdrama.png')
		
		#CBS Reality
		if selfAddon.getSetting('cbs_r') == 'FilmOn': addLink('CBS Reality','https://www.filmon.com/tv/cbs-reality',1,logos+'cbsreality.png')
		
		#CBS Reality+1
		if selfAddon.getSetting('cbs_r+1') == 'FilmOn': addLink('CBS Reality+1','https://www.filmon.com/tv/cbs-reality1',1,logos+'cbsreality.png')
		
		#Channel 4
		if selfAddon.getSetting('channel_4') == 'TVPlayer': addLink('Channel 4','92',2,logos_tvp+'92.png')
		if selfAddon.getSetting('channel_4') == 'FilmOn': addLink('Channel 4','https://www.filmon.com/tv/channel-4',1,logos_tvp+'92.png')
		
		#Channel 5
		if selfAddon.getSetting('channel_5') == 'TVPlayer': addLink('Channel 5','574',2,logos_tvp+'574.png')
		if selfAddon.getSetting('channel_5') == 'FilmOn': addLink('Channel 5','https://www.filmon.com/tv/channel-5',1,logos_tvp+'93.png')
		
		#Channel AKA
		if selfAddon.getSetting('channel_aka') == 'Direct': addLink('Channel AKA','http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8',1,logos_tvp+'227.png')
		if selfAddon.getSetting('channel_aka') == 'TVPlayer': addLink('Channel AKA','227',2,logos_tvp+'227.png')
		
		#Chilled
		if selfAddon.getSetting('chilled') == 'TVPlayer': addLink('Chilled','226',2,logos_tvp+'226.png')
		
		#CITV
		if selfAddon.getSetting('citv') == 'ITV Hub': addLink('CITV','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1,logos+'citv.png')
		
		#Clubbing TV
		if selfAddon.getSetting('clubbingtv') == 'FilmOn': addLink('Clubbing TV','https://www.filmon.com/tv/clubbing-tv',1,logos+'clubbingtv.png')
		
		#Clubland
		if selfAddon.getSetting('clubland') == 'TVPlayer': addLink('Clubland','225',2,logos_tvp+'225.png')
		
		#CNN International
		if selfAddon.getSetting('cnn') == 'TVPlayer': addLink('CNN International','286',2,logos_tvp+'286.png')
		
		#Community Channel
		if selfAddon.getSetting('community') == 'TVPlayer': addLink('Community Channel','259',2,logos_tvp+'259.png')
		
		#The Craft Channel
		if selfAddon.getSetting('craft_chan') == 'TVPlayer': addLink('The Craft Channel','554',2,logos_tvp+'554.png')
		
		#Dave
		if selfAddon.getSetting('dave') == 'TVPlayer': addLink('Dave','300',2,logos_tvp+'300.png')
		
		#Dave ja vu
		if selfAddon.getSetting('dave_ja_vu') == 'TVPlayer': addLink('Dave ja vu','317',2,logos_tvp+'317.png')
		
		#Drama
		if selfAddon.getSetting('drama') == 'TVPlayer': addLink('Drama','346',2,logos_tvp+'346.png')
		
		#E4
		if selfAddon.getSetting('e4') == 'FilmOn': addLink('E4','https://www.filmon.com/tv/e4',1,logos_tvp+'562.png')
		if selfAddon.getSetting('e4') == 'TVPlayer': addLink('E4','562',2,logos+'562.png')
		
		#Film4
		if selfAddon.getSetting('film4') == 'FilmOn': addLink('Film4','https://www.filmon.com/tv/film-4',1,logos_tvp+'564.png')
		if selfAddon.getSetting('film4') == 'TVPlayer': addLink('Film4','564',2,logos_tvp+'564.png')
		
		#Food Network
		if selfAddon.getSetting('food_net') == 'TVPlayer': addLink('Food Network','125',2,logos_tvp+'125.png')
		if selfAddon.getSetting('food_net') == 'FilmOn': addLink('Food Network','http://www.filmon.com/tv/food-network',1,logos_tvp+'125.png')
		
		#Food Network+1
		if selfAddon.getSetting('food_net+1') == 'TVPlayer': addLink('Food Network+1','254',2,logos_tvp+'254.png')
		if selfAddon.getSetting('food_net+1') == 'FilmOn': addLink('Food Network+1','http://www.filmon.com/tv/food-network-plus-1',1,logos_tvp+'254.png')
		
		#Forces TV
		if selfAddon.getSetting('forces_tv') == 'TVPlayer': addLink('Forces TV','555',2,logos_tvp+'555.png')
		
		#Heart TV
		if selfAddon.getSetting('heart') == 'Direct': addLink('Heart TV','http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8',1,logos_tvp+'153.png')
		if selfAddon.getSetting('heart') == 'TVPlayer': addLink('Heart TV','153',2,logos_tvp+'153.png')
		
		#Home
		if selfAddon.getSetting('home') == 'TVPlayer': addLink('Home','512',2,logos_tvp+'512.png')
		
		#Horror Channel
		if selfAddon.getSetting('horror_ch') == 'FilmOn': addLink('Horror Channel','https://www.filmon.com/tv/horror-channel',1,logos+'horrorchannel.png')
		
		#ITV1
		if selfAddon.getSetting('itv1') == 'ITV Hub': addLink('ITV1','http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8',1,logos_tvp+'204.png')
		if selfAddon.getSetting('itv1') == 'TVPlayer': addLink('ITV1','204',2,logos_tvp+'204.png')
		if selfAddon.getSetting('itv1') == 'FilmOn': addLink('ITV1','http://www.filmon.com/tv/itv1',1,logos_tvp+'204.png')
		
		#ITV1+1
		if selfAddon.getSetting('itv1+1') == 'FilmOn': addLink('ITV1+1','https://www.filmon.com/tv/itv-plus-1',1,logos_tvp+'204.png')
		
		#ITV2
		if selfAddon.getSetting('itv2') == 'ITV Hub': addLink('ITV2','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1,logos+'itv2.png')
		if selfAddon.getSetting('itv2') == 'FilmOn': addLink('ITV2','http://www.filmon.com/tv/itv2',1,logos+'itv2.png')
		
		#ITV2+1
		if selfAddon.getSetting('itv2+1') == 'FilmOn': addLink('ITV2+1','https://www.filmon.com/tv/itv2-plus-1',1,logos+'itv2.png')
		
		#ITV3
		if selfAddon.getSetting('itv3') == 'ITV Hub': addLink('ITV3','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1,logos+'itv3.png')
		if selfAddon.getSetting('itv3') == 'FilmOn': addLink('ITV3','http://www.filmon.com/tv/itv3',1,logos+'itv3.png')
		
		#ITV3+1
		if selfAddon.getSetting('itv3+1') == 'FilmOn': addLink('ITV3+1','https://www.filmon.com/tv/itv3-plus-1',1,logos+'itv3.png')
		
		#ITV4
		if selfAddon.getSetting('itv4') == 'ITV Hub': addLink('ITV4','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1,logos+'itv4.png')
		if selfAddon.getSetting('itv4') == 'FilmOn': addLink('ITV4','http://www.filmon.com/tv/itv4',1,logos+'itv4.png')
		
		#ITV4+1
		if selfAddon.getSetting('itv4+1') == 'FilmOn': addLink('ITV4+1','https://www.filmon.com/tv/itv4-plus-1',1,logos+'itv4.png')
		
		#ITVBe
		if selfAddon.getSetting('itvbe') == 'ITV Hub': addLink('ITVBe','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1,logos_tvp+'557.png')
		if selfAddon.getSetting('itvbe') == 'FilmOn': addLink('ITVBe','http://www.filmon.com/tv/itvbe',1,logos_tvp+'557.png')
		if selfAddon.getSetting('itvbe') == 'TVPlayer': addLink('ITVBe','557',2,logos_tvp+'557.png')
		
		#The Jewellery Channel
		if selfAddon.getSetting('tjc') == 'Direct': addLink('The Jewellery Channel','https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8',1,logos_tvp+'545.png')
		if selfAddon.getSetting('tjc') == 'TVPlayer': addLink('The Jewellery Channel','545',2,logos_tvp+'545.png')
		
		#Keep It Country
		if selfAddon.getSetting('kic') == 'TVPlayer': addLink('Keep It Country','569',2,logos_tvp+'569.png')
		
		#Kerrang
		if selfAddon.getSetting('kerrang') == 'Direct': addLink('Kerrang!','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8',1,logos_tvp+'133.png')
		if selfAddon.getSetting('kerrang') == 'TVPlayer': addLink('Kerrang!','133',2,logos_tvp+'133.png')
		
		#Kiss
		if selfAddon.getSetting('kiss') == 'Direct': addLink('Kiss','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8',1,logos_tvp+'131.png')
		if selfAddon.getSetting('kiss') == 'TVPlayer': addLink('Kiss','131',2,logos_tvp+'131.png')
		
		#Kix
		if selfAddon.getSetting('kix') == 'FilmOn': addLink('Kix!','https://www.filmon.com/tv/kix',1,logos+'kix.png')
		
		#London Live
		if selfAddon.getSetting('london_live') == 'Direct': addLink('London Live','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1,logos+'londonlive.png')
		
		#Magic
		if selfAddon.getSetting('magic') == 'Direct': addLink('Magic','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'132.png')
		if selfAddon.getSetting('magic') == 'TVPlayer': addLink('Magic','132',2,logos_tvp+'132.png')
		
		#More4
		if selfAddon.getSetting('more4') == 'FilmOn': addLink('More4','https://www.filmon.com/tv/more4',1,logos_tvp+'563.png')
		if selfAddon.getSetting('more4') == 'TVPlayer': addLink('More4','563',2,logos_tvp+'563.png')
		
		#NOW Music
		if selfAddon.getSetting('now') == 'Direct': addLink('NOW Music','http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8',1,logos_tvp+'228.png')
		if selfAddon.getSetting('now') == 'TVPlayer': addLink('NOW Music','228',2,logos_tvp+'228.png')
		
		#POP
		if selfAddon.getSetting('pop') == 'FilmOn': addLink('POP','https://www.filmon.com/tv/pop',1,logos+'pop.png')
		
		#Pick
		if selfAddon.getSetting('pick') == 'FilmOn': addLink('Pick','https://www.filmon.com/tv/pick-tv',1,logos+'pick.png')
		
		#QUEST
		if selfAddon.getSetting('quest') == 'TVPlayer': addLink('QUEST','327',2,logos_tvp+'327.png')
		if selfAddon.getSetting('quest') == 'FilmOn': addLink('QUEST','http://www.filmon.tv/tv/quest',1,logos_tvp+'327.png')
		
		#QUEST+1
		if selfAddon.getSetting('quest+1') == 'TVPlayer': addLink('QUEST+1','336',2,logos_tvp+'336.png')
		
		#QVC Beauty
		if selfAddon.getSetting('qvc_b') == 'TVPlayer': addLink('QVC Beauty','250',2,logos_tvp+'250.png')
		
		#QVC Extra
		if selfAddon.getSetting('qvc_e') == 'TVPlayer': addLink('QVC Extra','248',2,logos_tvp+'248.png')
		
		#QVC Plus
		if selfAddon.getSetting('qvc_p') == 'TVPlayer': addLink('QVC Plus','344',2,logos_tvp+'344.png')
		
		#QVC Style
		if selfAddon.getSetting('qvc_s') == 'TVPlayer': addLink('QVC Style','249',2,logos_tvp+'249.png')
		
		#QVC
		if selfAddon.getSetting('qvc') == 'TVPlayer': addLink('QVC','247',2,logos_tvp+'247.png')
		
		#Really
		if selfAddon.getSetting('really') == 'TVPlayer': addLink('Really','306',2,logos_tvp+'306.png')
		if selfAddon.getSetting('really') == 'FilmOn': addLink('Really','http://www.filmon.tv/tv/really',1,logos_tvp+'306.png')
		
		#S4C
		if selfAddon.getSetting('s4c') == 'BBC iPlayer': addLink('S4C','http://vs-hls-uk-live.edgesuite.net/pool_9/live/s4cpbs/s4cpbs.isml/s4cpbs-pa3%3d96000-video%3d1604032.norewind.m3u8',1,logos_tvp+'251.png')
		if selfAddon.getSetting('s4c') == 'TVPlayer': addLink('S4C','251',2,logos_tvp+'251.png')
		
		#Sky News
		if selfAddon.getSetting('sky_news') == 'YouTube': addLink('Sky News','https://www.youtube.com/watch?v=y60wDzZt8yg',1,logos+'skynews.png')
		
		#Spike
		if selfAddon.getSetting('spike') == 'TVPlayer': addLink('Spike','568',2,logos_tvp+'568.png')
		
		#Tiny Pop
		if selfAddon.getSetting('tiny_pop') == 'FilmOn': addLink('Tiny Pop','https://www.filmon.com/tv/tiny-pop',1,logos+'tinypop.png')
		
		#Travel Channel
		if selfAddon.getSetting('travel') == 'TVPlayer': addLink('Travel Channel','126',2,logos_tvp+'126.png')
		
		#Travel Channel+1
		if selfAddon.getSetting('travel+1') == 'TVPlayer': addLink('Travel Channel+1','255',2,logos_tvp+'255.png')
		if selfAddon.getSetting('travel+1') == 'FilmOn': addLink('Travel Channel+1','http://www.filmon.tv/tv/travel-channel1',1,logos_tvp+'255.png')
		
		#Yesterday
		if selfAddon.getSetting('yesterday') == 'TVPlayer': addLink('Yesterday','308',2,logos_tvp+'308.png')
		if selfAddon.getSetting('yesterday') == 'FilmOn': addLink('Yesterday','http://www.filmon.tv/tv/yesterday',1,logos_tvp+'308.png')
		
		#Yesterday+1
		if selfAddon.getSetting('yesterday+1') == 'TVPlayer': addLink('Yesterday+1','318',2,logos_tvp+'318.png')
		
		#truTV
		if selfAddon.getSetting('trutv') == 'Direct': addLink('truTV','http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8',1,logos_tvp+'295.png')
		if selfAddon.getSetting('trutv') == 'TVPlayer': addLink('truTV','295',2,logos_tvp+'295.png')
		if selfAddon.getSetting('trutv') == 'FilmOn': addLink('truTV','http://www.filmon.tv/tv/tru-tv',1,logos_tvp+'295.png')
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
