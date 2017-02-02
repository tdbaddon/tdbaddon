# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import base64
import json
import re
import urllib

from resources.lib.modules import client
from resources.lib.modules import logger
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.domains = ['fimlywap.im.to']
        self.base_link = 'http://fimlywap.desi'
        #self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5QktzR2FGempSMVF5eWxNUGM2elZvUDcxVXM1N2k5bUVrJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxMzA1Mjg2NDc5NDEyNDIwMTQ1MTpkZXl3cW1mNDVhYSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        #exodus
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNjE2OTI4MDMzMzcxNDY1MDkyNzotMGVwYXI3djBqeSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

    def movie(self, imdb, title, year):
        try:
            t = cleantitle.movie(title)

            try:
                query = '%s %s' % (title, year)
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.request(query)
                result = json.loads(result)['results']
                r = [(i['url'], i['titleNoFormatting']) for i in result]
                r = [(i[0], re.compile('(.+?) [\d{4}|(\d{4})]').findall(i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if t == cleantitle.movie(i[1])]
                u = [i[0] for i in r][0]

            except:
                return

            url = u
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            srcs = []

            if url == None: return sources

            #result = base64.b64decode("ICAgICAgPC9kaXY+DQogICAgICAgIDwvdGJvZHk+DQogICAgICA8L3RhYmxlPg0KICAgIAkgICAgDQogICAgPC9kaXY+DQoNCiAgICAgICAgICAgIA0KCTxkaXYgY2xhc3M9InRpdGxlIj5Eb3dubG9hZCBGdWxsIE1vdmllIEluOjwvZGl2Pg0KCQkJPGR0Pg0KICAgIDx0YWJsZSBjbGFzcz0icm93cyBkaWZmZXJfZG93bmxvYWQiIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCI+DQogICAgICAgIDx0Ym9keT4NCiAgICAgICAgCQkJCQkJPHRyPg0KCQkJCQkJPHRkPjxzcGFuIGNsYXNzPSJsZWZ0LWRlc2lnbiI+PC9zcGFuPg0KCQkJCQkJCQ0KCQkJCQkJCTxhIGhyZWY9Imh0dHA6Ly9wbS5pbnN1cmFuY2ViYW5rLm9yZy9kb3dubG9hZC5waHA/c29uZ19pZD0xNzQ5JnVybF9pZD0zNDM0MSI+DQoJCQkJCQkJCURvd25sb2FkIDxzcGFuIGNsYXNzPSJxdWFsaXR5XzEiPjNHUDwvc3Bhbj4NCgkJCQkJCQk8L2E+IA0KCQkJCQkJCTxzbWFsbD4NCgkJCQkJCQkJPHNwYW4gc3R5bGU9ImNvbG9yOmdyZWVuO2ZvbnQtc2l6ZToxMHB4OyI+KCAyNzIuNjggTUIpPC9zcGFuPg0KCQkJCQkJCTwvc21hbGw+DQoJCQkJCQk8L3RkPg0KCQkJCQk8L3RyPg0KCQkJCQkJCQk8dHI+DQoJCQkJCQk8dGQ+PHNwYW4gY2xhc3M9ImxlZnQtZGVzaWduIj48L3NwYW4+DQoJCQkJCQkJDQoJCQkJCQkJPGEgaHJlZj0iaHR0cDovL3BtLmluc3VyYW5jZWJhbmsub3JnL2Rvd25sb2FkLnBocD9zb25nX2lkPTE3NDkmdXJsX2lkPTM0MzM2Ij4NCgkJCQkJCQkJRG93bmxvYWQgPHNwYW4gY2xhc3M9InF1YWxpdHlfMSI+TVA0PC9zcGFuPg0KCQkJCQkJCTwvYT4gDQoJCQkJCQkJPHNtYWxsPg0KCQkJCQkJCQk8c3BhbiBzdHlsZT0iY29sb3I6Z3JlZW47Zm9udC1zaXplOjEwcHg7Ij4oIDQyNi4xNiBNQik8L3NwYW4+DQoJCQkJCQkJPC9zbWFsbD4NCgkJCQkJCTwvdGQ+DQoJCQkJCTwvdHI+DQoJCQkJCQkJCTx0cj4NCgkJCQkJCTx0ZD48c3BhbiBjbGFzcz0ibGVmdC1kZXNpZ24iPjwvc3Bhbj4NCgkJCQkJCQkNCgkJCQkJCQk8YSBocmVmPSJodHRwOi8vcG0uaW5zdXJhbmNlYmFuay5vcmcvZG93bmxvYWQucGhwP3NvbmdfaWQ9MTc0OSZ1cmxfaWQ9MzQzMzAiPg0KCQkJCQkJCQlEb3dubG9hZCA8c3BhbiBjbGFzcz0icXVhbGl0eV8xIj5NcDQgKDM2MHApPC9zcGFuPg0KCQkJCQkJCTwvYT4gDQoJCQkJCQkJPHNtYWxsPg0KCQkJCQkJCQk8c3BhbiBzdHlsZT0iY29sb3I6Z3JlZW47Zm9udC1zaXplOjEwcHg7Ij4oIDg0NS41NCBNQik8L3NwYW4+DQoJCQkJCQkJPC9zbWFsbD4NCgkJCQkJCTwvdGQ+DQoJCQkJCTwvdHI+DQoJCQkJCQkJCTx0cj4NCgkJCQkJCTx0ZD48c3BhbiBjbGFzcz0ibGVmdC1kZXNpZ24iPjwvc3Bhbj4NCgkJCQkJCQkNCgkJCQkJCQk8YSBocmVmPSJodHRwOi8vcG0uaW5zdXJhbmNlYmFuay5vcmcvZG93bmxvYWQucGhwP3NvbmdfaWQ9MTc0OSZ1cmxfaWQ9MzQzMjQiPg0KCQkJCQkJCQlEb3dubG9hZCA8c3BhbiBjbGFzcz0icXVhbGl0eV8xIj5NcDQgKDcyMHApPC9zcGFuPg0KCQkJCQkJCTwvYT4gDQoJCQkJCQkJPHNtYWxsPg0KCQkJCQkJCQk8c3BhbiBzdHlsZT0iY29sb3I6Z3JlZW47Zm9udC1zaXplOjEwcHg7Ij4oIDEuMDggR0IpPC9zcGFuPg0KCQkJCQkJCTwvc21hbGw+DQoJCQkJCQk8L3RkPg0KCQkJCQk8L3RyPg0KCQkJCQkJPHRyPg0KCQkJCTx0ZD4NCgkJCQkJCQkJCTwvdGQ+DQoJCQk8L3RyPg0KCQkJCQkJDQoJCQkJPHRyPg0KCQkJPHRkIGNsYXNzPSJuZXh0LW1vdmllIj4JDQoJCQkJPGEgaHJlZj0iLzE3NDlwL0Rvd25sb2FkLVZpZGVvLWluLXBhcnRzUHJlbS1SYXRhbi1EaGFuLVBheW8tMjAxNS1IRHMtRFZEUmlwLS0uaHRtIj4NCgkJCQkJRG93bmxvYWQgTW92aWUgaW50byBQYXJ0cw0KCQkJCTwvYT4NCgkJCTwvdGQ+DQoJCTwvdHI+DQoJCQkJPHRyPg0KCQkJPHRkPgkNCgkJCQkJCQk8L3RkPg0KCQk8L3RyPg0KICAgICAgICA8L3Rib2R5Pg0KCTwvdGFibGU+")
            result = client.request(url)
            #links = client.parseDOM(result, 'div', attrs = {'class': 'listed'})

            result = result.replace('\n','').replace('\t','').replace('\r','')

            result = client.parseDOM(result, "div", attrs={"id": "main"})[0]

            #result = re.compile('Download Full Movie In:(.+?)Download Movie into Parts').findall(result)
            #result = re.compile('Download Full Movie In:(.+?)Download Movie into Parts').findall(result)[0]
            result = re.compile('Download Full Movie In:</div>(.+?)<div class=\"next-movie\">').findall(result)[0]
            #result = client.parseDOM(result, name="div", attrs={"class":"head"})[0]
            #links = client.parseDOM(result, name="div")
            #if len(links) == 0:
            #    links = client.parseDOM(result, name="div", attrs={'class':'listed'})

            quality = client.parseDOM(result, "a")
            links = client.parseDOM(result, "a", ret="href")

            links = dict(zip(quality, links))
            for key in links:
                if not 'quality_1' in key:
                    continue
                try: quality = client.parseDOM(key, 'span', attrs = {'class': 'quality_1'})[0].lower()
                except: quality = 'hd'
                if quality == 'ts': quality = 'CAM'
                elif '360p' in quality : quality = 'SD'
                elif '720p' in quality : quality = 'HD'
                else: quality = 'SD'

                url = links[key]
                host = client.host(url)

                srcs.append({'source': host, 'parts' : '1', 'quality': quality, 'provider': 'filmywap', 'url': url, 'direct': False, 'debridonly': False})

            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except :
            return srcs

    def resolve(self, url, resolverList):
        return url