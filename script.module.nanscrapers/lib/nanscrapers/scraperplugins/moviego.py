import re
import urllib
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent, replaceHTMLCodes
from ..jsunpack import unpack
from ..scraper import Scraper


class Moviego(Scraper):
    domains = ['moviego.cc']
    name = "moviego"

    def __init__(self):
        self.base_link = 'http://moviego.cc'
        self.search_link = '/index.php?do=search&subaction=search&full_search=1&result_from=1&story=%s+%s'
        self.ep_url = '/engine/ajax/getlink.php?id=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            # print("MOVIEGO INIT")
            headers = {'User-Agent': random_agent()}
            searchquery = self.search_link % (urllib.quote_plus(title), year)
            query = urlparse.urljoin(self.base_link, searchquery)
            cleaned_title = clean_title(title)
            html = requests.get(query, headers=headers).content
            html = BeautifulSoup(html)

            containers = html.findAll('div', attrs={'class': 'short_content'})
            # print("MOVIEGO MOVIES",containers)
            for items in containers:
                href = items.findAll('a')[0]['href']
                title = items.findAll('div', attrs={'class': 'short_header'})[0]
                if year in str(title):
                    title = normalize(str(title))
                    if title == cleaned_title:
                        return self.sources(replaceHTMLCodes(href))

        except:
            return []

    def sources(self, url):
        sources = []
        alt_links = []
        play_links = []
        play_links_other = []
        try:

            if url == None: return sources
            headers = {'User-Agent': random_agent()}
            mainpage = requests.get(url, headers=headers)
            html = BeautifulSoup(requests.get(url, headers=headers).content)
            try:
                film_quality = re.findall('<div class="poster-qulabel">(.*?)</div>', mainpage)[0]
                print ("MOVIEGO film_quality", film_quality)
                if "1080" in film_quality:
                    quality = "1080"
                elif "720" in film_quality:
                    quality = "720"
                else:
                    quality = "SD"
                url = re.findall('file:\s+"([^"]+)"', mainpage)[0]
                url = url.encode('utf-8')
                sources.append({'source': 'CDN', 'quality': quality, 'scraper': self.name, 'url': url, 'direct': True})
            except:
                pass
            iframe = html.findAll("iframe")[0]
            original_frame = iframe['src']
            iframe_html = BeautifulSoup(requests.get(iframe["src"], headers=headers).content)
            scripts = iframe_html.findAll("script")
            unpacked_script = ""
            for script in scripts:
                try:
                    unpacked_script += unpack(script.text)
                except:
                    pass
            try:
                alternative_links = re.findall('Alternative (\d+)<', unpacked_script)
                for alts in alternative_links: alt_links.append(alts)
            except:
                pass
            # print ("MOVIEGO ALTS", alt_links)
            links = re.findall('<source src="(.*?)"', unpacked_script)
            if links:
                for link_url in links:
                    if "google" in link_url:
                        link_url = link_url.replace(' ', '')
                        play_links.append(link_url)
                    else:
                        link_url = link_url.replace(' ', '')
                        play_links_other.append(link_url)

        except:
            pass
        try:
            for ids in alt_links:
                headers = {'User-Agent': random_agent()}
                alt_frames = original_frame + "?source=a" + ids
                alt_iframe_html = BeautifulSoup(requests.get(alt_frames, headers=headers).content)
                alt_scripts = alt_iframe_html.findAll("script")
                unpacked_script = ""
                for script in alt_scripts:
                    try:
                        unpacked_script += unpack(script.text)
                    except:
                        pass
                links = re.findall('<source src="(.*?)"', unpacked_script)
                if links:
                    for link_url in links:
                        if "google" in link_url:
                            link_url = link_url.replace(' ', '')
                            play_links.append(link_url)
                        else:
                            link_url = link_url.replace(' ', '')
                            play_links_other.append(link_url)

        except:
            pass
        ############# DUPLICATES CHECK ################
        try:
            dupes = []
            for url in play_links:
                if not url in dupes:
                    dupes.append(url)
                    print ("MOVIEGO PLAY url", url)
                    quality = googletag(url)[0]['quality']
                    url = url.encode('utf-8')
                    sources.append({'source': 'google video', 'quality': quality, 'scraper': self.name, 'url': url,
                                    'direct': True})

            for url in play_links_other:
                if not url in dupes:
                    dupes.append(url)
                    loc = urlparse.urlparse(url).netloc # get base host (ex. www.google.com)
                    source_base = str.join(".",loc.split(".")[1:-1])
                    url = url.encode('utf-8')
                    sources.append({'source': source_base, 'quality': quality, 'scraper': self.name, 'url': url,
                                    'direct': False})

        except:
            pass

        return sources


def normalize(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([<].+?[>])|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


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
