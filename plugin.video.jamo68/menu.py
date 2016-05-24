import urllib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

ADDON_ID='plugin.video.jamo68'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

# the main menu structure
mainMenu=[
    {
        "title":"Jamo TV", 
        "url":"uncensored", 
        "mode":1, 
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Jav68", 
        "url":"censored", 
        "mode":2, 
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Latest from Jamo TV", 
        "url":"http://jamo.tv/most-recent-page-1.html", 
        "mode":111, 
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }, {
        "title":"Latest from Jav68", 
        "url":"http://jav68.me/recent", 
        "mode":211, 
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    }
]

# JAV sub menu
jamoMenu=[
    {
        "title":"Categories",
        "url":"category-link",
        "mode":11,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Studios",
        "url":"studio-link",
        "mode":12,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Models",
        "url":"model-link",
        "mode":13,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Most Viewed",
        "url":"http://jamo.tv/most-viewed-page-1.html",
        "mode":111,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Top Rated",
        "url":"http://jamo.tv/top-rated-page-1.html",
        "mode":111,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search",
        "url":"http://jamo.tv/search-movie/keyword-<search>-1-page-1.html",
        "mode":16,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
]

# Gravure sub menu
jav68Menu=[
    {
        "title":"Categories",
        "url":"category-link",
        "mode":21,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Studios",
        "url":"genre-link",
        "mode":21,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Most Viewed",
        "url":"http://jav68.me/hot",
        "mode":211,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Top Rated",
        "url":"http://jav68.me/popular",
        "mode":211,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search",
        "url":"http://jav68.me/search/<search>",
        "mode":26,
        "poster":"default.jpg",
        "icon":"default.jpg", 
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
]