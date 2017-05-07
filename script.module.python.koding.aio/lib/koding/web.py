# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by whufclee (info@totalrevolution.tv)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import time
import urllib
import xbmcgui
#----------------------------------------------------------------    
# TUTORIAL #
def Cleanup_URL(url):
    """
Clean a url, removes whitespaces and common buggy formatting when pulling from websites

CODE: Cleanup_URL(url)

    AVAILABLE PARAMS:
        
        (*) url   -  This is the main url you want cleaned up.

EXAMPLE CODE:
raw_url = '" http://test.com/video/"/'
clean_url = koding.Cleanup_URL(raw_url)
dialog.ok('CLEANUP URL', 'Orig: %s'%raw_url,'Clean: %s'%clean_url)
~"""
    from HTMLParser import HTMLParser

    bad_chars = ['/','\\',':',';','"',"'"]
    url = url.strip()

    while url[0] in bad_chars or url[-1] in bad_chars:
        if url[-1] in bad_chars:
            url = url[:-1]
        if url[0] in bad_chars:
            url = url[1:]
        url = url.strip()
    return HTMLParser().unescape(url)
#----------------------------------------------------------------    
# TUTORIAL #
def Download(url, dest, dp = None):
    """
This will download a file, currently this has to be a standard download link which doesn't require cookies/login.

CODE: koding.Download(src,dst,[dp])
dp is optional, by default it is set to false

AVAILABLE PARAMS:

    (*) src  - This is the source file, the URL to your download. If you attempted to download an item but it's not behaving the way you think it should (e.g. a zip file not unzipping) then change the extension of the downloaded file to .txt and open up in a text editor. You'll most likely find it's just a piece of text that was returned from the URL you gave and it should have details explaining why it failed. Could be that's the wrong URL, it requires some kind of login, it only accepts certain user-agents etc.

    (*) dst  - This is the destination file, make sure it's a physical path and not "special://...". Also remember you need to add the actual filename to the end of the path, so if we were downloading something to the "downloads" folder and we wanted the file to be called "test.txt" we would use this path: dst = "downloads/test.txt". Of course the downloads folder would actually need to exist otherwise it would fail and based on this poor example the downloads folder would be at root level of your device as we've not specified a path prior to that so it just uses the first level that's accessible.

    dp - This is optional, if you pass through the dp function as a DialogProgress() then you'll get to see the progress of the download. If you choose not to add this paramater then you'll just get a busy spinning circle icon until it's completed. See the example below for a dp example.

EXAMPLE CODE:
src = 'http://noobsandnerds.com/python_koding/my_first_addon.zip'
dst = xbmc.translatePath('special://home/my_first_addon.zip')
dp = xbmcgui.DialogProgress()
dp.create('Downloading File','Please Wait')
koding.Download(src,dst,dp)~"""

    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: Download_Progress(nb, bs, fs, dp, start_time))
#----------------------------------------------------------------    
def Download_Progress(numblocks, blocksize, filesize, dp, start_time):
    """ internal command ~"""

    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        if dp:
            dp.update(percent, mbs, e)
        if dp.iscanceled(): 
            dp.close()
    except: 
        percent = 100
        if dp:
            dp.update(percent) 
    if dp:
        if dp.iscanceled(): 
            dp.close()
        dp.close()
#----------------------------------------------------------------    
# TUTORIAL #
def Get_Extension(url):
    """
Return the extension of a url

CODE:   koding.Get_Extension(url)

AVAILABLE PARAMS:

    (*) url  -  This is the url you want to grab the extension from

EXAMPLE CODE:
url_extension = koding.Get_Extension('http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4')
dialog.ok('FILE EXTENSION','The file extension of this Big Buck Bunny sample is:','','[COLOR=dodgerblue]%s[/COLOR]'%url_extension)~"""
    
    import os
    import urlparse

    parsed = urlparse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext
#----------------------------------------------------------------
# TUTORIAL #
def Open_URL(url='',post_type='get',headers=None,cookies=True,auth=None,timeout=None,cookiejar=None):
    """
If you need to pull the contents of a webpage it's very simple to do so by using this function.

CODE:   koding.Open_URL(url,[post_type,headers,cookies,auth,timeout,cookiejar])

AVAILABLE PARAMS:

    url  -  This is the main url you want to send through. Send it through
    as a query string format even if it's a post.

    post_type  -  By default this is set to 'get' but this can be set to 'post',
    if set to post the query string will be split up into a post format automatically.
    
    headers -  Optionally send through headers in form of a dictionary.

    cookies  -  If set to true your request will send through and store cookies.

    auth  -  User/pass details

    timeout  -  Optionally set a timeout for the request.

    cookiejar  -  An name for the location to store cookies. By default it's
    set to addon_data/<addon_id>/cookies/cookiejar but if you have multiple
    websites you access then you may want to use a separate filename for each site.

EXAMPLE CODE:
url_contents = koding.Open_URL('http://testpage.com?query1=value1&query2=value2', post_type='get')
koding.Text_Box('CONTENTS OF WEB PAGE',url_contents)
~"""
    import os
    import pickle
    import requests
    import sys
    import xbmc
    import xbmcaddon

    from __init__   import converthex, dolog, Encryption, ADDON_ID, LOGIN, FORUM, USERNAME, PASSWORD, KODI_VER
    from addons     import Addon_Info
    from filetools  import Text_File

    Addon_Version = Addon_Info(id='version')
    Addon_Profile = xbmc.translatePath(Addon_Info(id='profile'))
    Cookie_Folder = os.path.join(Addon_Profile,'cookies')
    if not os.path.exists(Cookie_Folder):
        os.makedirs(Cookie_Folder)

    if cookiejar == None:
        Cookie_Jar = os.path.join(Cookie_Folder,'cookiejar')
    else:
        Cookie_Jar = os.path.join(Cookie_Folder,cookiejar)
    
    my_cookies = None
    if cookies:
        if os.path.exists(Cookie_Jar):
            try:
                with open(Cookie_Jar, 'rb') as f:
                    my_cookies = pickle.load(f)
            except:
                my_cookies = None

    payload      = {}

# If the url sent through is not http then we presume it's hitting the NaN page
    if not url.startswith(converthex('68747470')):
        NaN_URL = True
        args = url
        post_type = 'post'
        url = converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f6c6f67696e5f74657374696e672e7068703f753d257326703d257326663d257326613d257326763d2573266b3d257326653d2573') % (USERNAME, PASSWORD, FORUM, ADDON_ID, Addon_Version, KODI_VER, args)
    else:
        NaN_URL = False
    if '?' in url:
        url, args = url.split('?')
        args = args.split('&')
        for item in args:
            var, data = item.split('=')
            if NaN_URL:
                payload[var] = Encryption('e', data)
            else:
                payload[var] = data
    try:
        if post_type == 'post':
            r = requests.post(url, payload, headers=headers, cookies=my_cookies, auth=auth, timeout=timeout)
        else:
            r = requests.get(url, payload, headers=headers, cookies=my_cookies, auth=auth, timeout=timeout)
    except:
        return 'This url could not be opened: %s'%url
    dolog('### CODE: %s   |   REASON: %s' % (r.status_code, r.reason))
    if r.status_code >= 200 and r.status_code < 400:
        content = r.text.encode('utf-8')
        dolog('content: %s'%content)
        if cookies:
            with open(Cookie_Jar, 'wb') as f:
                pickle.dump(r.cookies, f)
        return content
    else:
        return 'This url could not be opened: %s'%url
#----------------------------------------------------------------
# TUTORIAL #
def Validate_Link(url=''):
    """
Returns the code for a particular link, so for example 200 is a good link and 404 is a URL not found

CODE:   koding.Validate_Link(url)

AVAILABLE PARAMS:

    (*) url  -  This is url you want to check the header code for

EXAMPLE CODE:
url_code = koding.Validate_Link('http://totalrevolution.tv')
if url_code == 200:
    dialog.ok('WEBSITE STATUS','The website [COLOR=dodgerblue]totalrevolution.tv[/COLOR] is [COLOR=lime]ONLINE[/COLOR]')
else:
    dialog.ok('WEBSITE STATUS','The website [COLOR=dodgerblue]totalrevolution.tv[/COLOR] is [COLOR=red]OFFLINE[/COLOR]')
~"""
    import requests
    import xbmc

    r = requests.get(url)
    return r.status_code
#----------------------------------------------------------------