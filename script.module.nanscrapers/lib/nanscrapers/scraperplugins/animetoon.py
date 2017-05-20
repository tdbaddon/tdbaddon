import re
import requests
from ..scraper import Scraper
import xbmc
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, replaceHTMLCodes
import urlparse


class Animetoon(Scraper):
    name = "animetoon"
    domains = ['animetoon.org']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.animetoon.org/'
        self.search_link = "/toon/search?key=%s"

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            # if season == '1':
            #     url = self.base_link + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
            # elif season == '01':
            #     url = self.base_link + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
            # else:
            #     url = self.base_link + title.replace(' ', '-').replace('!',
            #                                                            '') + '-season-' + season + '-episode-' + episode
            cleaned_title = clean_title(title)
            q = title.translate(None, '\/:*?"\'<>|!,').replace(' ', '+').replace('++', '+').lower()
            query = urlparse.urljoin(self.base_link, self.search_link % q)
            html = BeautifulSoup(requests.get(query, timeout=30).content)
            series_list = html.find('div', attrs={'class': 'series_list'})
            for header in series_list.findAll("h3"):
                link = header.find('a')
                href = link["href"]
                link_title = link.text
                cleaned_link_title = clean_title(link_title)
                if (str(season) in ['1', '01'] and cleaned_link_title == cleaned_title) or ("season %s" % season in link_title and cleaned_link_title in link_title) or cleaned_link_title == cleaned_title:
                    pages = [href]
                    html2 = BeautifulSoup(requests.get(href).text)
                    pagination = html2.find('ul', attrs={'class': 'pagination'})
                    if pagination:
                        page_buttons = pagination.findAll("button")
                        for button in page_buttons:
                            try:
                                pages.append(button["href"])
                            except:
                                pass
                    found = False
                    first_page = True
                    for page in pages:
                        if not first_page:
                            html2 = BeautifulSoup(requests.get(page).text)
                        videos = html2.find('div', attrs={'id':'videos'})
                        for video in videos.findAll('a'):
                            if "season" in video.text.lower():
                                if not "season " + season in video.text.lower() or\
                                   "season 0" + season in video.text.lower():
                                    continue
                            if "episode " + str(episode) in video.text.lower():
                                if " %s " % episode in video.text or video.text.lower().endswith('episode %s' % episode):
                                    url = video["href"]
                                    html = requests.get(url).text
                                    match = re.compile('"playlist">.+?</span></div><div><iframe src="(.+?)"').findall(
                                        html)
                                    for url2 in match:
                                        self.get_sources(url2)
                                    if match:
                                        found = True
                                        break
                        first_page = False
                        if found:
                            break

            return self.sources
        except:
            pass

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = 'http://www.animetoon.org/toon/search?key=' + title.replace(' ', '+').lower()
            html = BeautifulSoup(requests.get(start_url).text)
            container = html.findAll("div", attrs={'class': 'series_list'})[0]
            items = container.findAll("li")
            for item in items:
                try:
                    info = item.findAll("div", attrs={'class': 'right_col'})[0]
                    link = info.findAll("a")[0]
                    link_title = link.text
                    href = link["href"]
                    item_year = info.findAll("span", attrs={'class': 'bold'})[-2].text
                    if clean_title(title) == clean_title(link_title) and year.lower() in [item_year.lower(), str(
                                    int(item_year.lower()) - 1), str(int(item_year.lower()) + 1)]:
                        html = BeautifulSoup(requests.get(href).text)
                        videos_div = html.findAll("div", attrs={'id': 'videos'})[0]
                        links = videos_div.findAll("a")
                        for link in links:
                            self.check_for_split_streams(link["href"])
                except:
                    continue
            # match = re.compile('<div class="left_col">.+?<a href="(.+?)">',re.DOTALL).findall(html)
            # for url in match:
            #     html2 = requests.get(url).text
            #     match2 = re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(html2)
            #     for url2, year_check in match2:
            #         if year.lower() in year_check.lower():
            #             self.check_for_split_streams(url2)
            return self.sources
        except:
            pass

    def check_for_split_streams(self, url):
        try:
            html3 = requests.get(url).text
            match3 = re.compile('"playlist">.+?</span></div><div><iframe src="(.+?)"').findall(html3)
            for url2 in match3:
                self.get_sources(url2)
            block = re.compile('<span class="playlist">(.+?)"Report Video">', re.DOTALL).findall(html3)
            for item in block:
                Next = re.compile('<iframe src="(.+?)"').findall(str(item))
                for url in Next:
                    if 'mp4' in url:
                        self.get_sources(url)
        except:
            pass

    def get_sources(self, url):
        try:
            List = []
            if 'panda' in url:
                HTML = requests.get(url).text
                match2 = re.compile("url: '(.+?)'").findall(HTML)
                for url3 in match2:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append(
                                {'source': 'playpanda', 'quality': 'SD', 'scraper': self.name, 'url': url3,
                                 'direct': True})
                            List.append(url3)
            elif 'easy' in url:
                HTML2 = requests.get(url).text
                match3 = re.compile("url: '(.+?)'").findall(HTML2)
                for url3 in match3:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append(
                                {'source': 'easyvideo', 'quality': 'SD', 'scraper': self.name, 'url': url3,
                                 'direct': True})
                            List.append(url3)
            elif 'zoo' in url:
                HTML3 = requests.get(url).text
                match4 = re.compile("url: '(.+?)'").findall(HTML3)
                for url3 in match4:
                    if 'http' in url3:
                        if url3 not in List:
                            self.sources.append(
                                {'source': 'videozoo', 'quality': 'SD', 'scraper': self.name, 'url': url3,
                                 'direct': True})
                            List.append(url3)
            else:
                loc = urlparse.urlparse(url).netloc  # get base host (ex. www.google.com)
                self.sources.append(
                    {'source': loc, 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': True})
        except:
            pass
