import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,base64
from resources.lib.modules import plugintools

addon_id            = 'plugin.video.echodocs'
AddonTitle          = '[COLOR yellowgreen]Echo Documentaries[/COLOR]'
fanarts             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
dp                  = xbmcgui.DialogProgress()
dialog              = xbmcgui.Dialog()

def GetMenu():

    addLink('[COLOR yellowgreen][B]Watch A Random Documentary[/B][/COLOR]',base64.b64decode(b'aHR0cHM6Ly9kb2N1bWVudGFyeXN0b3JtLmNvbS8/cmFuZG9t'),902,icon,fanarts,'Watch a random documentary!')
    addDir('Search....','url',998,icon,fanarts,'Search through all of our supported websites for a documentary of your choice!')
    addDir('[COLOR white]Crime Documentaries[/COLOR]',base64.b64decode(b'aHR0cDovL2NyaW1lZG9jdW1lbnRhcnkuY29t'),33,icon,fanarts,'')
    addDir('[COLOR white]Documentary Addicts[/COLOR]',base64.b64decode(b'aHR0cHM6Ly9kb2N1bWVudGFyeWFkZGljdC5jb20='),30,icon,fanarts,'Now part of 5,341 documentaries online and counting! Welcome to the largest and best curated collection of documentaries on the planet.')
    addDir('[COLOR white]Documentary Heaven[/COLOR]',base64.b64decode(b'aHR0cDovL2RvY3VtZW50YXJ5aGVhdmVuLmNvbQ=='),19,icon,fanarts,'DocumentaryHeaven.com personally will only collect visitor information when our commenting system is used. This includes a users  IP address and e-mail address via our commenting system. This is only used to help us improve our site, and to prevent abuse of our commenting system DocumentaryHeaven.com will under no circumstances disclose any information collected unless required to do so by law or court order. Our visitors privacy is paramount to us!')
    addDir('[COLOR white]Documentary Lovers[/COLOR]',base64.b64decode(b'aHR0cDovL2RvY3VtZW50YXJ5bG92ZXJzLmNvbQ=='),14,icon,fanarts,'We are a curated movie catalog bringing you the best and most intriguing documentaries free to watch online from any device. Our list consists of short and full-length films, educational talks and video previews that you can sort by topic to pique your curiosity.')
    addDir('[COLOR white]Documentaries Storm[/COLOR]',base64.b64decode(b'aHR0cHM6Ly9kb2N1bWVudGFyeXN0b3JtLmNvbQ=='),9,icon,fanarts,'Welcome to DocumentaryStorm, the leading source for 100% free documentary films. We curate the best documentary films available online for educational purposes as well as personal enjoyment.')
    addDir('[COLOR white]Documentary Tube[/COLOR]',base64.b64decode(b'aHR0cDovL3d3dy5kb2N1bWVudGFyeXR1YmUuY29t'),24,icon,fanarts,"We're committed to providing the best documentaries from around the World. With hundreds of free documentaries published and categorised every month, there's something for every taste.")   
    addDir('[COLOR white]Free Documentaries[/COLOR]',base64.b64decode(b'aHR0cHM6Ly9mcmVlZG9jdW1lbnRhcmllcy5vcmc='),6,icon,fanarts,'Freedocumentaries.org streams full-length documentary films free of charge, with no registration needed. For several films, we even offer the ability to watch trailers or to download the actual film.')
    addDir('[COLOR white]SnagFilms[/COLOR]',base64.b64decode(b'aHR0cDovL3d3dy5zbmFnZmlsbXMuY29tL21vdmllcy9kb2N1bWVudGFyeQ=='),17,icon,fanarts,'SnagFilms is like that cool local video store with unique indie films and exciting hidden movie treasures except everything can be watched online! For those of us looking to discover something different, SnagFilms has over 5,000 movies, TV show episodes, eye-opening documentaries and exclusive original comedy shorts. There is something to watch for everyone!')
    addDir('[COLOR white]Sports Documentaries[/COLOR]',base64.b64decode(b'aHR0cDovL3Nwb3J0c2RvY3VtZW50YXJpZXMuY29t'),28,icon,fanarts,"Find all of the latest sports documentaries streaming online for free. Every week we add more sports related documentary videos so that you can watch videos about your favourite players or sports. Part of our dedication to keeping up this video site is offering as many of the tv series specials as possible. Some of those include ESPN's E60, 30 for 30, A Football Life, and more.")
    addDir('[COLOR white]Top Documentaries[/COLOR]',base64.b64decode(b'aHR0cDovL3d3dy50b3Bkb2N1bWVudGFyeWZpbG1zLmNvbQ=='),1,icon,fanarts,'View a wide selection of documentaries from Top Documentaries!')

def Top_Documentaries_Main(name,url,iconimage):

    link = open_url(url)
    addDir('[COLOR white]Catagories[/COLOR]',base64.b64decode(b'aHR0cDovL3d3dy50b3Bkb2N1bWVudGFyeWZpbG1zLmNvbQ=='),5,icon,fanarts,'Browse through all the catagories on Top Documentaries!')
    url = re.compile('<a class="browse" href="(.+?)">.+?</a>').findall(link)[0]
    addDir('[COLOR white]Browse[/COLOR]',url,2,icon,fanarts,'Browse the documentaries on Top Documentaries!')
    url = re.compile('<a class="list" href="(.+?)">.+?</a>').findall(link)[0]
    addDir('[COLOR white]List[/COLOR]',url,4,icon,fanarts,'List the documentaries on Top Documentaries!')
    url = re.compile('<a class="top-100" href="(.+?)">.+?</a>').findall(link)[0]
    addDir('[COLOR white]Top 100[/COLOR]',url,3,icon,fanarts,'View the top 100 documentaries on Top Documentaries!')

def Top_Documentaries_Browse(name,url,iconimage):

    link=open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article class="module">(.+?)</article>',re.DOTALL).findall(link)

    for items in match:
        year=re.compile('<div class="meta-bar">(.+?)<').findall(items)[0]
        genre=re.compile('category tag">(.+?)</a>').findall(items)[0]
        url=re.compile('<h2><a href="(.+?)"').findall(items)[0]
        name=re.compile('title="(.+?)"').findall(items)[0]
        iconimage=re.compile('src="(.+?)"').findall(items)[0]
        desc=re.compile('<p>(.+?)</p>').findall(items)[0]
        rating=re.compile('</span>(.+?)</span>').findall(items)[-1]

        name = name.replace('&#039;',"'")
        year = year.replace(',','').replace(' ','')
        rating = rating.replace(' ','')
        year = year.rstrip()
        year = year.lstrip()

        addLink('[COLOR white]' + name + ' | Rating: [COLOR yellowgreen]' + rating + '[/COLOR] - Year: [COLOR yellowgreen]' + year +'[/COLOR][/COLOR]',url,900,iconimage,fanarts,desc)

    try:
        np=re.compile('<a href="([^"]*)">Next</a>').findall(link)[0]
        addDir('[COLOR yellowgreen][I]Next Page -->[/I][/COLOR]',np,2,icon,fanarts,'Visit the next page.....')
    except: pass

def Top_Documentaries_Top100(name,url,iconimage):

    link=open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<meta itemprop="name"(.+?)<\/span>').findall(link)

    for items in match:
        rank=re.compile('<meta.+?content="(.+?)"').findall(items)[0]
        name=re.compile('content="(.+?)"').findall(items)[0]
        url=re.compile('href="(.+?)"').findall(items)[0]
        iconimage=re.compile('src="(.+?)"').findall(items)[0]
        a = int(rank)
        addLink('[COLOR yellowgreen]Rank: ' + rank + '[/COLOR] | [COLOR white]' + name + '[/COLOR]',url,900,iconimage,fanarts,"")

    while a <100:
        a = a + 1
        addLink('[COLOR yellowgreen]Rank: ' + str(a) + '[/COLOR] | [COLOR white]Unavailable at this time[/COLOR]',url,999,icon,fanarts,"")

