import xbmc,xbmcgui
import xbmc,xbmcgui
import os
import urllib, urllib2
import cookielib
import re
import jsunpack
import urlparse

''' Use addon.common library for http calls '''
from addon.common.net import Net
from addon.common.addon import Addon
net = Net()

addon = Addon('plugin.video.icefilms')
datapath = addon.get_profile()

cookie_path = os.path.join(datapath, 'cookies')

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

def handle_captchas(url, html, data, dialog):

    headers = {'Referer': url}

    puzzle_img = os.path.join(datapath, "solve_puzzle.png")
    
    #Check for type of captcha used
    solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
    recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
    numeric_captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)    

    #SolveMedia captcha
    if solvemedia:
        dialog.close()
        html = net.http_GET(solvemedia.group(1), headers=headers).content

        for match in re.finditer(r'type=hidden.*?name="([^"]+)".*?value="([^"]+)', html):
            name, value = match.groups()
            data[name] = value       
               
        #Check for alternate puzzle type - stored in a div
        alt_frame = re.search('<div><iframe src="(/papi/media[^"]+)', html)
        if alt_frame:
            html = net.http_GET("http://api.solvemedia.com%s" % alt_frame.group(1)).content
            alt_puzzle = re.search('<div\s+id="typein">\s*<img\s+src="data:image/png;base64,([^"]+)', html, re.DOTALL)
            if alt_puzzle:
                open(puzzle_img, 'wb').write(alt_puzzle.group(1).decode('base64'))
        else:
            open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(/papi/media[^"]+)"', html).group(1)).content)
       
        img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
    
        xbmc.sleep(3000)

        kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        kb.doModal()
        capcode = kb.getText()

        if (kb.isConfirmed()):
            userInput = kb.getText()
            if userInput != '':
                solution = kb.getText()
            elif userInput == '':
                raise Exception ('You must enter text in the image to access video')
                wdlg.close()
        else:
            wdlg.close()
            raise Exception ('Captcha Error')
        wdlg.close()
        data['adcopy_response'] = solution
        html = net.http_POST('http://api.solvemedia.com/papi/verify.noscript', data)       
        data.update({'adcopy_challenge': data['adcopy_challenge'],'adcopy_response': 'manual_challenge'})

    #Google Recaptcha
    elif recaptcha:
        dialog.close()
        html = net.http_GET(recaptcha.group(1), headers=headers).content
        part = re.search("challenge \: \\'(.+?)\\'", html)
        captchaimg = 'http://www.google.com/recaptcha/api/image?c=' + part.group(1)
        img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()

        xbmc.sleep(3000)

        kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        kb.doModal()
        capcode = kb.getText()

        if (kb.isConfirmed()):
            userInput = kb.getText()
            if userInput != '':
                solution = kb.getText()
            elif userInput == '':
                raise Exception ('You must enter text in the image to access video')
                wdlg.close()
        else:
            wdlg.close()
            raise Exception ('Captcha Error')
        wdlg.close()
        data.update({'recaptcha_challenge_field':part.group(1),'recaptcha_response_field':solution})               

    #Numeric captcha - we can programmatically figure this out
    elif numeric_captcha:
        result = sorted(numeric_captcha, key=lambda ltr: int(ltr[0]))
        solution = ''.join(str(int(num[1])-48) for num in result)
        data.update({'code':solution})  
        
    return data


def resolve_180upload(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        headers = {'Referer': url}
        
        media_id = re.search('//.+?/([\w]+)', url).group(1)
        web_url = 'http://180upload.com/embed-%s.html' % media_id
       
        addon.log_debug( '180Upload - Requesting GET URL: %s' % web_url)
        html = net.http_GET(web_url).content

        dialog.update(50)

        wrong_captcha = True
        
        while wrong_captcha:
        
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)"', html)

            if r:
                for name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve 180Upload Link')

            # 1st attempt, probably no captcha
            addon.log('180Upload - Requesting POST URL: %s Data values: %s' % (web_url, data))
            html = net.http_POST(web_url, data, headers=headers).content
 
            packed = re.search('id="player_code".*?(eval.*?\)\)\))', html,re.DOTALL)
            if packed:
                js = jsunpack.unpack(packed.group(1))
                link = re.search('name="src"0="([^"]+)"/>', js.replace('\\',''))
                if link:
                    addon.log('180Upload Link Found: %s' % link.group(1))
                    dialog.update(100)
                    return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
                else:
                    link = re.search("'file','(.+?)'", js.replace('\\',''))
                    if link:
                        addon.log('180Upload Link Found: %s' % link.group(1))
                        return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
                    
            #Cannot get video without captcha, so try regular url
            html = net.http_GET(url).content

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

            if r:
                for name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve 180Upload Link')            
            
            #Check for captcha
            data = handle_captchas(url, html, data, dialog)

            dialog.create('Resolving', 'Resolving 180Uploads Link...') 
            dialog.update(50)  
            
            addon.log_debug( '180Upload - Requesting POST URL: %s Data: %s' % (url, data))
            html = net.http_POST(url, data, headers=headers).content

            wrong_captcha = re.search('<div class="err">Wrong captcha</div>', html)
            if wrong_captcha:
                addon.show_ok_dialog(['Wrong captcha entered, try again'], title='Wrong Captcha', is_error=False)

        dialog.update(100)
        
        link = re.search('id="lnk_download[^"]*" href="([^"]+)', html)
        if link:
            addon.log_debug( '180Upload Link Found: %s' % link.group(1))
            return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        addon.log_error('**** 180Upload Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_24uploading(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 24Uploading Link...')
        dialog.update(0)
        
        addon.log_debug('24Uploading - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(33)

        wrong_captcha = True
        
        while wrong_captcha:
        
            data = {}
            r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
            if r:
                for none, name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve 24Uploading Link')
                
            addon.log('24Uploading - Requesting POST URL: %s DATA: %s' % (url, data))
            html = net.http_POST(url, data).content                
            dialog.update(66)

            data = {}
            r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
            if r:
                for none, name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve 24Uploading Link')
            
            #Handle captcha
            data = handle_captchas(url, html, data, dialog)

            dialog.create('Resolving', 'Resolving 24Uploading Link...') 
            dialog.update(66)

            addon.log('24Uploading - Requesting POST URL: %s DATA: %s' % (url, data))   
            html = net.http_POST(url, data).content

            wrong_captcha = re.search('<div class="err">Wrong captcha</div>', html)
            if wrong_captcha:
                addon.show_ok_dialog(['Wrong captcha entered, try again'], title='Wrong Captcha', is_error=False)
            
        dialog.update(100)
        
        link = re.search('<div class="btn_down">.+<a href="(.+?)" style="display:block;">', html, re.DOTALL)
        if link:
            addon.log_debug('24Uploading Link Found: %s' % link.group(1))
            return link.group(1)
        else:
            raise Exception('Unable to resolve 24Uploading Link')

    except Exception, e:
        addon.log_error('**** 24Uploading Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_clicknupload(url):

    try:

        media_id = re.search('//.+?/([\w]+)', url).group(1)
        url = 'http://clicknupload.link/%s' % media_id
        
        new_url = "https://clicknupload.link%s" % urlparse.urlsplit(url).path
		
        headers = {'Referer': new_url, 'User-Agent': USER_AGENT}
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving ClicknUpload Link...')       
        dialog.update(0)
        
        addon.log('ClicknUpload - Requesting GET URL: %s' % new_url)
        html = net.http_GET(new_url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** ClicknUpload - File is deleted')
            raise Exception('File has been deleted from the host')

        #Set POST data values
        data = data = get_hidden(html)				
        data['method_free'] = 'Free+Download+>>'
                
        addon.log('ClicknUpload - Requesting POST URL: %s DATA: %s' % (new_url, data))                
        html = net.http_POST(new_url, data, headers=headers).content
        dialog.update(66)

        data = data = get_hidden(html)

        #Check for captcha
        data = handle_captchas(new_url, html, data, dialog)                

        wait_string = re.search('<span id="countdown_str">Please wait <span id=".+?" style=".+?">([0-9]+)</span>', html)
        if wait_string:
            xbmc.sleep(int(wait_string.group(1)) * 1000)
    
        addon.log('ClicknUpload - Requesting POST URL: %s DATA: %s' % (new_url, data))                                
        html = net.http_POST(new_url, data, headers=headers).content

        #Get download link
        dialog.update(100)
        link = re.search('''class="downloadbtn"[^>]+onClick\s*=\s*\"window\.open\('([^']+)''', html)
        if link:
            return link.group(1) + '|User-Agent=%s' % USER_AGENT
        else:
            raise Exception("Unable to find final link")

    except Exception, e:
        addon.log_error('**** ClicknUpload Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_upload_af(url):

    try:

        headers = {'Referer': url}
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Upload.af Link...')       
        dialog.update(0)
        
        new_url = 'https://upload.af' + urlparse.urlsplit(url).path
        
        addon.log('Upload.af - Requesting GET URL: %s' % new_url)
        html = net.http_GET(new_url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** Upload.af - File is deleted')
            raise Exception('File has been deleted from the host')

        #Set POST data values
        data = get_hidden(html)

        data['method_free'] = 'Free Download >>'                
        
        addon.log('Upload.af - Requesting POST URL: %s DATA: %s' % (new_url, data))                
        html = net.http_POST(new_url, data, headers=headers).content
        addon.log(html)
        dialog.update(66)

        data = get_hidden(html)
        
        #Check for captcha
        data = handle_captchas(new_url, html, data, dialog)  
        
        wait_string = re.search('<div class="btn btn-danger" id="countdown">Wait <b class="seconds">([0-9]+)</b> seconds</div>', html)
        if wait_string:
            xbmc.sleep(int(wait_string.group(1)) * 1000)
    
        addon.log('Upload.af - Requesting POST URL: %s DATA: %s' % (new_url, data))                                
        html = net.http_POST(new_url, data, headers=headers).content
        addon.log(html)

        #Get download link
        dialog.update(100)

        link = re.search('<a href="(.+?)".*?>Download</a>', html)
        if link:
            return link.group(1) + '|User-Agent=%s' % USER_AGENT
        else:
            raise Exception("Unable to find final link")

    except Exception, e:
        addon.log_error('**** Upload.af Error occured: %s' % e)
        raise
    finally:
        dialog.close()
    
    
def get_hidden(html, form_id=None):
    hidden = {}
    if form_id:
        pattern = '''<form [^>]*id\s*=\s*['"]?%s['"]?[^>]*>(.*?)</form>'''
    else:
        pattern = '''<form[^>]*>(.*?)</form>'''
        
    for form in re.finditer(pattern, html, re.DOTALL | re.I):
        for field in re.finditer('''<input [^>]*type=['"]?hidden['"]?[^>]*>''', form.group(1)):
            match = re.search('''name\s*=\s*['"]([^'"]+)''', field.group(0))
            match1 = re.search('''value\s*=\s*['"]([^'"]*)''', field.group(0))
            if match and match1:
                hidden[match.group(1)] = match1.group(1)
            
    addon.log_debug('Hidden fields are: %s' % (hidden))
    return hidden
    
    
def resolve_uploadx(url):

    try:

        headers = {'Referer': url}
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Uploadx Link...')       
        dialog.update(0)
        
        addon.log('Uploadx - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** Uploadx - File is deleted')
            raise Exception('File has been deleted from the host')

        #Set POST data values
        data = {}
        r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
        if r:
            for none, name, value in r:
                data[name] = value

        data['method_free'] = 'Free Download >>'                
        
        addon.log('Uploadx - Requesting POST URL: %s DATA: %s' % (url, data))                
        html = net.http_POST(url, data, headers=headers).content
        dialog.update(66)

        data = {}
        r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
        if r:
            for none, name, value in r:
                data[name] = value

        #Check for captcha
        data = handle_captchas(url, html, data, dialog)                
        
        # wait_string = re.search('<div class="btn btn-danger" id="countdown">Wait <b class="seconds">([0-9]+)</b> seconds</div>', html)
        # if wait_string:
            # xbmc.sleep(int(wait_string.group(1)) * 1000)
    
        addon.log('Uploadx - Requesting POST URL: %s DATA: %s' % (url, data))                                
        html = net.http_POST(url, data, headers=headers).content

        #Get download link
        dialog.update(100)

        link = re.search('<a href="(.+?)".*?>Download</a>', html)
        if link:
            return link.group(1) + '|User-Agent=%s' % USER_AGENT
        else:
            raise Exception("Unable to find final link")

    except Exception, e:
        addon.log_error('**** Uploadx Error occured: %s' % e)
        raise
    finally:
        dialog.close()

        
def resolve_vidhog(url):

    try:
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving VidHog Link...')
        dialog.update(0)
        
        addon.log_debug('VidHog - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            raise Exception('File is currently unavailable on the host')
        if re.search('<b>File Not Found</b>', html):
            raise Exception('File has been deleted')

        filename = re.search('<strong>\(<font color="red">(.+?)</font>\)</strong><br><br>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://vidhog.com/(.+)$', url).group(1)
        
        vid_embed_url = 'http://vidhog.com/vidembed-%s%s' % (guid, extension)
        
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', USER_AGENT)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        addon.log_error('**** VidHog Error occured: %s' % e)
        raise
    finally:
        dialog.close()

        
def resolve_vidplay(url):

    try:
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving VidPlay Link...')
        dialog.update(0)
        
        addon.log_debug('VidPlay - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            raise Exception('File is currently unavailable on the host')
        if re.search('<b>File Not Found</b>', html):
            raise Exception('File has been deleted')

        filename = re.search('<h4>(.+?)</h4>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://vidplay.net/(.+)$', url).group(1)
        
        vid_embed_url = 'http://vidplay.net/vidembed-%s%s' % (guid, extension)
        
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', USER_AGENT)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename  + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        addon.log_error('**** VidPlay Error occured: %s' % e)
        raise
    finally:
        dialog.close()
        

def resolve_epicshare(url):

    try:
        
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving EpicShare Link...')
        dialog.update(0)
        
        addon.log('EpicShare - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            addon.log_error('***** EpicShare - Site reported maintenance mode')
            raise Exception('File is currently unavailable on the host')
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** EpicShare - File not found')
            raise Exception('File has been deleted')

        wrong_captcha = True
        
        while wrong_captcha:
        
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

            if r:
                for name, value in r:
                    data[name] = value
            else:
                addon.log_error('***** EpicShare - Cannot find data values')
                raise Exception('Unable to resolve EpicShare Link')

            #Handle captcha
            data = handle_captchas(url, html, data, dialog)
            
            dialog.create('Resolving', 'Resolving EpicShare Link...') 
            dialog.update(50) 
                
            addon.log('EpicShare - Requesting POST URL: %s' % url)
            html = net.http_POST(url, data).content

            wrong_captcha = re.search('<div class="err">Wrong captcha</div>', html)
            if wrong_captcha:
                addon.show_ok_dialog(['Wrong captcha entered, try again'], title='Wrong Captcha', is_error=False)            
        
        dialog.update(100)
        
        link = re.search('product_download_url=(.+?)"', html)
        if link:
            addon.log('EpicShare Link Found: %s' % link.group(1))
            return link.group(1)
        else:
            addon.log_error('***** EpicShare - Cannot find final link')
            raise Exception('Unable to resolve EpicShare Link')
        
    except Exception, e:
        addon.log_error('**** EpicShare Error occured: %s' % e)
        raise

    finally:
        dialog.close()


def resolve_hugefiles(url):

    try:
            
        headers = {'Referer': 'http://www.icefilms.info/'}
        
        puzzle_img = os.path.join(datapath, "hugefiles_puzzle.png")
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving HugeFiles Link...')       
        dialog.update(0)
        
        media_id = re.search('//.+?/([\w]+)', url).group(1)
        web_url = 'http://hugefiles.net/embed-%s.html' % media_id
        
        addon.log_debug('HugeFiles - Requesting GET URL: %s' % web_url)
        html = net.http_GET(web_url, headers=headers).content
        
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<h3>File Not found</h3>', html):
            addon.log_error('***** HugeFiles - File Not Found')
            raise Exception('File Not Found')

        wrong_captcha = True
        
        while wrong_captcha:
        
            #Set POST data values
            data = {}
            r = re.findall(r'type="hidden"\s+name="([^"]+)"\s+value="([^"]+)', html)
            
            if r:
                for name, value in r:
                    data[name] = value
            else:
                addon.log_error('***** HugeFiles - Cannot find data values')
                raise Exception('Unable to resolve HugeFiles Link')
            
            data['method_free'] = 'Free Download'

            #Handle captcha
            data.update(handle_captchas(web_url, html, data, dialog))
            
            dialog.create('Resolving', 'Resolving HugeFiles Link...') 
            dialog.update(50)             
            
            addon.log('HugeFiles - Requesting POST URL: %s DATA: %s' % (web_url, data))
            html = net.http_POST(web_url, data, headers=headers).content

            solvemedia = re.search('<iframe src="((?:http:)?//api.solvemedia.com[^"]+)', html)
            recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com[^"]+)', html)            
            numeric_captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)   

            if solvemedia or recaptcha or numeric_captcha:
                addon.show_ok_dialog(['Wrong captcha entered, try again'], title='Wrong Captcha', is_error=False)
            else:
                wrong_captcha = False
            
        #Get download link
        dialog.update(100)       

        packed = re.search('id="player_code".*?(eval.*?\)\)\))', html,re.DOTALL)
        if packed:
            js = jsunpack.unpack(packed.group(1))
            link = re.search('name="src"0="([^"]+)"/>', js.replace('\\',''))
            if link:
                addon.log('HugeFiles Link Found: %s' % link.group(1))
                return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
            else:
                link = re.search("'file','(.+?)'", js.replace('\\',''))
                if link:
                    addon.log('HugeFiles Link Found: %s' % link.group(1))
                    return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)


        #r = re.search('fileUrl\s*=\s*"([^"]+)', html)
        #if r:
        #    return r.group(1)        
        
    except Exception, e:
        addon.log_error('**** HugeFiles Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_kingfiles(url):

    try:
        puzzle_img = os.path.join(datapath, "kingfiles_puzzle.png")
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving KingFiles Link...')
        dialog.update(0)
        
        addon.log_debug('KingFiles - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(33)

        wrong_captcha = True
        
        while wrong_captcha:
        
            data = {}
            r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)"', html)
            if r:
                for none, name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve KingFiles Link')

            data['method_premium'] = ''                
            
            addon.log('KingFiles - Requesting POST URL: %s DATA: %s' % (url, data))
            html = net.http_POST(url, data).content                
            dialog.update(66)

            data = {}
            r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
            if r:
                for none, name, value in r:
                    data[name] = value
            else:
                raise Exception('Unable to resolve KingFiles Link')
            
            #Handle captcha
            data = handle_captchas(url, html, data, dialog)

            dialog.create('Resolving', 'Resolving KingFiles Link...') 
            dialog.update(66)

            addon.log('KingFiles - Requesting POST URL: %s DATA: %s' % (url, data))   
            html = net.http_POST(url, data).content

            wrong_captcha = re.search('<div class="err">Wrong captcha</div>', html)
            if wrong_captcha:
                addon.show_ok_dialog(['Wrong captcha entered, try again'], title='Wrong Captcha', is_error=False)
            
        dialog.update(100)
        
        
        packed = re.search('id="player_code".*?(eval.*?\)\)\))', html,re.DOTALL)
        if packed:
            js = jsunpack.unpack(packed.group(1))
            link = re.search('name="src"0="([^"]+)"/>', js.replace('\\',''))
            if link:
                addon.log('KingFiles Link Found: %s' % link.group(1))
                return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
            else:
                link = re.search("'file','(.+?)'", js.replace('\\',''))
                if link:
                    addon.log('KingFiles Link Found: %s' % link.group(1))
                    return link.group(1) + '|Referer=%s&User-Agent=%s' % (url, USER_AGENT)
                    
    except Exception, e:
        addon.log_error('**** KingFiles Error occured: %s' % e)
        raise
    finally:
        dialog.close()        

        
def resolve_entroupload(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving EntroUpload Link...')       
        dialog.update(0)
        
        addon.log('EntroUpload - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content
        
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** EntroUpload - File Not Found')
            raise Exception('File Not Found')

        #Set POST data values
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        
        if r:
            for name, value in r:
                data[name] = value
        else:
            addon.log_error('***** EntroUpload - Cannot find data values')
            raise Exception('Unable to resolve EntroUpload Link')
        
        data['method_free'] = 'Free Download'
        file_name = data['fname']

        addon.log('EntroUpload - Requesting POST URL: %s DATA: %s' % (url, data))
        html = net.http_POST(url, data).content

        #Get download link
        dialog.update(100)

        sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>(eval\('
        sPattern += 'function\(p,a,c,k,e,d\)(?!.+player_ads.+).+np_vid.+?)'
        sPattern += '\s+?</script>'
        r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)
        if r:
            sJavascript = r.group(1)
            sUnpacked = jsunpack.unpack(sJavascript)
            sPattern  = '<embed id="np_vid"type="video/divx"src="(.+?)'
            sPattern += '"custommode='
            r = re.search(sPattern, sUnpacked)
            if r:
                return r.group(1)
            else:
                addon.log_error('***** EntroUpload - Cannot find final link')
                raise Exception('Unable to resolve EntroUpload Link')
        else:
            addon.log_error('***** EntroUpload - Cannot find final link')
            raise Exception('Unable to resolve EntroUpload Link')
        
    except Exception, e:
        addon.log_error('**** EntroUpload Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_donevideo(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving DoneVideo Link...')       
        dialog.update(0)
        
        addon.log('DoneVideo - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content
    
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        
        if r:
          for name, value in r:
              data[name] = value
        else:
            addon.log_error('***** DoneVideo - Cannot find data values')
            raise Exception('Unable to resolve DoneVideo Link')
        
        data['method_free'] = 'Continue to Video'
        addon.log('DoneVideo - Requesting POST URL: %s' % url)
        
        html = net.http_POST(url, data).content
        
        dialog.update(50)
                
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        
        if r:
          for name, value in r:
              data[name] = value
        else:
          addon.log_error('Could not resolve link')
        
        data['method_free'] = 'Continue to Video'
        
        addon.log('DoneVideo - Requesting POST URL: %s' % url)
        
        html = net.http_POST(url, data).content

        #Get download link
        dialog.update(100)
        
        sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
        r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)

        if r:
          sJavascript = r.group(1)
          sUnpacked = jsunpack.unpack(sJavascript)
          sUnpacked = sUnpacked.replace("\\","")
                   
        r = re.search("addVariable.+?'file','(.+?)'", sUnpacked)
                
        if r:
            return r.group(1)
        else:
            sPattern  = '<embed id="np_vid"type="video/divx"src="(.+?)'
            sPattern += '"custommode='
            r = re.search(sPattern, sUnpacked)
            if r:
                return r.group(1)
            else:
                addon.log_error('***** DoneVideo - Cannot find final link')
                raise Exception('Unable to resolve DoneVideo Link')

    except Exception, e:
        addon.log_error('**** DoneVideo Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def SHARED2_HANDLER(url):

    html = net.http_GET(url).content

    #Check if a download limit msg is showing
    if re.search('Your free download limit is over.', html):
      wait_time = re.search('<span id="timeToWait">(.+?)</span>', html).group(1)
      Notify('big','2Shared Download Limit Exceeded','You have reached your download limit', '', '', 'You must wait ' + wait_time + ' to try again' )
      return None

    #If no download limit msg lets grab link, must post to it first for download to activate
    else:
      d3fid = re.search('<input type="hidden" name="d3fid" value="(.+?)">', html).group(1)
      d3link = re.search('<input type="hidden" name="d3link" value="(.+?)">', html).group(1)
      data = {'d3fid': d3fid, 'd3link': d3link}
      html = net.http_POST(url, data).content
      return d3link
      

def resolve_tusfiles(url):

    try:
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving TusFiles Link...')
        dialog.update(0)
        
        addon.log('TusFiles - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            addon.log_error('***** TusFiles - Site reported maintenance mode')
            raise Exception('File is currently unavailable on the host')
        if re.search('<b>File Not Found</b>', html):
            addon.log_error('***** TusFiles - File not found')
            raise Exception('File has been deleted')

        filename = re.search('Start download<h1><span class="label label-default"><FONT COLOR="#ffffff">(.+?)</FONT>', html).group(1)
        filename = filename.split('/')[-1]
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://tusfiles.net/(.+)$', url).group(1)
        
        vid_embed_url = 'http://tusfiles.net/vidembed-%s%s' % (guid, extension)
        
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', USER_AGENT)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http[s]*://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        addon.log_error('**** TusFiles Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_xfileload(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving XfileLoad Link...')       
        dialog.update(0)
        
        addon.log('XfileLoad - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content
        
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<li>The file was deleted by its owner', html):
            addon.log_error('***** XfileLoad - File is deleted')
            raise Exception('File has been deleted from the host')

        #Set POST data values
        data = {}
        r = re.findall('type="(hidden|submit)" name="(.+?)" value="(.*?)">', html)
        if r:
            for none, name, value in r:
                data[name] = value

        addon.log('XfileLoad - Requesting POST URL: %s DATA: %s' % (url, data))                
        html = net.http_POST(url, data).content

        #Get download link
        dialog.update(100)
        link = re.search('<a href="(.+?)" target=""><img src="http://xfileload.com/3ghdes/images/downdown.png" /></a>', html)
        if link:
            return link.group(1)
        else:
            raise Exception("Unable to find final link")

    except Exception, e:
        addon.log_error('**** XfileLoad Error occured: %s' % e)
        raise
    finally:
        dialog.close()
        

def resolve_mightyupload(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MightyUpload Link...')       
        dialog.update(0)
        
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://www.mightyupload.com/embed-%s.html' % url
        
        addon.log('MightyUpload - Requesting GET URL: %s' % url)
        html = net.http_GET(url).content
        dialog.update(100)    

        link = re.compile("file *: *'(.+?)'").findall(html)
        if len(link) > 0: 
            return link[0] + '|User-Agent=%s' % (USER_AGENT)    
                
        result = re.compile('(eval.*?\)\)\))').findall(html)[-1]
        if result:
            sJavascript = result
            sUnpacked = jsunpack.unpack(sJavascript)

            r = re.search("'file','([^']+)'", sUnpacked.replace('\\', ''))
            if not r:
                r = re.search('"src"value="([^"]+)', sUnpacked.replace('\\', ''))
                if not r:
                    r = re.search('"src"[0-9]="(.+?)"/>', sUnpacked.replace('\\', ''))
            if r:
                return r.group(1) + '|User-Agent=%s' % (USER_AGENT)
            else:
                raise Exception("Unable to find final link")

    except Exception, e:
        addon.log_error('**** MightyUpload Error occured: %s' % e)
        raise
    finally:
        dialog.close()


def resolve_xvidstage(url):

    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving XvidStage Link...')       
        dialog.update(0)
        
      
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://xvidstage.com/embed-%s.html' % url      

        addon.log('XvidStage - Requesting GET URL: %s' % url)        
        html = net.http_GET(url).content
        dialog.update(100)
        
        result = re.compile('(eval.*?\)\)\))').findall(html)[-1]
        if result:
            sJavascript = result
            sUnpacked = jsunpack.unpack(sJavascript)
            sPattern = "'file','(.+?)'"
            r = re.search(sPattern, sUnpacked)
            if r:
                return r.group(1)
            else:
                raise Exception("Unable to find final link")
        else:
            raise Exception("Unable to find final link")                

    except Exception, e:
        addon.log_error('**** XvidStage Error occured: %s' % e)
        raise
    finally:
        dialog.close()