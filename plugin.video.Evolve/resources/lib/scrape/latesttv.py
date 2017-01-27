import urllib,urllib2,re,sys,os

def INDEXER():
    scrapertype='tvshow'
    link=open_url('http://www.watchepisodes1.com/')
    link=link.replace('\n','').replace('  ','').replace("('",'"').replace("')",'')
    index=re.compile('<div class="featured-ep-box "(.+?)<div class="fel-grid">').findall(link)
    itemlist=''
    for item in index:
                name=re.compile('title="(.+?)">').findall(item)[0]
                iconimage=re.compile('style="background-image: url"(.+?)">').findall(item)[0]
                url=re.compile('<a href="(.+?)">').findall(item)[1]                
                name=name.replace('&amp;','&')
                item='<item><meta>%s</meta><title>%s</title><link>%s</link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(scrapertype,name,url,iconimage,iconimage)
                itemlist=itemlist+item
    return itemlist

def HOSTS(name,url,iconimage):
    link=open_url(url)
    link=link.replace('\n','').replace('\r','').replace('\t','').replace('  ','')
    hlist=re.compile('ico"></div><a href=".+?">(.+?)\.(.+?)</a>').findall(link)
    hostlist=[]
    for domain,ext in hlist:
        string=domain+'.'+ext
        hostlist.append(string)
        
        
    print hostlist
    return hostlist #links
    
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