def Top_Documentaries_List(name,url,iconimage):

    link=open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="sitemap-wraper clear">(.+?)</div>').findall(link)

    for items in match:
        cat_name=re.compile('<a href=".+?">(.+?)</a>.+?</h2>').findall(items)[0]
        cat_url=re.compile('<a href="(.+?)">.+?</a>.+?</h2>').findall(items)[0]
        cat_num=re.compile('<a href=".+?">.+?</a>(.+?)</h2>').findall(items)[0]
        addDir('[COLOR yellowgreen]' + cat_name + ' [COLOR white]' + cat_num + '[/COLOR] | Click here for all ' + cat_name + '....[/COLOR]',cat_url,2,icon,fanarts,"")

        match2 = re.compile('<a(.+?)</a>').findall(items)
        for entrys in match2:
            try:
                name=re.compile('title="(.+?)"').findall(entrys)[0]
                url=re.compile('href="(.+?)"').findall(entrys)[0]
                iconimage=re.compile('src="(.+?)"').findall(entrys)[0]
                name = name.replace('&#039;',"'")
                addLink('[COLOR white]' + name + '[/COLOR]',url,900,iconimage,fanarts,"")
            except: pass

def Top_Documentaries_Cats(name,url,iconimage):

    link=open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="cat-wrap">(.+?)</div>').findall(link)[0]
    match2= re.compile('<li>(.+?)</li>').findall(match)
    for items in match2:
        name=re.compile('<a href=".+?" >(.+?)</a>').findall(items)[0]
        url=re.compile('<a href="(.+?)" >.+?</a>').findall(items)[0]
        addDir('[COLOR white]' + name + '[/COLOR]',url,2,icon,fanarts,"")
    
def Play_Top_Documentaries(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url)
    url=re.compile('<meta itemprop="embedUrl" content="(.+?)">').findall(link)[0]
    Play_Link(name,url,iconimage)

def Free_Documentaries_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,8,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="films-slider-section">(.+?)</h1>').findall(link)
    for item in match:
        name = re.compile('<h1>(.+?)<').findall(item)[0]
        url = re.compile('<a href="(.+?)">').findall(item)[0]
        url = 'https://freedocumentaries.org' + url
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,7,icon,fanarts,'')

def Free_Documentaries_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="film"(.+?)<\/a>').findall(link)
    for item in match:
        name = re.compile('<h5>(.+?)</h5>').findall(item)[0]
        url = re.compile('<a href="(.+?)">').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        year = re.compile('b&gt;(.+?)&lt').findall(item)[0]
        try:
            min = re.compile('/b&gt\;&lt\;/li&gt\;&lt\;li&gt\;&lt\;b&gt\;(.+?).&lt').findall(item)[0]
        except: min = "Unknown"
        desc = re.compile('<div class=popover-film-blurb>(.+?)</div>').findall(item)[0]
        url = 'https://freedocumentaries.org' + url
        iconimage = 'https://freedocumentaries.org' + iconimage

        name = Cleaner(name)

        addLink('[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Year: [COLOR yellowgreen]' + year + '[/COLOR][/COLOR]',url,901,iconimage,fanarts,desc)

def Search_Free_Documentaries():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []
    
    url = "https://freedocumentaries.org/search?q=" + term
    
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="film"(.+?)<\/a>').findall(link)
    for item in match:
        name = re.compile('<h5>(.+?)</h5>').findall(item)[0]
        url = re.compile('<a href="(.+?)">').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        year = re.compile('b&gt;(.+?)&lt').findall(item)[0]
        try:
            min = re.compile('/b&gt\;&lt\;/li&gt\;&lt\;li&gt\;&lt\;b&gt\;(.+?).&lt').findall(item)[0]
        except: min = "Unknown"
        desc = re.compile('<div class=popover-film-blurb>(.+?)</div>').findall(item)[0]
        url = 'https://freedocumentaries.org' + url
        iconimage = 'https://freedocumentaries.org' + iconimage

        name = Cleaner(name)

        name = '[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Year: [COLOR yellowgreen]' + year + '[/COLOR][/COLOR]'
        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("901")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)

def Play_Free_Documentaries(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    
    trailer = 1
    film = 1

    try:
        trailer_type=re.compile('<a href="#watch-trailer".+?data-type="(.+?)" data-code=".+?">').findall(link)[0]
        trailer_id=re.compile('<a href="#watch-trailer".+?data-type=".+?" data-code="(.+?)">').findall(link)[0]
        string = trailer_type + "|SPLIT|" + trailer_id
        trailer_url = Make_Link_Free_Docs(string)
    except: trailer = 0
    
    try:
        try:
            video_type=re.compile('<a href="#watch-film".+?data-type="(.+?)" data-code=".+?">').findall(link)[0]
            video_id=re.compile('<a href="#watch-film".+?data-type=".+?" data-code="(.+?)">').findall(link)[0]
            string = video_type + "|SPLIT|" + video_id
            video_url = Make_Link_Free_Docs(string)
        except:
            video_id=re.compile('<a href="#watch-film".+?data-code="(.+?)">').findall(link)[0]
            string = "NULL|SPLIT|" + video_id
            video_url = Make_Link_Free_Docs(string)
    except: film = 0
    
    if trailer == 1:
        choice = dialog.select("[COLOR yellowgreen]" + name + "[/COLOR]", ['[COLOR white]Watch Film[/COLOR]','[COLOR white]Watch Trailer[/COLOR]'])
        if choice == 0: Play_Link(name,video_url,iconimage)
        elif choice == 1: Play_Link(name,trailer_url,iconimage)
        else: 
            dp.close()
            quit()
    elif film == 1: Play_Link(name,video_url,iconimage)
    else: 
        dp.close()
        dialog.ok(AddonTitle, "Sorry we could not play this video. Please try another.")
        quit()

def Make_Link_Free_Docs(string):

    type,id = string.split("|SPLIT|")
    
    if type == "NULL":
        url = 'https://www.youtube.com/embed/' + id
    elif type == 'vimeo':
        url = 'https://player.vimeo.com/video/' + id
    elif type == 'youtube':
        url = 'https://www.youtube.com/embed/' + id
    elif type == 'dailymotion':
        url = 'https://www.dailymotion.com/video/' + id
    return url

def Documentary_Storm_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,8,icon,fanarts,"")
    addDir('[COLOR white]Catagories[/COLOR]',base64.b64decode(b'aHR0cHM6Ly9kb2N1bWVudGFyeXN0b3JtLmNvbQ=='),10,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<ul class="dropdown-menu">(.+?)</ul>',re.DOTALL).findall(link)[0]
    match2 = re.compile('<li>(.+?)</li>').findall(match)
    for item in match2:
        name = re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
        url = re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
        name = Cleaner(name)
        if "full-documentary-list" in url:
            addDir('[COLOR white]' + name + '[/COLOR]',url,12,icon,fanarts,'')
        elif "?random" in url:
            addLink('[COLOR white]' + name + '[/COLOR]',url,902,icon,fanarts,'')
        else:
            addDir('[COLOR white]' + name + '[/COLOR]',url,11,icon,fanarts,'')

def Documentary_Storm_Cats(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li class="cat-item cat-item-.+?">(.+?)</li>',re.DOTALL).findall(link)
    for item in match:
        each = re.compile('<a href="(.+?)" title="(.+?)">(.+?)</a>').findall(item)
        for url,desc,name in each:
            addDir('[COLOR white]' + name + '[/COLOR]',url,11,icon,fanarts,desc)

def Documentary_Storm_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="item">(.+?)Watch Now</a>',re.DOTALL).findall(link)
    for item in match:
        name = re.compile('<h1><a href=".+?">(.+?)</a></h1>').findall(item)[0]
        url = re.compile('<h1><a href="(.+?)">.+?</a></h1>').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            min = re.compile('<span class="runtime"><i.+?><\/i>(.+?)<\/span>').findall(item)[0]
        except: min = "Unknown"
        try:
            year = re.compile('<span class="release-date"><.+?><\/i>(.+?)<\/span>').findall(item)[0]
        except: year = "Unknown"
        try:
            rating = re.compile('<span class="rating-summary"><.+?<\/i>(.+?)<span').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)<\/p>').findall(item)[0]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Year: [COLOR yellowgreen]' + year + '[/COLOR] - Rating: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,902,iconimage,fanarts,desc)

    try:
       np = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">').findall(link)[0]
       addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,11,icon,fanarts,'Visit the next page.')
    except: pass

