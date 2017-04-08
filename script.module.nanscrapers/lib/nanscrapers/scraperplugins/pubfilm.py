import StringIO
import gzip
import re
import urlparse
from BeautifulSoup import BeautifulSoup
from ..common import random_agent, replaceHTMLCodes
from ..scraper import Scraper
from nanscrapers.modules import cfscrape
import xbmcaddon

class Pubfilm(Scraper):
    domains = ['pubfilmno1.com', 'pubfilm.com', 'pidtv.com']
    name = "pubfilm"

    def __init__(self):
        self.base_link = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_baseurl" % (self.name))
        self.moviesearch_hd_link = '/%s-%s-full-hd-pubfilm-free.html'
        self.moviesearch_sd_link = '/%s-%s-pubfilm-free.html'
        self.tvsearch_link = '/wp-admin/admin-ajax.php'
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            title = title.translate(None, '\/:*?"\'<>|!,').replace(' ', '-').replace('--', '-').lower()
            headers = {'User-Agent': random_agent()}
            search_url = urlparse.urljoin(self.base_link, self.moviesearch_hd_link % (title, year))
            html = None
            try:
                prehtml = self.scraper.get(search_url, headers=headers, timeout=30)
                if prehtml.status_code != 404:
                    html = BeautifulSoup(prehtml.content)
            except:
                pass

            if html == None:
                search_url = urlparse.urljoin(self.base_link, self.moviesearch_sd_link % (title, year))

                html = BeautifulSoup(self.scraper.get(search_url, headers=headers, timeout=30).content)
            if html == None:
                raise Exception()
            return self.sources(search_url)
        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            for try_year in [str(year), str(int(year) - 1)]:
                tvshowtitle = '%s %s: Season %s' % (title, try_year, season)
                headers = {'X-Requested-With': 'XMLHttpRequest',
                           'User-Agent': random_agent()}

                post = {'aspp': tvshowtitle, 'action': 'ajaxsearchpro_search',
                        'options': 'qtranslate_lang=0&set_exactonly=checked&set_intitle=None&customset[]=post',
                        'asid': '4', 'asp_inst_id': '4_1'}

                url = urlparse.urljoin(self.base_link, self.tvsearch_link)
                html = BeautifulSoup(self.scraper.post(url, data=post, headers=headers, timeout=30).content)
                links = html.findAll('a', attrs={'class': 'asp_res_url'})
                show_url = None
                for link in links:
                    href = link["href"]
                    link_tvshowtitle = re.findall('(.+?: Season \d+)', link.contents[0].strip())[0]
                    if title.lower() in link_tvshowtitle.lower() and str(season) in link_tvshowtitle:
                        if try_year in link_tvshowtitle:
                            show_url = href
                            break
                if show_url is None:
                    continue
                episode_url = show_url + '?episode=%01d' % int(episode)
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
                    quality_url_pairs = [{'url': file[0], 'quality': file[1][:-1]} for file in files]
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
            '<setting id= "%s_baseurl" type="text" label="Base Url" default="http://pubfilm.ac"/>' % (clas.name)
        ]
        return xml
