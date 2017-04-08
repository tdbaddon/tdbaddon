import xbmc
import json
import re
import urllib
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import clean_title, random_agent
from ..scraper import Scraper


class Onemusic(Scraper):
    domains = ['Onemoviesmusic']
    name = "Onemusic"

    def __init__(self):
        self.base_link = 'http://123music.to'
        self.search_link = '/search/%s.html'
        self.sources_link = '/ajax/song/sources/%s'
        self.tv_search_link = '/tagtvs/%s'

    def scrape_music(self, title, artist, debrid = False):
        try:
            # print("ONEMUSIC")
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title.replace("'", "")))
            query = urlparse.urljoin(self.base_link, query)
            # print("ONEMUSIC", query)
            artist_name = clean_title(artist)
            song_name = clean_title(title)
            # print("ONEMUSIC ARTIST", artist_name)
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
            self.musiclist = []
            containers = html.findAll('div', attrs={'class': 'sr-songs-list'})
            for blocks in containers:
                song_block = blocks.findAll('div', attrs={'class': 'item-caption'})
                for item in song_block:
                    href = item.findAll('a')[0]['href']
                    song_title = item.findAll('a')[0]['title']
                    href = href.encode('utf-8')
                    song_title = song_title.encode('utf-8')
                    if clean_title(song_title) == song_name:
                        artist_block = item.findAll('span', attrs={'class': 'singer'})[0]
                        artist = artist_block.findAll('a')[0]['title']
                        artist = artist.encode('utf-8')
                        artist = clean_title(artist)
                        print("ONEMUSIC", href, song_title, artist_name)
                        if artist == artist_name:
                            print("ONEMUSIC PASSED", href, song_title, artist)
                            return self.sources(href, "HD")

        except:
            pass
        return []

    def sources(self, url, quality):
        sources = []
        try:
            headers = {'User-Agent': random_agent()}
            song_id = re.findall('-(\d+).html', url)[0]
            query = self.sources_link % song_id
            query = urlparse.urljoin(self.base_link, query)

            # print("ONEMUSIC SONG ID", song_id, query)
            response = requests.get(query, headers=headers).content
            source_json = json.loads(response)
            songs_json = source_json['sources']
            for item in songs_json:
                hdmusic = item['link_320']
                sdmusic = item['link_128']
                hdmusic = hdmusic.encode('utf-8')
                sdmusic = sdmusic.encode('utf-8')
                hdmusic = hdmusic.replace(' ', '%20')
                sdmusic = sdmusic.replace(' ', '%20')
                if not "/mobile/" in hdmusic: sources.append(
                    {'source': 'mp3', 'quality': 'HD', 'scraper': self.name, 'url': hdmusic, 'direct': True})
                if not "mobile" in sdmusic: sources.append(
                    {'source': 'mp3', 'quality': 'SD', 'scraper': self.name, 'url': sdmusic, 'direct': True})
                # print("ONEMUSIC SOURCES", sources)

        except:
            pass
        return sources


def googletag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try:
        quality = quality[0]
    except:
        return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': '480', 'url': url}]
    else:
        return []