def Documentary_Storm_FullList(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="row">(.+?)</div>',re.DOTALL).findall(link)
    for item in match:
        try:
            name = re.compile('title="(.+?)"').findall(item)[0]
            url = re.compile('href="(.+?)"').findall(item)[0]
            name = Cleaner(name)
            addLink('[COLOR white]' + name + '[/COLOR]',url,902,icon,fanarts,"")
        except: pass

def Search_Documentary_Storm():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []

    url = "https://documentarystorm.com/?s=" + term
    
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="item">(.+?)Watch Now</a>',re.DOTALL).findall(link)
    for item in match:
        name = re.compile('<h1><a href=".+?">(.+?)</a></h1>').findall(item)[0]
        url = re.compile('<h1><a href="(.+?)">.+?</a></h1>').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            min = re.compile('<span class="runtime"><i.+?><\/i>(.+?)<\/span>').findall(item)[0]
        except: min = "Unknown"
        try:
            year = re.compile('<span class="release-date"><.+?><\/i>(.+?)<\/span>').findall(item)[0]
        except: year = "Unknown"
        try:
            rating = re.compile('<span class="rating-summary"><.+?<\/i>(.+?)<span').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)<\/p>').findall(item)[0]
        except: desc = "Unknown"
        name = Cleaner(name)
        name = '[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Year: [COLOR yellowgreen]' + year + '[/COLOR] - Rating: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]'
        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("902")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)
               
def Play_Documentary_Storm(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    
    if "?random" in url:
        try:
            name = re.compile('<meta property="og:title" content="(.+?)" />').findall(link)[0]
            iconimage = re.compile('<meta property="og:image" content="(.+?)" />').findall(link)[0]
            dp.update(0,'','[COLOR blue]Starting ' + name.title() + '[/COLOR]')
        except: pass

    try:
        url = re.compile('<meta itemprop="embedUrl" content="(.+?)"').findall(link)[0]
    except:
        try:
            url = re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
        except:
            dp.close()
            dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
            quit()
    Play_Link(name,url,iconimage)

def Documentary_Lovers_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,16,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('id="menu-item(.+?)/a>',re.DOTALL).findall(link)
    
    blacklist = ["genres","topics"]
    
    for item in match:
        try:
            name = re.compile('title=".+?" href=".+?">(.+?)<',re.DOTALL).findall(item)[0]
            url = re.compile('title=".+?" href="(.+?)">.+?<',re.DOTALL).findall(item)[0]
            if "/" in url:
                if name.lower() not in str(blacklist):
                    if not "http://" in url:
                        url = 'http://documentarylovers.com' + url
                    name = Cleaner(name)
                    addDir('[COLOR white]' + name + '[/COLOR]',url,15,icon,fanarts,'')
        except: pass
       
def Documentary_Lovers_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article(.+?)</article>',re.DOTALL).findall(link)
    
    if "top-films" in url:
        for item in match:
            name = re.compile('<h2>(.+?)</h2>').findall(item)[0]
            url = re.compile('href="(.+?)"').findall(item)[0]
            iconimage = re.compile('src="(.+?)"').findall(item)[0]
            try:
                rank = re.compile('top_number"><p>(.+?)</p>').findall(item)[0]
            except: rank = "Unknown"
            try:
                rating = re.compile('class="rate_avg">(.+?)</span>').findall(item)[0]
            except: rating = "Unknown"
            try:
                desc = re.compile('<p>(.+?)</p>').findall(item)[-1]
            except: desc = "Unknown"
            name = Cleaner(name)
            addLink('[COLOR yellowgreen]Rank: ' + rank + '[/COLOR][COLOR white] - ' + name + ' - Stars: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,903,iconimage,fanarts,desc)
    else:    
        for item in match:
            if "/film" in url:
                name = re.compile('title="(.+?)"').findall(item)[1]
                url = re.compile('href="(.+?)"').findall(item)[2]
            else: 
                name = re.compile('title="(.+?)"').findall(item)[0]
                url = re.compile('href="(.+?)"').findall(item)[0]
            iconimage = re.compile('src="(.+?)"').findall(item)[0]
            try:
                min = re.compile('class=\"ico dl_icon dl_time\"><\/i>(.+?)<\/span>').findall(item)[0]
            except: min = "Unknown"
            try:
                rating = re.compile('class=\"ico dl_icon dl_star_filled\"><\/i>(.+?)<\/span>').findall(item)[0]
            except: rating = "Unknown"
            try:
                desc = re.compile('class="description_text">(.+?)<\/div>').findall(item)[0]
            except: desc = "Unknown"
            name = Cleaner(name)
            addLink('[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Stars: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,903,iconimage,fanarts,desc)

    try:
        np = re.compile('rel="next" href="(.+?)"').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,15,icon,fanarts,'View documentaries from next page.')
    except: pass

def Search_Documentary_Lovers():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []
    
    url = 'http://documentarylovers.com/?s=' + term
        
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article(.+?)</article>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('title="(.+?)"').findall(item)[1]
        url = re.compile('href="(.+?)"').findall(item)[2]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            min = re.compile('class=\"ico dl_icon dl_time\"><\/i>(.+?)<\/span>').findall(item)[0]
        except: min = "Unknown"
        try:
            rating = re.compile('class=\"ico dl_icon dl_star_filled\"><\/i>(.+?)<\/span>').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('class="description_text">(.+?)<\/div>').findall(item)[0]
        except: desc = "Unknown"
        name = Cleaner(name)
        name = '[COLOR white]' + name + ' | Runtime: [COLOR yellowgreen]' + min + '[/COLOR] - Stars: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]'

        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("903")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)
              
def Play_Documentary_Lovers(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        id = re.compile('id="playVideo" data-video="youtube" data-src="(.+?)">').findall(link)[0]
        url = 'https://www.youtube.com/embed/' + id
    except:
        try:
            id = re.compile('itemprop="embedURL" content="https://www.youtube-nocookie.com/v/(.+?)">').findall(link)[0]
            url = 'https://www.youtube.com/embed/' + id
        except:
            try:
                id = re.compile('player.vimeo.com/video/(.+?)"').findall(link)[0]
                id = id.split("?")[0]
                url = 'https://player.vimeo.com/video/' + id
            except:
                try:
                    id = re.compile('id="playVideo" data-video="youtube-list" data-src="(.+?)">').findall(link)[0]
                    url = 'https://www.youtube.com/embed/videoseries?list=' + id
                except:
                    dp.close()
                    dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
                    quit()

    Play_Link(name,url,iconimage)

def SnagFilms_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,18,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="snag-slider-item(.+?)</button>',re.DOTALL).findall(link)
    
    for item in match:
        try:
            id = re.compile('data-film-id="(.+?)"',re.DOTALL).findall(item)[0]
            url = 'http://www.snagfilms.com/embed/player?filmId=' + id
            name = re.compile('data-title="(.+?)"',re.DOTALL).findall(item)[0]
            try:
                iconimage = re.compile('data-src="(.+?)"',re.DOTALL).findall(item)[0]
            except: 
                try:
                    iconimage = re.compile('src="(.+?)"',re.DOTALL).findall(item)[0]
                except: iconimage = icon
            try:
                desc = re.compile('data-description="(.+?)"',re.DOTALL).findall(item)[0]
            except: desc = "Unknown"
            try:
                year = re.compile('data-year="(.+?)"',re.DOTALL).findall(item)[0]
            except: year = "Unknown"

            name = Cleaner(name)
            
            if not '{' in year:
                addLink('[COLOR white]' + name + ' | Year: [COLOR yellowgreen]' + year + '[/COLOR][/COLOR]',url,904,iconimage,fanarts,desc)
        except: pass

def Search_SnagFilms():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","%20")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []

    url = 'http://www.snagfilms.com/apis/search.json?searchTerm=' + term
  
    link = open_url(url).replace('\n','').replace('\r','')
    json_data = plugintools.load_json(link)

    for entry in json_data['results']:

        if "id" in entry and entry['id'] is not None:
            id = entry['id']
        else:
            id = "No ID Found"

        if "title" in entry and entry['title'] is not None:
            name = entry['title']
        else:
            name = "No Title Found"

        if "imageUrl" in entry and entry['imageUrl'] is not None:
            iconimage = entry['imageUrl']
        else:
            iconimage = "No Image Found"
         
        if "description" in entry and entry['description'] is not None:
            desc = entry['description']
        else:
            desc = "Unknown"
            
        if "year" in entry and entry['year'] is not None:
            year = entry['year']
        else:
            year = "Unknown"
            
        url = 'http://www.snagfilms.com/embed/player?filmId=' + id
        
        name = '[COLOR white]' + str(name) + ' | Year: [COLOR yellowgreen]' + str(year) + '[/COLOR][/COLOR]'
        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("904")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)
               
def Play_SnagFilms(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        url = re.compile('filmInfo.+?src: "(.+?)\?.+?"').findall(link)[-1]
    except:
        dp.close()
        dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
        quit()

    Play_Link(name,url,iconimage)

def Documentary_Heaven_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,23,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li id="menu-item-.+?" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-.+?"><a href="(.+?)">(.+?)<\/a><\/li>',re.DOTALL).findall(link)
    
    blacklist = ["home","submit","contact"]
    
    for url,name in match:
        if name.lower() not in str(blacklist):
            name = Cleaner(name)
            if "watch-online" in url:
                addDir('[COLOR white]' + name + '[/COLOR]',url,21,icon,fanarts,'')
            elif "popular" in url:
                addDir('[COLOR white]' + name + '[/COLOR]',url,22,icon,fanarts,'')
            else:
                addDir('[COLOR white]' + name + '[/COLOR]',url,20,icon,fanarts,'')
       
def Documentary_Heaven_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article(.+?)</article>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('title="(.+?)"').findall(item)[0]
        url = re.compile('href="(.+?)"').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rating = re.compile('<i class="fa fa-star"></i>(.+?)</li>').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[-1]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR white]' + name + ' - Rating:[COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,905,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="next-btn"><a href="(.+?)" >NEXT PAGE</a>').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,20,icon,fanarts,'View documentaries from next page.')
    except: pass

def Documentary_Heaven_Browse_Cats(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<a href="([^"]*)" class="browse-all">Browse (.+?) Documentaries<\/a>',re.DOTALL).findall(link)
    
    for url,name in match:
        url = "http://documentaryheaven.com" + url
        addDir('[COLOR white]' + name + '[/COLOR]',url,20,icon,fanarts,'')

def Documentary_Heaven_Top100(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="doc">(.+?)</aside>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('title="(.+?)"').findall(item)[0]
        url = re.compile('<a href="(.+?)"').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rank = re.compile('<span>(.+?)</span>').findall(item)[0]
        except: rank = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[-1]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR yellowgreen]Rank: ' + rank + '[/COLOR] | [COLOR white]' + name + '[/COLOR]',url,905,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="next-btn"><a href="(.+?)" >NEXT PAGE</a>').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,20,icon,fanarts,'View documentaries from next page.')
    except: pass

