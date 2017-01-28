#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,json,xbmcgui
import cookielib
from urlparse import urlparse
from HTMLParser import HTMLParser

###################################################################################
#Form Parser

class FormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                raise RuntimeError("Second form on page")
            if self.in_form:
                raise RuntimeError("Already in form")
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == "form":
            self.url = attrs["action"]
            if "method" in attrs:
                self.method = attrs["method"].upper()
        elif tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise RuntimeError("Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True

###################################################################################
#Login to vk.com

def auth(email, password, client_id, scope):
    def split_key_value(kv_pair):
        kv = kv_pair.split("=")
        return kv[0], kv[1]

    # Authorization form
    def auth_user(email, password, client_id, scope, opener):
        response = opener.open(
            "http://oauth.vk.com/oauth/authorize?" + \
            "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
            "client_id=%s&scope=%s&display=wap" % (client_id, ",".join(scope))
            )
        doc = response.read()
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        if not parser.form_parsed or parser.url is None or "pass" not in parser.params or \
          "email" not in parser.params:
              raise RuntimeError("Something wrong")
        parser.params["email"] = email
        parser.params["pass"] = password
        if parser.method == "POST":
            response = opener.open(parser.url, urllib.urlencode(parser.params))
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.read(), response.geturl()

    #2nd step of authentification
    def sms_code(doc, opener):
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        auth_code = xbmcgui.Dialog().numeric(0,'Auth code:')
        auth_code = int(auth_code)
        parser.params["code"] = auth_code
        if parser.method == "POST":
            response = opener.open("https://m.vk.com" + parser.url, urllib.urlencode(parser.params))
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.read(), response.geturl()

    # Permission request form
    def give_access(doc, opener):
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        if not parser.form_parsed or parser.url is None:
              raise RuntimeError("Something wrong")
        if parser.method == "POST":
            response = opener.open(parser.url, urllib.urlencode(parser.params))
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.geturl()


    if not isinstance(scope, list):
        scope = [scope]
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
        urllib2.HTTPRedirectHandler())
    doc, url = auth_user(email, password, client_id, scope, opener)
    if "/login" in urlparse(url).path: 
        doc, url = sms_code(doc, opener)
    if urlparse(url).path != "/blank.html":
        # Need to give access to requested scope
        url = give_access(doc, opener)
    if urlparse(url).path != "/blank.html":
        raise RuntimeError("Expected success here")
    answer = dict(split_key_value(kv_pair) for kv_pair in urlparse(url).fragment.split("&"))
    if "access_token" not in answer or "user_id" not in answer:
        raise RuntimeError("Missing some values in answer")
    return answer["access_token"]

###################################################################################
#Check if the vk.com token is valid

def isTokenValid(token):
    req = urllib2.Request('https://api.vk.com/method/audio.search.json?q=eminem&access_token='+token)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
    response = urllib2.urlopen(req)
    codigo_fonte=response.read()
    response.close()
    decoded_data = json.loads(codigo_fonte)
    if 'error' in decoded_data:
        #return the detailed error message
        try: return str(decoded_data['error']['error_msg'])
        except: return str(decoded_data['error'])
    else:
        return True