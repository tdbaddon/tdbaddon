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
import re, urllib, urlparse
import requests
from ..scraper import Scraper
from ..common import random_agent, filter_host
from ..scraper import Scraper
import xbmc


class Solar(Scraper):
    name = "Solar"

    def __init__(self):
        self.base_link = 'http://www.solarmovies.ag'
        self.movie_link = '/%s.html'
        self.ep_link = '/%s.html'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            headers = {'User-Agent': random_agent()}
            title = title.replace(' ', '-')
            title = title + "-" + year
            query = self.movie_link % title
            u = urlparse.urljoin(self.base_link, query)
            self.zen_url.append(u)
            return self.zen_url
        except:
            return

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title, year, season, episode)
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
            for url in self.zen_url:
                if url == None: return

                html = requests.get(url, headers=headers, timeout=10).text

                match = re.compile('<a href="[^"]+go.php\?url=([^"]+)" target="_blank">').findall(html)
                for url in match:
                    try:
                        # print("SOLAR SOURCE", url)
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                        host = host.encode('utf-8')
                        # if not host in hostDict: raise Exception()
                        if not filter_host(host):
                            continue
                        quality = "SD"
                        # print("OpenMovies SOURCE", stream_url, label)
                        sources.append(
                            {'source': host, 'quality': quality, 'provider': 'Solar', 'url': url, 'direct': False,
                             'debridonly': False})
                    except:
                        pass

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
