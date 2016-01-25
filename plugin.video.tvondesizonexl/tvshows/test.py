'''
Created on Dec 25, 2013

@author: ajju
'''
from xoze.utils import http
import BeautifulSoup

def retrieve_tv_shows(link):
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'all-tv-shows'})
    soup = http.HttpClient().get_beautiful_soup(url=link, parseOnlyThese=contentDiv, accept_500_error=True)
    list = soup.find('ul')
    for item in list.findChildren('li'):
        tv_show = item.findChild('a')
        link = tv_show['href']
        name = tv_show.getText()
        print '>>>>>>>>' + name
        print '>>>>>>>>' + link
    
if __name__ == '__main__':
    print 'DTF actions...'
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'tv-channel-list'})
    soup = http.HttpClient().get_beautiful_soup(url='http://desitvforum.net/television/', parseOnlyThese=contentDiv, accept_500_error=True)
    list = soup.find('ul')
    for item in list.findChildren('li'):
        channel = item.findChild('a')
        link = channel['href']
        name = channel.getText()
        print name
        print link
        print '------------------------'
        try:
            retrieve_tv_shows(link)
        except:
            pass
        


from xoze.lib.jsonrpclib.history import History
from xoze.lib.jsonrpclib.jsonrpc import Server
import json

try:
    videoLink = 'http://www.youtube.com/watch?v=p2KcObzrzLg'
    print videoLink
    client = Server('http://localhost:%d/TVonDESIZONE' % 11421)
    response = client.resolveStream(videoLink=videoLink)
    history = History.instance()
    print json.loads(history.request)
    print json.loads(history.response)
    print response['status']
    print response['streamLink']
except Exception, e:
    print json.loads(history.request)
    raise e
