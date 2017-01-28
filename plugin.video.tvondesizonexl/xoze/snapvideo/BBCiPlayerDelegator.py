'''
Created on Jun 29, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
import logging
import xbmcaddon # @UnresolvedImport
import xbmcgui # @UnresolvedImport


def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('BBC add-on by Hitcher')
    return video_host

def retrieveVideoInfo(videoUrl):
    try: 
        xbmcaddon.Addon('plugin.video.iplayer')
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok('[B][COLOR red]MISSING: [/COLOR][/B] BBC IPlayer v2 add-on', '', 'Please install BBC IPlayer v2 add-on created by Hitcher!', 'Available at http://code.google.com/p/xbmc-iplayerv2/')
        raise
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(videoUrl)
    video_info.set_url(videoUrl)
    addon_url = 'plugin://plugin.video.iplayer/?'
    video_params = videoUrl.split('/')
    
    addon_url += 'pid=%s' % video_params[0]
    video_info.add_stream_link(STREAM_QUAL_SD, addon_url)
    video_info.set_thumb_image('http://www.bbc.co.uk/iplayer/images/episode/%s_512_288.jpg' % video_params[0])
    video_info.set_name(video_params[1].replace('_', ' '))
    logging.getLogger().debug('addon_url : %s' % addon_url)
    video_info.set_stopped(False)
    return video_info
