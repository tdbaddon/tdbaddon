import xbmc, xbmcaddon
import os, re
try:
	try: import cPickle as pickle
	except ImportError: import pickle
except: pass
try:
	try: import json
	except ImportError: import simplejson as json
except: pass


addonId = 'plugin.video.cinemaxx'

selfAddon = xbmcaddon.Addon(id=addonId)
profilePath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

try: os.makedirs(profilePath)
except: pass


def getPluginVersion():
	return "%s v%s" % (addonId, selfAddon.getAddonInfo('version'))


def getPluginPath():
	return xbmc.translatePath(selfAddon.getAddonInfo('path'))


def getSetting(settingId):
	return selfAddon.getSetting(settingId)


def openSettings():
	selfAddon.openSettings()


def saveData(filename, data):
	savePath = os.path.join(profilePath, filename)
	try:
		pickle.dump(data, open(savePath, 'wb'))
		return True
	except pickle.PickleError:
		return False


def loadData(filename):
	loadPath = os.path.join(profilePath, filename)
	if os.path.isfile(loadPath):
		try: return pickle.load(open(loadPath))
		except: return False
	else:
		return False


def cacheList(listItems, filename):
	try:
		cacheFile = os.path.join(profilePath, filename + ".cache")
		with open(cacheFile, 'w') as f:
			f.write(json.dumps(listItems))
	except: pass


def cacheLoad(filename, expire):
	cacheFile = os.path.join(profilePath, filename + ".cache")
	try:
		import time
		if os.path.isfile(cacheFile) and os.path.getsize(cacheFile) > 0 and (time.time() - os.path.getmtime(cacheFile)) <= expire * 60:
			with open(cacheFile, 'r') as f:
				return json.loads(f.read())
		else:
			return False
	except:
		return False


def clearCache():
	try:
		filelist = [file for file in os.listdir(profilePath) if file.endswith(".cache")]
		for file in filelist:
			os.remove(profilePath + file)
		return True
	except: return False
		
def en2ro(string):
	dict = {
			'sd':			'calitate standard',
			'low':			'calitate redusa',
			'lowest':		'calitate scazuta',
			'mobile':		'calitate mobil',
	}
	try:
		string = string.strip()
		string = re.compile(r'\b(' + '|'.join(dict.keys()) + r')\b').sub(lambda x: dict[x.group()], string)
	except:
		pass
	return string