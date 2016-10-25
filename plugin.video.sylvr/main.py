import urllib,urllib2,re,xbmcaddon,xbmcplugin,xbmcgui,os,sys,datetime,string,hashlib,json,net,liveresolver,urlparse
net = net.Net()

ADDON = xbmcaddon.Addon(id="plugin.video.sylvr")
DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/plugin.video.sylvr"), "")
addon_id = xbmcaddon.Addon().getAddonInfo("id")
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.sylvr", "icon.jpg"))
fanart = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.sylvr", "fanart.jpg"))
logos = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.sylvr/logos", ""))
logos_tvp = "https://assets.tvplayer.com/common/logos/256/Inverted/"
useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0"}

def AerTV(link):
	if not selfAddon.getSetting("aertv_email") == "" and not selfAddon.getSetting("aertv_password") == "":
		try:

			req = urllib2.Request("https://api.aertv.ie/v2/users/login", urllib.urlencode({"email": selfAddon.getSetting("aertv_email"), "password": selfAddon.getSetting("aertv_password")}), useragent)
			html = urllib2.urlopen(req).read()

			req = urllib2.Request("https://api.aertv.ie/v2/players/"+link+"?user_token="+json.loads(html)["data"]["user_token"], None, useragent)
			html = urllib2.urlopen(req).read()
			j = json.loads(html)
			SD = ""
			HD = ""
			
			for item in j["data"]["urls"]["stream"]["rtmp"]:
				if int(item["bitrate"]) >= 500000 and int(item["bitrate"]) < 1500000:
					SD = item["source"] #Set the List Link to SD Variable;
				if int(item["bitrate"]) >= 1500000:
					HD = item["source"] #Set the List Link to HD Variable;
				if not HD:
					HD = SD #Set the HD Variable"s link to the SD Link;
			
			#Return Stream based on the Quality Setting;
			if selfAddon.getSetting("quality") == "SD":
				return SD
			else:
				return HD

		except:

			xbmc.executebuiltin("Notification(AerTV Error, The entered AerTV details are incorrect!)")
			return ""
	else:
		return "https://offshoregit.com/Shiny/data/plugin.video.sylvr/assets/no-aertv.mp4"

def Arconai(link):
	req = urllib2.Request("http://45.62.245.50/arconai.php?u="+link, None, useragent)
	try:
		html = urllib2.urlopen(req).read()
	except urllib2.HTTPError, e:
		xbmc.log(html)
		xbmc.log(str(e))
	return html
	
def UTV():
	req = urllib2.Request("http://player.utv.ie/live/", None, useragent)
	html = urllib2.urlopen(req).read()
	return re.findall('data-streamurl="(.*)" ', html)[0].replace("&","%26")

