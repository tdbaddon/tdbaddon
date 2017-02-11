
import re
import string
import urlparse
from libs import kodi
import scraper_utils
import main_scrape
import scrapeit



def __enum(**enums):
    return type('Enum', (), enums)

FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')



BASE_URL = kodi.get_setting('afdah_base_url')


class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('afdah_base_url')
        #kodi.log(self.base_url)

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'afdah'

    def get_sources(self, video):
        #kodi.log(video.url)
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            match = re.search('This movie is of poor quality', html, re.I)
            if match:
                quality = QUALITIES.LOW
            else:
                quality = QUALITIES.HIGH

            for match in re.finditer('href="([^"]+/embed\d*/[^"]+)', html):
                url = match.group(1)
                embed_html = self._http_get(url, cache_limit=.5)
                r = re.search('{\s*write\("([^"]+)', embed_html)
                if r:
                    plaintext = self._caesar(r.group(1), 13).decode('base-64')
                    if 'http' not in plaintext:
                        plaintext = self._caesar(r.group(1).decode('base-64'), 13).decode('base-64')
                else:
                    plaintext = embed_html
                hosters += self._get_links(plaintext)

            pattern = 'href="([^"]+)"[^>]*><[^>]+play_video.gif'
            for match in re.finditer(pattern, html, re.I):
                url = match.group(1)
                host = urlparse.urlparse(url).hostname
                hoster = {'hostname':'Afdah','multi-part': False, 'url': url, 'host': host, 'class': '',
                          'quality': scraper_utils.get_quality(video, host, quality), 'rating': None, 'views': None,
                          'direct': False}
                hosters.append(hoster)
                main_scrape.apply_urlresolver(hosters)
        return hosters

    def _get_links(self, html):
        hosters = []
        for match in re.finditer('file\s*:\s*"([^"]+).*?label\s*:\s*"([^"]+)', html):
            url, resolution = match.groups()
            url += '|User-Agent=%s&Cookie=%s' % (scraper_utils.get_ua(), self._get_stream_cookies())
            hoster = {'multi-part': False, 'url': url, 'host': self._get_direct_hostname(url), 'class': self,
                      'quality': scraper_utils.height_get_quality(resolution), 'rating': None, 'views': None,
                      'direct': True}
            hosters.append(hoster)
        return hosters

    def _caesar(self, plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/wp-content/themes/afdah/ajax-search.php')
        #kodi.log(search_url)
        data = {'search': title, 'type': 'title'}
        html = self._http_get(search_url, data=data, cache_limit=1)
        #kodi.log(html)
        pattern = '<li>.*?href="([^"]+)">([^<]+)\s+\((\d{4})\)'
        results = []
        for match in re.finditer(pattern, html, re.DOTALL | re.I):
            url, match_title, match_year = match.groups('')
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title),
                          'year': year}
                results.append(result)
        return results
