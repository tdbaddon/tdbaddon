import re
import urllib
import urlparse
from libs import log_utils
from libs import kodi
import scraper_utils
import scrapeit
from libs import dom_parser
import main_scrape


def __enum(**enums):
    return type('Enum', (), enums)

FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
########ALL NEED ABOVE#############


QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}

BASE_URL = kodi.get_setting('putlocker_base_url')

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('putlocker_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Putlocker'

    def resolve_link(self, link):
        if not link.startswith('http'):
            stream_url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(stream_url, cache_limit=0)
            iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
            if iframe_url:
                return iframe_url[0]
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            headers = {'Referer': ''}
            html = self._http_get(page_url, headers=headers, cache_limit=.5)
            page_links = []
            for iframe_url in dom_parser.parse_dom(html, 'iframe', ret='src'):
                if 'youtube' not in iframe_url:
                    host = urlparse.urlparse(iframe_url).hostname
                    page_links.append((iframe_url, 'embedded', host))

            page_links += re.findall('<a[^>]+href="([^"]+)[^>]+>(Version \d+)</a>([^<]+)', html)

            for stream_url, version, host in page_links:
                if not stream_url.startswith('http'):
                    url = source_url + stream_url
                    host = host.replace('&nbsp;', '')
                else:
                    url = stream_url
                    host = urlparse.urlparse(stream_url).hostname

                base_quality = QUALITIES.HD720 if version == 'embedded' else QUALITIES.HIGH
                hoster = {'hostname': 'Putlocker','multi-part': False, 'host': host, 'class': self,
                          'quality': scraper_utils.get_quality(video, host, base_quality), 'views': None,
                          'rating': None, 'url': url, 'direct': False}
                hoster['version'] = '(%s)' % (version)
                hosters.append(hoster)

        fullsource = main_scrape.apply_urlresolver(hosters)
        return fullsource

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/?s=%s&submit=Search+Now!' % (urllib.quote_plus(title)))
        headers = {'Referer': search_url}
        html = self._http_get(search_url, headers=headers, cache_limit=8)
        index = 0 if video_type == 'shows' else 1
        fragments = re.findall('<h2.*?(?=<h2|$)', html, re.DOTALL)
        if len(fragments) > index:
            for item in dom_parser.parse_dom(fragments[index], 'div', {'class': 'aaa_item'}):
                match_title_year = dom_parser.parse_dom(item, 'a', ret='title')
                match_url = dom_parser.parse_dom(item, 'a', ret='href')
                if match_title_year and match_url:
                    match_url = match_url[0]
                    match_title_year = match_title_year[0]
                    match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''

                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url),
                                  'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

    def _get_episode_url(self, show_url, video, sea, epi):
        episode_pattern = 'href="([^"]+season-%s-episode-%s-[^"]+)' % (sea,epi)
        title_pattern = 'href="(?P<url>[^"]+season-\d+-episode-\d+-[^"]+).*?\s+-\s+(?P<title>.*?)</td>'
        headers = {'Referer': urlparse.urljoin(self.base_url, show_url)}
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, headers=headers)
