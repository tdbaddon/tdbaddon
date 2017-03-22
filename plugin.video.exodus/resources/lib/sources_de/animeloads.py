# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper2k4

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

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze
from resources.lib.modules import anilist

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['anime-loads.org']
        self.base_link = 'http://www.anime-loads.org'
        self.search_link = '/search?q=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            if not self.__is_anime('movie', 'imdb', imdb): return

            url = self.__search([title, localtitle, anilist.getAlternativTitle(title)], year)

            if url:
                url = {'url': url}
                url = urllib.urlencode(url)
                return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            if not self.__is_anime('show', 'tvdb', tvdb): return

            url = self.__search([tvshowtitle, localtvshowtitle, tvmaze.tvMaze().showLookup('thetvdb', tvdb).get('name')], year)

            if url:
                url = {'url': url}
                url = urllib.urlencode(url)
                return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            episode = tvmaze.tvMaze().episodeAbsoluteNumber(tvdb, int(season), int(episode))

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'episode': episode})
            return urllib.urlencode(data)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            locDict = [i[0] for i in hostDict]

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = data['url']
            episode = int(data.get('episode', 1))

            r = client.request(urlparse.urljoin(self.base_link, url), headers={'Accept-Encoding': 'gzip'})
            r = client.parseDOM(r, 'div', attrs={'id': 'streams'})

            rels = client.parseDOM(r, 'ul', attrs={'class': '[^\'"]*nav[^\'"]*'})
            rels = client.parseDOM(rels, 'li')
            rels = [(client.parseDOM(i, 'a', attrs={'href': '#stream_\d*'}, ret='href'), client.parseDOM(i, 'a', attrs={'href': '#stream_\d*'})) for i in rels]
            rels = [(re.findall('stream_(\d+)', i[0][0]), re.findall('flag-(\w{2})', i[1][0])) for i in rels if len(i[0]) > 0 and len(i[1]) > 0]
            rels = [(i[0][0], ['subbed'] if i[1][0] != 'de' else []) for i in rels if len(i[0]) > 0 and 'de' in i[1]]

            for id, info in rels:
                rel = client.parseDOM(r, 'div', attrs={'id': 'stream_%s' % id})
                rel = [(client.parseDOM(i, 'div', attrs={'id': 'streams_episodes_%s' % id}), client.parseDOM(i, 'tr')) for i in rel]
                rel = [(i[0][0], [x for x in i[1] if 'fa-desktop' in x]) for i in rel if len(i[0]) > 0 and len(i[1]) > 0]
                rel = [(i[0], client.parseDOM(i[1][0], 'td')) for i in rel if len(i[1]) > 0]
                rel = [(i[0], re.findall('\d{3,4}x(\d{3,4})$', i[1][0])) for i in rel if len(i[1]) > 0]
                rel = [(i[0], i[1][0],) for i in rel if len(i[1]) > 0]

                links = [(x[0], '4K') for x in rel if int(x[1]) >= 2160]
                links += [(x[0], '1440') for x in rel if int(x[1]) >= 1440]
                links += [(x[0], '1080p') for x in rel if int(x[1]) >= 1080]
                links += [(x[0], 'HD') for x in rel if 720 <= int(x[1]) < 1080]
                links += [(x[0], 'SD') for x in rel if int(x[1]) < 720]

                for html, quality in links:
                    try:
                        s = client.parseDOM(html, 'a', attrs={'href': '#streams_episodes_%s_\d+' % id})
                        s = [(client.parseDOM(i, 'div', attrs={'data-loop': '\d+'}, ret='data-loop'), client.parseDOM(i, 'span')) for i in s]
                        s = [(i[0][0], [x for x in i[1] if '<strong' in x]) for i in s if len(i[0]) > 0]
                        s = [(i[0], re.findall('<.+?>(\d+)</.+?> (.+?)$', i[1][0])) for i in s if len(i[1]) > 0]
                        s = [(i[0], i[1][0]) for i in s if len(i[1]) > 0]
                        s = [(i[0], int(i[1][0]), re.findall('Episode (\d+):', i[1][1]), re.IGNORECASE) for i in s if len(i[1]) > 1]
                        s = [(i[0], i[1], int(i[2][0]) if len(i[2]) > 0 else -1) for i in s]
                        s = [(i[0], i[2] if i[2] >= 0 else i[1]) for i in s]
                        s = [i[0] for i in s if i[1] == episode][0]

                        enc = client.parseDOM(html, 'div', attrs={'id': 'streams_episodes_%s_%s' % (id, s)}, ret='data-enc')[0]

                        hosters = client.parseDOM(html, 'a', attrs={'href': '#streams_episodes_%s_%s' % (id, s)})
                        hosters = [client.parseDOM(i, 'i', ret='class') for i in hosters]
                        hosters = [re.findall('hoster-(\w+)', ' '.join(i)) for i in hosters if len(i) > 0][0]
                        hosters = [(re.sub('(co|to|net|pw|sx|tv|moe|ws|icon)$', '', i), i) for i in hosters]
                        hosters = [([x[1] for x in hostDict if x[0] == i[0]][0], i[1]) for i in hosters if i and i[0] in locDict]

                        info = ' | '.join(info)

                        for source, hoster in hosters:
                            sources.append({'source': source, 'quality': quality, 'language': 'de', 'url': [enc, hoster], 'info': info, 'direct': False, 'debridonly': False})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try: return al()._resolve(url)
        except: return

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query, headers={'Accept-Encoding': 'gzip'})

            r = client.parseDOM(r, 'div', attrs={'id': 'main'})
            r = client.parseDOM(r, 'div', attrs={'class': 'panel-body'})
            r = [(client.parseDOM(i, 'h4', attrs={'class': 'title-list'}), client.parseDOM(i, 'a', attrs={'href': '[^\'"]+/year/[^\'"]+'})) for i in r]
            r = [(client.parseDOM(i[0], 'a', ret='href'), client.parseDOM(i[0], 'a'), i[1][0] if len(i[1]) > 0 else '0') for i in r if len(i[0]) > 0]
            r = [(i[0][0], i[1][0], re.sub('<.+?>|</.+?>', '', i[2])) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], i[2].strip()) for i in r if i[2]]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    @staticmethod
    def __is_anime(content, type, type_id):
        try:
            r = 'search/%s/%s?type=%s&extended=full' % (type, type_id, content)
            r = json.loads(trakt.getTrakt(r))
            r = r[0].get(content, []).get('genres', [])
            return 'anime' in r or 'animation' in r
        except:
            return False

exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("MTggMTUsIDgsIDQ2CjQ4IDIxLjRkLjJmIDE4IDFlCgo0MiA1NDoKCTEyIDJjKDQ0KToKCQk0NC4xOSA9IDguOSgnNWE9JykKCQk0NC43ID0gOC45KCc1Nz0nKQoJCTQ0LjE0ID0gOC45KCcyPScpCgkJNDQuMTAgPSAnNDU6Ly81My4zZi0xYi41MC81Mi8lNTgnCgoJMTIgMmUoNDQsIDIyKToKCQkxNywgNTYgPSA0NC41MSgnNGUnLCAyMlswXSkKCQkxNyA9IDE3LjExKCczMicsIFtdKSAxZCAxNy4xMSgnMmInLCAnJykgPT0gJzM1JyAyNiBbXQoJCTE3ID0gWzNlIDI0IDNlIDJhIDE3IDFkIDNlLjExKCczNycsICcnKSA9PSAyMlsxXV1bMF0KCQkxNyA9IDE3LjExKCc0MycsIFtdKQoKCQk1ID0gW10KCgkJMjQgZCAyYSAxNzoKCQkJNTksIGMgPSA0NC41MSgnZCcsIGRbJ2QnXSwgNTYpCgkJCTFkIDU5LjExKCcyYicsICcnKSA9PSAnMzUnIDRjICdkJyAyYSA1OToKCQkJCTUuMzYoNTlbJ2QnXSkKCgkJMWQgMjMoNSkgPj0gMToKCQkJNSA9IDVbMF0gMWQgMjMoNSkgPT0gMSAyNiAnNDA6Ly8nICsgJyAsICcuMmQoNSkKCQkJYiA1CgoJMTIgNTEoNDQsIDE5LCAxYSwgNj00Nyk6CgkJNTUgPSAzYS4yNSh7MTk6IDFhLCAnM2InOiA0NC5lKCl9KQoJCTE3ID0gMzQuMzAoNDQuMTAgJSA0NC4xNCwgNDk9NTUsIDY9NiwgMzk9JzI4JywgNDE9NGIpCgkJNiA9IHsnMjctMWMnOiAxN1szXVsnMjctMWMnXSwgJzNjJzogMTdbNF19CgkJYiA0YS4xYigxN1swXSksIDYKCgkxMiBlKDQ0KToKCQliIDQ0LmEoNDQuMTksIDQ0LjcpCgoJMTIgYSg0NCwgNywgMTMpOgoJCTI5ID0gNDYuMzMoMTYpCgkJM2QgPSAxZS5mKDE1LjRmKDEzKS4yMCgpLCAyOT0yOSkKCQliIDguMWYoMjkgKyAnJy4yZChbM2QuMzEoN1szZTozZSArIDE2XSkgMjQgM2UgMmEgMzgoMCwgMjMoNyksIDE2KV0pKQ==")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|MnZmZDVKTEtsNnNkNVBPUTIwZmRsczk3WU0wM285ZlU|3|4|h_url|headers|phrase|base64|b64decode|_aes_encrypt|return|c|link|_get_cypher|AESModeOfOperationCBC|api_link|get|def|sec_key|api_key|hashlib|16|r|import|key|value|loads|Agent|if|pyaes|b64encode|hexdigest|resources|url|len|for|urlencode|else|User|extended|iv|in|code|__init__|join|_resolve|modules|request|encrypt|content|urandom|client|success|append|hoster|xrange|output|urllib|cypher|Cookie|aes|i|anime|stack|error|class|links|self|http|os|None|from|post|json|True|and|lib|enc|md5|org|_get_api_result|api|www|al|p|h|ZXhvZHVzZjJhM2JCYWQ5OTQ3MDhEZDU4ZWM5MTQwZEM|s|result|YkJhZDk5OGYyMUNhM2FkOTlEZDQ3ZDhlYzlleG9kdXM".split("|")))