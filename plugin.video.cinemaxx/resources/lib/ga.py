from random import randint
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlunparse
from hashlib import sha1
try: from sys import getwindowsversion
except: pass
import xbmc, xbmcgui
import uuid


def track(plugin=''):
	try:
		PROPERTY_ID = "UA-46834994-1"
		PATH = "/"
		
		ID = str(uuid.getnode())
		
		VISITOR = str(int("0x%s" % sha1(ID).hexdigest(), 0))[:10]
		
		DATA = {"utmwv": "5.2.2d",
				"utmn": str(randint(1, 9999999999)),
				"utmp": PATH,
				"utmac": PROPERTY_ID,
				"utmdt": getPlatform(plugin),
				"utmul": xbmc.getLanguage(),
				"utmsr": window().getResolution(),
				"utmcc": "__utma=%s;" % ".".join(["1", VISITOR, "1", "1", "1", "1"])}

		URL = urlunparse(("http",
						  "www.google-analytics.com",
						  "/__utm.gif",
						  "",
						  urlencode(DATA),
						  ""))
		urlopen(URL).info()
	except:
		pass


def getPlatform(plugin):
	try:
		os_platforms = {
			"Linux": "X11; Linux",
			"Windows": "Windows NT %d.%d",
			"OSX": "Macintosh; Intel Mac OS X",
			"IOS": "iPad; CPU OS 6_1 like Mac OS X",
		}
		
		for os, os_version in os_platforms.items():
			if xbmc.getCondVisibility("System.Platform.%s" % os):
				if os == "Windows":
					version = getwindowsversion()
					os_version %= (version[0], version[1])
				platform = "XBMC %s (%s) %s" % (xbmc.getInfoLabel("System.BuildVersion").split(" ")[0], os_version, plugin)
				paltform = platform.strip()
		return platform
	except:
		platform = "XBMC %s" % plugin
		platform = platform.strip()
		return platform

class window(xbmcgui.Window):
	def getResolution(self):
		screenx = self.getWidth()
		screeny = self.getHeight()
		return str(screenx) + 'x' + str(screeny)