def Streams(channel):

	# 24/7 TV
	if channel == "Adult Swim": return Arconai("as")
	elif channel == "Adventure Time": return Arconai("at")
	elif channel == "American Dad": return Arconai("amerro")
	elif channel == "Archer": return Arconai("arc")
	elif channel == "Better Call Saul": return Arconai("bcs")
	elif channel == "Bob's Burgers": return Arconai("bb")
	elif channel == "Doctor Who": return Arconai("thedoctors")
	elif channel == "DragonBall Z": return Arconai("dbz")
	elif channel == "Family Guy": return Arconai("fg")
	elif channel == "Friends": return Arconai("friendship")
	elif channel == "Futurama": return Arconai("future")
	elif channel == "Game of Thrones": return Arconai("got")
	elif channel == "It's Always Sunny in Philadelphia": return Arconai("asip")
	elif channel == "King of the Hill": return Arconai("koth")
	elif channel == "Malcolm in the Middle": return Arconai("malcolmmid")
	elif channel == "Regular Show": return Arconai("rs")
	elif channel == "Ren & Stimpy": return Arconai("renstimp")
	elif channel == "Rick & Morty": return Arconai("rm")
	elif channel == "Scrubs": return Arconai("scroobs")
	elif channel == "South Park": return Arconai("sp")
	elif channel == "The Big Bang Theory": return Arconai("tbbt")
	elif channel == "The Fresh Prince of Bel-Air": return Arconai("fpb")
	elif channel == "The Office (US)": return Arconai("to")
	elif channel == "The Simpsons": return Arconai("s")
	elif channel == "Workaholics": return Arconai("workers")

	# 24/7 Movies
	elif channel == "Action": return Arconai("action")
	elif channel == "Animation": return Arconai("animation")
	elif channel == "Comedy": return Arconai("comedy")
	elif channel == "Documentaries": return Arconai("docs")
	elif channel == "Horror": return Arconai("horror")
	elif channel == "Star Wars vs. Star Trek": return Arconai("spacewars")
	elif channel == "Random": return Arconai("moovaye")

	# Entertainment
	elif channel == "3e": return "http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,3e-prd.m3u8"
	elif channel == "Blaze": return "http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8"
	elif channel == "London Live": return "http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8"
	elif channel == "TG4": return "http://csm-e.cds1.yospace.com/csm/live/74246540.m3u8"
	elif channel == "truTV": return "http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8"
	elif channel == "TV3": return "http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,tv3-prd.m3u8"
	elif channel == "ABC": return Arconai("abcde")
	elif channel == "A&E": return Arconai("ae")
	elif channel == "BravoTV": return Arconai("braveotv")
	elif channel == "CBS": return Arconai("ceebees")
	elif channel == "Comedy Central": return Arconai("cc")
	elif channel == "CNBC": return Arconai("seenbeesee")
	elif channel == "FOX": return Arconai("foxxy")
	elif channel == "Fx": return Arconai("fx")
	elif channel == "Lifetime": return Arconai("lt")
	elif channel == "MTV (US)": return "rtmp://83.218.202.202/live swfUrl=http://webtv.md/swf/WebTV.swf playpath=wt_mtv.stream"
	elif channel == "NBC": return Arconai("nnnbsee")
	elif channel == "PBS": return Arconai("ppp")
	elif channel == "RTE One": return AerTV("rte-one")
	elif channel == "RTE One +1": return AerTV("rte-one1")
	elif channel == "RTE Two": return AerTV("rte-two")
	elif channel == "Spike TV": return Arconai("pointytv")
	elif channel == "SyFy": return Arconai("sify")
	elif channel == "TBS": return Arconai("teabees")
	elif channel == "The CW": return Arconai("tcw")
	elif channel == "USA Network": return Arconai("usan")
	elif channel == "UTV": return UTV()

	# Kids
	elif channel == "Cartoon Network": return Arconai("cn")
	elif channel == "Nickelodeon": return Arconai("nickie")
	elif channel == "RTEjr": return AerTV("rtejr")

	# Sports
	elif channel == "ESPN": return Arconai("sports")
	elif channel == "TNTUSA": return Arconai("teentee")

	# News/Parliament
	elif channel == "ABC News": return "http://abclive.abcnews.com/i/abc_live4@136330/index_2500_av-p.m3u8?sd=10&b=800-2500&rebase=on"
	elif channel == "Bloomberg TV (EU)": return "http://cdn3.videos.bloomberg.com/btv/eu/master.m3u8"
	elif channel == "Bloomberg TV (US)": return "http://cdn3.videos.bloomberg.com/btv/us/master.m3u8"
	elif channel == "Euronews": return "http://fr-par-iphone-1.cdn.hexaglobe.net/streaming/euronews_ewns/3-live.m3u8"
	elif channel == "FOX News": return Arconai("fn")
	elif channel == "France24": return "http://static.france24.com/live/F24_EN_LO_HLS/live_web.m3u8"
	elif channel == "Irish TV": return "http://cdn.fs-chf01-04-aa1a041f-8251-d66e-5678-d03fd8530fad.arqiva-ott-live.com/live-audio_track=96000-video=1900000.m3u8"
	elif channel == "Oireachtas TV": return "https://media.heanet.ie/transcode05/oireachtas/ngrp:oireachtas.stream_all/playlist.m3u8?DVR"
	elif channel == "RTE News Now": return "http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8"
	elif channel == "Sky News": return "https://www.youtube.com/watch?v=y60wDzZt8yg"

	# Documentary
	elif channel == "Animal Planet": return Arconai("ap")
	elif channel == "AMC": return Arconai("am")
	elif channel == "Discovery Channel": return Arconai("disco")
	elif channel == "History Channel": return Arconai("hc")
	elif channel == "National Geographic": return Arconai("ng")
	elif channel == "NASA ISS": return "http://iphone-streaming.ustream.tv/uhls/17074538/List/live/iphone/playlist.m3u8"
	elif channel == "NASA TV": return "http://nasatv-lh.akamaihd.net/i/NASA_101@319270/master.m3u8"

	# Music
	elif channel == "4Music": return "http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8"
	elif channel == "The Box": return "http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8"
	elif channel == "Box Hits": return "http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8"
	elif channel == "Box Upfront": return "http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8"
	elif channel == "Capital TV": return "http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on"
	elif channel == "Channel AKA": return "http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8"
	elif channel == "Heart TV": return "http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8"
	elif channel == "Kerrang!": return "http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8"
	elif channel == "Kiss": return "http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8"
	elif channel == "Magic": return "http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8"
	elif channel == "NOW Music": return "http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8"

