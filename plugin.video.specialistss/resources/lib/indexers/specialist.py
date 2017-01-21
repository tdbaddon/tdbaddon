import os as O00O00O0000OO00OO ,re as OOOOO0O00OO00OOOO ,sys as O000OO0OOO000OOO0 ,hashlib as O00OO0000000OO00O ,urllib as OOO000O0O0O00OOOO ,urlparse as O000000O0OOO0O000 ,json as OO0OO00OO00OO0O0O ,base64 as O0OOO0OOOO0OO0O0O ,random as OO000OOOOO0OO0000 ,datetime as O0O00OOO000O000O0 #line:1
import xbmc as O0OO000O000O0O000 #line:2
try :from sqlite3 import dbapi2 as OOOO0OOO000O00O00 #line:4
except :from pysqlite2 import dbapi2 as OOOO0OOO000O00O00 #line:5
from resources .lib .modules import cache as O0OOOO000O0OO000O #line:7
from resources .lib .modules import metacache as O0O000000OO0OOOOO #line:8
from resources .lib .modules import client as O0000OO0O000O000O #line:9
from resources .lib .modules import control as OOOOO00OOOO00000O #line:10
from resources .lib .modules import regex as OOOOO00OOO0O00000 #line:11
from resources .lib .modules import trailer as O000OO000000OO000 #line:12
from resources .lib .modules import workers as OOO0O00OOO0000O0O #line:13
from resources .lib .modules import youtube as O00000OOO0O0OOOO0 #line:14
from resources .lib .modules import views as OO0O0O00O00O000OO #line:15
class indexer :#line:19
    def __init__ (OO000OO000000OO00 ):#line:20
        OO000OO000000OO00 .list =[];OO000OO000000OO00 .hash =[]#line:21
    def root (O0OOOO0O00OOO00OO ):#line:24
        try :#line:25
            OOOOO00OOO0O00000 .clear ()#line:26
            O0OO0OO00OO00OOOO ='http://thespecialist.xyz/addon/specialist%20index.xml'#line:27
            O0OOOO0O00OOO00OO .list =O0OOOO0O00OOO00OO .specialist_list (O0OO0OO00OO00OOOO )#line:28
            for OO0O0O00000O0000O in O0OOOO0O00OOO00OO .list :OO0O0O00000O0000O .update ({'content':'addons'})#line:29
            O0OOOO0O00OOO00OO .addDirectory (O0OOOO0O00OOO00OO .list )#line:30
            return O0OOOO0O00OOO00OO .list #line:31
        except :#line:32
            pass #line:33
    def get (O0OO0OO000O0OO00O ,OO0O0O0O00OOOOO00 ):#line:36
        try :#line:37
            O0OO0OO000O0OO00O .list =O0OO0OO000O0OO00O .specialist_list (OO0O0O0O00OOOOO00 )#line:38
            O0OO0OO000O0OO00O .worker ()#line:39
            O0OO0OO000O0OO00O .addDirectory (O0OO0OO000O0OO00O .list )#line:40
            return O0OO0OO000O0OO00O .list #line:41
        except :#line:42
            pass #line:43
    def getq (O000OOO0OO0O00O00 ,O0OOOO000OOOOOO0O ):#line:46
        try :#line:47
            O000OOO0OO0O00O00 .list =O000OOO0OO0O00O00 .specialist_list (O0OOOO000OOOOOO0O )#line:48
            O000OOO0OO0O00O00 .worker ()#line:49
            O000OOO0OO0O00O00 .addDirectory (O000OOO0OO0O00O00 .list ,queue =True )#line:50
            return O000OOO0OO0O00O00 .list #line:51
        except :#line:52
            pass #line:53
    def getx (OO0000000O00O0000 ,OOOOOOO00OO00OO00 ,worker =False ):#line:56
        try :#line:57
            O00000O000O0000OO ,O0OOOOOO0000OO00O =OOOOO0O00OO00OOOO .findall ('(.+?)\|regex=(.+?)$',OOOOOOO00OO00OO00 )[0 ]#line:58
            O0OOOOOO0000OO00O =OOOOO00OOO0O00000 .fetch (O0OOOOOO0000OO00O )#line:59
            O00000O000O0000OO +=OOO000O0O0O00OOOO .unquote_plus (O0OOOOOO0000OO00O )#line:60
            OOOOOOO00OO00OO00 =OOOOO00OOO0O00000 .resolve (O00000O000O0000OO )#line:61
            OO0000000O00O0000 .list =OO0000000O00O0000 .specialist_list ('',result =OOOOOOO00OO00OO00 )#line:62
            OO0000000O00O0000 .addDirectory (OO0000000O00O0000 .list )#line:63
            return OO0000000O00O0000 .list #line:64
        except :#line:65
            pass #line:66
    def developer (O0OOOO0OOOO000O00 ):#line:69
        try :#line:70
            OO00O00OOO0OO0O00 =O00O00O0000OO00OO .path .join (OOOOO00OOOO00000O .dataPath ,'testings.xml')#line:71
            O00O0000000O000OO =OOOOO00OOOO00000O .openFile (OO00O00OOO0OO0O00 );OOO000000O0OO0O0O =O00O0000000O000OO .read ();O00O0000000O000OO .close ()#line:72
            O0OOOO0OOOO000O00 .list =O0OOOO0OOOO000O00 .specialist_list ('',result =OOO000000O0OO0O0O )#line:73
            for O0O0O00O0O0O00OO0 in O0OOOO0OOOO000O00 .list :O0O0O00O0O0O00OO0 .update ({'content':'videos'})#line:74
            O0OOOO0OOOO000O00 .addDirectory (O0OOOO0OOOO000O00 .list )#line:75
            return O0OOOO0OOOO000O00 .list #line:76
        except :#line:77
            pass #line:78
    def youtube (OOO0OOO0OO00O0OO0 ,OO0O0O0OO0OO00O00 ,OOO0OO0O00OOOO0OO ):#line:81
        try :#line:82
            O000OOOO0O0OO00O0 =O000OO000000OO000 .trailer ().key_link .split ('=',1 )[-1 ]#line:83
            if 'PlaylistTuner'in OOO0OO0O00OOOO0OO :#line:85
                OOO0OOO0OO00O0OO0 .list =O0OOOO000O0OO000O .get (O00000OOO0O0OOOO0 .youtube (key =O000OOOO0O0OO00O0 ).playlist ,1 ,OO0O0O0OO0OO00O00 )#line:86
            elif 'Playlist'in OOO0OO0O00OOOO0OO :#line:87
                OOO0OOO0OO00O0OO0 .list =O0OOOO000O0OO000O .get (O00000OOO0O0OOOO0 .youtube (key =O000OOOO0O0OO00O0 ).playlist ,1 ,OO0O0O0OO0OO00O00 ,True )#line:88
            elif 'ChannelTuner'in OOO0OO0O00OOOO0OO :#line:89
                OOO0OOO0OO00O0OO0 .list =O0OOOO000O0OO000O .get (O00000OOO0O0OOOO0 .youtube (key =O000OOOO0O0OO00O0 ).videos ,1 ,OO0O0O0OO0OO00O00 )#line:90
            elif 'Channel'in OOO0OO0O00OOOO0OO :#line:91
                OOO0OOO0OO00O0OO0 .list =O0OOOO000O0OO000O .get (O00000OOO0O0OOOO0 .youtube (key =O000OOOO0O0OO00O0 ).videos ,1 ,OO0O0O0OO0OO00O00 ,True )#line:92
            if 'Tuner'in OOO0OO0O00OOOO0OO :#line:94
                for OO0O00OOOO0OO0OOO in OOO0OOO0OO00O0OO0 .list :OO0O00OOOO0OO0OOO .update ({'name':OO0O00OOOO0OO0OOO ['title'],'poster':OO0O00OOOO0OO0OOO ['image'],'action':'plugin','folder':False })#line:95
                if 'Tuner2'in OOO0OO0O00OOOO0OO :OOO0OOO0OO00O0OO0 .list =sorted (OOO0OOO0OO00O0OO0 .list ,key =lambda OOOO00OOO0O0OO0OO :OO000OOOOO0OO0000 .random ())#line:96
                OOO0OOO0OO00O0OO0 .addDirectory (OOO0OOO0OO00O0OO0 .list ,queue =True )#line:97
            else :#line:98
                for OO0O00OOOO0OO0OOO in OOO0OOO0OO00O0OO0 .list :OO0O00OOOO0OO0OOO .update ({'name':OO0O00OOOO0OO0OOO ['title'],'poster':OO0O00OOOO0OO0OOO ['image'],'nextaction':OOO0OO0O00OOOO0OO ,'action':'play','folder':False })#line:99
                OOO0OOO0OO00O0OO0 .addDirectory (OOO0OOO0OO00O0OO0 .list )#line:100
            return OOO0OOO0OO00O0OO0 .list #line:102
        except :#line:103
            pass #line:104
    def tvtuner (O00OO000OO0000000 ,O0OO0O000O00000OO ):#line:107
        try :#line:108
            OO0OOOO000O00O00O =OOOOO0O00OO00OOOO .findall ('<preset>(.+?)</preset>',O0OO0O000O00000OO )[0 ]#line:109
            OOO0O0OO00O0O0O0O =((O0O00OOO000O000O0 .datetime .utcnow ()-O0O00OOO000O000O0 .timedelta (hours =5 ))).strftime ('%Y-%m-%d')#line:111
            OOO0O0OO00O0O0O0O =int (OOOOO0O00OO00OOOO .sub ('[^0-9]','',str (OOO0O0OO00O0O0O0O )))#line:112
            O0OO0O000O00000OO ,OOO0000O0O0000O0O ,O0O0OOOOO0OOO0O00 ,O000000O00OOO00O0 ,OOO0O00OO000O0OOO ,O0O0000OO000O0O00 ,OOOOO0OOOO00O0OO0 =OOOOO0O00OO00OOOO .findall ('<url>(.+?)</url>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<imdb>(.+?)</imdb>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<tvdb>(.+?)</tvdb>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<year>(.+?)</year>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<thumbnail>(.+?)</thumbnail>',O0OO0O000O00000OO )[0 ],OOOOO0O00OO00OOOO .findall ('<fanart>(.+?)</fanart>',O0OO0O000O00000OO )[0 ]#line:114
            O0O0O000OO0000OOO =O0000OO0O000O000O .request ('http://api.tvmaze.com/lookup/shows?thetvdb=%s'%O0O0OOOOO0OOO0O00 )#line:116
            if O0O0O000OO0000OOO ==None :O0O0O000OO0000OOO =O0000OO0O000O000O .request ('http://api.tvmaze.com/lookup/shows?imdb=%s'%OOO0000O0O0000O0O )#line:117
            O0O0O000OO0000OOO ='http://api.tvmaze.com/shows/%s/episodes'%str (OO0OO00OO00OO0O0O .loads (O0O0O000OO0000OOO ).get ('id'))#line:118
            O00OO000OOO0O00O0 =OO0OO00OO00OO0O0O .loads (O0000OO0O000O000O .request (O0O0O000OO0000OOO ))#line:119
            O00OO000OOO0O00O0 =[(str (OOOO0O0000OO00OO0 .get ('season')),str (OOOO0O0000OO00OO0 .get ('number')),OOOO0O0000OO00OO0 .get ('name').strip (),OOOO0O0000OO00OO0 .get ('airdate'))for OOOO0O0000OO00OO0 in O00OO000OOO0O00O0 ]#line:120
            if OO0OOOO000O00O00O =='tvtuner':#line:122
                O0OO00OOOO0OO0000 =OO000OOOOO0OO0000 .choice (O00OO000OOO0O00O0 )#line:123
                O00OO000OOO0O00O0 =O00OO000OOO0O00O0 [O00OO000OOO0O00O0 .index (O0OO00OOOO0OO0000 ):]+O00OO000OOO0O00O0 [:O00OO000OOO0O00O0 .index (O0OO00OOOO0OO0000 )]#line:124
                O00OO000OOO0O00O0 =O00OO000OOO0O00O0 [:100 ]#line:125
            OOOOO00O00O00O0OO =''#line:127
            for OOO0OO00OOOOOO0O0 in O00OO000OOO0O00O0 :#line:129
                try :#line:130
                    if int (OOOOO0O00OO00OOOO .sub ('[^0-9]','',str (OOO0OO00OOOOOO0O0 [3 ])))>OOO0O0OO00O0O0O0O :raise Exception ()#line:131
                    OOOOO00O00O00O0OO +='<item><title> %01dx%02d . %s</title><meta><content>episode</content><imdb>%s</imdb><tvdb>%s</tvdb><tvshowtitle>%s</tvshowtitle><year>%s</year><title>%s</title><premiered>%s</premiered><season>%01d</season><episode>%01d</episode></meta><link><sublink>search</sublink><sublink>searchsd</sublink></link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(int (OOO0OO00OOOOOO0O0 [0 ]),int (OOO0OO00OOOOOO0O0 [1 ]),OOO0OO00OOOOOO0O0 [2 ],OOO0000O0O0000O0O ,O0O0OOOOO0OOO0O00 ,O000000O00OOO00O0 ,OOO0O00OO000O0OOO ,OOO0OO00OOOOOO0O0 [2 ],OOO0OO00OOOOOO0O0 [3 ],int (OOO0OO00OOOOOO0O0 [0 ]),int (OOO0OO00OOOOOO0O0 [1 ]),O0O0000OO000O0O00 ,OOOOO0OOOO00O0OO0 )#line:132
                except :#line:133
                    pass #line:134
            OOOOO00O00O00O0OO =OOOOO0O00OO00OOOO .sub (r'[^\x00-\x7F]+',' ',OOOOO00O00O00O0OO )#line:136
            if OO0OOOO000O00O00O =='tvtuner':#line:138
                OOOOO00O00O00O0OO =OOOOO00O00O00O0OO .replace ('<sublink>searchsd</sublink>','')#line:139
            O00OO000OO0000000 .list =O00OO000OO0000000 .specialist_list ('',result =OOOOO00O00O00O0OO )#line:141
            if OO0OOOO000O00O00O =='tvtuner':#line:143
                O00OO000OO0000000 .addDirectory (O00OO000OO0000000 .list ,queue =True )#line:144
            else :#line:145
                O00OO000OO0000000 .worker ()#line:146
                O00OO000OO0000000 .addDirectory (O00OO000OO0000000 .list )#line:147
        except :#line:148
            pass #line:149
    def search (O000O000O0OOOOO00 ):#line:152
        try :#line:153
            O000O000O0OOOOO00 .list =[{'name':30702 ,'action':'addSearch'}]#line:154
            O000O000O0OOOOO00 .list +=[{'name':30703 ,'action':'delSearch'}]#line:155
            try :#line:157
                def O0OO0O00O0OO00O00 ():return #line:158
                OO0OO0O0OO0O0OOO0 =O0OOOO000O0OO000O .get (O0OO0O00O0OO00O00 ,600000000 ,table ='rel_srch')#line:159
                for OOO00O0OOOO00OOO0 in OO0OO0O0OO0O0OOO0 :#line:161
                    try :O000O000O0OOOOO00 .list +=[{'name':'%s...'%OOO00O0OOOO00OOO0 ,'url':OOO00O0OOOO00OOO0 ,'action':'addSearch'}]#line:162
                    except :pass #line:163
            except :#line:164
                pass #line:165
            O000O000O0OOOOO00 .addDirectory (O000O000O0OOOOO00 .list )#line:167
            return O000O000O0OOOOO00 .list #line:168
        except :#line:169
            pass #line:170
    def delSearch (OO0O0O0000OOO0O0O ):#line:173
        try :#line:174
            O0OOOO000O0OO000O .clear ('rel_srch')#line:175
            OOOOO00OOOO00000O .refresh ()#line:176
        except :#line:177
            pass #line:178
    def addSearch (O0000O0OOOOOOO00O ,url =None ):#line:181
        try :#line:182
            O000O00OOOOOOO0OO ='http://thespecialist.xyz/addon/search.xml'#line:183
            if (url ==None or url ==''):#line:185
                OO0O00OOOO0000O0O =OOOOO00OOOO00000O .keyboard ('',OOOOO00OOOO00000O .lang (30702 ).encode ('utf-8'))#line:186
                OO0O00OOOO0000O0O .doModal ()#line:187
                if not (OO0O00OOOO0000O0O .isConfirmed ()):return #line:188
                url =OO0O00OOOO0000O0O .getText ()#line:189
            if (url ==None or url ==''):return #line:191
            def O0OO0OOOO00O00OOO ():return [url ]#line:193
            OOO000OO0O0O0O0O0 =O0OOOO000O0OO000O .get (O0OO0OOOO00O00OOO ,600000000 ,table ='rel_srch')#line:194
            def O0OO0OOOO00O00OOO ():return [O00OOO00OO0OOOO0O for OOOOOOO00O00000O0 ,O00OOO00OO0OOOO0O in enumerate ((OOO000OO0O0O0O0O0 +[url ]))if O00OOO00OO0OOOO0O not in (OOO000OO0O0O0O0O0 +[url ])[:OOOOOOO00O00000O0 ]]#line:195
            O0OOOO000O0OO000O .get (O0OO0OOOO00O00OOO ,0 ,table ='rel_srch')#line:196
            O0OO00OOO00O00O0O =O0000OO0O000O000O .request (O000O00OOOOOOO0OO )#line:198
            O0OO00OOO00O00O0O =OOOOO0O00OO00OOOO .findall ('<link>(.+?)</link>',O0OO00OOO00O00O0O )#line:199
            O0OO00OOO00O00O0O =[O0OO00000000OO00O for O0OO00000000OO00O in O0OO00OOO00O00O0O if str (O0OO00000000OO00O ).startswith ('http')]#line:200
            O0000O0OOOOOOO00O .list =[];O0OO000OOOO0O0OO0 =[]#line:202
            for O000O00OOOOOOO0OO in O0OO00OOO00O00O0O :O0OO000OOOO0O0OO0 .append (OOO0O00OOO0000O0O .Thread (O0000O0OOOOOOO00O .specialist_list ,O000O00OOOOOOO0OO ))#line:203
            [OOOO0O0O00O0000O0 .start ()for OOOO0O0O00O0000O0 in O0OO000OOOO0O0OO0 ];[OOOOO0OOOOO0O0OO0 .join ()for OOOOO0OOOOO0O0OO0 in O0OO000OOOO0O0OO0 ]#line:204
            O0000O0OOOOOOO00O .list =[O00000O0O0OOOO0O0 for O00000O0O0OOOO0O0 in O0000O0OOOOOOO00O .list if url .lower ()in O00000O0O0OOOO0O0 ['name'].lower ()]#line:206
            for OOO00O0OO00O0000O in O0000O0OOOOOOO00O .list :#line:208
                try :#line:209
                    O0O00OO00OOOOOO0O =''#line:210
                    if not OOO00O0OO00O0000O ['vip']in ['specialist TV']:O0O00OO00OOOOOO0O +='[B]%s[/B] | '%OOO00O0OO00O0000O ['vip'].upper ()#line:211
                    O0O00OO00OOOOOO0O +=OOO00O0OO00O0000O ['name']#line:212
                    OOO00O0OO00O0000O .update ({'name':O0O00OO00OOOOOO0O })#line:213
                except :#line:214
                    pass #line:215
            for OOO00O0OO00O0000O in O0000O0OOOOOOO00O .list :OOO00O0OO00O0000O .update ({'content':'videos'})#line:217
            O0000O0OOOOOOO00O .addDirectory (O0000O0OOOOOOO00O .list )#line:218
        except :#line:219
            pass #line:220
    def specialist_list (OO000OO0OO0O0OOO0 ,OO00OO0OOOO0OO000 ,result =None ):#line:223
        try :#line:224
            if result ==None :result =O0OOOO000O0OO000O .get (O0000OO0O000O000O .request ,0 ,OO00OO0OOOO0OO000 )#line:225
            if result .strip ().startswith ('#EXTM3U')and '#EXTINF'in result :#line:227
                result =OOOOO0O00OO00OOOO .compile ('#EXTINF:.+?\,(.+?)\n(.+?)\n',OOOOO0O00OO00OOOO .MULTILINE |OOOOO0O00OO00OOOO .DOTALL ).findall (result )#line:228
                result =['<item><title>%s</title><link>%s</link></item>'%(O0OO0O0OO000O0000 [0 ],O0OO0O0OO000O0000 [1 ])for O0OO0O0OO000O0000 in result ]#line:229
                result =''.join (result )#line:230
            try :O000OO0OO0O0OO0OO =O0OOO0OOOO0OO0O0O .b64decode (result )#line:232
            except :O000OO0OO0O0OO0OO =''#line:233
            if '</link>'in O000OO0OO0O0OO0OO :result =O000OO0OO0O0OO0OO #line:234
            result =str (result )#line:236
            result =OO000OO0OO0O0OOO0 .account_filter (result )#line:238
            OO0O00O00O0O000OO =result .split ('<item>')[0 ].split ('<dir>')[0 ]#line:240
            try :O00O0O0OOO0O0000O =OOOOO0O00OO00OOOO .findall ('<poster>(.+?)</poster>',OO0O00O00O0O000OO )[0 ]#line:242
            except :O00O0O0OOO0O0000O ='0'#line:243
            try :O0O00O00O00000000 =OOOOO0O00OO00OOOO .findall ('<thumbnail>(.+?)</thumbnail>',OO0O00O00O0O000OO )[0 ]#line:245
            except :O0O00O00O00000000 ='0'#line:246
            try :O0O0OO000O0OOO0OO =OOOOO0O00OO00OOOO .findall ('<fanart>(.+?)</fanart>',OO0O00O00O0O000OO )[0 ]#line:248
            except :O0O0OO000O0OOO0OO ='0'#line:249
            OOOO0O00OOOOO0O0O =OOOOO0O00OO00OOOO .compile ('((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',OOOOO0O00OO00OOOO .MULTILINE |OOOOO0O00OO00OOOO .DOTALL ).findall (result )#line:251
        except :#line:252
            return #line:253
        for O0O000O00O00O00O0 in OOOO0O00OOOOO0O0O :#line:255
            try :#line:256
                OO00O00O0OOOOO00O =OOOOO0O00OO00OOOO .compile ('(<regex>.+?</regex>)',OOOOO0O00OO00OOOO .MULTILINE |OOOOO0O00OO00OOOO .DOTALL ).findall (O0O000O00O00O00O0 )#line:257
                OO00O00O0OOOOO00O =''.join (OO00O00O0OOOOO00O )#line:258
                O0OO00OOOO00O000O =OOOOO0O00OO00OOOO .compile ('(<listrepeat>.+?</listrepeat>)',OOOOO0O00OO00OOOO .MULTILINE |OOOOO0O00OO00OOOO .DOTALL ).findall (OO00O00O0OOOOO00O )#line:259
                OO00O00O0OOOOO00O =OOO000O0O0O00OOOO .quote_plus (OO00O00O0OOOOO00O )#line:260
                OOO0O000O00OOO0OO =O00OO0000000OO00O .md5 ()#line:262
                for O0000O0OO0OOOO000 in OO00O00O0OOOOO00O :OOO0O000O00OOO0OO .update (str (O0000O0OO0OOOO000 ))#line:263
                OOO0O000O00OOO0OO =str (OOO0O000O00OOO0OO .hexdigest ())#line:264
                O0O000O00O00O00O0 =O0O000O00O00O00O0 .replace ('\r','').replace ('\n','').replace ('\t','').replace ('&nbsp;','')#line:266
                O0O000O00O00O00O0 =OOOOO0O00OO00OOOO .sub ('<regex>.+?</regex>','',O0O000O00O00O00O0 )#line:267
                O0O000O00O00O00O0 =OOOOO0O00OO00OOOO .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',O0O000O00O00O00O0 )#line:268
                O0O000O00O00O00O0 =OOOOO0O00OO00OOOO .sub ('<link></link>','',O0O000O00O00O00O0 )#line:269
                OOOOOO0OO00OO00O0 =OOOOO0O00OO00OOOO .sub ('<meta>.+?</meta>','',O0O000O00O00O00O0 )#line:271
                try :OOOOOO0OO00OO00O0 =OOOOO0O00OO00OOOO .findall ('<title>(.+?)</title>',OOOOOO0OO00OO00O0 )[0 ]#line:272
                except :OOOOOO0OO00OO00O0 =OOOOO0O00OO00OOOO .findall ('<name>(.+?)</name>',OOOOOO0OO00OO00O0 )[0 ]#line:273
                try :OOOOO00OO0O0O0OO0 =OOOOO0O00OO00OOOO .findall ('<date>(.+?)</date>',O0O000O00O00O00O0 )[0 ]#line:275
                except :OOOOO00OO0O0O0OO0 =''#line:276
                if OOOOO0O00OO00OOOO .search (r'\d+',OOOOO00OO0O0O0OO0 ):OOOOOO0OO00OO00O0 +=' [COLOR red] Updated %s[/COLOR]'%OOOOO00OO0O0O0OO0 #line:277
                try :OO000000O0OOO00O0 =OOOOO0O00OO00OOOO .findall ('<thumbnail>(.+?)</thumbnail>',O0O000O00O00O00O0 )[0 ]#line:279
                except :OO000000O0OOO00O0 =O0O00O00O00000000 #line:280
                try :OOOO0OOO000000O00 =OOOOO0O00OO00OOOO .findall ('<fanart>(.+?)</fanart>',O0O000O00O00O00O0 )[0 ]#line:282
                except :OOOO0OOO000000O00 =O0O0OO000O0OOO0OO #line:283
                try :OOO0OOOOOOO0OOO0O =OOOOO0O00OO00OOOO .findall ('<meta>(.+?)</meta>',O0O000O00O00O00O0 )[0 ]#line:285
                except :OOO0OOOOOOO0OOO0O ='0'#line:286
                try :OO00OO0OOOO0OO000 =OOOOO0O00OO00OOOO .findall ('<link>(.+?)</link>',O0O000O00O00O00O0 )[0 ]#line:288
                except :OO00OO0OOOO0OO000 ='0'#line:289
                OO00OO0OOOO0OO000 =OO00OO0OOOO0OO000 .replace ('>search<','><preset>search</preset>%s<'%OOO0OOOOOOO0OOO0O )#line:290
                OO00OO0OOOO0OO000 ='<preset>search</preset>%s'%OOO0OOOOOOO0OOO0O if OO00OO0OOOO0OO000 =='search'else OO00OO0OOOO0OO000 #line:291
                OO00OO0OOOO0OO000 =OO00OO0OOOO0OO000 .replace ('>searchsd<','><preset>searchsd</preset>%s<'%OOO0OOOOOOO0OOO0O )#line:292
                OO00OO0OOOO0OO000 ='<preset>searchsd</preset>%s'%OOO0OOOOOOO0OOO0O if OO00OO0OOOO0OO000 =='searchsd'else OO00OO0OOOO0OO000 #line:293
                OO00OO0OOOO0OO000 =OOOOO0O00OO00OOOO .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OO00OO0OOOO0OO000 )#line:294
                if O0O000O00O00O00O0 .startswith ('<item>'):OOOO0O0OOOOOOO0O0 ='play'#line:296
                elif O0O000O00O00O00O0 .startswith ('<plugin>'):OOOO0O0OOOOOOO0O0 ='plugin'#line:297
                elif O0O000O00O00O00O0 .startswith ('<info>')or OO00OO0OOOO0OO000 =='0':OOOO0O0OOOOOOO0O0 ='0'#line:298
                else :OOOO0O0OOOOOOO0O0 ='directory'#line:299
                if OOOO0O0OOOOOOO0O0 =='play'and O0OO00OOOO00O000O :OOOO0O0OOOOOOO0O0 ='xdirectory'#line:300
                if not OO00O00O0OOOOO00O =='':#line:302
                    OO000OO0OO0O0OOO0 .hash .append ({'regex':OOO0O000O00OOO0OO ,'response':OO00O00O0OOOOO00O })#line:303
                    OO00OO0OOOO0OO000 +='|regex=%s'%OOO0O000O00OOO0OO #line:304
                if OOOO0O0OOOOOOO0O0 in ['directory','xdirectory','plugin']:#line:306
                    O00000O0000OOO000 =True #line:307
                else :#line:308
                    O00000O0000OOO000 =False #line:309
                try :OO00OO0OOOOOOOOOO =OOOOO0O00OO00OOOO .findall ('<content>(.+?)</content>',OOO0OOOOOOO0OOO0O )[0 ]#line:311
                except :OO00OO0OOOOOOOOOO ='0'#line:312
                if OO00OO0OOOOOOOOOO =='0':#line:313
                    try :OO00OO0OOOOOOOOOO =OOOOO0O00OO00OOOO .findall ('<content>(.+?)</content>',O0O000O00O00O00O0 )[0 ]#line:314
                    except :OO00OO0OOOOOOOOOO ='0'#line:315
                if not OO00OO0OOOOOOOOOO =='0':OO00OO0OOOOOOOOOO +='s'#line:316
                if 'tvshow'in OO00OO0OOOOOOOOOO and not OO00OO0OOOO0OO000 .strip ().endswith ('.xml'):#line:318
                    OO00OO0OOOO0OO000 ='<preset>tvindexer</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OO00OO0OOOO0OO000 ,OO000000O0OOO00O0 ,OOOO0OOO000000O00 ,OOO0OOOOOOO0OOO0O )#line:319
                    OOOO0O0OOOOOOO0O0 ='tvtuner'#line:320
                if 'tvtuner'in OO00OO0OOOOOOOOOO and not OO00OO0OOOO0OO000 .strip ().endswith ('.xml'):#line:322
                    OO00OO0OOOO0OO000 ='<preset>tvtuner</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OO00OO0OOOO0OO000 ,OO000000O0OOO00O0 ,OOOO0OOO000000O00 ,OOO0OOOOOOO0OOO0O )#line:323
                    OOOO0O0OOOOOOO0O0 ='tvtuner'#line:324
                try :OO0O00OOOOOOOO00O =OOOOO0O00OO00OOOO .findall ('<imdb>(.+?)</imdb>',OOO0OOOOOOO0OOO0O )[0 ]#line:326
                except :OO0O00OOOOOOOO00O ='0'#line:327
                try :O0000OO00O0O0OO0O =OOOOO0O00OO00OOOO .findall ('<tvdb>(.+?)</tvdb>',OOO0OOOOOOO0OOO0O )[0 ]#line:329
                except :O0000OO00O0O0OO0O ='0'#line:330
                try :O0OOOO00OO000OO00 =OOOOO0O00OO00OOOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',OOO0OOOOOOO0OOO0O )[0 ]#line:332
                except :O0OOOO00OO000OO00 ='0'#line:333
                try :OO0000O0O00OO0O0O =OOOOO0O00OO00OOOO .findall ('<title>(.+?)</title>',OOO0OOOOOOO0OOO0O )[0 ]#line:335
                except :OO0000O0O00OO0O0O ='0'#line:336
                if OO0000O0O00OO0O0O =='0'and not O0OOOO00OO000OO00 =='0':OO0000O0O00OO0O0O =O0OOOO00OO000OO00 #line:338
                try :OOO000OO000OOO000 =OOOOO0O00OO00OOOO .findall ('<year>(.+?)</year>',OOO0OOOOOOO0OOO0O )[0 ]#line:340
                except :OOO000OO000OOO000 ='0'#line:341
                try :OOOO00000O0OO00OO =OOOOO0O00OO00OOOO .findall ('<premiered>(.+?)</premiered>',OOO0OOOOOOO0OOO0O )[0 ]#line:343
                except :OOOO00000O0OO00OO ='0'#line:344
                try :OOO000OO000OOO00O =OOOOO0O00OO00OOOO .findall ('<season>(.+?)</season>',OOO0OOOOOOO0OOO0O )[0 ]#line:346
                except :OOO000OO000OOO00O ='0'#line:347
                try :O00OOO0O0OOO00OOO =OOOOO0O00OO00OOOO .findall ('<episode>(.+?)</episode>',OOO0OOOOOOO0OOO0O )[0 ]#line:349
                except :O00OOO0O0OOO00OOO ='0'#line:350
                OO000OO0OO0O0OOO0 .list .append ({'name':OOOOOO0OO00OO00O0 ,'vip':O00O0O0OOO0O0000O ,'url':OO00OO0OOOO0OO000 ,'action':OOOO0O0OOOOOOO0O0 ,'folder':O00000O0000OOO000 ,'poster':OO000000O0OOO00O0 ,'banner':'0','fanart':OOOO0OOO000000O00 ,'content':OO00OO0OOOOOOOOOO ,'imdb':OO0O00OOOOOOOO00O ,'tvdb':O0000OO00O0O0OO0O ,'tmdb':'0','title':OO0000O0O00OO0O0O ,'originaltitle':OO0000O0O00OO0O0O ,'tvshowtitle':O0OOOO00OO000OO00 ,'year':OOO000OO000OOO000 ,'premiered':OOOO00000O0OO00OO ,'season':OOO000OO000OOO00O ,'episode':O00OOO0O0OOO00OOO })#line:352
            except :#line:353
                pass #line:354
        OOOOO00OOO0O00000 .insert (OO000OO0OO0O0OOO0 .hash )#line:356
        return OO000OO0OO0O0OOO0 .list #line:358
    def account_filter (OO00O00O00OOO00OO ,O0O0O000000000O0O ):#line:361
        if (OOOOO00OOOO00000O .setting ('ustvnow_email')==''or OOOOO00OOOO00000O .setting ('ustvnow_pass')==''):#line:362
            O0O0O000000000O0O =OOOOO0O00OO00OOOO .sub ('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<','<',O0O0O000000000O0O )#line:363
        if (OOOOO00OOOO00000O .setting ('streamlive_user')==''or OOOOO00OOOO00000O .setting ('streamlive_pass')==''):#line:365
            O0O0O000000000O0O =OOOOO0O00OO00OOOO .sub ('http(?:s|)://(?:www\.|)streamlive\.to/.+?<','<',O0O0O000000000O0O )#line:366
        return O0O0O000000000O0O #line:368
    def worker (O0O0O00O000O00000 ):#line:371
        if not OOOOO00OOOO00000O .setting ('metadata')=='true':return #line:372
        O0O0O00O000O00000 .imdb_info_link ='http://www.omdbapi.com/?i=%s&plot=full&r=json'#line:374
        O0O0O00O000O00000 .tvmaze_info_link ='http://api.tvmaze.com/lookup/shows?thetvdb=%s'#line:375
        O0O0O00O000O00000 .lang ='en'#line:376
        O0O0O00O000O00000 .meta =[]#line:378
        O00OO00OOO0O0OOOO =len (O0O0O00O000O00000 .list )#line:379
        if O00OO00OOO0O0OOOO ==0 :return #line:380
        for O000000O0O000OOO0 in range (0 ,O00OO00OOO0O0OOOO ):O0O0O00O000O00000 .list [O000000O0O000OOO0 ].update ({'metacache':False })#line:382
        O0O0O00O000O00000 .list =O0O000000OO0OOOOO .fetch (O0O0O00O000O00000 .list ,O0O0O00O000O00000 .lang )#line:383
        O0O00O00O00OO000O =[O00000000OO000000 ['imdb']for O00000000OO000000 in O0O0O00O000O00000 .list ]#line:385
        O0O00O00O00OO000O =[OO000OOO00OO0O00O for O000OO00O0OOO0000 ,OO000OOO00OO0O00O in enumerate (O0O00O00O00OO000O )if OO000OOO00OO0O00O not in O0O00O00O00OO000O [:O000OO00O0OOO0000 ]]#line:386
        if len (O0O00O00O00OO000O )==1 :#line:387
                O0O0O00O000O00000 .movie_info (0 );O0O0O00O000O00000 .tv_info (0 )#line:388
                if O0O0O00O000O00000 .meta :O0O000000OO0OOOOO .insert (O0O0O00O000O00000 .meta )#line:389
        for O000000O0O000OOO0 in range (0 ,O00OO00OOO0O0OOOO ):O0O0O00O000O00000 .list [O000000O0O000OOO0 ].update ({'metacache':False })#line:391
        O0O0O00O000O00000 .list =O0O000000OO0OOOOO .fetch (O0O0O00O000O00000 .list ,O0O0O00O000O00000 .lang )#line:392
        for O0000000O0000OO0O in range (0 ,O00OO00OOO0O0OOOO ,50 ):#line:394
            OO0O0OOO000O00000 =[]#line:395
            for O000000O0O000OOO0 in range (O0000000O0000OO0O ,O0000000O0000OO0O +50 ):#line:396
                if O000000O0O000OOO0 <=O00OO00OOO0O0OOOO :OO0O0OOO000O00000 .append (OOO0O00OOO0000O0O .Thread (O0O0O00O000O00000 .movie_info ,O000000O0O000OOO0 ))#line:397
                if O000000O0O000OOO0 <=O00OO00OOO0O0OOOO :OO0O0OOO000O00000 .append (OOO0O00OOO0000O0O .Thread (O0O0O00O000O00000 .tv_info ,O000000O0O000OOO0 ))#line:398
            [O00OO00OO0O0O00OO .start ()for O00OO00OO0O0O00OO in OO0O0OOO000O00000 ]#line:399
            [OO0OOO00OOOOOO0O0 .join ()for OO0OOO00OOOOOO0O0 in OO0O0OOO000O00000 ]#line:400
        if O0O0O00O000O00000 .meta :O0O000000OO0OOOOO .insert (O0O0O00O000O00000 .meta )#line:402
    def movie_info (OO00OOOO00OO0OOOO ,OOO0OOOO0OOO0OOOO ):#line:405
        try :#line:406
            if OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ]['metacache']==True :raise Exception ()#line:407
            if not OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ]['content']=='movies':raise Exception ()#line:409
            O0OO0OO0000000000 =OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ]['imdb']#line:411
            if O0OO0OO0000000000 =='0':raise Exception ()#line:412
            OOOO000OOO0000O0O =OO00OOOO00OO0OOOO .imdb_info_link %O0OO0OO0000000000 #line:414
            O00OOOO0O00O0OO00 =O0000OO0O000O000O .request (OOOO000OOO0000O0O ,timeout ='10')#line:416
            O00OOOO0O00O0OO00 =OO0OO00OO00OO0O0O .loads (O00OOOO0O00O0OO00 )#line:417
            if 'Error'in O00OOOO0O00O0OO00 and 'incorrect imdb'in O00OOOO0O00O0OO00 ['Error'].lower ():#line:419
                return OO00OOOO00OO0OOOO .meta .append ({'imdb':O0OO0OO0000000000 ,'tmdb':'0','tvdb':'0','lang':OO00OOOO00OO0OOOO .lang ,'item':{'code':'0'}})#line:420
            OOOO0OOOOOOOOO0O0 =O00OOOO0O00O0OO00 ['Title']#line:422
            OOOO0OOOOOOOOO0O0 =OOOO0OOOOOOOOO0O0 .encode ('utf-8')#line:423
            if not OOOO0OOOOOOOOO0O0 =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'title':OOOO0OOOOOOOOO0O0 })#line:424
            OOOO00O00O0O0OOOO =O00OOOO0O00O0OO00 ['Year']#line:426
            OOOO00O00O0O0OOOO =OOOO00O00O0O0OOOO .encode ('utf-8')#line:427
            if not OOOO00O00O0O0OOOO =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'year':OOOO00O00O0O0OOOO })#line:428
            O0OO0OO0000000000 =O00OOOO0O00O0OO00 ['imdbID']#line:430
            if O0OO0OO0000000000 ==None or O0OO0OO0000000000 ==''or O0OO0OO0000000000 =='N/A':O0OO0OO0000000000 ='0'#line:431
            O0OO0OO0000000000 =O0OO0OO0000000000 .encode ('utf-8')#line:432
            if not O0OO0OO0000000000 =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'imdb':O0OO0OO0000000000 ,'code':O0OO0OO0000000000 })#line:433
            O0O00OOO0OO00OO00 =O00OOOO0O00O0OO00 ['Released']#line:435
            if O0O00OOO0OO00OO00 ==None or O0O00OOO0OO00OO00 ==''or O0O00OOO0OO00OO00 =='N/A':O0O00OOO0OO00OO00 ='0'#line:436
            O0O00OOO0OO00OO00 =OOOOO0O00OO00OOOO .findall ('(\d*) (.+?) (\d*)',O0O00OOO0OO00OO00 )#line:437
            try :O0O00OOO0OO00OO00 ='%s-%s-%s'%(O0O00OOO0OO00OO00 [0 ][2 ],{'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}[O0O00OOO0OO00OO00 [0 ][1 ]],O0O00OOO0OO00OO00 [0 ][0 ])#line:438
            except :O0O00OOO0OO00OO00 ='0'#line:439
            O0O00OOO0OO00OO00 =O0O00OOO0OO00OO00 .encode ('utf-8')#line:440
            if not O0O00OOO0OO00OO00 =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'premiered':O0O00OOO0OO00OO00 })#line:441
            OOO00OO0OOOOOOO0O =O00OOOO0O00O0OO00 ['Genre']#line:443
            if OOO00OO0OOOOOOO0O ==None or OOO00OO0OOOOOOO0O ==''or OOO00OO0OOOOOOO0O =='N/A':OOO00OO0OOOOOOO0O ='0'#line:444
            OOO00OO0OOOOOOO0O =OOO00OO0OOOOOOO0O .replace (', ',' / ')#line:445
            OOO00OO0OOOOOOO0O =OOO00OO0OOOOOOO0O .encode ('utf-8')#line:446
            if not OOO00OO0OOOOOOO0O =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'genre':OOO00OO0OOOOOOO0O })#line:447
            OO0OO00OOO0OOO00O =O00OOOO0O00O0OO00 ['Runtime']#line:449
            if OO0OO00OOO0OOO00O ==None or OO0OO00OOO0OOO00O ==''or OO0OO00OOO0OOO00O =='N/A':OO0OO00OOO0OOO00O ='0'#line:450
            OO0OO00OOO0OOO00O =OOOOO0O00OO00OOOO .sub ('[^0-9]','',str (OO0OO00OOO0OOO00O ))#line:451
            try :OO0OO00OOO0OOO00O =str (int (OO0OO00OOO0OOO00O )*60 )#line:452
            except :pass #line:453
            OO0OO00OOO0OOO00O =OO0OO00OOO0OOO00O .encode ('utf-8')#line:454
            if not OO0OO00OOO0OOO00O =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'duration':OO0OO00OOO0OOO00O })#line:455
            O0000O0OOO0O0OO00 =O00OOOO0O00O0OO00 ['imdbRating']#line:457
            if O0000O0OOO0O0OO00 ==None or O0000O0OOO0O0OO00 ==''or O0000O0OOO0O0OO00 =='N/A'or O0000O0OOO0O0OO00 =='0.0':O0000O0OOO0O0OO00 ='0'#line:458
            O0000O0OOO0O0OO00 =O0000O0OOO0O0OO00 .encode ('utf-8')#line:459
            if not O0000O0OOO0O0OO00 =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'rating':O0000O0OOO0O0OO00 })#line:460
            O00O0OOOOO00O0O0O =O00OOOO0O00O0OO00 ['imdbVotes']#line:462
            try :O00O0OOOOO00O0O0O =str (format (int (O00O0OOOOO00O0O0O ),',d'))#line:463
            except :pass #line:464
            if O00O0OOOOO00O0O0O ==None or O00O0OOOOO00O0O0O ==''or O00O0OOOOO00O0O0O =='N/A':O00O0OOOOO00O0O0O ='0'#line:465
            O00O0OOOOO00O0O0O =O00O0OOOOO00O0O0O .encode ('utf-8')#line:466
            if not O00O0OOOOO00O0O0O =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'votes':O00O0OOOOO00O0O0O })#line:467
            O0O0O00OOOOOOO0OO =O00OOOO0O00O0OO00 ['Rated']#line:469
            if O0O0O00OOOOOOO0OO ==None or O0O0O00OOOOOOO0OO ==''or O0O0O00OOOOOOO0OO =='N/A':O0O0O00OOOOOOO0OO ='0'#line:470
            O0O0O00OOOOOOO0OO =O0O0O00OOOOOOO0OO .encode ('utf-8')#line:471
            if not O0O0O00OOOOOOO0OO =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'mpaa':O0O0O00OOOOOOO0OO })#line:472
            O000O0O00O0O0O0OO =O00OOOO0O00O0OO00 ['Director']#line:474
            if O000O0O00O0O0O0OO ==None or O000O0O00O0O0O0OO ==''or O000O0O00O0O0O0OO =='N/A':O000O0O00O0O0O0OO ='0'#line:475
            O000O0O00O0O0O0OO =O000O0O00O0O0O0OO .replace (', ',' / ')#line:476
            O000O0O00O0O0O0OO =OOOOO0O00OO00OOOO .sub (r'\(.*?\)','',O000O0O00O0O0O0OO )#line:477
            O000O0O00O0O0O0OO =' '.join (O000O0O00O0O0O0OO .split ())#line:478
            O000O0O00O0O0O0OO =O000O0O00O0O0O0OO .encode ('utf-8')#line:479
            if not O000O0O00O0O0O0OO =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'director':O000O0O00O0O0O0OO })#line:480
            OOO0O0OO0O0OOO00O =O00OOOO0O00O0OO00 ['Writer']#line:482
            if OOO0O0OO0O0OOO00O ==None or OOO0O0OO0O0OOO00O ==''or OOO0O0OO0O0OOO00O =='N/A':OOO0O0OO0O0OOO00O ='0'#line:483
            OOO0O0OO0O0OOO00O =OOO0O0OO0O0OOO00O .replace (', ',' / ')#line:484
            OOO0O0OO0O0OOO00O =OOOOO0O00OO00OOOO .sub (r'\(.*?\)','',OOO0O0OO0O0OOO00O )#line:485
            OOO0O0OO0O0OOO00O =' '.join (OOO0O0OO0O0OOO00O .split ())#line:486
            OOO0O0OO0O0OOO00O =OOO0O0OO0O0OOO00O .encode ('utf-8')#line:487
            if not OOO0O0OO0O0OOO00O =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'writer':OOO0O0OO0O0OOO00O })#line:488
            OO0OOO00OOO00O00O =O00OOOO0O00O0OO00 ['Actors']#line:490
            if OO0OOO00OOO00O00O ==None or OO0OOO00OOO00O00O ==''or OO0OOO00OOO00O00O =='N/A':OO0OOO00OOO00O00O ='0'#line:491
            OO0OOO00OOO00O00O =[OO0O00O0O0O0OO0O0 .strip ()for OO0O00O0O0O0OO0O0 in OO0OOO00OOO00O00O .split (',')if not OO0O00O0O0O0OO0O0 =='']#line:492
            try :OO0OOO00OOO00O00O =[(OOOOO000OO0O0O0O0 .encode ('utf-8'),'')for OOOOO000OO0O0O0O0 in OO0OOO00OOO00O00O ]#line:493
            except :OO0OOO00OOO00O00O =[]#line:494
            if OO0OOO00OOO00O00O ==[]:OO0OOO00OOO00O00O ='0'#line:495
            if not OO0OOO00OOO00O00O =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'cast':OO0OOO00OOO00O00O })#line:496
            OOO00OO00O0OOO000 =O00OOOO0O00O0OO00 ['Plot']#line:498
            if OOO00OO00O0OOO000 ==None or OOO00OO00O0OOO000 ==''or OOO00OO00O0OOO000 =='N/A':OOO00OO00O0OOO000 ='0'#line:499
            OOO00OO00O0OOO000 =O0000OO0O000O000O .replaceHTMLCodes (OOO00OO00O0OOO000 )#line:500
            OOO00OO00O0OOO000 =OOO00OO00O0OOO000 .encode ('utf-8')#line:501
            if not OOO00OO00O0OOO000 =='0':OO00OOOO00OO0OOOO .list [OOO0OOOO0OOO0OOOO ].update ({'plot':OOO00OO00O0OOO000 })#line:502
            OO00OOOO00OO0OOOO .meta .append ({'imdb':O0OO0OO0000000000 ,'tmdb':'0','tvdb':'0','lang':OO00OOOO00OO0OOOO .lang ,'item':{'title':OOOO0OOOOOOOOO0O0 ,'year':OOOO00O00O0O0OOOO ,'code':O0OO0OO0000000000 ,'imdb':O0OO0OO0000000000 ,'premiered':O0O00OOO0OO00OO00 ,'genre':OOO00OO0OOOOOOO0O ,'duration':OO0OO00OOO0OOO00O ,'rating':O0000O0OOO0O0OO00 ,'votes':O00O0OOOOO00O0O0O ,'mpaa':O0O0O00OOOOOOO0OO ,'director':O000O0O00O0O0O0OO ,'writer':OOO0O0OO0O0OOO00O ,'cast':OO0OOO00OOO00O00O ,'plot':OOO00OO00O0OOO000 }})#line:504
        except :#line:505
            pass #line:506
    def tv_info (OO0000000OOO000OO ,OO0O0O00OOO0OOO0O ):#line:509
        try :#line:510
            if OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ]['metacache']==True :raise Exception ()#line:511
            if not OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ]['content']in ['tvshows','seasons','episodes']:raise Exception ()#line:513
            OO0O00OOO0O00OOO0 =OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ]['tvdb']#line:515
            if OO0O00OOO0O00OOO0 =='0':raise Exception ()#line:516
            O0O000OOOOOOOO0OO =OO0000000OOO000OO .tvmaze_info_link %OO0O00OOO0O00OOO0 #line:518
            O000O0OOOO0000O00 =O0000OO0O000O000O .request (O0O000OOOOOOOO0OO ,output ='extended',error =True ,timeout ='10')#line:520
            if O000O0OOOO0000O00 [1 ]=='404':#line:522
                return OO0000000OOO000OO .meta .append ({'imdb':'0','tmdb':'0','tvdb':OO0O00OOO0O00OOO0 ,'lang':OO0000000OOO000OO .lang ,'item':{'code':'0'}})#line:523
            O000O0OOOO0000O00 =OO0OO00OO00OO0O0O .loads (O000O0OOOO0000O00 [0 ])#line:525
            O00O0O00OO0OOOO0O =O000O0OOOO0000O00 ['name']#line:527
            O00O0O00OO0OOOO0O =O00O0O00OO0OOOO0O .encode ('utf-8')#line:528
            if not O00O0O00OO0OOOO0O =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'tvshowtitle':O00O0O00OO0OOOO0O })#line:529
            O0OO0O0000O0O00OO =O000O0OOOO0000O00 ['premiered']#line:531
            O0OO0O0000O0O00OO =OOOOO0O00OO00OOOO .findall ('(\d{4})',O0OO0O0000O0O00OO )[0 ]#line:532
            O0OO0O0000O0O00OO =O0OO0O0000O0O00OO .encode ('utf-8')#line:533
            if not O0OO0O0000O0O00OO =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'year':O0OO0O0000O0O00OO })#line:534
            try :OOO000O0OO0OOO000 =O000O0OOOO0000O00 ['externals']['imdb']#line:536
            except :OOO000O0OO0OOO000 ='0'#line:537
            if OOO000O0OO0OOO000 ==''or OOO000O0OO0OOO000 ==None :OOO000O0OO0OOO000 ='0'#line:538
            OOO000O0OO0OOO000 =OOO000O0OO0OOO000 .encode ('utf-8')#line:539
            if OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ]['imdb']=='0'and not OOO000O0OO0OOO000 =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'imdb':OOO000O0OO0OOO000 })#line:540
            try :OOO00OO000O000O00 =O000O0OOOO0000O00 ['network']['name']#line:542
            except :OOO00OO000O000O00 ='0'#line:543
            if OOO00OO000O000O00 ==''or OOO00OO000O000O00 ==None :OOO00OO000O000O00 ='0'#line:544
            OOO00OO000O000O00 =OOO00OO000O000O00 .encode ('utf-8')#line:545
            if not OOO00OO000O000O00 =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'studio':OOO00OO000O000O00 })#line:546
            OO0O000O0O00O0O0O =O000O0OOOO0000O00 ['genres']#line:548
            if OO0O000O0O00O0O0O ==''or OO0O000O0O00O0O0O ==None or OO0O000O0O00O0O0O ==[]:OO0O000O0O00O0O0O ='0'#line:549
            OO0O000O0O00O0O0O =' / '.join (OO0O000O0O00O0O0O )#line:550
            OO0O000O0O00O0O0O =OO0O000O0O00O0O0O .encode ('utf-8')#line:551
            if not OO0O000O0O00O0O0O =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'genre':OO0O000O0O00O0O0O })#line:552
            try :O0OOOOO000OO0O0OO =str (O000O0OOOO0000O00 ['runtime'])#line:554
            except :O0OOOOO000OO0O0OO ='0'#line:555
            if O0OOOOO000OO0O0OO ==''or O0OOOOO000OO0O0OO ==None :O0OOOOO000OO0O0OO ='0'#line:556
            try :O0OOOOO000OO0O0OO =str (int (O0OOOOO000OO0O0OO )*60 )#line:557
            except :pass #line:558
            O0OOOOO000OO0O0OO =O0OOOOO000OO0O0OO .encode ('utf-8')#line:559
            if not O0OOOOO000OO0O0OO =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'duration':O0OOOOO000OO0O0OO })#line:560
            OO00O00OOOO00O000 =str (O000O0OOOO0000O00 ['rating']['average'])#line:562
            if OO00O00OOOO00O000 ==''or OO00O00OOOO00O000 ==None :OO00O00OOOO00O000 ='0'#line:563
            OO00O00OOOO00O000 =OO00O00OOOO00O000 .encode ('utf-8')#line:564
            if not OO00O00OOOO00O000 =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'rating':OO00O00OOOO00O000 })#line:565
            O00O00O0OOO0OO0O0 =O000O0OOOO0000O00 ['summary']#line:567
            if O00O00O0OOO0OO0O0 ==''or O00O00O0OOO0OO0O0 ==None :O00O00O0OOO0OO0O0 ='0'#line:568
            O00O00O0OOO0OO0O0 =OOOOO0O00OO00OOOO .sub ('\n|<.+?>|</.+?>|.+?#\d*:','',O00O00O0OOO0OO0O0 )#line:569
            O00O00O0OOO0OO0O0 =O00O00O0OOO0OO0O0 .encode ('utf-8')#line:570
            if not O00O00O0OOO0OO0O0 =='0':OO0000000OOO000OO .list [OO0O0O00OOO0OOO0O ].update ({'plot':O00O00O0OOO0OO0O0 })#line:571
            OO0000000OOO000OO .meta .append ({'imdb':OOO000O0OO0OOO000 ,'tmdb':'0','tvdb':OO0O00OOO0O00OOO0 ,'lang':OO0000000OOO000OO .lang ,'item':{'tvshowtitle':O00O0O00OO0OOOO0O ,'year':O0OO0O0000O0O00OO ,'code':OOO000O0OO0OOO000 ,'imdb':OOO000O0OO0OOO000 ,'tvdb':OO0O00OOO0O00OOO0 ,'studio':OOO00OO000O000O00 ,'genre':OO0O000O0O00O0O0O ,'duration':O0OOOOO000OO0O0OO ,'rating':OO00O00OOOO00O000 ,'plot':O00O00O0OOO0OO0O0 }})#line:573
        except :#line:574
            pass #line:575
    def addDirectory (OOO0O0O00000OOOO0 ,O0000OO000000O0OO ,queue =False ):#line:578
        if O0000OO000000O0OO ==None or len (O0000OO000000O0OO )==0 :return #line:579
        OOOOOO00OOO000OO0 =O000OO0OOO000OOO0 .argv [0 ]#line:581
        OO0O0000O000O0OO0 =OO0OOOO0O0OOOO0O0 =OOOOO00OOOO00000O .addonInfo ('icon')#line:582
        O0OO0OO00O0O0O00O =OOOOO00OOOO00000O .addonInfo ('fanart')#line:583
        O0OO0OO0O0O0O0000 =OOOOO00OOOO00000O .playlist #line:585
        if not queue ==False :O0OO0OO0O0O0O0000 .clear ()#line:586
        try :OO0OOO00OOO00OO00 =True if 'testings.xml'in OOOOO00OOOO00000O .listDir (OOOOO00OOOO00000O .dataPath )[1 ]else False #line:588
        except :OO0OOO00OOO00OO00 =False #line:589
        O000OOO00O0OOO00O =[O00OOO00OOO0OOOOO ['content']for O00OOO00OOO0OOOOO in O0000OO000000O0OO if 'content'in O00OOO00OOO0OOOOO ]#line:591
        if 'movies'in O000OOO00O0OOO00O :O000OOO00O0OOO00O ='movies'#line:592
        elif 'tvshows'in O000OOO00O0OOO00O :O000OOO00O0OOO00O ='tvshows'#line:593
        elif 'seasons'in O000OOO00O0OOO00O :O000OOO00O0OOO00O ='seasons'#line:594
        elif 'episodes'in O000OOO00O0OOO00O :O000OOO00O0OOO00O ='episodes'#line:595
        elif 'addons'in O000OOO00O0OOO00O :O000OOO00O0OOO00O ='addons'#line:596
        else :O000OOO00O0OOO00O ='videos'#line:597
        for O000O0OOO0000OO00 in O0000OO000000O0OO :#line:599
            try :#line:600
                try :OO00OOOO000OO0000 =OOOOO00OOOO00000O .lang (int (O000O0OOO0000OO00 ['name'])).encode ('utf-8')#line:601
                except :OO00OOOO000OO0000 =O000O0OOO0000OO00 ['name']#line:602
                OOOO0OOO0000OOOO0 ='%s?action=%s'%(OOOOOO00OOO000OO0 ,O000O0OOO0000OO00 ['action'])#line:604
                try :OOOO0OOO0000OOOO0 +='&url=%s'%OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['url'])#line:605
                except :pass #line:606
                try :OOOO0OOO0000OOOO0 +='&content=%s'%OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['content'])#line:607
                except :pass #line:608
                if O000O0OOO0000OO00 ['action']=='plugin'and 'url'in O000O0OOO0000OO00 :OOOO0OOO0000OOOO0 =O000O0OOO0000OO00 ['url']#line:610
                try :OO000O000OOOO0OOO =dict (O000000O0OOO0O000 .parse_qsl (O000000O0OOO0O000 .urlparse (OOOO0OOO0000OOOO0 ).query ))['action']#line:612
                except :OO000O000OOOO0OOO =None #line:613
                if OO000O000OOOO0OOO =='developer'and not OO0OOO00OOO00OO00 ==True :raise Exception ()#line:614
                O0O0OOOOO0OO00O00 =O000O0OOO0000OO00 ['poster']if 'poster'in O000O0OOO0000OO00 else '0'#line:616
                OO0000O0O00O0O000 =O000O0OOO0000OO00 ['banner']if 'banner'in O000O0OOO0000OO00 else '0'#line:617
                O0000OOO000OO00OO =O000O0OOO0000OO00 ['fanart']if 'fanart'in O000O0OOO0000OO00 else '0'#line:618
                if O0O0OOOOO0OO00O00 =='0':O0O0OOOOO0OO00O00 =OO0O0000O000O0OO0 #line:619
                if OO0000O0O00O0O000 =='0'and O0O0OOOOO0OO00O00 =='0':OO0000O0O00O0O000 =OO0OOOO0O0OOOO0O0 #line:620
                elif OO0000O0O00O0O000 =='0':OO0000O0O00O0O000 =O0O0OOOOO0OO00O00 #line:621
                OO0O0OO0OOO0OO0OO =O000O0OOO0000OO00 ['content']if 'content'in O000O0OOO0000OO00 else '0'#line:623
                O0OO0OO0OO0000OO0 =O000O0OOO0000OO00 ['folder']if 'folder'in O000O0OOO0000OO00 else True #line:625
                O0O0000OO0OOO0O0O =dict ((OO0O0O000OO000O0O ,OO0O0OOOOO000O0OO )for OO0O0O000OO000O0O ,OO0O0OOOOO000O0OO in O000O0OOO0000OO00 .iteritems ()if not OO0O0OOOOO000O0OO =='0')#line:627
                OOOOOOO000000O0O0 =[]#line:629
                if OO0O0OO0OOO0OO0OO in ['movies','tvshows']:#line:631
                    O0O0000OO0OOO0O0O .update ({'trailer':'%s?action=trailer&name=%s'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (OO00OOOO000OO0000 ))})#line:632
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30707 ).encode ('utf-8'),'RunPlugin(%s?action=trailer&name=%s)'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (OO00OOOO000OO0000 ))))#line:633
                if OO0O0OO0OOO0OO0OO in ['movies','tvshows','seasons','episodes']:#line:635
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30708 ).encode ('utf-8'),'XBMC.Action(Info)'))#line:636
                if (O0OO0OO0OO0000OO0 ==False and not '|regex='in str (O000O0OOO0000OO00 .get ('url')))or (O0OO0OO0OO0000OO0 ==True and OO0O0OO0OOO0OO0OO in ['tvshows','seasons']):#line:638
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30723 ).encode ('utf-8'),'RunPlugin(%s?action=queueItem)'%OOOOOO00OOO000OO0 ))#line:639
                if OO0O0OO0OOO0OO0OO =='movies':#line:641
                    try :OO00O000OOO0O00OO ='%s (%s)'%(O000O0OOO0000OO00 ['title'],O000O0OOO0000OO00 ['year'])#line:642
                    except :OO00O000OOO0O00OO =OO00OOOO000OO0000 #line:643
                    try :OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (OO00O000OOO0O00OO ),OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['url']),OOO000O0O0O00OOOO .quote_plus (O0O0OOOOO0OO00O00 ))))#line:644
                    except :pass #line:645
                elif OO0O0OO0OOO0OO0OO =='episodes':#line:646
                    try :OO00O000OOO0O00OO ='%s S%02dE%02d'%(O000O0OOO0000OO00 ['tvshowtitle'],int (O000O0OOO0000OO00 ['season']),int (O000O0OOO0000OO00 ['episode']))#line:647
                    except :OO00O000OOO0O00OO =OO00OOOO000OO0000 #line:648
                    try :OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (OO00O000OOO0O00OO ),OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['url']),OOO000O0O0O00OOOO .quote_plus (O0O0OOOOO0OO00O00 ))))#line:649
                    except :pass #line:650
                elif OO0O0OO0OOO0OO0OO =='songs':#line:651
                    try :OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (OO00OOOO000OO0000 ),OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['url']),OOO000O0O0O00OOOO .quote_plus (O0O0OOOOO0OO00O00 ))))#line:652
                    except :pass #line:653
                if O000OOO00O0OOO00O =='movies':#line:655
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30711 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=movies)'%OOOOOO00OOO000OO0 ))#line:656
                elif O000OOO00O0OOO00O =='tvshows':#line:657
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30712 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=tvshows)'%OOOOOO00OOO000OO0 ))#line:658
                elif O000OOO00O0OOO00O =='seasons':#line:659
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30713 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=seasons)'%OOOOOO00OOO000OO0 ))#line:660
                elif O000OOO00O0OOO00O =='episodes':#line:661
                    OOOOOOO000000O0O0 .append ((OOOOO00OOOO00000O .lang (30714 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=episodes)'%OOOOOO00OOO000OO0 ))#line:662
                if OO0OOO00OOO00OO00 ==True :#line:664
                    try :OOOOOOO000000O0O0 .append (('Open in browser','RunPlugin(%s?action=browser&url=%s)'%(OOOOOO00OOO000OO0 ,OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['url']))))#line:665
                    except :pass #line:666
                O0O0OO0O0O0OOO00O =OOOOO00OOOO00000O .item (label =OO00OOOO000OO0000 ,iconImage =O0O0OOOOO0OO00O00 ,thumbnailImage =O0O0OOOOO0OO00O00 )#line:669
                try :O0O0OO0O0O0OOO00O .setArt ({'poster':O0O0OOOOO0OO00O00 ,'tvshow.poster':O0O0OOOOO0OO00O00 ,'season.poster':O0O0OOOOO0OO00O00 ,'banner':OO0000O0O00O0O000 ,'tvshow.banner':OO0000O0O00O0O000 ,'season.banner':OO0000O0O00O0O000 })#line:671
                except :pass #line:672
                if not O0000OOO000OO00OO =='0':#line:674
                    O0O0OO0O0O0OOO00O .setProperty ('Fanart_Image',O0000OOO000OO00OO )#line:675
                elif not O0OO0OO00O0O0O00O ==None :#line:676
                    O0O0OO0O0O0OOO00O .setProperty ('Fanart_Image',O0OO0OO00O0O0O00O )#line:677
                if queue ==False :#line:679
                    O0O0OO0O0O0OOO00O .setInfo (type ='Video',infoLabels =O0O0000OO0OOO0O0O )#line:680
                    O0O0OO0O0O0OOO00O .addContextMenuItems (OOOOOOO000000O0O0 )#line:681
                    OOOOO00OOOO00000O .addItem (handle =int (O000OO0OOO000OOO0 .argv [1 ]),url =OOOO0OOO0000OOOO0 ,listitem =O0O0OO0O0O0OOO00O ,isFolder =O0OO0OO0OO0000OO0 )#line:682
                else :#line:683
                    O0O0OO0O0O0OOO00O .setInfo (type ='Video',infoLabels =O0O0000OO0OOO0O0O )#line:684
                    O0OO0OO0O0O0O0000 .add (url =OOOO0OOO0000OOOO0 ,listitem =O0O0OO0O0O0OOO00O )#line:685
            except :#line:686
                pass #line:687
        if not queue ==False :#line:689
            return OOOOO00OOOO00000O .player .play (O0OO0OO0O0O0O0000 )#line:690
        try :#line:692
            O000O0OOO0000OO00 =O0000OO000000O0OO [0 ]#line:693
            if O000O0OOO0000OO00 ['next']=='':raise Exception ()#line:694
            OOOO0OOO0000OOOO0 ='%s?action=%s&url=%s'%(OOOOOO00OOO000OO0 ,O000O0OOO0000OO00 ['nextaction'],OOO000O0O0O00OOOO .quote_plus (O000O0OOO0000OO00 ['next']))#line:695
            O0O0OO0O0O0OOO00O =OOOOO00OOOO00000O .item (label =OOOOO00OOOO00000O .lang (30500 ).encode ('utf-8'))#line:696
            O0O0OO0O0O0OOO00O .setArt ({'addonPoster':OO0O0000O000O0OO0 ,'thumb':OO0O0000O000O0OO0 ,'poster':OO0O0000O000O0OO0 ,'tvshow.poster':OO0O0000O000O0OO0 ,'season.poster':OO0O0000O000O0OO0 ,'banner':OO0O0000O000O0OO0 ,'tvshow.banner':OO0O0000O000O0OO0 ,'season.banner':OO0O0000O000O0OO0 })#line:697
            O0O0OO0O0O0OOO00O .setProperty ('addonFanart_Image',O0OO0OO00O0O0O00O )#line:698
            OOOOO00OOOO00000O .addItem (handle =int (O000OO0OOO000OOO0 .argv [1 ]),url =OOOO0OOO0000OOOO0 ,listitem =O0O0OO0O0O0OOO00O ,isFolder =True )#line:699
        except :#line:700
            pass #line:701
        if not O000OOO00O0OOO00O ==None :OOOOO00OOOO00000O .content (int (O000OO0OOO000OOO0 .argv [1 ]),O000OOO00O0OOO00O )#line:703
        OOOOO00OOOO00000O .directory (int (O000OO0OOO000OOO0 .argv [1 ]),cacheToDisc =True )#line:704
        if O000OOO00O0OOO00O in ['movies','tvshows','seasons','episodes']:#line:705
            OO0O0O00O00O000OO .setView (O000OOO00O0OOO00O ,{'skin.estuary':55 })#line:706
class resolver :#line:710
    def browser (O0O0O0OO00OOOOOOO ,OO00OO0O00OO00O00 ):#line:711
        try :#line:712
            OO00OO0O00OO00O00 =O0O0O0OO00OOOOOOO .get (OO00OO0O00OO00O00 )#line:713
            if OO00OO0O00OO00O00 ==False :return #line:714
            OOOOO00OOOO00000O .execute ('RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)'%OOO000O0O0O00OOOO .quote_plus (OO00OO0O00OO00O00 ))#line:715
        except :#line:716
            pass #line:717
    def link (O0OOO0OO00O0OO00O ,OO0OOOOO00OO0000O ):#line:720
        try :#line:721
            OO0OOOOO00OO0000O =O0OOO0OO00O0OO00O .get (OO0OOOOO00OO0000O )#line:722
            if OO0OOOOO00OO0000O ==False :return #line:723
            OOOOO00OOOO00000O .execute ('ActivateWindow(busydialog)')#line:725
            OO0OOOOO00OO0000O =O0OOO0OO00O0OO00O .process (OO0OOOOO00OO0000O )#line:726
            OOOOO00OOOO00000O .execute ('Dialog.Close(busydialog)')#line:727
            if OO0OOOOO00OO0000O ==None :return OOOOO00OOOO00000O .infoDialog (OOOOO00OOOO00000O .lang (30705 ).encode ('utf-8'))#line:729
            return OO0OOOOO00OO0000O #line:730
        except :#line:731
            pass #line:732
    def get (O000000OO0OOO0OOO ,O0OOOOOOO0O00O0O0 ):#line:735
        try :#line:736
            OO00OO00O0O0O0OO0 =OOOOO0O00OO00OOOO .compile ('<sublink(?:\s+name=|)(?:\'|\"|)(.*?)(?:\'|\"|)>(.+?)</sublink>').findall (O0OOOOOOO0O00O0O0 )#line:737
            if len (OO00OO00O0O0O0OO0 )==0 :return O0OOOOOOO0O00O0O0 #line:739
            if len (OO00OO00O0O0O0OO0 )==1 :return OO00OO00O0O0O0OO0 [0 ][1 ]#line:740
            OO00OO00O0O0O0OO0 =[('Link %s'%(int (OO00OO00O0O0O0OO0 .index (OO0O00O00OOO000OO ))+1 )if OO0O00O00OOO000OO [0 ]==''else OO0O00O00OOO000OO [0 ],OO0O00O00OOO000OO [1 ])for OO0O00O00OOO000OO in OO00OO00O0O0O0OO0 ]#line:742
            O0O00O0OO0O0000O0 =OOOOO00OOOO00000O .selectDialog ([O0OO0OO0000O0O0O0 [0 ]for O0OO0OO0000O0O0O0 in OO00OO00O0O0O0OO0 ],OOOOO00OOOO00000O .infoLabel ('listitem.label'))#line:744
            if O0O00O0OO0O0000O0 ==-1 :return False #line:746
            else :return OO00OO00O0O0O0OO0 [O0O00O0OO0O0000O0 ][1 ]#line:747
        except :#line:748
            pass #line:749
    def f4m (O00OO0000O000OOO0 ,OO000OOO00O0O0OOO ,O0O0OO0OO0OOOOOO0 ):#line:752
            try :#line:753
                if not any (O00O00O0O0O0000O0 in OO000OOO00O0O0OOO for O00O00O0O0O0000O0 in ['.f4m','.ts']):raise Exception ()#line:754
                O00OOOOOO00OOOO00 =OO000OOO00O0O0OOO .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:755
                if not O00OOOOOO00OOOO00 in ['f4m','ts']:raise Exception ()#line:756
                O0OOO0000000OOO00 =O000000O0OOO0O000 .parse_qs (OO000OOO00O0O0OOO )#line:758
                try :O0OOO00OO0O0OO00O =O0OOO0000000OOO00 ['proxy'][0 ]#line:760
                except :O0OOO00OO0O0OO00O =None #line:761
                try :O00000OOOO0O0OO00 =OO0OO00OO00OO0O0O .loads (O0OOO0000000OOO00 ['proxy_for_chunks'][0 ])#line:763
                except :O00000OOOO0O0OO00 =True #line:764
                try :O0OO0OOO00OOO00OO =int (O0OOO0000000OOO00 ['maxbitrate'][0 ])#line:766
                except :O0OO0OOO00OOO00OO =0 #line:767
                try :OOOOO000O0O00O00O =OO0OO00OO00OO0O0O .loads (O0OOO0000000OOO00 ['simpledownloader'][0 ])#line:769
                except :OOOOO000O0O00O00O =False #line:770
                try :O0O00OO0000O0000O =O0OOO0000000OOO00 ['auth'][0 ]#line:772
                except :O0O00OO0000O0000O =''#line:773
                try :O000O0O0OO00O00O0 =O0OOO0000000OOO00 ['streamtype'][0 ]#line:775
                except :O000O0O0OO00O00O0 ='TSDOWNLOADER'if O00OOOOOO00OOOO00 =='ts'else 'HDS'#line:776
                try :OOO00OO000000000O =O0OOO0000000OOO00 ['swf'][0 ]#line:778
                except :OOO00OO000000000O =None #line:779
                from F4mProxy import f4mProxyHelper as O000000OO0000OO00 #line:781
                return O000000OO0000OO00 ().playF4mLink (OO000OOO00O0O0OOO ,O0O0OO0OO0OOOOOO0 ,O0OOO00OO0O0OO00O ,O00000OOOO0O0OO00 ,O0OO0OOO00OOO00OO ,OOOOO000O0O00O00O ,O0O00OO0000O0000O ,O000O0O0OO00O00O0 ,False ,OOO00OO000000000O )#line:782
            except :#line:783
                pass #line:784
    def process (OO000O0OO0OO000O0 ,OO000O0O00000000O ,direct =True ):#line:787
        try :#line:788
            if not any (OOO0OO00OO00OOOO0 in OO000O0O00000000O for OOO0OO00OO00OOOO0 in ['.jpg','.png','.gif']):raise Exception ()#line:789
            O000OO00O000OO00O =OO000O0O00000000O .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:790
            if not O000OO00O000OO00O in ['jpg','png','gif']:raise Exception ()#line:791
            try :#line:792
                OO0O0000O000OOO00 =O00O00O0000OO00OO .path .join (OOOOO00OOOO00000O .dataPath ,'img')#line:793
                OOOOO00OOOO00000O .deleteFile (OO0O0000O000OOO00 )#line:794
                OO0OO0000OOOO0O0O =OOOOO00OOOO00000O .openFile (OO0O0000O000OOO00 ,'w')#line:795
                OO0OO0000OOOO0O0O .write (O0000OO0O000O000O .request (OO000O0O00000000O ))#line:796
                OO0OO0000OOOO0O0O .close ()#line:797
                OOOOO00OOOO00000O .execute ('ShowPicture("%s")'%OO0O0000O000OOO00 )#line:798
                return False #line:799
            except :#line:800
                return #line:801
        except :#line:802
            pass #line:803
        try :#line:805
            OOOOOO0O00O0000OO ,O0O0OOOO0O0OO0O0O =OOOOO0O00OO00OOOO .findall ('(.+?)\|regex=(.+?)$',OO000O0O00000000O )[0 ]#line:806
            O0O0OOOO0O0OO0O0O =OOOOO00OOO0O00000 .fetch (O0O0OOOO0O0OO0O0O )#line:807
            OOOOOO0O00O0000OO +=OOO000O0O0O00OOOO .unquote_plus (O0O0OOOO0O0OO0O0O )#line:808
            if not '</regex>'in OOOOOO0O00O0000OO :raise Exception ()#line:809
            OO0OO00OOO00O0OO0 =OOOOO00OOO0O00000 .resolve (OOOOOO0O00O0000OO )#line:810
            if not OO0OO00OOO00O0OO0 ==None :OO000O0O00000000O =OO0OO00OOO00O0OO0 #line:811
        except :#line:812
            pass #line:813
        try :#line:815
            if not OO000O0O00000000O .startswith ('rtmp'):raise Exception ()#line:816
            if len (OOOOO0O00OO00OOOO .compile ('\s*timeout=(\d*)').findall (OO000O0O00000000O ))==0 :OO000O0O00000000O +=' timeout=10'#line:817
            return OO000O0O00000000O #line:818
        except :#line:819
            pass #line:820
        try :#line:822
            if not any (O0OOO0000OOO00OO0 in OO000O0O00000000O for O0OOO0000OOO00OO0 in ['.m3u8','.f4m','.ts']):raise Exception ()#line:823
            O000OO00O000OO00O =OO000O0O00000000O .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:824
            if not O000OO00O000OO00O in ['m3u8','f4m','ts']:raise Exception ()#line:825
            return OO000O0O00000000O #line:826
        except :#line:827
            pass #line:828
        try :#line:830
            OO00OOO0OOO0O0OOO =OOOOO0O00OO00OOOO .findall ('<preset>(.+?)</preset>',OO000O0O00000000O )[0 ]#line:831
            if not 'search'in OO00OOO0OOO0O0OOO :raise Exception ()#line:833
            O0OOOOOOOOOOOO0OO ,O00O00O0OO00OO0OO ,O0O0O00OO00O0OO00 =OOOOO0O00OO00OOOO .findall ('<title>(.+?)</title>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<year>(.+?)</year>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<imdb>(.+?)</imdb>',OO000O0O00000000O )[0 ]#line:835
            try :OOO0O0OO00O000OO0 ,O00O000O000O0000O ,O0OOO0O0O00OO00O0 ,OOO0O00O00O0OOO00 ,O00O000O0OO00O0OO =OOOOO0O00OO00OOOO .findall ('<tvdb>(.+?)</tvdb>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<premiered>(.+?)</premiered>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<season>(.+?)</season>',OO000O0O00000000O )[0 ],OOOOO0O00OO00OOOO .findall ('<episode>(.+?)</episode>',OO000O0O00000000O )[0 ]#line:837
            except :OOO0O0OO00O000OO0 =O00O000O000O0000O =O0OOO0O0O00OO00O0 =OOO0O00O00O0OOO00 =O00O000O0OO00O0OO =None #line:838
            direct =False #line:840
            O0O00O0OO0O0OOOO0 ='HD'if not OO00OOO0OOO0O0OOO =='searchsd'else 'SD'#line:842
            from resources .lib .sources import sources as OO00OOOOOOO0O0OOO #line:844
            OO0OO00OOO00O0OO0 =OO00OOOOOOO0O0OOO ().getSources (O0OOOOOOOOOOOO0OO ,O00O00O0OO00OO0OO ,O0O0O00OO00O0OO00 ,OOO0O0OO00O000OO0 ,OOO0O00O00O0OOO00 ,O00O000O0OO00O0OO ,O00O000O000O0000O ,O0OOO0O0O00OO00O0 ,O0O00O0OO0O0OOOO0 )#line:846
            if not OO0OO00OOO00O0OO0 ==None :return OO0OO00OOO00O0OO0 #line:848
        except :#line:849
            pass #line:850
        try :#line:852
            from resources .lib .sources import sources as OO00OOOOOOO0O0OOO #line:853
            OO0OO00OOO00O0OO0 =OO00OOOOOOO0O0OOO ().getURISource (OO000O0O00000000O )#line:855
            if not OO0OO00OOO00O0OO0 ==False :direct =False #line:857
            if OO0OO00OOO00O0OO0 ==None or OO0OO00OOO00O0OO0 ==False :raise Exception ()#line:858
            return OO0OO00OOO00O0OO0 #line:860
        except :#line:861
            pass #line:862
        try :#line:864
            if not '.google.com'in OO000O0O00000000O :raise Exception ()#line:865
            from resources .lib .modules import directstream as O0OOO0OOOOOOOO000 #line:866
            OO0OO00OOO00O0OO0 =O0OOO0OOOOOOOO000 .google (OO000O0O00000000O )[0 ]['url']#line:867
            return OO0OO00OOO00O0OO0 #line:868
        except :#line:869
            pass #line:870
        try :#line:872
            if not 'filmon.com/'in OO000O0O00000000O :raise Exception ()#line:873
            from resources .lib .modules import filmon as OOOOO00OO000OOO00 #line:874
            OO0OO00OOO00O0OO0 =OOOOO00OO000OOO00 .resolve (OO000O0O00000000O )#line:875
            return OO0OO00OOO00O0OO0 #line:876
        except :#line:877
            pass #line:878
        try :#line:880
            import urlresolver as OOO0OOO0O0O00OO00 #line:881
            OO00OOOOO0OOO0OOO =OOO0OOO0O0O00OO00 .HostedMediaFile (url =OO000O0O00000000O )#line:883
            if OO00OOOOO0OOO0OOO .valid_url ()==False :raise Exception ()#line:885
            direct =False ;OO0OO00OOO00O0OO0 =OO00OOOOO0OOO0OOO .resolve ()#line:887
            if not OO0OO00OOO00O0OO0 ==False :return OO0OO00OOO00O0OO0 #line:889
        except :#line:890
            pass #line:891
        if direct ==True :return OO000O0O00000000O #line:893
class player (O0OO000O000O0O000 .Player ):#line:896
    def __init__ (O0OOO00O0OOOO0OOO ):#line:897
        O0OO000O000O0O000 .Player .__init__ (O0OOO00O0OOOO0OOO )#line:898
    def play (OOOOO00OOOOOOO000 ,OOOO00000OOOO0OO0 ,content =None ):#line:901
        try :#line:902
            OOOO0OO0000O000OO =OOOO00000OOOO0OO0 #line:903
            OOOO00000OOOO0OO0 =resolver ().get (OOOO00000OOOO0OO0 )#line:905
            if OOOO00000OOOO0OO0 ==False :return #line:906
            OOOOO00OOOO00000O .execute ('ActivateWindow(busydialog)')#line:908
            OOOO00000OOOO0OO0 =resolver ().process (OOOO00000OOOO0OO0 )#line:909
            OOOOO00OOOO00000O .execute ('Dialog.Close(busydialog)')#line:910
            if OOOO00000OOOO0OO0 ==None :return OOOOO00OOOO00000O .infoDialog (OOOOO00OOOO00000O .lang (30705 ).encode ('utf-8'))#line:912
            if OOOO00000OOOO0OO0 ==False :return #line:913
            OO0OO00O00OO00000 ={}#line:915
            for OO0OO00OO0000O00O in ['title','originaltitle','tvshowtitle','year','season','episode','genre','rating','votes','director','writer','plot','tagline']:#line:916
                try :OO0OO00O00OO00000 [OO0OO00OO0000O00O ]=OOOOO00OOOO00000O .infoLabel ('listitem.%s'%OO0OO00OO0000O00O )#line:917
                except :pass #line:918
            OO0OO00O00OO00000 =dict ((OO00OOOO000000O0O ,OOO0O0OOOOOO0O0OO )for OO00OOOO000000O0O ,OOO0O0OOOOOO0O0OO in OO0OO00O00OO00000 .iteritems ()if not OOO0O0OOOOOO0O0OO =='')#line:919
            if not 'title'in OO0OO00O00OO00000 :OO0OO00O00OO00000 ['title']=OOOOO00OOOO00000O .infoLabel ('listitem.label')#line:920
            OOO0O0O0O000000OO =OOOOO00OOOO00000O .infoLabel ('listitem.icon')#line:921
            OOOOO00OOOOOOO000 .name =OO0OO00O00OO00000 ['title'];OOOOO00OOOOOOO000 .year =OO0OO00O00OO00000 ['year']if 'year'in OO0OO00O00OO00000 else '0'#line:924
            OOOOO00OOOOOOO000 .getbookmark =True if (content =='movies'or content =='episodes')else False #line:926
            OOOOO00OOOOOOO000 .offset =bookmarks ().get (OOOOO00OOOOOOO000 .name ,OOOOO00OOOOOOO000 .year )#line:928
            O0000OOO00O0OOO00 =resolver ().f4m (OOOO00000OOOO0OO0 ,OOOOO00OOOOOOO000 .name )#line:930
            if not O0000OOO00O0OOO00 ==None :return #line:931
            OO0OOO00000O0OOOO =OOOOO00OOOO00000O .item (path =OOOO00000OOOO0OO0 ,iconImage =OOO0O0O0O000000OO ,thumbnailImage =OOO0O0O0O000000OO )#line:934
            try :OO0OOO00000O0OOOO .setArt ({'icon':OOO0O0O0O000000OO })#line:935
            except :pass #line:936
            OO0OOO00000O0OOOO .setInfo (type ='Video',infoLabels =OO0OO00O00OO00000 )#line:937
            OOOOO00OOOO00000O .player .play (OOOO00000OOOO0OO0 ,OO0OOO00000O0OOOO )#line:938
            OOOOO00OOOO00000O .resolve (int (O000OO0OOO000OOO0 .argv [1 ]),True ,OO0OOO00000O0OOOO )#line:939
            OOOOO00OOOOOOO000 .totalTime =0 ;OOOOO00OOOOOOO000 .currentTime =0 #line:941
            for OO0OO00OO0000O00O in range (0 ,240 ):#line:943
                if OOOOO00OOOOOOO000 .isPlayingVideo ():break #line:944
                OOOOO00OOOO00000O .sleep (1000 )#line:945
            while OOOOO00OOOOOOO000 .isPlayingVideo ():#line:946
                try :#line:947
                    OOOOO00OOOOOOO000 .totalTime =OOOOO00OOOOOOO000 .getTotalTime ()#line:948
                    OOOOO00OOOOOOO000 .currentTime =OOOOO00OOOOOOO000 .getTime ()#line:949
                except :#line:950
                    pass #line:951
                OOOOO00OOOO00000O .sleep (2000 )#line:952
            OOOOO00OOOO00000O .sleep (5000 )#line:953
        except :#line:954
            pass #line:955
    def onPlayBackStarted (O00O000O0OO000000 ):#line:958
        OOOOO00OOOO00000O .execute ('Dialog.Close(all,true)')#line:959
        if O00O000O0OO000000 .getbookmark ==True and not O00O000O0OO000000 .offset =='0':#line:960
            O00O000O0OO000000 .seekTime (float (O00O000O0OO000000 .offset ))#line:961
    def onPlayBackStopped (O00OO00O000O0000O ):#line:964
        if O00OO00O000O0000O .getbookmark ==True :#line:965
            bookmarks ().reset (O00OO00O000O0000O .currentTime ,O00OO00O000O0000O .totalTime ,O00OO00O000O0000O .name ,O00OO00O000O0000O .year )#line:966
    def onPlayBackEnded (O00OO000000OOO0OO ):#line:969
        O00OO000000OOO0OO .onPlayBackStopped ()#line:970
class bookmarks :#line:974
    def get (O00OO00OO0O0O00O0 ,OOOOO00OO0O000OOO ,year ='0'):#line:975
        try :#line:976
            OOOOO000000O000O0 ='0'#line:977
            O000OO00O0OOO000O =O00OO0000000OO00O .md5 ()#line:981
            for O0OOO0OO0O0OOO000 in OOOOO00OO0O000OOO :O000OO00O0OOO000O .update (str (O0OOO0OO0O0OOO000 ))#line:982
            for O0OOO0OO0O0OOO000 in year :O000OO00O0OOO000O .update (str (O0OOO0OO0O0OOO000 ))#line:983
            O000OO00O0OOO000O =str (O000OO00O0OOO000O .hexdigest ())#line:984
            OO000O00O00O0OO0O =OOOO0OOO000O00O00 .connect (OOOOO00OOOO00000O .bookmarksFile )#line:986
            O0O00O00O0O00O00O =OO000O00O00O0OO0O .cursor ()#line:987
            O0O00O00O0O00O00O .execute ("SELECT * FROM bookmark WHERE idFile = '%s'"%O000OO00O0OOO000O )#line:988
            OOO0000OOO000O0OO =O0O00O00O0O00O00O .fetchone ()#line:989
            O00OO00OO0O0O00O0 .offset =str (OOO0000OOO000O0OO [1 ])#line:990
            OO000O00O00O0OO0O .commit ()#line:991
            if O00OO00OO0O0O00O0 .offset =='0':raise Exception ()#line:993
            OOOO00O000OOOO000 ,O0O0OOO000OO0O00O =divmod (float (O00OO00OO0O0O00O0 .offset ),60 );OOO0OO000OO0O0O0O ,OOOO00O000OOOO000 =divmod (OOOO00O000OOOO000 ,60 )#line:995
            OO000O00OOOO0O00O ='%02d:%02d:%02d'%(OOO0OO000OO0O0O0O ,OOOO00O000OOOO000 ,O0O0OOO000OO0O00O )#line:996
            OO000O00OOOO0O00O =(OOOOO00OOOO00000O .lang (32502 )%OO000O00OOOO0O00O ).encode ('utf-8')#line:997
            try :O0O00O0OO0O00OO00 =OOOOO00OOOO00000O .dialog .contextmenu ([OO000O00OOOO0O00O ,OOOOO00OOOO00000O .lang (32501 ).encode ('utf-8'),])#line:999
            except :O0O00O0OO0O00OO00 =OOOOO00OOOO00000O .yesnoDialog (OO000O00OOOO0O00O ,'','',str (OOOOO00OO0O000OOO ),OOOOO00OOOO00000O .lang (32503 ).encode ('utf-8'),OOOOO00OOOO00000O .lang (32501 ).encode ('utf-8'))#line:1000
            if O0O00O0OO0O00OO00 :O00OO00OO0O0O00O0 .offset ='0'#line:1002
            return O00OO00OO0O0O00O0 .offset #line:1004
        except :#line:1005
            return OOOOO000000O000O0 #line:1006
    def reset (OO0O00OOOO000OOO0 ,OOOO00OO000O00OOO ,O0OO0O000OO0O000O ,O00O0000O000OO00O ,year ='0'):#line:1009
        try :#line:1010
            OO00O00O0O00000O0 =str (OOOO00OO000O00OOO )#line:1013
            O00000000O00O0O00 =int (OOOO00OO000O00OOO )>180 and (OOOO00OO000O00OOO /O0OO0O000OO0O000O )<=.92 #line:1014
            OOO000OOO0O00OO0O =O00OO0000000OO00O .md5 ()#line:1016
            for OO0000OO0O0O000O0 in O00O0000O000OO00O :OOO000OOO0O00OO0O .update (str (OO0000OO0O0O000O0 ))#line:1017
            for OO0000OO0O0O000O0 in year :OOO000OOO0O00OO0O .update (str (OO0000OO0O0O000O0 ))#line:1018
            OOO000OOO0O00OO0O =str (OOO000OOO0O00OO0O .hexdigest ())#line:1019
            OOOOO00OOOO00000O .makeFile (OOOOO00OOOO00000O .dataPath )#line:1021
            O00OO00O00OOOO000 =OOOO0OOO000O00O00 .connect (OOOOO00OOOO00000O .bookmarksFile )#line:1022
            OO000O000OO0OOOOO =O00OO00O00OOOO000 .cursor ()#line:1023
            OO000O000OO0OOOOO .execute ("CREATE TABLE IF NOT EXISTS bookmark (" "idFile TEXT, " "timeInSeconds TEXT, " "UNIQUE(idFile)" ");")#line:1024
            OO000O000OO0OOOOO .execute ("DELETE FROM bookmark WHERE idFile = '%s'"%OOO000OOO0O00OO0O )#line:1025
            if O00000000O00O0O00 :OO000O000OO0OOOOO .execute ("INSERT INTO bookmark Values (?, ?)",(OOO000OOO0O00OO0O ,OO00O00O0O00000O0 ))#line:1026
            O00OO00O00OOOO000 .commit ()#line:1027
        except :#line:1028
            pass 
#e9015584e6a44b14988f13e2298bcbf9

