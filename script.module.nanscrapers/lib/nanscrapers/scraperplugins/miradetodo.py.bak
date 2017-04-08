import json
import re
import urllib
import urllib2
import urlparse

import xbmc
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import random_agent, clean_title
from ..scraper import Scraper


class Miradetodo(Scraper):
    domains = ['miradetodo.net']
    name = "miradetodo"

    def __init__(self):
        self.base_link = 'http://miradetodo.net'
        self.search_link = '/?s=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if imdb is None:  # TODO get imdb from title
                return
            imdb_title = self.get_imdb_title(imdb)

            query_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(imdb_title))

            headers = {'User-Agent': random_agent()}
            request = urllib2.Request(query_url, headers=headers)
            html = BeautifulSoup(urllib2.urlopen(request))

            items = html.findAll('div', attrs={'class': 'item'})
            for item in items:
                item_title = item.findAll('span', attrs={'class': 'tt'})[0].text.encode('utf-8')
                item_year = item.findAll('span', attrs={'class': 'year'})[0].text
                link = item.findAll('a')[0]
                href = link['href']
                if clean_title(imdb_title) == clean_title(item_title) and year == item_year:
                    movie_url = re.findall('(?://.+?|)(/.+)', href)[0]
                    return self.sources(movie_url)
        except:
            pass
        return []


    # def scrape_episode(self, title, year, season, episode, imdb, tvdb):
    #     if imdb is None:  # TODO get imdb from title
    #         return
    #     imdb_title = self.get_imdb_title(imdb)
    #
    #     query_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(imdb_title))
    #
    #     headers = {'User-Agent': random_agent()}
    #     request = urllib2.Request(query_url, headers=headers)
    #     html = BeautifulSoup(urllib2.urlopen(request))
    #
    #     items = html.findAll('div', attrs={'class': 'item'})
    #     for item in items:
    #         item_title = item.findAll('span', attrs={'class': 'tt'})[0].text.encode('utf-8')
    #         item_year = item.findAll('span', attrs={'class': 'year'})[0].text
    #         link = item.findAll('a')[0]
    #         href = link['href']
    #         if clean_title(imdb_title) == clean_title(item_title):
    #             relative_show_url = re.findall('(?://.+?|)(/.+)', href)[0]
    #             show_url = urlparse.urljoin(self.base_link, relative_show_url)
    #             request = urllib2.Request(show_url, headers=headers)
    #             show_html = BeautifulSoup(urllib2.urlopen(request))
    #             episodes = show_html.findAll('ul', attrs={'class': 'episodios'})
    #             for show_episode in episodes:
    #                 number = show_episode.findAll('div', attrs={'class': 'numerando'})[0].text
    #                 parsed = re.findall('(\d+)\s*x\s*(\d+)', number)[0]
    #                 episode_number = parsed[0]
    #                 season_number = parsed[1]
    #                 if episode_number == episode and season_number == season:
    #                     episode_url = show_episode.findAll('a')[0]["href"]
    #                     return self.movie_sources(episode_url)


    def get_imdb_title(self, imdb):
        headers = {'User-Agent': random_agent(), 'Accept-Language': 'es-AR'}
        request = urllib2.Request('http://www.imdb.com/title/%s' % imdb, headers=headers)
        html = BeautifulSoup(urllib2.urlopen(request))
        html_title = html.findAll("title")[0].text.encode('utf-8')
        imdb_title = re.sub('(?:\(||\(TV Series\s|\s)\d{4}.+', '', html_title).strip()
        return imdb_title

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)  # get absolute url

            headers = {'User-Agent': random_agent()}
            request = urllib2.Request(url, headers=headers)
            html = BeautifulSoup(urllib2.urlopen(request))

            movie_plays = html.findAll('div', attrs={'class': 'movieplay'})
            player_link_ids = []
            containers = []
            if len(movie_plays) > 0: #movie
                containers = movie_plays
            else:
                containers = html.findAll('div', attrs={'class': 'player2'})

            for container in containers:
                try:
                    player_link = container.findAll('iframe')[0]['data-lazy-src']
                    player_link_id = urlparse.parse_qs(urlparse.urlparse(player_link).query)['id'][0]
                    if player_link_id in player_link_ids:
                        continue
                    player_link_ids.append(player_link_id)

                    headers['X-Requested-With'] = 'XMLHttpRequest'
                    headers['Referer'] = player_link

                    post = urllib.urlencode({'link': player_link_id})

                    gkplugins_url = urlparse.urljoin(self.base_link, '/stream/plugins/gkpluginsphp.php')
                    request = urllib2.Request(gkplugins_url, data=post, headers=headers)
                    links = json.loads(urllib2.urlopen(request).read())['link']

                    link_infos = []

                    if type(links) is list:
                        for link in links:
                            link_infos.append({'url': link['link'], 'quality': link['label'][:-1]})
                    else:
                        link_infos = [{'url': url, 'quality': 'HD'}]  # TODO check quality another way

                    for link_info in link_infos:
                        if 'google' in link_info['url'] or 'blogspot' in link_info['url']:
                            sources.append(
                                {'source': 'google video', 'quality': link_info['quality'], 'scraper': self.name,
                                 'url': link_info['url'], 'direct': True})
                except:
                    pass
        except:
            return sources

        return sources
