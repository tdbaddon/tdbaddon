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
import json

from resources.lib.modules import client, cleantitle, directstream


class source:
    def __init__(self):
        self.domains = ['fmovies.se', 'fmovies.to']
        self.base_link = 'https://fmovies.se'
        self.movie_search_path = ('/filter?keyword=%s&sort=post_date:Adesc'
                                  '&type[]=movie&release[]=%s')
        self.episode_search_path = ('/filter?keyword=%s&sort=post_date:Adesc'
                                    '&type[]=series')
        self.film_path = '/film/%s'
        self.info_path = '/ajax/episode/info?ts=%s&_=%s&id=%s&update=0'
        self.grabber_path = '/grabber-api/?ts=%s&id=%s&token=%s&mobile=0'

    def movie(self, imdb, title, year):
        try:
            clean_title = cleantitle.geturl(title)
            query = (self.movie_search_path % (clean_title, year))
            url = urlparse.urljoin(self.base_link, query)

            search_response = client.request(url)

            results_list = client.parseDOM(
                search_response, 'div', attrs={'class': 'item'})[0]
            film_id = re.findall('(\/film\/)([^\"]*)', results_list)[0][1]

            query = (self.film_path % film_id)
            url = urlparse.urljoin(self.base_link, query)

            film_response = client.request(url)

            ts = re.findall('(data-ts=\")(.*?)(\">)', film_response)[0][1]

            sources_dom_list = client.parseDOM(
                film_response, 'ul', attrs={'class': 'episodes range active'})
            sources_list = []

            for i in sources_dom_list:
                source_id = re.findall('([\/])(.{0,6})(\">)', i)[0][1]
                sources_list.append(source_id)

            data = {
                'ts': ts,
                'sources': sources_list
            }
            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):

        try:
            data = {
                'imdb': imdb,
                'tvdb': tvdb,
                'tvshowtitle': tvshowtitle,
                'year': year
            }
            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):

        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)

            clean_title = cleantitle.geturl(data['tvshowtitle'])
            query = (self.episode_search_path % clean_title)
            url = urlparse.urljoin(self.base_link, query)

            search_response = client.request(url)

            results_list = client.parseDOM(
                search_response, 'div', attrs={'class': 'row movie-list'})[0]

            film_id = ''

            film_tries = [
             '\/' + (clean_title + '-0' + season) + '[^-0-9](.+?)\"',
             '\/' + (clean_title + '-' + season) + '[^-0-9](.+?)\"',
             '\/' + clean_title + '[^-0-9](.+?)\"'
             ]

            for i in range(len(film_tries)):
                if not film_id:
                    film_id = re.findall(film_tries[i], results_list)
                else:
                    break

            film_id = film_id[0]

            query = (self.film_path % film_id)
            url = urlparse.urljoin(self.base_link, query)

            film_response = client.request(url)

            ts = re.findall('(data-ts=\")(.*?)(\">)', film_response)[0][1]

            sources_dom_list = client.parseDOM(
                film_response, 'ul', attrs={'class': 'episodes range active'})

            if not re.findall(
             '([^\/]*)\">' + episode + '[^0-9]', sources_dom_list[0]):
                episode = '%02d' % int(episode)

            sources_list = []

            for i in sources_dom_list:
                source_id = re.findall(
                    ('([^\/]*)\">' + episode + '[^0-9]'), i)[0]
                sources_list.append(source_id)

            data.update({
                'ts': ts,
                'sources': sources_list
            })

            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            data['sources'] = re.findall("[^', u\]\[]+", data['sources'])

            for i in data['sources']:
                token = str(self.__token(
                    {'id': i, 'update': '0', 'ts': data['ts']}))
                query = (self.info_path % (data['ts'], token, i))
                url = urlparse.urljoin(self.base_link, query)

                info_response = client.request(url, XHR=True)

                grabber_dict = json.loads(info_response)

                if grabber_dict['type'] == 'direct':
                    token64 = grabber_dict['params']['token']
                    query = (self.grabber_path % (data['ts'], i, token64))
                    url = urlparse.urljoin(self.base_link, query)

                    response = client.request(url, XHR=True)

                    sources_list = json.loads(response)['data']

                    for j in sources_list:
                        source = directstream.googletag(j['file'])[0]

                        sources.append({
                            'source': 'gvideo',
                            'quality': source['quality'],
                            'provider': 'Fmovies',
                            'url': source['url'],
                            'direct': True,
                            'debridonly': False
                        })

            return sources

        except Exception:
            return sources

    def resolve(self, url):

        try:
            if not url.startswith('http'):
                url = 'http:' + url

            for i in range(3):
                url = directstream.googlepass(url)

                if url:
                    break

            return url

        except Exception:
            return

    def __token(self, d):
        try:
            token = 857

            for k, v in d.iteritems():
                n = 0

                k = 'location' + k

                for i in range(len(k)):
                    n += ord(v[i]) if i < len(v) else 0
                    n += ord(k[i]) if i < len(k) else 0

                n = hex(n)[2:]
                i = 0

                for e in range(len(n)):
                    i += ord(n[e])

                token += i

            return token

        except Exception:
            return
