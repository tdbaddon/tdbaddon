import urllib,urllib2,re,sys,os

def INDEXER():
    scrapertype='tvshow'
    link=open_url('http://www.watchepisodes1.com/')
    link=link.replace('\n','').replace('  ','').replace("('",'"').replace("')",'')
    index=re.compile('class="hb-image" style="background-image: url"(.+?)".+?div class="hb-right".+?href="(.+?)" class="episode">(.+?)<').findall(link)
    itemlist=''
    for iconimage,url,name in index:
        item='<item><meta>%s</meta><title>%s</title><link>%s</link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(scrapertype,name,url,iconimage,iconimage)
        itemlist=itemlist+item
    return itemlist

def HOSTS(name,url,iconimage):
    link=open_url(url)
    hostlist=re.compile('data-actuallink="(.+?)" data-hostname=".+?"  >.+?</a>').findall(link)
    return hostlist #links
    
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
