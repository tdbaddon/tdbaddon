import base64
import hashlib
import random
import re
import string
import urllib
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper
import xbmcaddon
import xbmc


class Onemovies(Scraper):
    domains = ['123movies.gs']
    name = "onemovies"

    def __init__(self):
        self.base_link = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_baseurl" % (self.name))
        self.search_link = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'
        self.session = requests.Session()

    def scrape_movie(self, title, year, imdb):
        try:
            # print("ONEMOVIES")
            headers = {'User-Agent': random_agent()}
            # print("ONEMOVIES", headers)
            query = self.search_link % (urllib.quote_plus(
                    " ".join(title.translate(None, '"?:!@#$&-').replace("'",
                                                                        " ").split())))  # clean up string and remove double spaces
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = clean_title(title)
            cleaned_title = " ".join(cleaned_title.translate(None, '\'"?:!@#$&-').split())
            # print("ONEMOVIES", query)
            page = 1
            while True:
                html = self.session.get(query, headers=headers, timeout=30).content
                if "no result found" in html.lower():
                    break
                html = BeautifulSoup(html)
                containers = html.findAll('div', attrs={'class': 'ml-item'})
                for result in containers:
                    links = result.findAll('a')
                    # print("ONEMOVIES", links)
                    for link in links:
                        link_title = str(link['title'])
                        href = str(link['href'])
                        info = str(link['data-url'])
                        # print("ONEMOVIES", link_title, href, info)
                        cleaned_link_title = " ".join(clean_title(link_title).translate(None, '\'"?:!@#$&-').split())
                        if cleaned_link_title == cleaned_title:
                            html = self.session.get(info, headers=headers).content
                            pattern = '<div class="jt-info">%s</div>' % year
                            match = re.findall(pattern, html)
                            if match:
                                # print("ONEMOVIES MATCH", href)
                                return self.sources(replaceHTMLCodes(href))
                page += 1
                query = self.search_link % (urllib.quote_plus(" ".join(title.translate(None, '\'"?:!@#$&-').split())))
                query = urlparse.urljoin(self.base_link, query)
                query += "/" + str(page)

        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb):
        try:
            headers = {'User-Agent': random_agent()}
            query = "%s+season+%s" % (urllib.quote_plus(" ".join(title.translate(None, '\'"?:!@#$&-').split())), season)
            query = self.search_link % query
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = clean_title(title)
            checkseason = cleaned_title + "season" + season
            # print("ONEMOVIES", query,checkseason)
            html = BeautifulSoup(self.session.get(query, headers=headers, timeout=30).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
                links = result.findAll('a')
                # print("ONEMOVIES", links)
                for link in links:
                    link_title = str(link['title'])
                    href = str(link['href'])

                    # print("ONEMOVIES", link_title, href, info)
                    if clean_title(link_title) == checkseason:
                        ep_id = '?episode=%01d' % int(episode)
                        href = href + ep_id
                        # print("ONEMOVIES Passed", href)
                        return self.sources(replaceHTMLCodes(href))

        except:
            pass
        return []

    def sources(self, url):
        original_url = url
        sources = []
        try:
            # print("ONEMOVIES SOURCES", url)

            if url == None: return sources
            referer = url
            headers = {'User-Agent': random_agent()}
            url = url.replace('/watching.html', '')
            request = self.session.get(url, headers=headers)
            html = request.content
            # print ("ONEMOVIES Source", html)
            try:
                url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except:
                episode = None
            vid_id = re.findall('-(\d+)', url)[-1]
            getc = re.findall(r'<img title=.*?src="(.*?)"', html, re.I | re.DOTALL)[0]
            cookie = get_cookie(getc, original_url, self.session)
            # print ("ONEMOVIES", vid_id)
            quality = re.findall('<span class="quality">(.*?)</span>', html)
            quality = str(quality)
            if quality == 'cam' or quality == 'ts':
                quality = 'CAM'
            elif quality == 'hd':
                quality = '720'
            else:
                quality = '480'
            try:
                headers = {'X-Requested-With': 'XMLHttpRequest'}
                headers['Referer'] = referer
                headers[
                    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
                u = urlparse.urljoin(self.base_link, self.server_link % vid_id)
                # print("SERVERS", u)
                request = self.session.get(u, headers=headers)
                r = BeautifulSoup(request.content)
                # print("SERVERS", r)
                containers = r.findAll('div', attrs={'class': 'les-content'})
                for result in containers:
                    try:
                        links = result.findAll('a')
                        # print("ONEMOVIES", links)
                        for link in links:
                            title = str(link['title'])
                            # print("ONEMOVIES TITLE", title)
                            if not episode == None:
                                title = re.findall('Episode\s+(\d+):', title)[0]
                                title = '%01d' % int(title)
                                if title == episode:
                                    episode_id = str(link['episode-id'])
                                # print("ONEMOVIES EPISODE", episode_id)
                                else:
                                    continue

                            else:
                                episode_id = str(link['episode-id'])
                            onclick = str(link['onclick'])

                            key_gen = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
                            ################# FIX FROM MUCKY DUCK & XUNITY TALK ################
                            key = '87wwxtp3dqii'
                            key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'
                            coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' % key_gen
                            cookie = '%s; %s' % (cookie, coookie)
                            a = episode_id + key2
                            b = key_gen
                            # i = b[-1]
                            # h = b[:-1]
                            # b = i + h + i + h + i + h
                            hash_id = uncensored(a, b)
                            ################# FIX FROM MUCKY DUCK & XUNITY TALK ################

                            serverurl = self.base_link + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(
                                    hash_id)
                            # print ("playurl ONEMOVIES", serverurl)

                            headers = {'Accept-Language' : 'en-US',
                                       'Accept-Encoding' : 'gzip, deflate, sdch',
                                       'Cookie'          : cookie,
                                       'Referer'         : referer,
                                       'x-requested-with': 'XMLHttpRequest',
                                       'Accept'          : 'application/json, text/javascript, */*; q=0.01',
                                       'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                                       }
                            # print ("playurl ONEMOVIES", headers)
                            result = self.session.get(serverurl, headers=headers).content
                            # print ("RESULT ONEMOVIES", result)
                            result = result.replace('\\', '')
                            # print ("ONEMOVIES Result", result)
                            url = re.findall('"?file"?\s*:\s*"(.+?)"', result)
                            url = [googletag(i) for i in url]
                            url = [i[0] for i in url if len(i) > 0]
                            u = []
                            try:
                                u += [[i for i in url if i['quality'] == '1080p'][0]]
                            except:
                                pass
                            try:
                                u += [[i for i in url if i['quality'] == '720'][0]]
                            except:
                                pass
                            try:
                                u += [[i for i in url if i['quality'] == '480'][0]]
                            except:
                                pass
                            url = replaceHTMLCodes(u[0]['url'])
                            quality = googletag(url)[0]['quality']

                            # print ("ONEMOVIES PLAY URL", quality, url)

                            sources.append(
                                    {'source': 'google video', 'quality': quality, 'scraper': self.name, 'url': url,
                                     'direct': True})
                    except:
                        pass
            except:
                pass

        except:
            pass
        return sources

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name),
            '<setting id= "%s_baseurl" type="text" label="Base Url" default="https://123movies.pp.ru"/>' % (clas.name)
        ]
        return xml


def __jav(a):
    b = str(a)
    code = ord(b[0])
    if 0xD800 <= code and code <= 0xDBFF:
        c = code
        if len(b) == 1:
            return code
        d = ord(b[1])
        return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000

    if 0xDC00 <= code and code <= 0xDFFF:
        return code
    return code


def uncensored(a, b):
    c = ''
    i = 0
    for i, d in enumerate(a):
        e = b[i % len(b) - 1]
        d = int(__jav(d) + __jav(e))
        c += chr(d)

    return base64.b64encode(c)


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


def get_cookie(url, referer, session):
    headers = {'Accept'         : 'image/webp,image/*,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-US,en;q=0.8',
               'Referer'        : referer,
               'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
               }
    request = session.get(url, headers=headers)
    cookie = request.cookies.get_dict()
    newcookie = ""
    for i in cookie:
        newcookie = i + '=' + cookie[i]
    return newcookie
