'''
Created on Jun 29, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, XBMC_EXECUTE_PLUGIN, STREAM_QUAL_SD
from xoze.utils import http
import logging
import urllib
import xbmcaddon # @UnresolvedImport
import xbmcgui # @UnresolvedImport

try:
    import json
except ImportError:
    import simplejson as json

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('Vevo add-on by BlueCop')
    return video_host

def retrieveVideoInfo(videoUrl):
    try: 
        xbmcaddon.Addon('plugin.video.vevo')
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok('[B][COLOR red]MISSING: [/COLOR][/B] VEVO add-on', '', 'Please install VEVO add-on created by BlueCop!', 'Available at http://code.google.com/p/bluecop-xbmc-repo/')
        raise
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(videoUrl)
    addon_url = 'plugin://plugin.video.vevo/?'
    vevo_id = videoUrl.split('/')[-1]
    if videoUrl.startswith('playlist'):
        url = urllib.quote_plus('http://api.vevo.com/mobile/v2/playlist/%s.json?' % vevo_id)
        addon_url += 'url=%s' % url
        addon_url += '&mode=playPlaylist'
        addon_url += '&duration=210'
        addon_url += '&page=1'
        video_info.add_stream_link(XBMC_EXECUTE_PLUGIN, addon_url)
        video_info.set_thumb_image('')
        video_info.set_name(' ')
    else:
        url = 'http://videoplayer.vevo.com/VideoService/AuthenticateVideo?isrc=%s&extended=true' % vevo_id
        video = json.loads(http.HttpClient().get_html_content(url=url))['video']
        title = ''
        try:title = video['title'].encode('utf-8')
        except: title = ''                  
        video_image = video['imageUrl']
        if len(video['featuredArtists']) > 0:
            feats = ''
            for featuredartist in video['featuredArtists']:
                # featuredartist_image = featuredartist['image_url']
                featuredartist_name = featuredartist['artistName'].encode('utf-8')
                feats += featuredartist_name + ', '
            feats = feats[:-2]
            title += ' (ft. ' + feats + ')'
                
        addon_url += 'url=%s' % vevo_id
        addon_url += '&mode=playVideo'
        addon_url += '&duration=210'
        video_info.add_stream_link(STREAM_QUAL_SD, addon_url)
        video_info.set_thumb_image(video_image)
        video_info.set_name(title)
    logging.getLogger().debug(addon_url)
    video_info.set_stopped(False)
    return video_info