def Search_Documentary_Heaven():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","%20")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []
    
    url = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=581c068e7ad56cae00e4e2e8f7dc3837&cx=partner-pub-8793303567743140:2816297709&q=" + term + "&googlehost=www.google.com&callback=google.search.Search.apiary14769&nocache=1489702476518"
    link = open_url(url)
    
    match = re.compile('{"GsearchResultClass":(.+?)}}}',re.DOTALL).findall(link)
    
    for items in match:
    
        url = re.compile('"unescapedUrl":"(.+?)"').findall(items)[0]
        name = re.compile('"titleNoFormatting":"(.+?)"').findall(items)[0]
        iconimage = re.compile('"src":"(.+?)"').findall(items)[0]
        desc = re.compile('"contentNoFormatting":"(.+?)"').findall(items)[0]
        desc = desc.replace("\\n","")
        
        if len(desc) < 2:
            desc = "Unknown"
        try:
            rating = re.compile('"average":"(.+?)"').findall(items)[0]
        except: rating = "Unknown"
        
        try:
            check_rating = float(rating)
            if check_rating < 0.01:
                rating = "Unknown"
        except: rating = "Unknown"
        name = name.replace(" | Documentary Heaven","")
        
        if not "category" in url:
            name = '[COLOR white]' + str(name) + ' | Rating: [COLOR yellowgreen]' + str(rating) + '[/COLOR][/COLOR]'
            namelist.append(name)
            urllist.append(url)
            iconlist.append(iconimage)
            desclist.append(desc)
            modelist.append("905")
            combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)

def Play_Documentary_Heaven(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        url = re.compile('iframe.+?src="(.+?)"',re.IGNORECASE).findall(link)[0]
        if not "http" in url:
            url = 'http:' + url
    except:
        try:
            id = re.compile('itemprop="embedURL" content="https://www.youtube-nocookie.com/v/(.+?)">').findall(link)[0]
            url = 'https://www.youtube.com/embed/' + id
        except:
            try:
                id = re.compile('player.vimeo.com/video/(.+?)"').findall(link)[0]
                id = id.split("?")[0]
                url = 'https://player.vimeo.com/video/' + id
            except:
                try:
                    id = re.compile('id="playVideo" data-video="youtube-list" data-src="(.+?)">').findall(link)[0]
                    url = 'https://www.youtube.com/embed/videoseries?list=' + id
                except:
                    dp.close()
                    dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
                    quit()

    Play_Link(name,url,iconimage)

def Documentary_Tube_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,27,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li class="active">(.+?)<li class="ml20 login-btn">',re.DOTALL).findall(link)[0]
    match2 = re.compile('<li>(.+?)</li>').findall(match)
    blacklist = ["home","articles","suggest"]
    
    for items in match2:
        name = re.compile('<a href=".+?">(.+?)</a>').findall(items)[0]
        url = re.compile('<a href="(.+?)">.+?</a>').findall(items)[0]
        if name.lower() not in str(blacklist):
            name = Cleaner(name)
            addDir('[COLOR white]' + name + '[/COLOR]',url,25,icon,fanarts,'')
     
    match = re.compile('<div class="panel-body alt categories">(.+?)<div class="panel-title alt">',re.DOTALL).findall(link)[0]
    match2 = re.compile('<a(.+?)</a>').findall(match)

    for items in match2:
        name = re.compile('href=".+?" title="(.+?)">').findall(items)[0]
        url = re.compile('href="(.+?)" title=".+?">').findall(items)[0]
        url = 'http://www.documentarytube.com' + url
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,25,icon,fanarts,'')
       
def Documentary_Tube_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div data-key(.+?)</ul></div>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<div class="box-title"><a href=".+?">(.+?)</a>').findall(item)[0]
        url = re.compile('<div class="box-title"><a href="(.+?)">').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rating = re.compile('<li class="star">(.+?)<').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[-1]
        except: desc = "Unknown"
        try:
            time = re.compile('<div class="timestamp">(.+?)</div>').findall(item)[0]
        except: time = "Unknown"
        try:
            upload = re.compile('<li class="ago"><span class="fa fa-history"></span>(.+?)</li>').findall(item)[-1]
        except: upload = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR white]' + name + ' [COLOR yellowgreen](' + upload + ')[/COLOR] -  | Runtime: [COLOR yellowgreen]' + time + '[/COLOR] Rating: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,906,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="next"><a href="(.+?)"').findall(link)[0]
        np = 'http://www.documentarytube.com' + np
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,25,icon,fanarts,'View documentaries from next page.')
    except: pass

