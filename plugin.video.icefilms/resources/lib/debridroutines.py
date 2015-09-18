import urllib, urllib2
import re, os, cookielib
import simplejson as json

class RealDebrid:

    def __init__(self, cookie_file, username, password):
        self.cookie_file = cookie_file
        self.username = username
        self.password = password
        


    def GetURL(self, url):

        print 'DebridRoutines - Requesting URL: %s' % url
        if self.cookie_file is not None and os.path.exists(self.cookie_file):
            cj = cookielib.LWPCookieJar()
            cj.load(self.cookie_file)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'XBMC Plugin')   
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            response = opener.open(req)

            #check if we might have been redirected (megapremium Direct Downloads...)
            finalurl = response.geturl()

            #if we weren't redirected, return the page source
            if finalurl is url:
                link=response.read()
                response.close()
                return link

            #if we have been redirected, return the redirect url
            elif finalurl is not url:               
                return finalurl    


    def Resolve(self, url):
        print 'DebridRoutines - Resolving url: %s' % url
        url = 'https://real-debrid.com/ajax/unrestrict.php?link=%s' % url
        source = self.GetURL(url)
        jsonresult = json.loads(source)
        print 'DebridRoutines - Returned Source: %s' % source
        download_details = {}
        download_details['download_link'] = ''
        download_details['message'] = ''
        if 'generated_links' in jsonresult:
            generated_links = jsonresult['generated_links']
            link = generated_links[0][2]
            download_details['download_link'] = link
            return download_details
        else:
            message = jsonresult['message']
            download_details['message'] = message
            return download_details


    def valid_host(self, host):
        url = 'https://real-debrid.com/api/hosters.php'
        allhosts = self.GetURL(url)
        if re.search(host, allhosts):
            return True
        else:
            return False

    def  checkLogin(self):
        url = 'https://real-debrid.com/api/account.php'
        source = self.GetURL(url)
        if source is not None and re.search('expiration', source):
            return False
        else:
            return True


    def Login(self):    
        if self.checkLogin():
            cj = cookielib.LWPCookieJar()
            login_data = urllib.urlencode({'user' : self.username, 'pass' : self.password})
            url = 'https://real-debrid.com/ajax/login.php?' + login_data
            print 'DebridRoutines - Requesting URL: %s' % url
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'XBMC Plugin')
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            #do the login and get the response
            response = opener.open(req)
            source = response.read()
            response.close()
            cj.save(self.cookie_file)
            print source
            if re.search('OK', source):
                return True
            else:
                return False
        else:
            return True
