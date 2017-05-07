# -*- coding: utf-8 -*- 

import base64,cfscrape,re
from incapsula import crack


User_Agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2"'
scraper = cfscrape.create_scraper()




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





def open_url(url, method='get', headers=None, cookies=None, params=None, data=None, redirects=True, verify=True):

        if headers == None:

                headers = {}
                headers['User-Agent'] = User_Agent

        link = getattr(scraper,method)(url, headers=headers, cookies=cookies, params=params, data=data, allow_redirects=redirects, verify=verify)

        try:
                if link.headers['Server'] == 'Sucuri/Cloudproxy':

                        su = sucuri().get(link.content)
                        headers['Cookie'] = su

                        if not url[-1] == '/':
                                url = '%s/' %url

                        link = getattr(scraper,method)(url, headers=headers, cookies=cookies, params=params, data=data, allow_redirects=redirects, verify=verify)
        except:
                pass

        if '_Incapsula_' in link.content:

                link = getattr(scraper,method)(url, headers=headers, cookies=cookies, params=params, data=data, allow_redirects=redirects, verify=verify)
                link = crack(scraper, link)

        return link