def Documentary_Tube_Top100(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="doc">(.+?)</aside>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('title="(.+?)"').findall(item)[0]
        url = re.compile('<a href="(.+?)"').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rank = re.compile('<span>(.+?)</span>').findall(item)[0]
        except: rank = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[-1]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR yellowgreen]Rank: ' + rank + '[/COLOR] | [COLOR white]' + name + '[/COLOR]',url,905,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="next-btn"><a href="(.+?)" >NEXT PAGE</a>').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,20,icon,fanarts,'View documentaries from next page.')
    except: pass

def Search_Documentary_Tube(url):

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","%20")
        else: quit()
    else: quit()

    url =  'https://www.googleapis.com//customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=581c068e7ad56cae00e4e2e8f7dc3837&cx=006999953522606869358:s0xahe54lum&q=' + term + '&sort=&googlehost=www.google.com&callback=google.search.Search.apiary11755&nocache=1489760342424'

    link = open_url(url)
    
    match = re.compile('{"GsearchResultClass":(.+?)}}}',re.DOTALL).findall(link)
        
    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []
    
    for items in match:
    
        url = re.compile('"unescapedUrl":"(.+?)"').findall(items)[0]
        name = re.compile('"titleNoFormatting":"(.+?)"').findall(items)[0]
        iconimage = re.compile('"src":"(.+?)"').findall(items)[0]
        desc = re.compile('"contentNoFormatting":"(.+?)"').findall(items)[0]
        desc = desc.replace("\\n","")
        
        if len(desc) < 2:
            desc = "Unknown"

        name = name.replace(" | DocumentaryTube","")
        
        if "videos/" in url:
            name = '[COLOR white]' + str(name) + '[/COLOR]'
            namelist.append(name)
            urllist.append(url)
            iconlist.append(iconimage)
            desclist.append(desc)
            modelist.append("906")
            combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)

def Play_Documentary_Tube(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        url = re.compile('<iframe class="vimeo" src="(.+?)"').findall(link)[0]
        url = url.split("?")[0]
    except:
        try:
            id = re.compile('data-vidid="(.+?)"').findall(link)[0]
            player = re.compile('<div class="end-screen-(.+?)">').findall(link)[0]

            if player == "dailymo":
                url = 'https://www.dailymotion.com/video/' + id
            elif player == "youtube":
                url = 'https://www.youtube.com/embed/' + id
            else:
                dp.close()
                dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
                quit()
        except:
            dp.close()
            dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
            quit()

    Play_Link(name,url,iconimage)

def Sports_Documentaries_Main(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li style="text-align: left;">(.+?)</li>').findall(link)
    
    for items in match:
        name = re.compile('<a href=".+?">(.+?)</a>').findall(items)[0]
        url = re.compile('<a href="(.+?)">.+?</a>').findall(items)[0]
        url = "http://sportsdocumentaries.com/" + url
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,29,icon,fanarts,'')

def Sports_Documentaries_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<h4>(.+?)/p>',re.DOTALL).findall(link)
    
    for item in match:
        try:
            name = re.compile('<a href=".+?">(.+?)->').findall(item)[0]
        except: name = re.compile('<a href=".+?">(.+?)<').findall(item)[0]
        url = re.compile('<a href="(.+?)">').findall(item)[0]
        url = "http://sportsdocumentaries.com/" + url
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        iconimage = "http://sportsdocumentaries.com/" + iconimage
        try:
            desc = re.compile('<p>(.+?)<').findall(item)[-1]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR white]' + name + '[/COLOR]',url,907,iconimage,fanarts,desc)

def Play_Sports_Documentaries(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        url = re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
    except:
        dp.close()
        dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
        quit()

    Play_Link(name,url,iconimage)

def Documentary_Addicts_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,32,icon,fanarts,"")
    addDir('[COLOR white]Show 8 Random Documentaries[/COLOR]',base64.b64decode(b'aHR0cHM6Ly9kb2N1bWVudGFyeWFkZGljdC5jb20vZmlsbXMvcmFuZG9t'),31,icon,fanarts,"")
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li class="">(.+?)</li>',re.DOTALL).findall(link)
    
    for items in match:
        name = re.compile('<spa.+?>(.+?)</span>').findall(items)[0]
        url = re.compile('href="(.+?)">').findall(items)[0]
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,31,icon,fanarts,'')

def Documentary_Addicts_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="col-xs-12 col-sm-6 col-md-3 widget-film">(.+?)</div></div>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<a title="(.+?)" href=".+?">').findall(item)[0]
        url = re.compile('<a title=".+?" href="(.+?)">').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rating = re.compile('<i class=".+?">(.+?)</i>').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[0]
        except: desc = "Unknown"
        name = Cleaner(name)
        addLink('[COLOR white]' + name + ' | Rating: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]',url,908,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="next"><a href="(.+?)"').findall(link)[0]
        np = 'http://www.documentarytube.com' + np
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,25,icon,fanarts,'View documentaries from next page.')
    except: pass

def Search_Documentary_Addicts(url):

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []

    url = "https://documentaryaddict.com/films?utf8=&q%5BC_Name_cont%5D=" + term
    
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<div class="col-xs-12 col-sm-6 col-md-3 widget-film">(.+?)</div></div>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<a title="(.+?)" href=".+?">').findall(item)[0]
        url = re.compile('<a title=".+?" href="(.+?)">').findall(item)[0]
        iconimage = re.compile('src="(.+?)"').findall(item)[0]
        try:
            rating = re.compile('<i class=".+?">(.+?)</i>').findall(item)[0]
        except: rating = "Unknown"
        try:
            desc = re.compile('<p>(.+?)</p>').findall(item)[0]
        except: desc = "Unknown"
        name = Cleaner(name)
        name = '[COLOR white]' + name + ' | Rating: [COLOR yellowgreen]' + rating + '[/COLOR][/COLOR]'
        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("908")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
               addLink(name,url,int(mode),iconimage,fanarts,desc)

