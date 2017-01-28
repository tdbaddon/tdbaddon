import urllib,urllib2,re,sys,os

def INDEXER():
    scrapertype='movie'
    link=open_url('http://newmoviesonline.ws/')
    index=re.compile('<a href="(.+?)" title="Watch (.+?) Online"><img width=".+?" height=".+?" src="(.+?)" class="attachment-post-thumbnail size-post-thumbnail wp-post-image"').findall(link)
    itemlist=''
    for url,name,iconimage in index:
        item='<item><meta>%s</meta><title>%s</title><link>%s</link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(scrapertype,name,url,iconimage,iconimage)
        itemlist=itemlist+item
    return itemlist
    
def HOSTS(name,url,iconimage):
    link=open_url(url)
    hostlist=re.compile('<a href="(.+?)" title=".+?" rel="nofollow" target="blank">.+?</a><br/>').findall(link)
    return hostlist #links

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
