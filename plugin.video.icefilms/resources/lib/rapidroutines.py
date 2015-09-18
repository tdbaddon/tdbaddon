'''

Python class for RapidShare

Uses RapidShare API - http://images.rapidshare.com/apidoc.txt

'''

import re
import urllib2
            
class rapidshare:
    def __init__(self, use_ssl=False):
        self.class_name='rapidshare'
        
        if use_ssl:
            self.accountdetails = 'https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&withcookie=1&login=%s&password=%s'
            self.checkfile = 'https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=checkfiles&files=%s&filenames=%s'
            self.downloadfile = 'https://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s'
            #Free users must use non-ssl for this call
            self.download_link = 'http://rs%s%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&dlauth=%s'
            self.download_link_cookie = 'https://rs%s%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&cookie=%s'
        else:
            self.accountdetails = 'http://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=getaccountdetails&withcookie=1&login=%s&password=%s'
            self.checkfile = 'http://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=checkfiles&files=%s&filenames=%s'
            self.downloadfile = 'http://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s'
            self.download_link = 'http://rs%s%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&dlauth=%s'
            self.download_link_cookie = 'http://rs%s%s.rapidshare.com/cgi-bin/rsapi.cgi?sub=download&fileid=%s&filename=%s&cookie=%s'


    def file_status(self, status):
        if status == '0':
            message = 'File not found'
        elif status == '1':
            message = 'OK'
        elif status == '3':
            message = 'Server is currently down'
        elif status == '4':
            message = 'File has been marked as illegal and removed'
        else:
            message = 'Unknown file status'
        return message


    def check_account(self, login, password):
        
        try:
            account_details = {}
            html = self.get_url(self.accountdetails % (login, password))
            
            #Check for error
            if html.startswith('ERROR:'):
                print 'RapidRoutines - Check Account Returned Error: %s' % html
                return None
            elif html:
                account_details['rapids'] = re.search('rapids=([0-9]+)', html).group(1)
                account_details['billeduntil'] = re.search('billeduntil=([0-9]+)', html).group(1)
                
                #Only return a cookie if it's an active premium account            
                if account_details['billeduntil'] != '0':
                    account_details['cookie'] = re.search('cookie=(.+)', html).group(1)
                else:
                    account_details['cookie'] = ''
                
                print 'RapidRoutines - Check Account Returning:', account_details
                return account_details
            else:
                return None
        except Exception, e:
            print '**** RapidRoutines - Error in check_account: %s' % e
            raise


    #Main method to call to return all information including final download link
    def resolve_link(self, url, cookie='', login='', password=''):
        
        account_details = {}
        download_details = {}

        #If a login and password are passed in then lets get the cookie
        if login and password:
            cookie = self.check_account(login, password)['cookie']

        #Check that the file is available and grab host/server id details
        file_details = self.validate_file(url)

        if file_details:
            if file_details['status'] == '1':
                download_details = self.get_download_link(file_details['server_id'], file_details['short_host'], file_details['file_id'], file_details['file_name'], cookie=cookie)
            else:
                download_details['wait_time'] = 0
                download_details['download_link'] = ''
            
            file_details.update(download_details)
            print 'RapidRoutines - Resolve Link Returning:', file_details
            return file_details
        else:
            return None


    def validate_file(self, url):
        
        file_details = self.parse_filelink(url)
        
        try:
            if file_details:
                #File link is valid url - now grab details from RapidShare to ensure file exists there
                file_check_url = self.checkfile % (file_details['file_id'], file_details['file_name'])
    
                html = self.get_url(file_check_url)        
    
                #If file is available, RapidShare will return a '1' in 5th comma position of returned data         
                file_details['file_name'] = html.split(',')[1]
                file_details['file_size'] = html.split(',')[2]
                file_details['server_id'] = html.split(',')[3]
                file_details['status'] = html.split(',')[4]
                file_details['short_host'] = html.split(',')[5]
                file_details['message'] = self.file_status(file_details['status'])
                
                print 'RapidRoutines - Validate File Details:', file_details
                return file_details
          
            else:
                #Invalid file link
                return None
        except Exception, e:
            print '**** RapidRoutines - Error in validate_file: %s' % e
            raise


    def parse_filelink(self, url):
        try:
            r = re.search('https://rapidshare.com/files/([0-9]+)/(.+)', url)
            if r:
                file_details = {}
                file_details['file_id'] = r.group(1)
                file_details['file_name'] = r.group(2)
                return file_details
            else:
                return None
        except Exception, e:
            print '**** RapidRoutines - Error in parse_filelink: %s' % e
            raise


    def get_download_link(self, server_id, short_host, file_id, file_name, cookie=''):
        
        try:
            download_details = {}
            
            #If free user - need to get an authkey and wait time, not needed for premium
            if not cookie:
                rapid_download = self.downloadfile % (file_id, file_name)
                html = self.get_url(rapid_download)
                
                if html.startswith("ERROR:"):
                    print 'RapidRoutines - Download Link Returned Error: %s' % html
                    return None
                else:
                    download_details['host'] = html.split(",")[0].split(":")[1]
                    download_details['authkey'] = html.split(",")[1]
                    download_details['wait_time'] = html.split(",")[2]
                    download_details['download_link'] = self.download_link % (server_id, short_host, file_id, file_name, download_details['authkey'])
            
            #Premium user
            else:
                download_details['download_link'] = self.download_link_cookie % (server_id, short_host, file_id, file_name, cookie)
                download_details['wait_time'] = 1

            print 'RapidRoutines - Get Download Link Details:', download_details
            return download_details
        
        except Exception, e:
            print '**** RapidRoutines - Error in get_download_link: %s' % e
            raise

    
    def get_url(self, url):

        #Ensure we remove logins, passwords and cookies from logging
        logurl = re.sub('&login=(.*)&password=(.*)', '&login=XXXXXX&password=XXXXXX',url)
        logurl = re.sub('&cookie=(.*)', '&cookie=XXXXXX',logurl)
        print 'RapidRoutines - Requesting URL: %s' % logurl
        
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            html=response.read()
            response.close()
            return html
        except Exception, e:
            print 'Error retrieving url: %s' % e
            raise Exception('Error occured retrieving URL: %s' % e)