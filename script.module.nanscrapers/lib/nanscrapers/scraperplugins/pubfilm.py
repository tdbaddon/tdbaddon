import StringIO
import gzip
import re
import urlparse
from BeautifulSoup import BeautifulSoup
from ..common import random_agent, replaceHTMLCodes, clean_title
from ..scraper import Scraper
from nanscrapers.modules import cfscrape
import xbmcaddon
import urllib
import xbmc

class Pubfilm(Scraper):
    domains = ['pubfilmno1.com', 'pubfilm.com', 'pidtv.com', 'pubfilm.is']
    name = "pubfilm"

    def __init__(self):
        self.base_link = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_baseurl" % (self.name))
        self.moviesearch_hd_link = '/%s-%s-full-hd-pubfilm-free.html'
        self.moviesearch_sd_link = '/%s-%s-pubfilm-free.html'
        self.tvsearch_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            cleanmovie = clean_title(title) 
            headers = {'User-Agent': random_agent(), 'X-Requested-With':'XMLHttpRequest', 'Referer': "http://pubfilm.is/"}
            search_url = urlparse.urljoin(self.base_link, '/wp-content/plugins/ajax-search-pro/ajax_search.php')
            data = {'action': 'ajaxsearchpro_search', 'aspp': title, 'asid' : '1', 'asp_inst_id': '1_1', 'options': 'current_page_id=29697&qtranslate_lang=0&set_intitle=None&customset%5B%5D=post'}
            moviesearch = self.scraper.post(search_url, headers=headers, data=data)
            moviesearch = moviesearch.content
            match = re.compile('<a class="asp_res_url" href=\'(.+?)\'.*?>(.+?)<span class=\'overlap\'></span>.*?</a>', flags=re.DOTALL).findall(moviesearch)
            for href, movietitle in match:
                movietitle = movietitle.replace('\n', '').strip()
                if year in movietitle and cleanmovie in clean_title(movietitle):
                    url = href.encode('utf-8')
                    if not "http" in url: url = urlparse.urljoin(self.base_link, url)
                    return self.sources(url)
        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            cleantitle = clean_title(title) 
            headers = {'User-Agent': random_agent(), 'X-Requested-With':'XMLHttpRequest', 'Referer': "http://pubfilm.is/"}
            search_url = urlparse.urljoin(self.base_link, '/wp-content/plugins/ajax-search-pro/ajax_search.php')
            data = {'action': 'ajaxsearchpro_search', 'aspp': title, 'asid' : '1', 'asp_inst_id': '1_1', 'options': 'current_page_id=29697&qtranslate_lang=0&set_intitle=None&customset%5B%5D=post'}
            tvsearch = self.scraper.post(search_url, headers=headers, data=data)
            tvsearch = tvsearch.content
            match = re.compile('<a class="asp_res_url" href=\'(.+?)\'.*?>(.+?)<span class=\'overlap\'></span>.*?</a>', flags=re.DOTALL).findall(tvsearch)
            for href, linktitle in match:
                linktitle = linktitle.replace('\n', '').strip()
                for try_year in [str(year), str(int(year) - 1), str(int(year) + 1)]:
                    clean_link_title = clean_title(linktitle)
                    if (try_year in linktitle or show_year in linktitle) and cleantitle in clean_link_title and "season" + season in clean_link_title:
                        url = href.encode('utf-8')
                        if not "http" in url: url = urlparse.urljoin(self.base_link, url)
                        episode_url = url + '?episode=%01d' % int(episode)
                        return self.sources(episode_url)
        except:
            pass
        return []

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            if not self.base_link in url:
                url = urlparse.urljoin(self.base_link, url)

            content = re.compile('(.+?)\?episode=\d*$').findall(url)
            video_type = 'movie' if len(content) == 0 else 'episode'

            try:
                url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except:
                pass

            headers = {'User-Agent': random_agent()}
            html = self.scraper.get(url, headers=headers, timeout=30).content

            try:
                compressedstream = StringIO.StringIO(html)
                html = gzip.GzipFile(fileobj=compressedstream).read()
                html = BeautifulSoup(html)
            except:
                html = BeautifulSoup(html)

            links = html.findAll('a', attrs={'target': 'EZWebPlayer'})
            for link in links:
                href = replaceHTMLCodes(link['href'])
                if not "get.php" in href:
                    continue

                if video_type == 'episode':
                    link_episode_number = re.compile('(\d+)').findall(link.string)
                    if len(link_episode_number) > 0:
                        link_episode_number = link_episode_number[-1]
                        if not link_episode_number == '%01d' % int(episode):
                            continue

                referer = url
                headers = {'User-Agent': random_agent(), 'Referer': referer}
                html = self.scraper.get(href, headers=headers, timeout=30).content
                source = re.findall('sources\s*:\s*\[(.+?)\]', html)[0]
                files = re.findall('"file"\s*:\s*"(.+?)".+?"label"\s*:\s*"(.+?)"', source)
                if files:
                    quality_url_pairs = [{'url': file[0], 'quality': file[1]} for file in files]
                else:
                    files = re.findall('"file"\s*:\s*"(.+?)".+?}', source)
                    quality_url_pairs = [{'url': file, 'quality': "SD"} for file in files]

                for pair in quality_url_pairs:
                    sources.append(
                        {'source': 'google video', 'quality': pair['quality'], 'scraper': self.name, 'url': pair['url'],
                         'direct': True})
        except:
            pass

        return sources

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name),
            '<setting id= "%s_baseurl" type="text" label="Base Url" default="http://pubfilm.is"/>' % (clas.name)
        ]
        return xml

