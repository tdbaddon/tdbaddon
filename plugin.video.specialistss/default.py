import urlparse as O00OOO0O00OOOO00O ,sys as OOOOO0O0O0O0OO0OO ,re as O0000000000OO000O #line:1
params =dict (O00OOO0O00OOOO00O .parse_qsl (OOOOO0O0O0O0OO0OO .argv [2 ].replace ('?','')))#line:3
action =params .get ('action')#line:5
content =params .get ('content')#line:7
name =params .get ('name')#line:9
url =params .get ('url')#line:11
image =params .get ('image')#line:13
fanart =params .get ('fanart')#line:15
if action ==None :#line:18
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:19
    OO0O0O0O0O0OOO0O0 .indexer ().root ()#line:20
elif action =='directory':#line:22
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:23
    OO0O0O0O0O0OOO0O0 .indexer ().get (url )#line:24
elif action =='qdirectory':#line:26
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:27
    OO0O0O0O0O0OOO0O0 .indexer ().getq (url )#line:28
elif action =='xdirectory':#line:30
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:31
    OO0O0O0O0O0OOO0O0 .indexer ().getx (url )#line:32
elif action =='developer':#line:34
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:35
    OO0O0O0O0O0OOO0O0 .indexer ().developer ()#line:36
elif action =='tvtuner':#line:38
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:39
    OO0O0O0O0O0OOO0O0 .indexer ().tvtuner (url )#line:40
elif 'youtube'in str (action ):#line:42
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:43
    OO0O0O0O0O0OOO0O0 .indexer ().youtube (url ,action )#line:44
elif action =='play':#line:46
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:47
    OO0O0O0O0O0OOO0O0 .player ().play (url ,content )#line:48
elif action =='browser':#line:50
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:51
    OO0O0O0O0O0OOO0O0 .resolver ().browser (url )#line:52
elif action =='search':#line:54
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:55
    OO0O0O0O0O0OOO0O0 .indexer ().search ()#line:56
elif action =='addSearch':#line:58
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:59
    OO0O0O0O0O0OOO0O0 .indexer ().addSearch (url )#line:60
elif action =='delSearch':#line:62
    from resources .lib .indexers import specialist as OO0O0O0O0O0OOO0O0 #line:63
    OO0O0O0O0O0OOO0O0 .indexer ().delSearch ()#line:64
elif action =='queueItem':#line:66
    from resources .lib .modules import control as O0OO00OO0O0O000O0 #line:67
    O0OO00OO0O0O000O0 .queueItem ()#line:68
elif action =='openSettings':#line:70
    from resources .lib .modules import control as O0OO00OO0O0O000O0 #line:71
    O0OO00OO0O0O000O0 .openSettings ()#line:72
elif action =='urlresolverSettings':#line:74
    from resources .lib .modules import control as O0OO00OO0O0O000O0 #line:75
    O0OO00OO0O0O000O0 .openSettings (id ='script.module.urlresolver')#line:76
elif action =='addView':#line:78
    from resources .lib .modules import views as OOOO0O0O00OOO000O #line:79
    OOOO0O0O00OOO000O .addView (content )#line:80
elif action =='downloader':#line:82
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:83
    OOOOOO0O0O0O0O00O .downloader ()#line:84
elif action =='addDownload':#line:86
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:87
    OOOOOO0O0O0O0O00O .addDownload (name ,url ,image )#line:88
elif action =='removeDownload':#line:90
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:91
    OOOOOO0O0O0O0O00O .removeDownload (url )#line:92
elif action =='startDownload':#line:94
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:95
    OOOOOO0O0O0O0O00O .startDownload ()#line:96
elif action =='startDownloadThread':#line:98
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:99
    OOOOOO0O0O0O0O00O .startDownloadThread ()#line:100
elif action =='stopDownload':#line:102
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:103
    OOOOOO0O0O0O0O00O .stopDownload ()#line:104
elif action =='statusDownload':#line:106
    from resources .lib .modules import downloader as OOOOOO0O0O0O0O00O #line:107
    OOOOOO0O0O0O0O00O .statusDownload ()#line:108
elif action =='trailer':#line:110
    from resources .lib .modules import trailer as OO00OOO0OO0O0O000 #line:111
    OO00OOO0OO0O0O000 .trailer ().play (name )#line:112
elif action =='clearCache':#line:114
    from resources .lib .modules import cache as OOOO0OO00O00OOO0O #line:115
    OOOO0OO00O00OOO0O .clear ()
#e9015584e6a44b14988f13e2298bcbf9

