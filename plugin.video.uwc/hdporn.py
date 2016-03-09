'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

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

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import urlparse, json

import utils

progress = utils.progress

def PAQMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.pornaq.com',63,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.pornaq.com/page/1/?s=',68,'','')
    PAQList('http://www.pornaq.com/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def P00Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.porn00.org',63,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.porn00.org/page/1/?s=',68,'','')
    PAQList('http://www.porn00.org/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)    


def PAQList(url, page, onelist=None):
    if onelist:
        url = url.replace('page/1/','page/'+str(page)+'/')    
    listhtml = utils.getHtml(url, '')
    if 'pornaq' in url:
        match = re.compile(r'<h2>\s+<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)" class="attachment-primary-post-thumbnail', re.DOTALL | re.IGNORECASE).findall(listhtml)
        for name, videopage, img in match:
            name = utils.cleantext(name)
            utils.addDownLink(name, videopage, 62, img, '')
    elif 'porn00' in url:
        match = re.compile('<h2> <a title="([^"]+)" href="([^"]+)".*?src="([^"]+)" class="attachment-primary-post-thumbnail', re.DOTALL | re.IGNORECASE).findall(listhtml)
        for name, videopage, img in match:
            name = utils.cleantext(name)
            utils.addDownLink(name, videopage, 62, img, '')    
    if not onelist:
        if re.search("<span class='current'>\d+?</span><span>", listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('page/'+str(page)+'/','page/'+str(npage)+'/')
            utils.addDir('Next Page ('+str(npage)+')', url, 61, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)


def GetAlternative(url, alternative):
    progress.update( 70, "", "Loading alternative page", "" )
    if alternative == 1:
        nalternative = 2
        url = url + str(nalternative)
    else:
        nalternative = int(alternative) + 1
        url.replace('/'+str(alternative),'/'+str(nalternative))
    return url, nalternative


def PPlayvid(url, name, alternative=1, download=None):

    def playvid():
        progress.close()
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)    
    
    progress.create('Play video', 'Searching videofile.')
    progress.update( 25, "", "Loading video page", "" )
    
    videopage = utils.getHtml(url, '', '', True)
    if re.search('server/\?t=', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile(r'/server/\?t=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videopage)
        match = "http://www.porn00.org/server/?t=" + match[0]
        progress.update( 50, "", "Opening porn00 video page", "" )
        iframepage = utils.getHtml(match, url)
        video720 = re.compile(r'file: "([^"]+)",\s+label: "7', re.DOTALL | re.IGNORECASE).findall(iframepage)
        if not video720:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.notify('Oh oh','Couldn\'t find a supported videohost')
        else:
            videourl = video720[0]
            playvid()
    elif re.search('video_ext.php\?', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile('<iframe.*?src="([^"]+video_ext[^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        progress.update( 30, "", "Opening VK video page", "" )
        videourl = getVK(match[0])
        if not videourl:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.notify('Oh oh','Couldn\'t find a supported videohost')
        else:
            playvid()              
    elif re.search('/\?V=', videopage, re.DOTALL | re.IGNORECASE):
        try:
            match = re.compile('<iframe.*?src="([^"]+watch/[^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
            progress.update( 50, "", "Opening porn00/pornAQ video page", "" )
            iframepage = utils.getHtml(match[0], url)
            video720 = re.compile(r'file: "([^"]+)",\s+label: "7', re.DOTALL | re.IGNORECASE).findall(iframepage)
            if not video720:
                if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                    alturl, nalternative = GetAlternative(url, alternative)
                    PPlayvid(alturl, name, nalternative, download)
                else:
                    progress.close()
                    utils.notify('Oh oh','Couldn\'t find a supported videohost')
            else:
                videourl = video720[0]
                playvid()
        except:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.notify('Oh oh','Couldn\'t find a supported videohost')        
    elif re.search('google.com/file', videopage, re.DOTALL | re.IGNORECASE):
        match = re.compile('file/d/([^/]+)/', re.DOTALL | re.IGNORECASE).findall(videopage)
        googleurl = "https://docs.google.com/uc?id="+match[0]+"&export=download"
        progress.update( 50, "", "Opening Google docs video page", "" )
        googlepage = utils.getHtml(googleurl, '')
        video720 = re.compile('"downloadUrl":"([^?]+)', re.DOTALL | re.IGNORECASE).findall(googlepage)
        if not video720:
            if re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
                alturl, nalternative = GetAlternative(url, alternative)
                PPlayvid(alturl, name, nalternative, download)
            else:
                progress.close()
                utils.notify('Oh oh','Couldn\'t find a supported videohost')
        else:
            videourl = video720[0]
            playvid()
    elif re.search('id="alternatives"', videopage, re.DOTALL | re.IGNORECASE):
        alturl, nalternative = GetAlternative(url, alternative)
        PPlayvid(alturl, name, nalternative, download)
    else:
        progress.close()
        utils.notify('Oh oh','Couldn\'t find a supported videohost')


def PCat(url):
    caturl = utils.getHtml(url, '')
    cathtml = re.compile('<ul id="categorias">(.*?)</html>', re.DOTALL | re.IGNORECASE).findall(caturl)
    if 'pornaq' in url:
        match = re.compile("""<li.*?href=(?:'|")(/[^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    elif 'porn00' in url:
        match = re.compile("""<li.*?href=(?:'|")([^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    for videolist, name in match:
        if 'pornaq' in url:
            videolist = "http://www.pornaq.com" + videolist + "page/1/"
            utils.addDir(name, videolist, 61, '', 1)
        elif 'porn00' in url:
            videolist = videolist + "page/1/"
            utils.addDir(name, videolist, 61, '', 1)            
    xbmcplugin.endOfDirectory(utils.addon_handle)


def PSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 68)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        PAQList(searchUrl, 1)


def getVK(url):

    def __get_private(oid, video_id):
        private_url = 'http://vk.com/al_video.php?act=show_inline&al=1&video=%s_%s' % (oid, video_id)
        html = utils.getHtml(private_url,'')
        html = re.sub(r'[^\x00-\x7F]+', ' ', html)
        match = re.search('var\s+vars\s*=\s*({.+?});', html)
        try: return json.loads(match.group(1))
        except: return {}
        return {}
    
    query = url.split('?', 1)[-1]
    query = urlparse.parse_qs(query)
    api_url = 'http://api.vk.com/method/video.getEmbed?oid=%s&video_id=%s&embed_hash=%s' % (query['oid'][0], query['id'][0], query['hash'][0])
    progress.update( 40, "", "Opening VK video page", "" )
    html = utils.getHtml(api_url,'')
    html = re.sub(r'[^\x00-\x7F]+', ' ', html)
    
    try: result = json.loads(html)['response']
    except: result = __get_private(query['oid'][0], query['id'][0])
    
    quality_list = []
    link_list = []
    best_link = ''
    for quality in ['url240', 'url360', 'url480', 'url540', 'url720']:
        if quality in result:
            quality_list.append(quality[3:])
            link_list.append(result[quality])
            best_link = result[quality]
    
    if quality_list:
        if len(quality_list) > 1:
            result = xbmcgui.Dialog().select('Choose the quality', quality_list)
            if result == -1:
                utils.notify('Oh oh','No video selected')
            else:
                return link_list[result] + '|User-Agent=%s' % (utils.USER_AGENT)
        else:
            return link_list[0] + '|User-Agent=%s' % (utils.USER_AGENT)
    return