def Play_Documentary_Addicts(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    link = open_url(url).replace('\n','').replace('\r','')
    try:
        url = re.compile('<iframe.+?src="(.+?)"').findall(link)[-1]
    except:
        dp.close()
        dialog.ok(AddonTitle, "Sorry, we could not play this documentary. Please try another.")
        quit()

    Play_Link(name,url,iconimage)

def Crime_Documentaries_Main(name,url,iconimage):

    addDir('[COLOR yellowgreen]Search...[/COLOR]',url,39,icon,fanarts,"")
    addDir('[COLOR white]Featured Documentary[/COLOR]',url,34,icon,fanarts,"")
    addDir('[COLOR white]Popular This Week[/COLOR]',base64.b64decode(b'aHR0cDovL2NyaW1lZG9jdW1lbnRhcnkuY29tL3dwLWFkbWluL2FkbWluLWFqYXgucGhwP2FjdGlvbj13cHBfZ2V0X3BvcHVsYXImaWQ9Mw=='),34,icon,fanarts,"")
    addDir('[COLOR white]Popular All Time[/COLOR]',base64.b64decode(b'aHR0cDovL2NyaW1lZG9jdW1lbnRhcnkuY29tL3dwLWFkbWluL2FkbWluLWFqYXgucGhwP2FjdGlvbj13cHBfZ2V0X3BvcHVsYXImaWQ9NA=='),34,icon,fanarts,"")
    addDir('[COLOR white]Browse All[/COLOR]',base64.b64decode(b'aHR0cDovL2NyaW1lZG9jdW1lbnRhcnkuY29tL2Jyb3dzZS1hbGw='),36,icon,fanarts,"")
    addDir('[COLOR white]Categories[/COLOR]',url,34,icon,fanarts,"")
    addDir('[COLOR white]Shows[/COLOR]',url,35,icon,fanarts,"")

def Crime_Documentaries_Categories(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    
    if "Featured Documentary" in name:
        match = re.compile('<h2 class="g1-delta g1-delta-2nd widgettitle">Featured Documentary</h2>(.+?)</div>').findall(link)[0]
        url = re.compile('href="(.+?)"').findall(match)[0]
        Crime_Documentaries_List_Eps(name,url,iconimage)

    elif "Popular" in name:
        match = re.compile('<li>(.+?)</li>').findall(link)
        
        for item in match:
            name = re.compile('title="(.+?)"').findall(item)[0]
            url = re.compile('href="(.+?)"').findall(item)[0]
            iconimage = re.compile('src="(.+?)"').findall(item)[0]
            name = Cleaner(name)
            addDir('[COLOR white]' + name + '[/COLOR]',url,38,iconimage,fanarts,"")

    else:
        match = re.compile('<li class="cat-item cat-item(.+?)</li>').findall(link)
        
        for item in match:
            name = re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
            url = re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
            name = Cleaner(name)
            addDir('[COLOR white]' + name + '[/COLOR]',url,37,iconimage,fanarts,"")

def Crime_Documentaries_Shows(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<li class="cat-item">(.+?)</li>').findall(link)
    
    for item in match:
        name = re.compile('<a href=".+?">(.+?)</a>').findall(item)[0]
        url = re.compile('<a href="(.+?)">.+?</a>').findall(item)[0]
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,37,iconimage,fanarts,"")

def Crime_Documentaries_BrowseAll(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article class=(.+?)</article>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<a href=".+?" target="_self">(.+?)</a>').findall(item)[0]
        url = re.compile('<a href="(.+?)" target="_self">.+?</a>').findall(item)[0]
        iconimage = re.compile('url\((.+?)\)').findall(item)[0]
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,38,iconimage,fanarts,'')

def Crime_Documentaries_Browse(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article class="(.+?)</article>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<a href=".+?" title="(.+?)" >.+?</a>').findall(item)[0]
        url = re.compile('itemprop="headline"><a href="(.+?)"').findall(item)[0]
        iconimage = re.compile('data-src="(.+?)"').findall(item)[0]
        desc = re.compile('<p>(.+?)</p>').findall(item)[0]
        name = Cleaner(name)
        addDir('[COLOR white]' + name + '[/COLOR]',url,38,iconimage,fanarts,desc)

    try:
        np = re.compile('<li class="g1-pagination-item-next"><a href="(.+?)">Next</a>').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,37,icon,fanarts,'View documentaries from next page.')
    except: pass
    
def Crime_Documentaries_List_Eps(name,url,iconimage):

    link = open_url(url).replace('\n','').replace('\r','')
    
    got = 0
        
    try:
        match = re.compile('<div id="g1-divider-(.+?)</center>',re.DOTALL).findall(link)
        
        for item in match:
            name = re.compile('<h4 align="center">(.+?)</h4>').findall(item)[0]
            url = re.compile('<iframe.+?src="(.+?)"').findall(item)[0]
            imdb = re.compile('<a class="g1-quote-source-text".+?>(.+?)</a>').findall(item)[0]
            desc = re.compile('<blockquote><p>(.+?)</p>').findall(item)[0]
            name = Cleaner(name)
            got = 1
            if not "imdb" in imdb:
                addLink('[COLOR white]' + name + '[/COLOR]',url,909,iconimage,fanarts,desc)
            else:
                addLink('[COLOR white]' + name + ' - [/COLOR][COLOR yellowgreen]' + imdb + '[/COLOR]',url,909,iconimage,fanarts,desc)
    except: pass
    
    if got == 0:
        match = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(link)[0]
        Play_Crime_Documentaries(name,match,iconimage)
        quit()

    try:
        np = re.compile('<li class="g1-pagination-item-next"><a href="(.+?)">Next</a>').findall(link)[0]
        addDir('[COLOR yellowgreen]Next Page -->[/COLOR]',np,37,icon,fanarts,'View documentaries from next page.')
    except: pass

def Search_Crime_Documentaries(url):

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    namelist      = []
    urllist       = []
    iconlist      = []
    desclist      = []
    modelist      = []
    combinedlists = []

    url = 'http://crimedocumentary.com/?s=' + term + '&limit=12'
    
    link = open_url(url).replace('\n','').replace('\r','')
    match = re.compile('<article class="(.+?)</article>',re.DOTALL).findall(link)
    
    for item in match:
        name = re.compile('<a href=".+?" title="(.+?)" >.+?</a>').findall(item)[0]
        url = re.compile('itemprop="headline"><a href="(.+?)"').findall(item)[0]
        iconimage = re.compile('data-src="(.+?)"').findall(item)[0]
        desc = re.compile('<p>(.+?)</p>').findall(item)[0]

        name = Cleaner(name)
        name = '[COLOR white]' + name + '[/COLOR]'
        namelist.append(name)
        urllist.append(url)
        iconlist.append(iconimage)
        desclist.append(desc)
        modelist.append("38")
        combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                addDir(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
                addDir(name,url,int(mode),iconimage,fanarts,desc)

def Play_Crime_Documentaries(name,url,iconimage):

    dp.create(AddonTitle, "Getting playable link.............","Please wait....")
    Play_Link(name,url,iconimage)

def Multi_Search():

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Search Term')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            term = string.lower()
            term = term.replace(" ","+")
        else: quit()
    else: quit()

    current = 0
    totalsites = 8

    dp.create(AddonTitle, '[COLOR white]Searching for ' + string.title())
    dp.update(0)

    namelist     = []
    urllist      = []
    iconlist     = []
    desclist     = []
    modelist     = []
    combinedlists= []

    current = current + 1
    progress = 100 * int(current)/int(totalsites)
    dp.update(progress, '','[COLOR yellowgreen]Currently searching Free Documentaries...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

    url = "https://freedocumentaries.org/search?q=" + term
    
    try:
        link = open_url_search(url).replace('\n','').replace('\r','')
        match = re.compile('<div class="film"(.+?)<\/a>').findall(link)
        for item in match:
            name = re.compile('<h5>(.+?)</h5>').findall(item)[0]
            url = re.compile('<a href="(.+?)">').findall(item)[0]
            iconimage = re.compile('src="(.+?)"').findall(item)[0]
            year = re.compile('b&gt;(.+?)&lt').findall(item)[0]
            try:
                min = re.compile('/b&gt\;&lt\;/li&gt\;&lt\;li&gt\;&lt\;b&gt\;(.+?).&lt').findall(item)[0]
            except: min = "Unknown"
            desc = re.compile('<div class=popover-film-blurb>(.+?)</div>').findall(item)[0]
            url = 'https://freedocumentaries.org' + url
            iconimage = 'https://freedocumentaries.org' + iconimage

            name = Cleaner(name)
            
            name = '[COLOR white]' + name + ' - Year: ' + year + ' | [COLOR yellowgreen]Source: Free Documentaries[/COLOR]'
            namelist.append(name)
            urllist.append(url)
            iconlist.append(iconimage)
            desclist.append(desc)
            modelist.append("901")
            combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
    except: pass
 
    if not dp.iscanceled(): 

        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Documentary Storm...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')
    
        try:
            url = "https://documentarystorm.com/?s=" + term
            
            link = open_url_search(url).replace('\n','').replace('\r','')
            match = re.compile('<div class="item">(.+?)Watch Now</a>',re.DOTALL).findall(link)
            for item in match:
                name = re.compile('<h1><a href=".+?">(.+?)</a></h1>').findall(item)[0]
                url = re.compile('<h1><a href="(.+?)">.+?</a></h1>').findall(item)[0]
                iconimage = re.compile('src="(.+?)"').findall(item)[0]
                try:
                    min = re.compile('<span class="runtime"><i.+?><\/i>(.+?)<\/span>').findall(item)[0]
                except: min = "Unknown"
                try:
                    year = re.compile('<span class="release-date"><.+?><\/i>(.+?)<\/span>').findall(item)[0]
                except: year = "Unknown"
                try:
                    rating = re.compile('<span class="rating-summary"><.+?<\/i>(.+?)<span').findall(item)[0]
                except: rating = "Unknown"
                try:
                    desc = re.compile('<p>(.+?)<\/p>').findall(item)[0]
                except: desc = "Unknown"
                
                name = Cleaner(name)
                name = '[COLOR white]' + name + ' - Year: ' + year + ' | [COLOR yellowgreen]Source: Documentary Storm[/COLOR]'
                
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                desclist.append(desc)
                modelist.append("902")   
                combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass
        
    if not dp.iscanceled(): 

        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Documentary Lovers...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        url = 'http://documentarylovers.com/?s=' + term
                
        try:
            link = open_url_search(url).replace('\n','').replace('\r','')
            match = re.compile('<article(.+?)</article>',re.DOTALL).findall(link)
            
            for item in match:
                name = re.compile('title="(.+?)"').findall(item)[1]
                url = re.compile('href="(.+?)"').findall(item)[2]
                iconimage = re.compile('src="(.+?)"').findall(item)[0]
                try:
                    min = re.compile('class=\"ico dl_icon dl_time\"><\/i>(.+?)<\/span>').findall(item)[0]
                except: min = "Unknown"
                try:
                    rating = re.compile('class=\"ico dl_icon dl_star_filled\"><\/i>(.+?)<\/span>').findall(item)[0]
                except: rating = "Unknown"
                try:
                    desc = re.compile('class="description_text">(.+?)<\/div>').findall(item)[0]
                except: desc = "Unknown"
                
                name = Cleaner(name)
                name = '[COLOR white]' + name + ' - Year: Unknown | [COLOR yellowgreen]Source: Documentary Lovers[/COLOR]'
                
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                desclist.append(desc)
                modelist.append("903")
                combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass

    if not dp.iscanceled(): 

        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Snag Films...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        try:
            term_snag = term.replace("+","%20")
            url = 'http://www.snagfilms.com/apis/search.json?searchTerm=' + term_snag
          
            link = open_url_search(url).replace('\n','').replace('\r','')

            json_data = plugintools.load_json(link)

            for entry in json_data['results']:

                if "id" in entry and entry['id'] is not None:
                    id = entry['id']
                else:
                    id = "No ID Found"

                if "title" in entry and entry['title'] is not None:
                    name = entry['title']
                else:
                    name = "No Title Found"

                if "imageUrl" in entry and entry['imageUrl'] is not None:
                    iconimage = entry['imageUrl']
                else:
                    iconimage = "No Image Found"
                 
                if "description" in entry and entry['description'] is not None:
                    desc = entry['description']
                else:
                    desc = "Unknown"
                    
                if "year" in entry and entry['year'] is not None:
                    year = entry['year']
                else:
                    year = "Unknown"
                    
                url = 'http://www.snagfilms.com/embed/player?filmId=' + id
                
                name = Cleaner(name)
                name = '[COLOR white]' + name + ' - Year: ' + str(year) + ' | [COLOR yellowgreen]Source: SnagFilms[/COLOR]'
                
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                desclist.append(desc)
                modelist.append("904")
                combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass
    
    if not dp.iscanceled(): 
        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Documentary Heaven...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        term_docheaven = term.replace("+","%20")
        url = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=581c068e7ad56cae00e4e2e8f7dc3837&cx=partner-pub-8793303567743140:2816297709&q=" + term_docheaven + "&googlehost=www.google.com&callback=google.search.Search.apiary14769&nocache=1489702476518"

        try:
            link = open_url_search(url)
            
            match = re.compile('{"GsearchResultClass":(.+?)}}}',re.DOTALL).findall(link)
            
            for items in match:
            
                url = re.compile('"unescapedUrl":"(.+?)"').findall(items)[0]
                name = re.compile('"titleNoFormatting":"(.+?)"').findall(items)[0]
                iconimage = re.compile('"src":"(.+?)"').findall(items)[0]
                desc = re.compile('"contentNoFormatting":"(.+?)"').findall(items)[0]
                desc = desc.replace("\\n","")
                
                if len(desc) < 2:
                    desc = "Unknown"
                try:
                    rating = re.compile('"average":"(.+?)"').findall(items)[0]
                except: rating = "Unknown"
                
                try:
                    check_rating = float(rating)
                    if check_rating < 0.01:
                        rating = "Unknown"
                except: rating = "Unknown"
                name = name.replace(" | Documentary Heaven","")
                
                if not "category" in url:
                    name = '[COLOR white]' + name + ' - Rating: ' + str(rating) + ' | [COLOR yellowgreen]Source: Documentary Heaven[/COLOR]'

                    namelist.append(name)
                    urllist.append(url)
                    iconlist.append(iconimage)
                    desclist.append(desc)
                    modelist.append("905")
                    combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass
 
    if not dp.iscanceled(): 
        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Documentary Tube...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        term_doctube = term.replace("+","%20")
        url =  'https://www.googleapis.com//customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=581c068e7ad56cae00e4e2e8f7dc3837&cx=006999953522606869358:s0xahe54lum&q=' + term_doctube + '&sort=&googlehost=www.google.com&callback=google.search.Search.apiary11755&nocache=1489760342424'
 
        try:
            link = open_url_search(url)
            match = re.compile('{"GsearchResultClass":(.+?)}}}',re.DOTALL).findall(link)
                
            for items in match:
            
                url = re.compile('"unescapedUrl":"(.+?)"').findall(items)[0]
                name = re.compile('"titleNoFormatting":"(.+?)"').findall(items)[0]
                iconimage = re.compile('"src":"(.+?)"').findall(items)[0]
                desc = re.compile('"contentNoFormatting":"(.+?)"').findall(items)[0]
                desc = desc.replace("\\n","")
                
                if len(desc) < 2:
                    desc = "Unknown"

                name = name.replace(" | DocumentaryTube","")
                
                if "videos/" in url:
                    name = '[COLOR white]' + name + ' | [COLOR yellowgreen]Source: Documentary Tube[/COLOR]'

                    namelist.append(name)
                    urllist.append(url)
                    iconlist.append(iconimage)
                    desclist.append(desc)
                    modelist.append("906")
                    combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass
        
    if not dp.iscanceled(): 
        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Documentary Addicts...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        url = "https://documentaryaddict.com/films?utf8=&q%5BC_Name_cont%5D=" + term
        
        link = open_url(url).replace('\n','').replace('\r','')
        match = re.compile('<div class="col-xs-12 col-sm-6 col-md-3 widget-film">(.+?)</div></div>',re.DOTALL).findall(link)
        
        try:
            for item in match:
                name = re.compile('<a title="(.+?)" href=".+?">').findall(item)[0]
                url = re.compile('<a title=".+?" href="(.+?)">').findall(item)[0]
                iconimage = re.compile('src="(.+?)"').findall(item)[0]
                try:
                    rating = re.compile('<i class=".+?">(.+?)</i>').findall(item)[0]
                except: rating = "Unknown"
                try:
                    desc = re.compile('<p>(.+?)</p>').findall(item)[0]
                except: desc = "Unknown"
                name = Cleaner(name)
                name = '[COLOR white]' + name + ' - Rating: ' + str(rating) + ' | [COLOR yellowgreen]Source: Documentary Addicts[/COLOR]'
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                desclist.append(desc)
                modelist.append("908")
                combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass

    if not dp.iscanceled(): 
        current = current + 1
        progress = 100 * int(current)/int(totalsites)
        dp.update(progress, '','[COLOR yellowgreen]Currently searching Crime Documentaries...','[COLOR blue]Site number ' + str(current) + ' of ' + str(totalsites) + '[/COLOR]')

        try:
            url = 'http://crimedocumentary.com/?s=' + term + '&limit=12'
            
            link = open_url(url).replace('\n','').replace('\r','')
            match = re.compile('<article class="(.+?)</article>',re.DOTALL).findall(link)
            
            for item in match:
                name = re.compile('<a href=".+?" title="(.+?)" >.+?</a>').findall(item)[0]
                url = re.compile('itemprop="headline"><a href="(.+?)"').findall(item)[0]
                iconimage = re.compile('data-src="(.+?)"').findall(item)[0]
                desc = re.compile('<p>(.+?)</p>').findall(item)[0]

                name = Cleaner(name)
                name = '[COLOR white]' + name + '[/COLOR] | [COLOR yellowgreen]Source: Crime Documentaries[/COLOR]'
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                desclist.append(desc)
                modelist.append("38")
                combinedlists = list(zip(namelist,urllist,iconlist,desclist,modelist))
        except: pass

    dp.update(progress, '','[COLOR yellowgreen]Filtering results...','[COLOR blue]Please wait...[/COLOR]')

    finalnamelist       = []
    finalurllist        = []
    finaliconlist       = []
    finaldesclist       = []
    finalmodelist       = []
    finalcombinedlists  = []

    for name,url,iconimage,desc,mode in sorted(combinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:    
                finalnamelist.append(name)
                finalurllist.append(url)
                finaliconlist.append(iconimage)
                finaldesclist.append(desc)
                finalmodelist.append(str(mode))
                finalcombinedlists = list(zip(finalnamelist,finalurllist,finaliconlist,finaldesclist,finalmodelist))
        else:
            if string.lower() in name.lower():
                finalnamelist.append(name)
                finalurllist.append(url)
                finaliconlist.append(iconimage)
                finaldesclist.append(desc)
                finalmodelist.append(str(mode))
                finalcombinedlists = list(zip(finalnamelist,finalurllist,finaliconlist,finaldesclist,finalmodelist))   
                
    results = len(finalcombinedlists)

    addLink("[COLOR yellowgreen][B]" + str(results) + " results found for " + string.title() + "[/B][/COLOR]",'url',999,icon,fanarts,'')
    addLink("[COLOR white]-----------------------------------------------------[/COLOR]",'url',999,icon,fanarts,'')

    for name,url,iconimage,desc,mode in sorted(finalcombinedlists):
        if " " in string:
            checks = string.split(" ")
            notfound = 0
            for check in checks:
                if not check.lower() in name.lower():
                    notfound = 1
            if notfound == 0:
                if mode == "38":
                    addDir(name,url,int(mode),iconimage,fanarts,desc)
                else:
                    addLink(name,url,int(mode),iconimage,fanarts,desc)
        else:
            if string.lower() in name.lower():
                if mode == "38":
                    addDir(name,url,int(mode),iconimage,fanarts,desc)
                else:
                    addLink(name,url,int(mode),iconimage,fanarts,desc)
    
    dp.close()
    
def Cleaner(string):

    string = string.lstrip()
    string = string.rstrip()
    string = string.replace('<p>',"")
    string = string.replace('</p>',"")
    string = string.replace('&#8211;',"-")
    string = string.replace('&#8212;',"'")
    string = string.replace('&#8221;',"")
    string = string.replace('&#8220;',"")
    string = string.replace('&#8217;',"'")
    string = string.replace('&#039;',"'")
    string = string.replace('&#038;',"&")
    string = string.replace('&amp;','&')
    string = string.replace('&quot;','"')
    string = string.replace('&#x27;',"'")
    string = string.replace('&#39;',"'")

    return string

def Play_Link(name,url,iconimage):

    import urlresolver
    if urlresolver.HostedMediaFile(url).valid_url(): 
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        liz = xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage)
        liz.setPath(stream_url)
        dp.close()
        xbmc.Player ().play(stream_url, liz, False)
    else:
        stream_url=url
        liz = xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage)
        liz.setPath(stream_url)
        dp.close()
        xbmc.Player ().play(stream_url, liz, False)

def open_url(url):

    req = urllib2.Request(url)
    if not "&Referer" in url:
        req.add_header('Referer', 'https://www.google.com/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
    response = urllib2.urlopen(req, timeout = 15)
    link=response.read()
    response.close()
    return link
    
def open_url_search(url):

    req = urllib2.Request(url)
    if not "&Referer" in url:
        req.add_header('Referer', 'https://www.google.com/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
    response = urllib2.urlopen(req, timeout = 4)
    link=response.read()
    response.close()
    return link
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]                    
        return param
    
def addDir(name,url,mode,iconimage,fanart,description):

    description = '[COLOR yellowgreen]' + description + '[/COLOR]'
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description):

    description = Cleaner(description)
    description = '[COLOR yellowgreen]' + description + '[/COLOR]'
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None; fanart=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()
elif mode==1:Top_Documentaries_Main(name,url,iconimage)
elif mode==2:Top_Documentaries_Browse(name,url,iconimage)
elif mode==3:Top_Documentaries_Top100(name,url,iconimage)
elif mode==4:Top_Documentaries_List(name,url,iconimage)
elif mode==5:Top_Documentaries_Cats(name,url,iconimage)
elif mode==6:Free_Documentaries_Main(name,url,iconimage)
elif mode==7:Free_Documentaries_Browse(name,url,iconimage)
elif mode==8:Search_Free_Documentaries()
elif mode==9:Documentary_Storm_Main(name,url,iconimage)
elif mode==10:Documentary_Storm_Cats(name,url,iconimage)
elif mode==11:Documentary_Storm_Browse(name,url,iconimage)
elif mode==12:Documentary_Storm_FullList(name,url,iconimage)
elif mode==13:Search_Documentary_Storm()
elif mode==14:Documentary_Lovers_Main(name,url,iconimage)
elif mode==15:Documentary_Lovers_Browse(name,url,iconimage)
elif mode==16:Search_Documentary_Lovers()
elif mode==17:SnagFilms_Main(name,url,iconimage)
elif mode==18:Search_SnagFilms()
elif mode==19:Documentary_Heaven_Main(name,url,iconimage)
elif mode==20:Documentary_Heaven_Browse(name,url,iconimage)
elif mode==21:Documentary_Heaven_Browse_Cats(name,url,iconimage)
elif mode==22:Documentary_Heaven_Top100(name,url,iconimage)
elif mode==23:Search_Documentary_Heaven()
elif mode==24:Documentary_Tube_Main(name,url,iconimage)
elif mode==25:Documentary_Tube_Browse(name,url,iconimage)
elif mode==26:Documentary_Tube_Top100(name,url,iconimage)
elif mode==27:Search_Documentary_Tube(url)
elif mode==28:Sports_Documentaries_Main(name,url,iconimage)
elif mode==29:Sports_Documentaries_Browse(name,url,iconimage)
elif mode==30:Documentary_Addicts_Main(name,url,iconimage)
elif mode==31:Documentary_Addicts_Browse(name,url,iconimage)
elif mode==32:Search_Documentary_Addicts(url)
elif mode==33:Crime_Documentaries_Main(name,url,iconimage)
elif mode==34:Crime_Documentaries_Categories(name,url,iconimage)
elif mode==35:Crime_Documentaries_Shows(name,url,iconimage)
elif mode==36:Crime_Documentaries_BrowseAll(name,url,iconimage)
elif mode==37:Crime_Documentaries_Browse(name,url,iconimage)
elif mode==38:Crime_Documentaries_List_Eps(name,url,iconimage)
elif mode==39:Search_Crime_Documentaries(url)
elif mode==900:Play_Top_Documentaries(name,url,iconimage)
elif mode==901:Play_Free_Documentaries(name,url,iconimage)
elif mode==902:Play_Documentary_Storm(name,url,iconimage)
elif mode==903:Play_Documentary_Lovers(name,url,iconimage)
elif mode==904:Play_SnagFilms(name,url,iconimage)
elif mode==905:Play_Documentary_Heaven(name,url,iconimage)
elif mode==906:Play_Documentary_Tube(name,url,iconimage)
elif mode==907:Play_Sports_Documentaries(name,url,iconimage)
elif mode==908:Play_Documentary_Addicts(name,url,iconimage)
elif mode==909:Play_Crime_Documentaries(name,url,iconimage)

elif mode==998:Multi_Search()

if mode <= 1: 
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
else:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)