def ListStreams(category):
	if category == "24/7 TV":
		addItem("Adult Swim", "resolve", logos+"247-adultswim.png")
		addItem("Adventure Time", "resolve", logos+"247-adventuretime.jpg")
		addItem("American Dad", "resolve", logos+"247-americandad.png")
		addItem("Archer", "resolve", logos+"247-archer.png")
		addItem("Better Call Saul", "resolve", logos+"247-bettercallsaul.png")
		addItem("Bob's Burgers", "resolve", logos+"247-bobsburgers.png")
		addItem("Doctor Who", "resolve", logos+"247-doctorwho.jpg")
		addItem("DragonBall Z", "resolve", logos+"247-dragonballz.jpg")
		addItem("Family Guy", "resolve", logos+"247-familyguy.png")
		addItem("Friends", "resolve", logos+"247-friends.jpg")
		addItem("Futurama", "resolve", logos+"247-futurama.png")
		addItem("Game of Thrones", "resolve", logos+"247-gameofthrones.jpg")
		addItem("It's Always Sunny in Philadelphia", "resolve", logos+"247-iasip.png")
		addItem("King of the Hill", "resolve", logos+"247-kingofthehill.png")
		addItem("Malcolm in the Middle", "resolve", logos+"247-malcominthemiddle.jpg")
		addItem("Regular Show", "resolve", logos+"247-regularshow.jpg")
		addItem("Ren & Stimpy", "resolve", logos+"247-renandstimpy.jpg")
		addItem("Rick & Morty", "resolve", logos+"247-rickandmorty.png")
		addItem("Scrubs", "resolve", logos+"247-scrubs.jpg")
		addItem("South Park", "resolve", logos+"247-southpark.png")
		addItem("The Big Bang Theory", "resolve", logos+"247-thebigbangtheory.jpg")
		addItem("The Fresh Prince of Bel-Air", "resolve", logos+"247-tfpob.jpg")
		addItem("The Office (US)", "resolve", logos+"247-theoffice.jpg")
		addItem("The Simpsons", "resolve", logos+"247-thesimpsons.png")
		addItem("Workaholics", "resolve", logos+"247-workaholics.png")
	elif category == "24/7 Movies":
		addItem("Action", "resolve", logos+"247-actionmovies.png")
		addItem("Animation", "resolve", logos+"247-animationmovies.png")
		addItem("Comedy", "resolve", logos+"247-comedymovies.png")
		addItem("Documentaries", "resolve", logos+"247-documentaries.png")
		addItem("Horror", "resolve", logos+"247-horrormovies.png")
		addItem("Star Wars vs. Star Trek", "resolve", logos+"247-spacewars.png")
		addItem("Random", "resolve", logos+"247-randommovies.png")
	elif category == "Entertainment":
		addItem("3e", "play", logos+"3e.png")
		addItem("ABC", "resolve", logos+"abc.png")
		addItem("A&E", "resolve", logos+"ae.png")
		addItem("Blaze", "play", logos+"blaze.png")
		addItem("BravoTV", "resolve", logos+"bravotv.png")
		addItem("CBS", "resolve", logos+"cbs.png")
		addItem("Comedy Central", "resolve", logos+"comedycentral.png")
		addItem("CNBC", "resolve", logos+"cnbc.png")
		addItem("FOX", "resolve", logos+"fox.png")
		addItem("Fx", "resolve", logos+"fx.png")
		addItem("Lifetime", "resolve", logos+"lifetime.png")
		addItem("London Live", "play", logos+"londonlive.png")
		addItem("MTV (US)", "play", logos+"mtv.png")
		addItem("NBC", "resolve", logos+"nbc.png")
		addItem("PBS", "resolve", logos+"pbs.png")
		addItem("RTE One", "play", logos+"rteone.png")
		addItem("RTE One +1", "play", logos+"rteoneplusone.png")
		addItem("RTE Two", "play", logos+"rtetwo.png")
		addItem("Spike TV", "resolve", logos+"spiketv.png")
		addItem("SyFy", "resolve", logos+"syfy.png")
		addItem("TBS", "resolve", logos+"tbs.png")
		addItem("TG4", "play", logos+"tg4.png")
		addItem("The CW", "resolve", logos+"thecw.png")
		addItem("truTV", "play", logos_tvp+"295.png")
		addItem("TV3", "play", logos+"tv3.png")
		addItem("USA Network", "resolve", logos+"usanetwork.png")
		addItem("UTV", "play", logos+"utv.png")
	elif category == "Kids":
		addItem("Cartoon Network", "resolve", logos+"cartoonnetwork.png")
		addItem("Nickelodeon", "resolve", logos+"nickelodeon.png")
		addItem("RTEjr", "play", logos+"rtejr.png")
	elif category == "Sports":
		addItem("ESPN", "resolve", logos+"espn.png")
		addItem("TNTUSA", "resolve", logos+"tntusa.png")
	elif category == "News/Parliament":
		addItem("ABC News", "play", logos+"abcnews.png")
		addItem("Bloomberg TV (EU)", "play", logos+"bloombergtv.png")
		addItem("Bloomberg TV (US)", "play", logos+"bloombergtv.png")
		addItem("Euronews", "play", logos+"euronews.png")
		addItem("FOX News", "resolve", logos+"foxnews.png")
		addItem("France24", "play", logos+"france24.png")
		addItem("Irish TV", "play", logos+"irishtv.png")
		addItem("Oireachtas TV", "play", logos+"oireachtastv.png")
		addItem("RTE News Now", "play", logos+"rtenewsnow.png")
		addItem("Sky News", "resolve", logos+"skynews.png")
	elif category == "Documentary":
		addItem("Animal Planet", "resolve", logos+"animalplanet.png")
		addItem("AMC", "resolve", logos+"amc.png")
		addItem("Discovery Channel", "resolve", logos+"discoverychannel.png")
		addItem("History Channel", "resolve", logos+"historychannel.png")
		addItem("National Geographic", "resolve", logos+"nationalgeographic.png")
		addItem("NASA ISS", "play", logos+"nasaiss.png")
		addItem("NASA TV", "play", logos+"nasatv.png")
	elif category == "Music":
		addItem("4Music", "play", logos_tvp+"128.png")
		addItem("The Box", "play", logos_tvp+"129.png")
		addItem("Box Hits", "play", logos+"boxhits.png")
		addItem("Box Upfront", "play", logos_tvp+"158.png")
		addItem("Capital TV", "play", logos_tvp+"157.png")
		addItem("Channel AKA", "play", logos_tvp+"227.png")
		addItem("Heart TV", "play", logos_tvp+"153.png")
		addItem("Kerrang!", "play", logos_tvp+"133.png")
		addItem("Kiss", "play", logos_tvp+"131.png")
		addItem("Magic", "play", logos_tvp+"132.png")
		addItem("NOW Music", "play", logos_tvp+"228.png")
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

