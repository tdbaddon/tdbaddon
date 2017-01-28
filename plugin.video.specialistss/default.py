import urlparse as OOOO0OOOOOO0OOO00 ,sys as OOOOOO0OO0OOOOOOO ,re as OO0OO0O00OO0O0OOO #line:1
params =dict (OOOO0OOOOOO0OOO00 .parse_qsl (OOOOOO0OO0OOOOOOO .argv [2 ].replace ('?','')))#line:3
action =params .get ('action')#line:5
content =params .get ('content')#line:7
name =params .get ('name')#line:9
url =params .get ('url')#line:11
image =params .get ('image')#line:13
fanart =params .get ('fanart')#line:15
if action ==None :#line:18
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:19
    O00O00OO000O00OO0 .indexer ().root ()#line:20
elif action =='directory':#line:22
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:23
    O00O00OO000O00OO0 .indexer ().get (url )#line:24
elif action =='qdirectory':#line:26
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:27
    O00O00OO000O00OO0 .indexer ().getq (url )#line:28
elif action =='xdirectory':#line:30
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:31
    O00O00OO000O00OO0 .indexer ().getx (url )#line:32
elif action =='developer':#line:34
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:35
    O00O00OO000O00OO0 .indexer ().developer ()#line:36
elif action =='tvtuner':#line:38
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:39
    O00O00OO000O00OO0 .indexer ().tvtuner (url )#line:40
elif 'youtube'in str (action ):#line:42
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:43
    O00O00OO000O00OO0 .indexer ().youtube (url ,action )#line:44
elif action =='play':#line:46
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:47
    O00O00OO000O00OO0 .player ().play (url ,content )#line:48
elif action =='browser':#line:50
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:51
    O00O00OO000O00OO0 .resolver ().browser (url )#line:52
elif action =='search':#line:54
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:55
    O00O00OO000O00OO0 .indexer ().search ()#line:56
elif action =='addSearch':#line:58
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:59
    O00O00OO000O00OO0 .indexer ().addSearch (url )#line:60
elif action =='delSearch':#line:62
    from resources .lib .indexers import specialist as O00O00OO000O00OO0 #line:63
    O00O00OO000O00OO0 .indexer ().delSearch ()#line:64
elif action =='queueItem':#line:66
    from resources .lib .modules import control as OOOOO0O00OOO00000 #line:67
    OOOOO0O00OOO00000 .queueItem ()#line:68
elif action =='openSettings':#line:70
    from resources .lib .modules import control as OOOOO0O00OOO00000 #line:71
    OOOOO0O00OOO00000 .openSettings ()#line:72
elif action =='urlresolverSettings':#line:74
    from resources .lib .modules import control as OOOOO0O00OOO00000 #line:75
    OOOOO0O00OOO00000 .openSettings (id ='script.module.urlresolver')#line:76
elif action =='addView':#line:78
    from resources .lib .modules import views as OOOO00O0O00O00O00 #line:79
    OOOO00O0O00O00O00 .addView (content )#line:80
elif action =='downloader':#line:82
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:83
    O0O00O0O0O00OOO0O .downloader ()#line:84
elif action =='addDownload':#line:86
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:87
    O0O00O0O0O00OOO0O .addDownload (name ,url ,image )#line:88
elif action =='removeDownload':#line:90
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:91
    O0O00O0O0O00OOO0O .removeDownload (url )#line:92
elif action =='startDownload':#line:94
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:95
    O0O00O0O0O00OOO0O .startDownload ()#line:96
elif action =='startDownloadThread':#line:98
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:99
    O0O00O0O0O00OOO0O .startDownloadThread ()#line:100
elif action =='stopDownload':#line:102
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:103
    O0O00O0O0O00OOO0O .stopDownload ()#line:104
elif action =='statusDownload':#line:106
    from resources .lib .modules import downloader as O0O00O0O0O00OOO0O #line:107
    O0O00O0O0O00OOO0O .statusDownload ()#line:108
elif action =='trailer':#line:110
    from resources .lib .modules import trailer as O0OOO000O00O0000O #line:111
    O0OOO000O00O0000O .trailer ().play (name )#line:112
elif action =='clearCache':#line:114
    from resources .lib .modules import cache as OO0O00O00OOO00O0O #line:115
    OO0O00O00OOO00O0O .clear ()
#e9015584e6a44b14988f13e2298bcbf9

