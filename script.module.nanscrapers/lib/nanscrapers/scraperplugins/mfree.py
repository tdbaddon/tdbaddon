import re
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent
from ..scraper import Scraper


class Mfree(Scraper):
    domains = ['m4ufree.info']
    name = "M4U"

    def __init__(self):
        self.base_link = 'http://m4ufree.info'
        self.include_link = '/include/autocomplete.php?q='
        self.movie_search_link = '/tag/%s'
        self.tv_search_link = '/tagtvs/%s'

    def scrape_movie(self, title, year, imdb):
        try:
            headers = {'User-Agent': random_agent()}
            q = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
            query = urlparse.urljoin(self.base_link, self.movie_search_link % q)
            cleaned_title = clean_title(title)
            html = requests.get(query, headers=headers, timeout=30).content
            containers = re.compile('<a class="top-item".*href="(.*?)"><cite>(.*?)</cite></a>').findall(html)
            for href, title in containers:
                parsed = re.findall('(.+?) \((\d{4})', title)
                parsed_title = parsed[0][0]
                parsed_years = parsed[0][1]
                if cleaned_title == clean_title(parsed_title) and year == parsed_years:
                    try:
                        headers = {'User-Agent': random_agent()}
                        html = requests.get(href, headers=headers, timeout=30).content
                        parsed_html = BeautifulSoup(html)
                        quality_title = parsed_html.findAll("h3", attrs={'title': re.compile("Quality of ")})[0]
                        quality = quality_title.findAll('span')[0].text
                        match = re.search('href="([^"]+-full-movie-[^"]+)', html)
                        if match:
                            url = match.group(1)
                            return self.sources(url, "SD")
                    except:
                        pass

        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb):
        headers = {'User-Agent': random_agent()}
        q = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
        query = urlparse.urljoin(self.base_link, self.tv_search_link % q)
        cleaned_title = clean_title(title)
        html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)

        links = html.findAll('a', attrs={'class': 'top-h1'})
        show_url = None

        for link in links:
            link_title = link.text
            if cleaned_title == clean_title(link_title):
                show_url = link["href"]
                break

        if show_url:
            html = BeautifulSoup(requests.get(show_url, headers=headers, timeout=30).content)
            link_container = html.findAll("div", attrs={'class': 'bottom'})[-1]
            episode_links = link_container.findAll("a")
            episode_format1 = "S%02dE%02d" % (int(season), int(episode))
            episode_format2 = "S%02d-E%02d" % (int(season), int(episode))
            for episode_link in episode_links:
                button = episode_link.contents[0]
                episode_text = button.text
                if episode_format1 in episode_text or episode_format2 in episode_text:
                    episode_url = episode_link["href"]
                    return self.sources(episode_url, "SD")

    def sources(self, url, quality):
        sources = []
        try:
            headers = {'User-Agent': random_agent(),
                       'X-Requested-With': 'XMLHttpRequest',
                       'Referer': url}
            html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
            servers = html.findAll("span", attrs={'class': re.compile(".*?btn-eps.*?")})
            for server in servers:
                try:
                    server_url = '/demo.php?v=%s' % server["link"]
                    server_url = urlparse.urljoin(self.base_link, server_url)
                    server_html = requests.get(server_url, headers=headers, timeout=30).content
                    links = []
                    try:
                        links.extend(re.findall(r'sources: \[ \{file: "(.*?)"', server_html, re.I | re.DOTALL))
                    except:
                        pass
                    try:
                        links.extend(re.findall(r'<source.*?src="(.*?)"', server_html, re.I | re.DOTALL))
                    except:
                        pass
                    try:
                        links.extend(re.findall(r'<iframe.*?src="(.*?)"', server_html, re.I | re.DOTALL))
                    except:
                        pass

                    for link in links:
                        try:
                            link_source = link.replace('../view.php?', 'view.php?').replace('./view.php?', 'view.php?')
                            if not link_source.startswith('http'): link_source = urlparse.urljoin(self.base_link,
                                                                                                  link_source)

                            if "m4u" in link_source:
                                try:
                                    req = requests.head(link_source, headers=headers)
                                    if req.headers['Location'] != "":
                                        link_source = req.headers['Location']
                                except:
                                    pass

                            if 'google' in link_source:
                                quality = googletag(link_source)[0]['quality']
                                sources.append(
                                    {'source': 'google video', 'quality': quality, 'scraper': self.name,
                                     'url': link_source,
                                     'direct': True})
                            elif 'openload.co' in link_source:
                                sources.append(
                                    {'source': 'openload.co', 'quality': quality, 'scraper': self.name,
                                     'url': link_source,
                                     'direct': False})
                            else:
                                sources.append(
                                    {'source': 'M4U', 'quality': quality, 'scraper': self.name, 'url': link_source,
                                     'direct': True})
                        except:
                            continue
                except:
                    continue
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