def addItem(name, mode, logo):
	item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=logo)
	item.setProperty("fanart_image", fanart)
	item.setProperty("IsPlayable","true")
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0]+"?mode="+mode+"&c="+urllib.quote_plus(name), listitem=item, isFolder=False)

def addDir(category, logo):
	item = xbmcgui.ListItem(category, iconImage="DefaultFolder.png", thumbnailImage=logo)
	item.setProperty("fanart_image", fanart)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0]+"?mode=list&c="+urllib.quote_plus(category), listitem=item, isFolder=True)
	
# Try populate the Args
args = urlparse.parse_qs(sys.argv[2][1:])
try: mode = args.get('mode', None)
except: mode = None
try: c = args.get('c', None)
except: c = None

if mode is None:
	addDir("24/7 TV", "DefaultFolder.png")
	addDir("24/7 Movies", "DefaultFolder.png")
	addDir("Entertainment", "DefaultFolder.png")
	addDir("Kids", "DefaultFolder.png")
	addDir("Sports", "DefaultFolder.png")
	addDir("News/Parliament", "DefaultFolder.png")
	addDir("Documentary", "DefaultFolder.png")
	addDir("Music", "DefaultFolder.png")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode[0] == "list": ListStreams(urllib.unquote_plus(c[0]))
elif mode[0] == "play": xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=urllib.unquote_plus(Streams(c[0]))))
elif mode[0] == "resolve": xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=liveresolver.resolve(Streams(c[0]))))
elif mode[0] == "directplay": xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=liveresolver.resolve(Streams(c[0]))))