# -*- coding: utf-8 -*-
import xbmcgui,sys
import xbmcplugin
import xbmcaddon,xbmc
import urlparse
from lib.modules.webutils import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def get_show_list_cod(url):
    html=read_url(url)
    regex=re.compile('\["(.+?)","(.+?)","(.+?)"\]')

    items=re.findall(regex,html)
    return items

def normal(string):
    string=string.replace('Š','S').replace('Ž','Z').replace('Č','C').replace('Ć','C').replace('Đ','D')
    return string.replace('š','s').replace('ž','z').replace('č','c').replace('ć','c').replace('đ','d')

def otvori_epizodu(url,title,thumb):
    #prvo pogledaj ako ima vise dijelova
    try:
        soup=get_soup(url)
        tag=soup.find('div',{'id':'Playerholder'})
        frames=tag.findAll('iframe')
        if len(frames)>1:
            sources=[]
            for i in range(len(frames)):
                sources+=['%s. dio'%(i+1)]
            dialog = xbmcgui.Dialog()
            index = dialog.select('Odaberite:', sources)
            li = xbmcgui.ListItem('%s'%title)
            li.setInfo('video', { 'title': '%s'%title })
            li.setThumbnailImage(thumb)
            if index>-1:
                link=frames[index]

                
                link=link['src']
                try:
                    from lib.resolvers import dailymotion
                    resolved=dailymotion.resolve(link)
                    resolved=resolved[0]['url']
        
                except:
                    import urlresolver
                    resolved=urlresolver.resolve(link)
                
            

            
                xbmc.Player().play(resolved,li)
                return
            else:
                return

    except:
        pass

    try:   
        soup=get_soup(url)
        link=soup.findAll('iframe')[1]['src']
       
    except:

        try:
            html=read_url(url)

        
            soup=bs(html)
            link=soup.findAll('iframe')[1]['src']
          
        except:
            try:
                soup=get_soup(url)
                try:
                    link=soup.find('div',{'id':'Playerholder'}).find('embed')['src']
                except:
                    link=soup.find('div',{'id':'Playerholder'}).find('iframe')['src']
               
            except:
                html=read_url(url).lower()
                ind=html.index('player.src')
                html=html[ind:ind+80]
                
                reg=r'watch\?v=(.+?)"'
                link=re.findall(re.compile(reg),html)[0]
                
                link='http://www.youtube.com/watch?v=' + link

    if 'moevideo' in link or 'playreplay' in link :

        import YDStreamExtractor
        vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
        resolved = vid.streamURL() 
    
    else:          
        try:
            from lib.resolvers import dailymotion
            resolved=dailymotion.resolve(link)
            resolved=resolved[0]['url']
            
        except:
            try:
                import urlresolver
                resolved=urlresolver.resolve(link)
            except:
                try:
                    import YDStreamExtractor
                    vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
                    resolved = vid.streamURL() 
                except:
                    pass
            

    li = xbmcgui.ListItem('%s'%title)
    li.setInfo('video', { 'title': '%s'%title })
    li.setThumbnailImage(thumb)
    xbmc.Player().play(item=resolved, listitem=li)
def download_epizodu(title,url):
    try:
        soup=get_soup(url)
        tag=soup.find('div',{'id':'Playerholder'})
        frames=tag.findAll('iframe')
        if len(frames)>1:
            sources=[]
            for i in range(len(frames)):
                sources+=['%s. dio'%(i+1)]
            dialog = xbmcgui.Dialog()
            index = dialog.select('Odaberite:', sources)
            li = xbmcgui.ListItem('%s'%title)
            li.setInfo('video', { 'title': '%s'%title })
            if index>-1:
                link=frames[index]
                title=title+' (%s od %s)'%(index+1,len(frames))

                
                link=link['src']
                try:
                    from lib.resolvers import dailymotion
                    resolved=dailymotion.resolve(link)
                    resolved=resolved[0]['url']
        
                except:

                    try:
                        import urlresolver
                        resolved=urlresolver.resolve(link)
                    except:
                        try:
                            import YDStreamExtractor
                            YDStreamExtractor.disableDASHVideo(True) 
                            vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
                            resolved = vid.streamURL() 
                        except:
                            pass
                
            

            
                download(title,resolved)

                return
            else:
                return

    except:
        pass

    try:   
        soup=get_soup(url)
        link=soup.findAll('iframe')[1]['src']
       
    except:

        try:
            soup=get_soup(url)
            link=soup.findAll('iframe')[1]['src']
          
        except:
            try:
                soup=get_soup(url)
                try:
                    link=soup.find('div',{'id':'Playerholder'}).find('embed')['src']
                except:
                    link=soup.find('div',{'id':'Playerholder'}).find('iframe')['src']
               
            except:
                html=read_url(url).lower()
                ind=html.index('player.src')
                html=html[ind:ind+80]
                
                reg=r'watch\?v=(.+?)"'
                link=re.findall(re.compile(reg),html)[0]
                
                link='http://www.youtube.com/watch?v=' + link


    if 'moevideo' in link or 'playreplay' in link :
        import YDStreamExtractor
        YDStreamExtractor.disableDASHVideo(True) 
        vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
        resolved = vid.streamURL() 
    
    else:          
        try:
            from lib.resolvers import dailymotion
            resolved=dailymotion.resolve(link)
            resolved=resolved[0]['url']

        except:

            try:
                import urlresolver
                resolved=urlresolver.resolve(link)
            except:
                try:
                    import YDStreamExtractor
                    YDStreamExtractor.disableDASHVideo(True) 
                    vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
                    resolved = vid.streamURL() 
                except:
                    pass
            

    download(title,resolved)

def nadi_epizode(url,page,linky):

    soup=get_soup(url)
    tag=soup.find('ul',{'class':'pm-ul-browse-videos thumbnails'})

    lis=tag.findAll('li')
    results=[]
    for i in range(len(lis)):
        thumb=lis[i].find('img')['src']
        item=lis[i].find('h3').find('a')
        link=item['href']
        title=item['title']
        
        url = build_url({'mode': 'otvori_epizodu', 'link':'%s'%link, 'title':'%s'%title, 'thumb':'%s'%thumb})
        li = xbmcgui.ListItem('%s '%(title), iconImage=thumb)
        down_uri = build_url({'mode': 'download_epizodu', 'title': '%s'%(title.encode('ascii','ignore')), 'link': link})
        fav_uri = build_url({'mode': 'add_favourite', 'name': title.encode('utf-8'), 'url': url, 'thumb':thumb})


        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri),
                                ('Dodaj u favorite','RunPlugin(%s)'%fav_uri)])


        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'otvori_seriju_balkanje', 'link':'%s'%linky, 'page':'%s'%(str(int(page)+1))})
    li = xbmcgui.ListItem('Sljedeca strana --> ', iconImage='http://www.basspirate.com/wp-content/uploads/2011/10/Right-Arrow.gif')

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)