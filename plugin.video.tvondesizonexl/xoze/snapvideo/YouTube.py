'''
Created on Oct 29, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_HD_720, \
    STREAM_QUAL_HD_1080, STREAM_QUAL_SD, STREAM_QUAL_LOW
from xoze.utils import http
import logging
import re
import urllib
import xbmcgui  # @UnresolvedImport

VIDEO_HOSTING_NAME = 'YouTube'
STREAMS_QUAL_MAP = {STREAM_QUAL_LOW:[18, 34, 43, 5, 17, 100], STREAM_QUAL_SD:[35, 44, 101], STREAM_QUAL_HD_720:[22, 45, 120, 38, 84, 102], STREAM_QUAL_HD_1080:[37, 121]}

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.automotivefinancingsystems.com/images/icons/socialmedia_youtube_256x256.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        
        http.HttpClient().enable_cookies()
        video_info.set_thumb_image('http://i.ytimg.com/vi/' + video_id + '/default.jpg')
        html = http.HttpClient().get_html_content(url='http://www.youtube.com/get_video_info?video_id=' + video_id + '&asv=3&el=detailpage&hl=en_US')
        stream_map = None
        
        html = html.decode('utf8')
        html = html.replace('\n', '')
        html = html.replace('\r', '')
        html = unicode(html + '&').encode('utf-8')
        if re.search('status=fail', html):
            # XBMCInterfaceUtils.displayDialogMessage('Video info retrieval failed', 'Reason: ' + ((re.compile('reason\=(.+?)\.').findall(html))[0]).replace('+', ' ') + '.')
            logging.getLogger().info('YouTube video is removed for Id = ' + video_id + ' reason = ' + html)
            video_info.set_stopped(True)
            return video_info
        
        title = urllib.unquote_plus(re.compile('title=(.+?)&').findall(html)[0]).replace('/\+/g', ' ')
        video_info.set_name(title)
        stream_info = None
        if not re.search('url_encoded_fmt_stream_map=&', html):
            stream_info = re.compile('url_encoded_fmt_stream_map=(.+?)&').findall(html)
        stream_map = None
        if (stream_info is None or len(stream_info) == 0) and re.search('fmt_stream_map": "', html):
            stream_map = re.compile('fmt_stream_map": "(.+?)"').findall(html)[0].replace("\\/", "/")
        elif stream_info is not None:
            stream_map = stream_info[0]
            
        if stream_map is None:
            params = http.parse_url_params(html)
            logging.getLogger().debug('ENTERING live video scenario...')
            for key in params:
                logging.getLogger().debug(key + " : " + urllib.unquote_plus(params[key]))
            hlsvp = urllib.unquote_plus(params['hlsvp'])
            playlistItems = http.HttpClient().get_html_content(url=hlsvp).splitlines()
            qualityIdentified = None
            for item in playlistItems:
                logging.getLogger().debug(item)
                if item.startswith('#EXT-X-STREAM-INF'):
                    if item.endswith('1280x720'):
                        qualityIdentified = STREAM_QUAL_HD_720
                    elif item.endswith('1080'):
                        qualityIdentified = STREAM_QUAL_HD_1080
                    elif item.endswith('854x480'):
                        qualityIdentified = STREAM_QUAL_SD
                    elif item.endswith('640x360'):
                        qualityIdentified = STREAM_QUAL_LOW
                elif item.startswith('http') and qualityIdentified is not None:
                    videoUrl = http.HttpClient().add_http_cookies_to_url(item, extraExtraHeaders={'Referer':'https://www.youtube.com/watch?v=' + video_id})
                    video_info.add_stream_link(qualityIdentified, videoUrl)
                    qualityIdentified = None
            video_info.set_stopped(False)
            return video_info
        
        stream_map = urllib.unquote_plus(stream_map)
        logging.getLogger().debug(stream_map)
        formatArray = stream_map.split(',')
        streams = {}
        for formatContent in formatArray:
            if formatContent == '':
                continue
            formatUrl = ''
            try:
                formatUrl = urllib.unquote(re.compile("url=([^&]+)").findall(formatContent)[0]) + "&title=" + urllib.quote_plus(title)   
            except Exception, e:
                logging.getLogger().error(e)     
            if re.search("rtmpe", stream_map):
                try:
                    conn = urllib.unquote(re.compile("conn=([^&]+)").findall(formatContent)[0]);
                    host = re.compile("rtmpe:\/\/([^\/]+)").findall(conn)[0];
                    stream = re.compile("stream=([^&]+)").findall(formatContent)[0];
                    path = 'videoplayback';
                    
                    formatUrl = "-r %22rtmpe:\/\/" + host + "\/" + path + "%22 -V -a %22" + path + "%22 -f %22WIN 11,3,300,268%22 -W %22http:\/\/s.ytimg.com\/yt\/swfbin\/watch_as3-vfl7aCF1A.swf%22 -p %22http:\/\/www.youtube.com\/watch?v=" + video_id + "%22 -y %22" + urllib.unquote(stream) + "%22"
                except Exception, e:
                    logging.getLogger().error(e)
            if formatUrl == '':
                continue
            logging.getLogger().debug('************************')
            logging.getLogger().debug(formatContent)
            if(formatUrl[0: 4] == "http" or formatUrl[0: 2] == "-r"):
                formatQual = re.compile("itag=([^&]+)").findall(formatContent)[0]
                if not re.search("signature=", formatUrl):
                    sig = re.compile("sig=([^&]+)").findall(formatContent)
                    if sig is not None and len(sig) == 1:
                        formatUrl += "&signature=" + sig[0]
                    else:
                        sig = re.compile("s=([^&]+)").findall(formatContent)
                        if sig is not None and len(sig) == 1:
                            formatUrl += "&signature=" + parseSignature(sig[0])
        
            qual = formatQual
            url = http.HttpClient().add_http_cookies_to_url(formatUrl, addHeaders=False,addCookies=False, extraExtraHeaders={'Referer':'https://www.youtube.com/watch?v=' + video_id})
            streams[int(qual)] = url
            
        
        logging.getLogger().debug(streams)
        for qual in STREAMS_QUAL_MAP:
            for key in STREAMS_QUAL_MAP[qual]:
                if streams.has_key(key):
                    url = streams[key]
                    video_info.add_stream_link(qual, url)
                    break
        video_info.set_stopped(False)
    except Exception, e:
        logging.getLogger().error(e)
        video_info.set_stopped(True)
    return video_info


def swap(a , b):
    c = a[0]
    a[0] = a[b % len(a)]
    a[b] = c
    return a

def parseSignature(s):
    ''' use decryption solution by Youtube-DL project '''
    if len(s) == 93:
        return s[86:29:-1] + s[88] + s[28:5:-1]
    elif len(s) == 92:
        return s[25] + s[3:25] + s[0] + s[26:42] + s[79] + s[43:79] + s[91] + s[80:83]
    elif len(s) == 91:
        return s[84:27:-1] + s[86] + s[26:5:-1]
    elif len(s) == 90:
        return s[25] + s[3:25] + s[2] + s[26:40] + s[77] + s[41:77] + s[89] + s[78:81]
    elif len(s) == 89:
        return s[84:78:-1] + s[87] + s[77:60:-1] + s[0] + s[59:3:-1]
    elif len(s) == 88:
        return s[7:28] + s[87] + s[29:45] + s[55] + s[46:55] + s[2] + s[56:87] + s[28]
    elif len(s) == 87:
        return s[6:27] + s[4] + s[28:39] + s[27] + s[40:59] + s[2] + s[60:]
    elif len(s) == 86:
        return s[80:72:-1] + s[16] + s[71:39:-1] + s[72] + s[38:16:-1] + s[82] + s[15::-1]
    elif len(s) == 85:
        return s[3:11] + s[0] + s[12:55] + s[84] + s[56:84]
    elif len(s) == 84:
        return s[78:70:-1] + s[14] + s[69:37:-1] + s[70] + s[36:14:-1] + s[80] + s[:14][::-1]
    elif len(s) == 83:
        return s[80:63:-1] + s[0] + s[62:0:-1] + s[63]
    elif len(s) == 82:
        return s[80:37:-1] + s[7] + s[36:7:-1] + s[0] + s[6:0:-1] + s[37]
    elif len(s) == 81:
        return s[56] + s[79:56:-1] + s[41] + s[55:41:-1] + s[80] + s[40:34:-1] + s[0] + s[33:29:-1] + s[34] + s[28:9:-1] + s[29] + s[8:0:-1] + s[9]
    elif len(s) == 80:
        return s[1:19] + s[0] + s[20:68] + s[19] + s[69:80]
    elif len(s) == 79:
        return s[54] + s[77:54:-1] + s[39] + s[53:39:-1] + s[78] + s[38:34:-1] + s[0] + s[33:29:-1] + s[34] + s[28:9:-1] + s[29] + s[8:0:-1] + s[9]
    else:
        logging.getLogger().fatal(u'Unable to decrypt signature, key length %d not supported; retrying might work' % (len(s)))
        return s

def retrievePlaylistVideoItems(playlistId):
    logging.getLogger().error('YouTube Playlist ID = ' + playlistId)
    soupXml = http.HttpClient().get_beautiful_soup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId + '?max-results=50')
    videoItemsList = []
    for media in soupXml.findChildren('media:player'):
        videoUrl = str(media['url'])
        videoItemsList.append(videoUrl)
    return videoItemsList
    
def retrieveReloadedPlaylistVideoItems(playlistId):
    logging.getLogger().error('YouTube Reloaded Playlist ID = ' + playlistId)
    soupXml = http.HttpClient().get_beautiful_soup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('track'):
        videoUrl = media.findChild('location').getText()
        videoItemsList.append(videoUrl)
    return videoItemsList
    
