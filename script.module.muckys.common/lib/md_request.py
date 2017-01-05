#
#      Copyright (C) 2017 Mucky Duck (class sucuri Derived from Lambda's)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import base64,cfscrape,re,requests


User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
scraper = cfscrape.create_scraper()
s = requests.session()

class sucuri:

        def __init__(self):
                self.cookie = None


        def get(self, result):

                try:

                    s = re.compile("S\s*=\s*'([^']+)").findall(result)[0]
                    s = base64.b64decode(s)
                    s = s.replace(' ', '')
                    s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
                    s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
                    s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
                    s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
                    s = re.sub(';location.reload\(\);', '', s)
                    s = re.sub(r'\n', '', s)
                    s = re.sub(r'document\.cookie', 'cookie', s)

                    cookie = '' ; exec(s)
                    self.cookie = re.compile('([^=]+)=(.*)').findall(cookie)[0]
                    self.cookie = '%s=%s' % (self.cookie[0], self.cookie[1])

                    return self.cookie

                except:
                        pass





def open_url(url, headers=None):

        if headers == None:
                headers = {}
                headers['User-Agent'] = User_Agent

        link = scraper.get(url, headers=headers)

        if link.headers['Server'] == 'Sucuri/Cloudproxy':
                su = sucuri().get(link.content)

                headers['Cookie'] = su
                link = scraper.get(url+'/', headers=headers)

        return link




def open_url2(url,header=None):

        if headers == None:
                headers = {}
                headers['User-Agent'] = User_Agent

        link = scraper.post(url, headers=headers)

        if link.headers['Server'] == 'Sucuri/Cloudproxy':
                su = sucuri().get(link.content)

                headers['Cookie'] = su
                link = scraper.post(url+'/', headers=headers)

        return link
