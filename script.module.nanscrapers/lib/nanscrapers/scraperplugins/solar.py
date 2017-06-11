# -*- coding: utf-8 -*-

'''
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
import re
import urllib
import urlparse

import requests

import xbmc
from BeautifulSoup import BeautifulSoup

from ..common import filter_host, random_agent
from ..modules import cfscrape
from ..scraper import Scraper


class Solar(Scraper):
    name = "Solar"

    def __init__(self):
        self.base_link = 'https://putlockeris.org/'
        self.movie_link = '/%s'
        self.ep_link = '/%s'
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            sources = self.movie(imdb, title, year)
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            headers = {'User-Agent': random_agent()}
            title = title.lower().replace(' ', '-').replace(":","-")
            title = title.replace("--", "-")
            title2 = title + "-" + year
            query = self.movie_link % title
            u = urlparse.urljoin(self.base_link, query)
            sources = self.sources(u, [], [])
            if sources:
                return sources

            query = self.movie_link % title2
            u = urlparse.urljoin(self.base_link, query)
            sources = self.sources(u, [], [])
            return sources
        except:
            return

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title, year, season, episode)[0]
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []
        try:
            headers = {'User-Agent': random_agent()}
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            data['season'], data['episode'] = season, episode
            self.zen_url = []
            title = title.replace(' ', '-')
            query = title + "-season-" + season + "-episode-" + episode
            query = self.ep_link % query
            # print("SOLAR query", query)
            u = urlparse.urljoin(self.base_link, query)
            self.zen_url.append(u)
            return self.zen_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            headers = {'User-Agent': random_agent()}
            if url is None:
                return
            html = self.scraper.get(url, headers=headers, timeout=10).text
            html = BeautifulSoup(html)
            table = html.findAll("table", attrs={"class": "dataTable"})[0]
            rows = table.findAll("tr")
            for row in rows:
                #quality_container = row.find("td", attrs={"class": "qualityCell js-link-format"})
                #quality = quality_container.text.upper()
                quality = "SD"
                link_containers = row.findAll("td", attrs={"class": "entry"})
                for link_container in link_containers:
                    links = link_container.findAll("a")
                    for link in links:
                        url = link["href"]
                        url = url.replace("/gotolink.php?url=", "")
                        if url.endswith("%20"):
                            url = url[:-3]
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                        host = host.encode('utf-8')
                        # if not host in hostDict: raise Exception()
                        if not filter_host(host):
                            continue
                        # print("OpenMovies SOURCE", stream_url, label)
                        sources.append(
                            {'source': host, 'quality': quality, 'provider': 'Solar', 'url': url, 'direct': False,
                             'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url


def quality_tag(txt):
    if any(value in txt for value in ['1080', '1080p', '1080P']):
        quality = "1080p"

    elif any(value in txt for value in ['720', '720p', '720P']):
        quality = "HD"

    else:
        quality = "SD"
    return quality
