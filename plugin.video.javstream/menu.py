import urllib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

ADDON_ID='plugin.video.javstream'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

# the main menu structure
mainMenu=[
    {
        "title":"Latest JAV Censored", 
        "url":"http://javpop.com/category/censored", 
        "mode":4, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'jav-latest.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Latest JAV Uncensored", 
        "url":"http://javpop.com/category/uncensored", 
        "mode":4, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'jav-latest.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Latest Gravure", 
        "url":"http://javpop.com/category/idol", 
        "mode":4, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'gravure-latest.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Search", 
        "url":"http://javpop.com/index.php", 
        "mode":3, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'search-main.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, 
]

"""{
        "title":"JAV", 
        "url":"jav-menu", 
        "mode":1, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'jav-main.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Gravure", 
        "url":"gravure-menu", 
        "mode":2, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'gravure-main.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, , {
        "title":"My JAV", 
        "url":"my-jav", 
        "mode":7, 
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'search-main.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }"""

# JAV sub menu
javMenu=[
    {
        "title":"Genres",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'jav-genres.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Censored",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'jav-censored.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Uncensored",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'jav-uncensored.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Popular JAV",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'jav-popular.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Latest JAV",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'jav-latest.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search",
        "url":"http://javpop.com/category/censored, http://javpop.com/category/uncensored",
        "mode":3,
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'jav-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
]

# Gravure sub menu
gravureMenu=[
    {
        "title":"Studios",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'gravure-studios.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Idols",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'gravure-idols.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Popular gravure",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'gravure-popular.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Latest Gravure",
        "url":"genre-link",
        "mode":5,
        "poster":"",
        "icon":os.path.join(home, 'resources/media', 'gravure-latest.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search",
        "url":"http://javpop.com/category/idol",
        "mode":3,
        "poster":"none",
        "icon":os.path.join(home, 'resources/media', 'gravure-search.jpg'), 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
]