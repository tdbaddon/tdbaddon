import json
import re
import urllib
import urlparse

from BeautifulSoup import BeautifulSoup
from .. import proxy
from ..common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper
from ..modules import cfscrape
import xbmc


class Xmovies(Scraper):
    domains = ['xmovies8.tv']
    name = "xmovies"

    def __init__(self):
        self.base_link = 'https://xmovies8.ru'
        self.search_link = '/movies/search?s=%s'
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            headers = {'User-Agent': random_agent()}
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)
            # print ("XMOVIES query", query)
            cleaned_title = clean_title(title)
            prehtml = self.scraper.get(query, headers=headers, timeout=30)
            html = BeautifulSoup(prehtml.content)
            containers = html.findAll('div', attrs={'class': 'item_movie'})
            # print ("XMOVIES r1", containers)
            for container in containers:
                try:
                    links = container.findAll('h2', attrs={'class': 'tit'})[0]
                    r = links.findAll('a')
                    for link in r:
                        link_title = link['title'].encode('utf-8')
                        href = link['href'].encode('utf-8')
                        if len(link_title) > 0 and len(href) > 0:
                            parsed = re.findall('(.+?) \((\d{4})', link_title)
                            parsed_title = parsed[0][0]
                            parsed_years = parsed[0][1]
                            if cleaned_title.lower() == clean_title(parsed_title).lower() and year == parsed_years:
                                if not "http:" in href: href = "http:" + href
                                return self.sources(replaceHTMLCodes(href))
                except:
                    pass
        except:
            pass
        return []

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            absolute_url = urlparse.urljoin(self.base_link, url)
            referer_url = url.replace('watching.html', '') + 'watching.html'

            headers = {'User-Agent': random_agent}
            post = self.scraper.get(absolute_url, headers=headers, timeout=30).content

            post = re.findall('movie=(\d+)', post)[0]
            post = {'id': post, 'episode_id': '0', 'link_id': '0', 'from': 'v3'}

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Accept-Formating': 'application/json, text/javascript',
                       'Server': 'cloudflare-nginx'}
            headers['Referer'] = referer_url
            headers['User-Agent'] = random_agent()
            load_episode_url = urlparse.urljoin(self.base_link, '/ajax/movie/load_episodes')
            html = BeautifulSoup(self.scraper.post(load_episode_url, data=post, headers=headers).content)

            pattern = re.compile("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?")
            links = html.findAll('a', attrs={'onclick': pattern})

            for link in links:
                info = re.findall(pattern, link['onclick'])[0]  # (id, quality) quality can be 0
                try:
                    play = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v2')
                    post = {'id': info[0], 'quality': info[1]}
                    player_url = self.scraper.post(play, data=post, headers=headers).content

                    json_url = json.loads(player_url)['link']

                    response = proxy.get_raw(json_url, headers=headers)
                    video_url = response.geturl()

                    try:
                        unproxied_video_url = urlparse.parse_qs(urlparse.urlparse(video_url).query)['u'][0]
                    except:
                        pass
                    try:
                        unproxied_video_url = urlparse.parse_qs(urlparse.urlparse(video_url).query)['q'][0]
                    except:
                        pass
                        pass

                    if 'openload.' in unproxied_video_url:
                        sources.append(
                            {'source': 'openload.co', 'quality': 'HD', 'scraper': self.name, 'url': unproxied_video_url,
                             'direct': False})

                    else:
                        sources.append(
                            {'source': 'google video', 'quality': googletag(unproxied_video_url)[0]['quality'],
                             'scraper': self.name, 'url': unproxied_video_url, 'direct': True})
                except:
                    continue
            return sources
        except:
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
