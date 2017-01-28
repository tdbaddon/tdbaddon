# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector for OPENLOAD JULY 2016
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

# fixed by cmos


import re, urllib, urllib2, requests, base64, cookielib, string, time

	
def downloadpageWithoutCookies(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')
    req.add_header('X-Requested-With','XMLHttpRequest')
    try:
        response = urllib2.urlopen(req)
    except:
        req = urllib2.Request(url.replace(" ","%20"))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')

        response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data
	
	
def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""

def find_multiple_matches(text,pattern):
    return re.findall(pattern,text,re.DOTALL)
	
def toString(number,base):
   string = "0123456789abcdefghijklmnopqrstuvwxyz"
   if number < base:
      return string[number]
   else:
      return toString(number//base,base) + string[number%base]
	  
def decode(text):
    text = re.sub(r"\s+", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)","u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)
        for x in find_multiple_matches(char,'(\(\d\+\d\))'):
            char = char.replace( x, str(eval(x)) )
        for x in find_multiple_matches(char,'(\(\d\^\d\^\d\))'):
            char = char.replace( x, str(eval(x)) )
        for x in find_multiple_matches(char,'(\(\d\+\d\+\d\))'):
            char = char.replace( x, str(eval(x)) )
        for x in find_multiple_matches(char,'(\(\d\+\d\))'):
            char = char.replace( x, str(eval(x)) )
        for x in find_multiple_matches(char,'(\(\d\-\d\))'):
            char = char.replace( x, str(eval(x)) )
        if 'u' not in char: txt+= char + "|"
    txt = txt[:-1].replace('+','')
    txt_result = "".join([ chr(int(n, 8)) for n in txt.split('|') ])
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in  txt_result:
            m3 = True
            sum_base = "+"+find_single_match(txt_result,".toString...(\d+).")
            txt_pre_temp = find_multiple_matches(txt_result,"..(\d),(\d+).")
            txt_temp = [ (n, b) for b ,n in txt_pre_temp ]
        else:
            txt_temp = find_multiple_matches(txt_result, '(\d+)\.0.\w+.([^\)]+).')
        for numero, base in txt_temp:
            code = toString( int(numero), eval(base+sum_base) )
            if m3:
                txt_result = re.sub( r'"|\+', '', txt_result.replace("("+base+","+numero+")", code) )
            else:
                txt_result = re.sub( r"'|\+", '', txt_result.replace(numero+".0.toString("+base+")", code) )
    return txt_result

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    video_urls = [] ; page_url=page_url.replace('/f/', '/embed/')
    data = downloadpageWithoutCookies(page_url)
    subtitle = find_single_match(data, '<track kind="captions" src="([^"]+)" srclang="es"')
    #Header para la descarga
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}	
    header_down = "|User-Agent="+headers['User-Agent']+"|"
    if "videocontainer" not in data:
        url = page_url.replace("/embed/","/f/")
        data = downloadpageWithoutCookies(url)
        text_encode = find_single_match(data,"Click to start Download.*?<script[^>]+>(.*?)</script")
        text_decode = decode(text_encode)
        videourl = find_single_match(text_decode, '(http.*?)\}')
    else:
        text_encode = find_multiple_matches(data,'<script type="text/javascript">(ﾟωﾟ.*?)</script>')
        # Buscamos la variable que nos indica el script correcto
        subtract = find_single_match(data, 'welikekodi_ya_rly = ([^;]+)')
        index = eval(subtract)
        text_decode = decode(text_encode[index])
        videourl = find_single_match(text_decode, "(http.*?true)")
    videourl = videourl  + '|User-Agent=Mozilla/5.0(iPhone;U;CPUiPhoneOS4_0likeMacOSX;en-us)AppleWebKit/532.9(KHTML,likeGecko)Version/4.0.5Mobile/8A293Safari/6531.22.7'
    videourl = videourl.replace('https','http')	
    return videourl





