import os as O000OO0OO000OOO00 ,re as OOO0O0000OOOO0O0O ,sys as O0OOO0000OO0O00O0 ,hashlib as O0000O0O00O0OOO0O ,urllib as OO0O0OOOOOOOOOOO0 ,urlparse as OOOOOO00O000OOOOO ,json as OOO0O0OO0O00O0OO0 ,base64 as OOO00000OOOO0O0OO ,random as OOOOOOO0OOOO00O00 ,datetime as O0O00OOOOO000OOO0 #line:1
import xbmc as OOO00O000OOOO00OO #line:2
try :from sqlite3 import dbapi2 as OO000OO0000OO000O #line:4
except :from pysqlite2 import dbapi2 as OO000OO0000OO000O #line:5
from resources .lib .modules import cache as OOO000OOOO0O0O0O0 #line:7
from resources .lib .modules import metacache as OOO00OOO0OO0O0000 #line:8
from resources .lib .modules import client as O0OOOOO0O0OOO0OO0 #line:9
from resources .lib .modules import control as O000OO0O0OOO00O0O #line:10
from resources .lib .modules import regex as O0O0000OOO0OO0OO0 #line:11
from resources .lib .modules import trailer as OO00O00O0OO0OO0O0 #line:12
from resources .lib .modules import workers as O0OO0OOO0OO00O0O0 #line:13
from resources .lib .modules import youtube as OO0OOO00O000O0O00 #line:14
from resources .lib .modules import views as O00O0OO0OOOOOO0O0 #line:15
version =103 #line:18
class indexer :#line:20
    def __init__ (O0OOOOO0OO0OO0OO0 ):#line:21
        O0OOOOO0OO0OO0OO0 .list =[];O0OOOOO0OO0OO0OO0 .hash =[]#line:22
    def root (O0O0OO0OO0000OOOO ):#line:25
        try :#line:26
            O0O0000OOO0OO0OO0 .clear ()#line:27
            O0O0OOO00OOOOO0OO ='http://brettusbuilds.com/.WHITE%20DEVIL/MAIN%20INDEX.XML'#line:28
            O0O0OO0OO0000OOOO .list =O0O0OO0OO0000OOOO .hub_list (O0O0OOO00OOOOO0OO )#line:29
            for OOO0000OO0OO00OOO in O0O0OO0OO0000OOOO .list :OOO0000OO0OO00OOO .update ({'content':'addons'})#line:30
            O0O0OO0OO0000OOOO .addDirectory (O0O0OO0OO0000OOOO .list )#line:31
            return O0O0OO0OO0000OOOO .list #line:32
        except :#line:33
            pass #line:34
    def get (O000OOOO000000OOO ,O000OO0O00OO0O0O0 ):#line:37
        try :#line:38
            O000OOOO000000OOO .list =O000OOOO000000OOO .hub_list (O000OO0O00OO0O0O0 )#line:39
            O000OOOO000000OOO .worker ()#line:40
            O000OOOO000000OOO .addDirectory (O000OOOO000000OOO .list )#line:41
            return O000OOOO000000OOO .list #line:42
        except :#line:43
            pass #line:44
    def getq (O0OOOO0O000O0O0OO ,O0OOO00OO0O0OOO0O ):#line:47
        try :#line:48
            O0OOOO0O000O0O0OO .list =O0OOOO0O000O0O0OO .hub_list (O0OOO00OO0O0OOO0O )#line:49
            O0OOOO0O000O0O0OO .worker ()#line:50
            O0OOOO0O000O0O0OO .addDirectory (O0OOOO0O000O0O0OO .list ,queue =True )#line:51
            return O0OOOO0O000O0O0OO .list #line:52
        except :#line:53
            pass #line:54
    def getx (O0OO0000O0OOO0O00 ,OO00O0000O0O00OO0 ,worker =False ):#line:57
        try :#line:58
            O0OOOO00O00OO00O0 ,OO0OO0OOOOO0OO0OO =OOO0O0000OOOO0O0O .findall ('(.+?)\|regex=(.+?)$',OO00O0000O0O00OO0 )[0 ]#line:59
            OO0OO0OOOOO0OO0OO =O0O0000OOO0OO0OO0 .fetch (OO0OO0OOOOO0OO0OO )#line:60
            O0OOOO00O00OO00O0 +=OO0O0OOOOOOOOOOO0 .unquote_plus (OO0OO0OOOOO0OO0OO )#line:61
            OO00O0000O0O00OO0 =O0O0000OOO0OO0OO0 .resolve (O0OOOO00O00OO00O0 )#line:62
            O0OO0000O0OOO0O00 .list =O0OO0000O0OOO0O00 .hub_list ('',result =OO00O0000O0O00OO0 )#line:63
            O0OO0000O0OOO0O00 .addDirectory (O0OO0000O0OOO0O00 .list )#line:64
            return O0OO0000O0OOO0O00 .list #line:65
        except :#line:66
            pass #line:67
    def developer (OOOO0OOOOOO0O0O00 ):#line:70
        try :#line:71
            OO0OO0O000O00OOO0 =O000OO0OO000OOO00 .path .join (O000OO0O0OOO00O0O .dataPath ,'testings.xml')#line:72
            OO0O00000000OOOO0 =O000OO0O0OOO00O0O .openFile (OO0OO0O000O00OOO0 );OOO0OO0O0O0OO0000 =OO0O00000000OOOO0 .read ();OO0O00000000OOOO0 .close ()#line:73
            OOOO0OOOOOO0O0O00 .list =OOOO0OOOOOO0O0O00 .hub_list ('',result =OOO0OO0O0O0OO0000 )#line:74
            for OO00OOO00OO0O00O0 in OOOO0OOOOOO0O0O00 .list :OO00OOO00OO0O00O0 .update ({'content':'videos'})#line:75
            OOOO0OOOOOO0O0O00 .addDirectory (OOOO0OOOOOO0O0O00 .list )#line:76
            return OOOO0OOOOOO0O0O00 .list #line:77
        except :#line:78
            pass #line:79
    def youtube (OO000OOOOO000O0OO ,OO0OOO000O0000000 ,O0O0O0OOOO0OOOOO0 ):#line:82
        try :#line:83
            OO0OO0OO0O00O0O00 =OO00O00O0OO0OO0O0 .trailer ().key_link .split ('=',1 )[-1 ]#line:84
            if 'PlaylistTuner'in O0O0O0OOOO0OOOOO0 :#line:86
                OO000OOOOO000O0OO .list =OOO000OOOO0O0O0O0 .get (OO0OOO00O000O0O00 .youtube (key =OO0OO0OO0O00O0O00 ).playlist ,1 ,OO0OOO000O0000000 )#line:87
            elif 'Playlist'in O0O0O0OOOO0OOOOO0 :#line:88
                OO000OOOOO000O0OO .list =OOO000OOOO0O0O0O0 .get (OO0OOO00O000O0O00 .youtube (key =OO0OO0OO0O00O0O00 ).playlist ,1 ,OO0OOO000O0000000 ,True )#line:89
            elif 'ChannelTuner'in O0O0O0OOOO0OOOOO0 :#line:90
                OO000OOOOO000O0OO .list =OOO000OOOO0O0O0O0 .get (OO0OOO00O000O0O00 .youtube (key =OO0OO0OO0O00O0O00 ).videos ,1 ,OO0OOO000O0000000 )#line:91
            elif 'Channel'in O0O0O0OOOO0OOOOO0 :#line:92
                OO000OOOOO000O0OO .list =OOO000OOOO0O0O0O0 .get (OO0OOO00O000O0O00 .youtube (key =OO0OO0OO0O00O0O00 ).videos ,1 ,OO0OOO000O0000000 ,True )#line:93
            if 'Tuner'in O0O0O0OOOO0OOOOO0 :#line:95
                for OOOO0O00OO0O0000O in OO000OOOOO000O0OO .list :OOOO0O00OO0O0000O .update ({'name':OOOO0O00OO0O0000O ['title'],'poster':OOOO0O00OO0O0000O ['image'],'action':'plugin','folder':False })#line:96
                if 'Tuner2'in O0O0O0OOOO0OOOOO0 :OO000OOOOO000O0OO .list =sorted (OO000OOOOO000O0OO .list ,key =lambda OOOO0OOO00O0OOOO0 :OOOOOOO0OOOO00O00 .random ())#line:97
                OO000OOOOO000O0OO .addDirectory (OO000OOOOO000O0OO .list ,queue =True )#line:98
            else :#line:99
                for OOOO0O00OO0O0000O in OO000OOOOO000O0OO .list :OOOO0O00OO0O0000O .update ({'name':OOOO0O00OO0O0000O ['title'],'poster':OOOO0O00OO0O0000O ['image'],'nextaction':O0O0O0OOOO0OOOOO0 ,'action':'play','folder':False })#line:100
                OO000OOOOO000O0OO .addDirectory (OO000OOOOO000O0OO .list )#line:101
            return OO000OOOOO000O0OO .list #line:103
        except :#line:104
            pass #line:105
    def tvtuner (OO0OOOOO000O0OO0O ,OOOOOOOOO0O0OOO0O ):#line:108
        try :#line:109
            OO00OO000O0O000OO =OOO0O0000OOOO0O0O .findall ('<preset>(.+?)</preset>',OOOOOOOOO0O0OOO0O )[0 ]#line:110
            OO0O0000000O0000O =((O0O00OOOOO000OOO0 .datetime .utcnow ()-O0O00OOOOO000OOO0 .timedelta (hours =5 ))).strftime ('%Y-%m-%d')#line:112
            OO0O0000000O0000O =int (OOO0O0000OOOO0O0O .sub ('[^0-9]','',str (OO0O0000000O0000O )))#line:113
            OOOOOOOOO0O0OOO0O ,O0OOO000OO0OO00O0 ,OOO0O0O0O0OO0O0O0 ,O0O0O0O0OO0O0OOOO ,OOO0OO0OO000OO0OO ,O0O0000O00O0OO0OO ,O00OO0000O0O0OOO0 =OOO0O0000OOOO0O0O .findall ('<url>(.+?)</url>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<imdb>(.+?)</imdb>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<tvdb>(.+?)</tvdb>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<year>(.+?)</year>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<thumbnail>(.+?)</thumbnail>',OOOOOOOOO0O0OOO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<fanart>(.+?)</fanart>',OOOOOOOOO0O0OOO0O )[0 ]#line:115
            O0O000O0O00O000OO =O0OOOOO0O0OOO0OO0 .request ('http://api.tvmaze.com/lookup/shows?thetvdb=%s'%OOO0O0O0O0OO0O0O0 )#line:117
            if O0O000O0O00O000OO ==None :O0O000O0O00O000OO =O0OOOOO0O0OOO0OO0 .request ('http://api.tvmaze.com/lookup/shows?imdb=%s'%O0OOO000OO0OO00O0 )#line:118
            O0O000O0O00O000OO ='http://api.tvmaze.com/shows/%s/episodes'%str (OOO0O0OO0O00O0OO0 .loads (O0O000O0O00O000OO ).get ('id'))#line:119
            OO00000OO00OOOOOO =OOO0O0OO0O00O0OO0 .loads (O0OOOOO0O0OOO0OO0 .request (O0O000O0O00O000OO ))#line:120
            OO00000OO00OOOOOO =[(str (O0OO0OOOOO0OOO0O0 .get ('season')),str (O0OO0OOOOO0OOO0O0 .get ('number')),O0OO0OOOOO0OOO0O0 .get ('name').strip (),O0OO0OOOOO0OOO0O0 .get ('airdate'))for O0OO0OOOOO0OOO0O0 in OO00000OO00OOOOOO ]#line:121
            if OO00OO000O0O000OO =='tvtuner':#line:123
                OO0OO00OO0O00O0O0 =OOOOOOO0OOOO00O00 .choice (OO00000OO00OOOOOO )#line:124
                OO00000OO00OOOOOO =OO00000OO00OOOOOO [OO00000OO00OOOOOO .index (OO0OO00OO0O00O0O0 ):]+OO00000OO00OOOOOO [:OO00000OO00OOOOOO .index (OO0OO00OO0O00O0O0 )]#line:125
                OO00000OO00OOOOOO =OO00000OO00OOOOOO [:100 ]#line:126
            OO00O00O000OO0OOO =''#line:128
            for O0000O000OO0OOOOO in OO00000OO00OOOOOO :#line:130
                try :#line:131
                    if int (OOO0O0000OOOO0O0O .sub ('[^0-9]','',str (O0000O000OO0OOOOO [3 ])))>OO0O0000000O0000O :raise Exception ()#line:132
                    OO00O00O000OO0OOO +='<item><title> %01dx%02d . %s</title><meta><content>episode</content><imdb>%s</imdb><tvdb>%s</tvdb><tvshowtitle>%s</tvshowtitle><year>%s</year><title>%s</title><premiered>%s</premiered><season>%01d</season><episode>%01d</episode></meta><link><sublink>search</sublink><sublink>searchsd</sublink></link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(int (O0000O000OO0OOOOO [0 ]),int (O0000O000OO0OOOOO [1 ]),O0000O000OO0OOOOO [2 ],O0OOO000OO0OO00O0 ,OOO0O0O0O0OO0O0O0 ,O0O0O0O0OO0O0OOOO ,OOO0OO0OO000OO0OO ,O0000O000OO0OOOOO [2 ],O0000O000OO0OOOOO [3 ],int (O0000O000OO0OOOOO [0 ]),int (O0000O000OO0OOOOO [1 ]),O0O0000O00O0OO0OO ,O00OO0000O0O0OOO0 )#line:133
                except :#line:134
                    pass #line:135
            OO00O00O000OO0OOO =OOO0O0000OOOO0O0O .sub (r'[^\x00-\x7F]+',' ',OO00O00O000OO0OOO )#line:137
            if OO00OO000O0O000OO =='tvtuner':#line:139
                OO00O00O000OO0OOO =OO00O00O000OO0OOO .replace ('<sublink>searchsd</sublink>','')#line:140
            OO0OOOOO000O0OO0O .list =OO0OOOOO000O0OO0O .hub_list ('',result =OO00O00O000OO0OOO )#line:142
            if OO00OO000O0O000OO =='tvtuner':#line:144
                OO0OOOOO000O0OO0O .addDirectory (OO0OOOOO000O0OO0O .list ,queue =True )#line:145
            else :#line:146
                OO0OOOOO000O0OO0O .worker ()#line:147
                OO0OOOOO000O0OO0O .addDirectory (OO0OOOOO000O0OO0O .list )#line:148
        except :#line:149
            pass #line:150
    def search (O0OO00OOOO0O00O0O ):#line:153
        try :#line:154
            O0OO00OOOO0O00O0O .list =[{'name':30702 ,'action':'addSearch'}]#line:155
            O0OO00OOOO0O00O0O .list +=[{'name':30703 ,'action':'delSearch'}]#line:156
            try :#line:158
                def OO0O00O000000000O ():return #line:159
                O0OO0000OOO000000 =OOO000OOOO0O0O0O0 .get (OO0O00O000000000O ,600000000 ,table ='rel_srch')#line:160
                for O00O000OOO00O0O00 in O0OO0000OOO000000 :#line:162
                    try :O0OO00OOOO0O00O0O .list +=[{'name':'%s...'%O00O000OOO00O0O00 ,'url':O00O000OOO00O0O00 ,'action':'addSearch'}]#line:163
                    except :pass #line:164
            except :#line:165
                pass #line:166
            O0OO00OOOO0O00O0O .addDirectory (O0OO00OOOO0O00O0O .list )#line:168
            return O0OO00OOOO0O00O0O .list #line:169
        except :#line:170
            pass #line:171
    def delSearch (O00000OO00OOO00O0 ):#line:174
        try :#line:175
            OOO000OOOO0O0O0O0 .clear ('rel_srch')#line:176
            O000OO0O0OOO00O0O .refresh ()#line:177
        except :#line:178
            pass #line:179
    def addSearch (OO0OO0OOOO00O0OO0 ,url =None ):#line:182
        try :#line:183
            O00OOO00O000O0000 ='http://brettusbuilds.com/.WHITE%20DEVIL/SEARCH/SEARCH.XML'#line:184
            if (url ==None or url ==''):#line:186
                O0O000OOOOOOO0O00 =O000OO0O0OOO00O0O .keyboard ('',O000OO0O0OOO00O0O .lang (30702 ).encode ('utf-8'))#line:187
                O0O000OOOOOOO0O00 .doModal ()#line:188
                if not (O0O000OOOOOOO0O00 .isConfirmed ()):return #line:189
                url =O0O000OOOOOOO0O00 .getText ()#line:190
            if (url ==None or url ==''):return #line:192
            def OOOOO000OOOOOO0OO ():return [url ]#line:194
            O0000OO00000OO00O =OOO000OOOO0O0O0O0 .get (OOOOO000OOOOOO0OO ,600000000 ,table ='rel_srch')#line:195
            def OOOOO000OOOOOO0OO ():return [O00O0OOO0O00O0O0O for OOO0O00OO0O0000O0 ,O00O0OOO0O00O0O0O in enumerate ((O0000OO00000OO00O +[url ]))if O00O0OOO0O00O0O0O not in (O0000OO00000OO00O +[url ])[:OOO0O00OO0O0000O0 ]]#line:196
            OOO000OOOO0O0O0O0 .get (OOOOO000OOOOOO0OO ,0 ,table ='rel_srch')#line:197
            O00O0OOO0O0OO00O0 =O0OOOOO0O0OOO0OO0 .request (O00OOO00O000O0000 )#line:199
            O00O0OOO0O0OO00O0 =OOO0O0000OOOO0O0O .findall ('<link>(.+?)</link>',O00O0OOO0O0OO00O0 )#line:200
            O00O0OOO0O0OO00O0 =[O0OO0O00OO0OO0OOO for O0OO0O00OO0OO0OOO in O00O0OOO0O0OO00O0 if str (O0OO0O00OO0OO0OOO ).startswith ('http')]#line:201
            OO0OO0OOOO00O0OO0 .list =[];OO00OOO0O0OO0O000 =[]#line:203
            for O00OOO00O000O0000 in O00O0OOO0O0OO00O0 :OO00OOO0O0OO0O000 .append (O0OO0OOO0OO00O0O0 .Thread (OO0OO0OOOO00O0OO0 .hub_list ,O00OOO00O000O0000 ))#line:204
            [OOO0OO00OO000O00O .start ()for OOO0OO00OO000O00O in OO00OOO0O0OO0O000 ];[O0OO000O0OOO00O00 .join ()for O0OO000O0OOO00O00 in OO00OOO0O0OO0O000 ]#line:205
            OO0OO0OOOO00O0OO0 .list =[OO0OOOOOO0O0O0O0O for OO0OOOOOO0O0O0O0O in OO0OO0OOOO00O0OO0 .list if url .lower ()in OO0OOOOOO0O0O0O0O ['name'].lower ()]#line:207
            for O0O000OOOOOOOO00O in OO0OO0OOOO00O0OO0 .list :#line:209
                try :#line:210
                    O0O000O0OOOOO0OOO =''#line:211
                    if not O0O000OOOOOOOO00O ['vip']in ['hub TV']:O0O000O0OOOOO0OOO +='[B]%s[/B] | '%O0O000OOOOOOOO00O ['vip'].upper ()#line:212
                    O0O000O0OOOOO0OOO +=O0O000OOOOOOOO00O ['name']#line:213
                    O0O000OOOOOOOO00O .update ({'name':O0O000O0OOOOO0OOO })#line:214
                except :#line:215
                    pass #line:216
            for O0O000OOOOOOOO00O in OO0OO0OOOO00O0OO0 .list :O0O000OOOOOOOO00O .update ({'content':'videos'})#line:218
            OO0OO0OOOO00O0OO0 .addDirectory (OO0OO0OOOO00O0OO0 .list )#line:219
        except :#line:220
            pass #line:221
    def hub_list (O00000OO00000000O ,OO00OO0OOOO0O0O00 ,result =None ):#line:224
        try :#line:225
            if result ==None :result =OOO000OOOO0O0O0O0 .get (O0OOOOO0O0OOO0OO0 .request ,0 ,OO00OO0OOOO0O0O00 )#line:226
            if result .strip ().startswith ('#EXTM3U')and '#EXTINF'in result :#line:228
                result =OOO0O0000OOOO0O0O .compile ('#EXTINF:.+?\,(.+?)\n(.+?)\n',OOO0O0000OOOO0O0O .MULTILINE |OOO0O0000OOOO0O0O .DOTALL ).findall (result )#line:229
                result =['<item><title>%s</title><link>%s</link></item>'%(O00OOOO00O0O00O0O [0 ],O00OOOO00O0O00O0O [1 ])for O00OOOO00O0O00O0O in result ]#line:230
                result =''.join (result )#line:231
            try :O0O00O0OO0O0O0O00 =OOO00000OOOO0O0OO .b64decode (result )#line:233
            except :O0O00O0OO0O0O0O00 =''#line:234
            if '</link>'in O0O00O0OO0O0O0O00 :result =O0O00O0OO0O0O0O00 #line:235
            result =str (result )#line:237
            result =O00000OO00000000O .account_filter (result )#line:239
            OO0OO0OOO0OOO0O0O =result .split ('<item>')[0 ].split ('<dir>')[0 ]#line:241
            try :OOOOO0O000O0O0000 =OOO0O0000OOOO0O0O .findall ('<poster>(.+?)</poster>',OO0OO0OOO0OOO0O0O )[0 ]#line:243
            except :OOOOO0O000O0O0000 ='0'#line:244
            try :OOO0O0OO0O0O00OO0 =OOO0O0000OOOO0O0O .findall ('<thumbnail>(.+?)</thumbnail>',OO0OO0OOO0OOO0O0O )[0 ]#line:246
            except :OOO0O0OO0O0O00OO0 ='0'#line:247
            try :O0O0OOOOO0OOOO0OO =OOO0O0000OOOO0O0O .findall ('<fanart>(.+?)</fanart>',OO0OO0OOO0OOO0O0O )[0 ]#line:249
            except :O0O0OOOOO0OOOO0OO ='0'#line:250
            O0OOOO0OOOO00000O =OOO0O0000OOOO0O0O .compile ('((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',OOO0O0000OOOO0O0O .MULTILINE |OOO0O0000OOOO0O0O .DOTALL ).findall (result )#line:252
        except :#line:253
            return #line:254
        for OO0O0O0O0O00000O0 in O0OOOO0OOOO00000O :#line:256
            try :#line:257
                OO0OO0OOOOO00OO00 =OOO0O0000OOOO0O0O .compile ('(<regex>.+?</regex>)',OOO0O0000OOOO0O0O .MULTILINE |OOO0O0000OOOO0O0O .DOTALL ).findall (OO0O0O0O0O00000O0 )#line:258
                OO0OO0OOOOO00OO00 =''.join (OO0OO0OOOOO00OO00 )#line:259
                O0OOO0O00OO0000O0 =OOO0O0000OOOO0O0O .compile ('(<listrepeat>.+?</listrepeat>)',OOO0O0000OOOO0O0O .MULTILINE |OOO0O0000OOOO0O0O .DOTALL ).findall (OO0OO0OOOOO00OO00 )#line:260
                OO0OO0OOOOO00OO00 =OO0O0OOOOOOOOOOO0 .quote_plus (OO0OO0OOOOO00OO00 )#line:261
                O0OOOOOO00O00OO0O =O0000O0O00O0OOO0O .md5 ()#line:263
                for OOOOO0OOOOO00OOOO in OO0OO0OOOOO00OO00 :O0OOOOOO00O00OO0O .update (str (OOOOO0OOOOO00OOOO ))#line:264
                O0OOOOOO00O00OO0O =str (O0OOOOOO00O00OO0O .hexdigest ())#line:265
                OO0O0O0O0O00000O0 =OO0O0O0O0O00000O0 .replace ('\r','').replace ('\n','').replace ('\t','').replace ('&nbsp;','')#line:267
                OO0O0O0O0O00000O0 =OOO0O0000OOOO0O0O .sub ('<regex>.+?</regex>','',OO0O0O0O0O00000O0 )#line:268
                OO0O0O0O0O00000O0 =OOO0O0000OOOO0O0O .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OO0O0O0O0O00000O0 )#line:269
                OO0O0O0O0O00000O0 =OOO0O0000OOOO0O0O .sub ('<link></link>','',OO0O0O0O0O00000O0 )#line:270
                OOO00000OO0O0O000 =OOO0O0000OOOO0O0O .sub ('<meta>.+?</meta>','',OO0O0O0O0O00000O0 )#line:272
                try :OOO00000OO0O0O000 =OOO0O0000OOOO0O0O .findall ('<title>(.+?)</title>',OOO00000OO0O0O000 )[0 ]#line:273
                except :OOO00000OO0O0O000 =OOO0O0000OOOO0O0O .findall ('<name>(.+?)</name>',OOO00000OO0O0O000 )[0 ]#line:274
                try :O0OOO00OOO0O00O00 =OOO0O0000OOOO0O0O .findall ('<date>(.+?)</date>',OO0O0O0O0O00000O0 )[0 ]#line:276
                except :O0OOO00OOO0O00O00 =''#line:277
                if OOO0O0000OOOO0O0O .search (r'\d+',O0OOO00OOO0O00O00 ):OOO00000OO0O0O000 +=' [COLOR red] Updated %s[/COLOR]'%O0OOO00OOO0O00O00 #line:278
                try :O0O00OOOOO00OOOO0 =OOO0O0000OOOO0O0O .findall ('<thumbnail>(.+?)</thumbnail>',OO0O0O0O0O00000O0 )[0 ]#line:280
                except :O0O00OOOOO00OOOO0 =OOO0O0OO0O0O00OO0 #line:281
                try :OO0OOO0OO0OO0O0OO =OOO0O0000OOOO0O0O .findall ('<fanart>(.+?)</fanart>',OO0O0O0O0O00000O0 )[0 ]#line:283
                except :OO0OOO0OO0OO0O0OO =O0O0OOOOO0OOOO0OO #line:284
                try :OOO0OOO0O000O0OO0 =OOO0O0000OOOO0O0O .findall ('<meta>(.+?)</meta>',OO0O0O0O0O00000O0 )[0 ]#line:286
                except :OOO0OOO0O000O0OO0 ='0'#line:287
                try :OO00OO0OOOO0O0O00 =OOO0O0000OOOO0O0O .findall ('<link>(.+?)</link>',OO0O0O0O0O00000O0 )[0 ]#line:289
                except :OO00OO0OOOO0O0O00 ='0'#line:290
                OO00OO0OOOO0O0O00 =OO00OO0OOOO0O0O00 .replace ('>search<','><preset>search</preset>%s<'%OOO0OOO0O000O0OO0 )#line:291
                OO00OO0OOOO0O0O00 ='<preset>search</preset>%s'%OOO0OOO0O000O0OO0 if OO00OO0OOOO0O0O00 =='search'else OO00OO0OOOO0O0O00 #line:292
                OO00OO0OOOO0O0O00 =OO00OO0OOOO0O0O00 .replace ('>searchsd<','><preset>searchsd</preset>%s<'%OOO0OOO0O000O0OO0 )#line:293
                OO00OO0OOOO0O0O00 ='<preset>searchsd</preset>%s'%OOO0OOO0O000O0OO0 if OO00OO0OOOO0O0O00 =='searchsd'else OO00OO0OOOO0O0O00 #line:294
                OO00OO0OOOO0O0O00 =OOO0O0000OOOO0O0O .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OO00OO0OOOO0O0O00 )#line:295
                if OO0O0O0O0O00000O0 .startswith ('<item>'):O0000OO00O0OOOO00 ='play'#line:297
                elif OO0O0O0O0O00000O0 .startswith ('<plugin>'):O0000OO00O0OOOO00 ='plugin'#line:298
                elif OO0O0O0O0O00000O0 .startswith ('<info>')or OO00OO0OOOO0O0O00 =='0':O0000OO00O0OOOO00 ='0'#line:299
                else :O0000OO00O0OOOO00 ='directory'#line:300
                if O0000OO00O0OOOO00 =='play'and O0OOO0O00OO0000O0 :O0000OO00O0OOOO00 ='xdirectory'#line:301
                if not OO0OO0OOOOO00OO00 =='':#line:303
                    O00000OO00000000O .hash .append ({'regex':O0OOOOOO00O00OO0O ,'response':OO0OO0OOOOO00OO00 })#line:304
                    OO00OO0OOOO0O0O00 +='|regex=%s'%O0OOOOOO00O00OO0O #line:305
                if O0000OO00O0OOOO00 in ['directory','xdirectory','plugin']:#line:307
                    OO0OO0OOO0OO0O000 =True #line:308
                else :#line:309
                    OO0OO0OOO0OO0O000 =False #line:310
                try :OO0OO00000OOOOO00 =OOO0O0000OOOO0O0O .findall ('<content>(.+?)</content>',OOO0OOO0O000O0OO0 )[0 ]#line:312
                except :OO0OO00000OOOOO00 ='0'#line:313
                if OO0OO00000OOOOO00 =='0':#line:314
                    try :OO0OO00000OOOOO00 =OOO0O0000OOOO0O0O .findall ('<content>(.+?)</content>',OO0O0O0O0O00000O0 )[0 ]#line:315
                    except :OO0OO00000OOOOO00 ='0'#line:316
                if not OO0OO00000OOOOO00 =='0':OO0OO00000OOOOO00 +='s'#line:317
                if 'tvshow'in OO0OO00000OOOOO00 and not OO00OO0OOOO0O0O00 .strip ().endswith ('.xml'):#line:319
                    OO00OO0OOOO0O0O00 ='<preset>tvindexer</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OO00OO0OOOO0O0O00 ,O0O00OOOOO00OOOO0 ,OO0OOO0OO0OO0O0OO ,OOO0OOO0O000O0OO0 )#line:320
                    O0000OO00O0OOOO00 ='tvtuner'#line:321
                if 'tvtuner'in OO0OO00000OOOOO00 and not OO00OO0OOOO0O0O00 .strip ().endswith ('.xml'):#line:323
                    OO00OO0OOOO0O0O00 ='<preset>tvtuner</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OO00OO0OOOO0O0O00 ,O0O00OOOOO00OOOO0 ,OO0OOO0OO0OO0O0OO ,OOO0OOO0O000O0OO0 )#line:324
                    O0000OO00O0OOOO00 ='tvtuner'#line:325
                try :OOO0OO0O0OO000000 =OOO0O0000OOOO0O0O .findall ('<imdb>(.+?)</imdb>',OOO0OOO0O000O0OO0 )[0 ]#line:327
                except :OOO0OO0O0OO000000 ='0'#line:328
                try :O00OOO00OO0000000 =OOO0O0000OOOO0O0O .findall ('<tvdb>(.+?)</tvdb>',OOO0OOO0O000O0OO0 )[0 ]#line:330
                except :O00OOO00OO0000000 ='0'#line:331
                try :OOOO0O0O0OOOOO0OO =OOO0O0000OOOO0O0O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',OOO0OOO0O000O0OO0 )[0 ]#line:333
                except :OOOO0O0O0OOOOO0OO ='0'#line:334
                try :O0000O0000O0O00O0 =OOO0O0000OOOO0O0O .findall ('<title>(.+?)</title>',OOO0OOO0O000O0OO0 )[0 ]#line:336
                except :O0000O0000O0O00O0 ='0'#line:337
                if O0000O0000O0O00O0 =='0'and not OOOO0O0O0OOOOO0OO =='0':O0000O0000O0O00O0 =OOOO0O0O0OOOOO0OO #line:339
                try :OO0000OOO00000OOO =OOO0O0000OOOO0O0O .findall ('<year>(.+?)</year>',OOO0OOO0O000O0OO0 )[0 ]#line:341
                except :OO0000OOO00000OOO ='0'#line:342
                try :OOO00000O0OOOOOO0 =OOO0O0000OOOO0O0O .findall ('<premiered>(.+?)</premiered>',OOO0OOO0O000O0OO0 )[0 ]#line:344
                except :OOO00000O0OOOOOO0 ='0'#line:345
                try :O0O00O00OOOOOO0OO =OOO0O0000OOOO0O0O .findall ('<season>(.+?)</season>',OOO0OOO0O000O0OO0 )[0 ]#line:347
                except :O0O00O00OOOOOO0OO ='0'#line:348
                try :O000O000O00OO00OO =OOO0O0000OOOO0O0O .findall ('<episode>(.+?)</episode>',OOO0OOO0O000O0OO0 )[0 ]#line:350
                except :O000O000O00OO00OO ='0'#line:351
                O00000OO00000000O .list .append ({'name':OOO00000OO0O0O000 ,'vip':OOOOO0O000O0O0000 ,'url':OO00OO0OOOO0O0O00 ,'action':O0000OO00O0OOOO00 ,'folder':OO0OO0OOO0OO0O000 ,'poster':O0O00OOOOO00OOOO0 ,'banner':'0','fanart':OO0OOO0OO0OO0O0OO ,'content':OO0OO00000OOOOO00 ,'imdb':OOO0OO0O0OO000000 ,'tvdb':O00OOO00OO0000000 ,'tmdb':'0','title':O0000O0000O0O00O0 ,'originaltitle':O0000O0000O0O00O0 ,'tvshowtitle':OOOO0O0O0OOOOO0OO ,'year':OO0000OOO00000OOO ,'premiered':OOO00000O0OOOOOO0 ,'season':O0O00O00OOOOOO0OO ,'episode':O000O000O00OO00OO })#line:353
            except :#line:354
                pass #line:355
        O0O0000OOO0OO0OO0 .insert (O00000OO00000000O .hash )#line:357
        return O00000OO00000000O .list #line:359
    def account_filter (O000OO00O0OO00O0O ,O0O0OOO0O0OOOO0O0 ):#line:362
        if (O000OO0O0OOO00O0O .setting ('ustvnow_email')==''or O000OO0O0OOO00O0O .setting ('ustvnow_pass')==''):#line:363
            O0O0OOO0O0OOOO0O0 =OOO0O0000OOOO0O0O .sub ('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<','<',O0O0OOO0O0OOOO0O0 )#line:364
        if (O000OO0O0OOO00O0O .setting ('streamlive_user')==''or O000OO0O0OOO00O0O .setting ('streamlive_pass')==''):#line:366
            O0O0OOO0O0OOOO0O0 =OOO0O0000OOOO0O0O .sub ('http(?:s|)://(?:www\.|)streamlive\.to/.+?<','<',O0O0OOO0O0OOOO0O0 )#line:367
        return O0O0OOO0O0OOOO0O0 #line:369
    def worker (OOO00000000OO0O00 ):#line:372
        if not O000OO0O0OOO00O0O .setting ('metadata')=='true':return #line:373
        OOO00000000OO0O00 .imdb_info_link ='http://www.omdbapi.com/?i=%s&plot=full&r=json'#line:375
        OOO00000000OO0O00 .tvmaze_info_link ='http://api.tvmaze.com/lookup/shows?thetvdb=%s'#line:376
        OOO00000000OO0O00 .lang ='en'#line:377
        OOO00000000OO0O00 .meta =[]#line:379
        OOO0O00000O0O00O0 =len (OOO00000000OO0O00 .list )#line:380
        if OOO0O00000O0O00O0 ==0 :return #line:381
        for OO00OO0OO0000OOO0 in range (0 ,OOO0O00000O0O00O0 ):OOO00000000OO0O00 .list [OO00OO0OO0000OOO0 ].update ({'metacache':False })#line:383
        OOO00000000OO0O00 .list =OOO00OOO0OO0O0000 .fetch (OOO00000000OO0O00 .list ,OOO00000000OO0O00 .lang )#line:384
        OO00OO00OO00000O0 =[O00OO00000OOO00OO ['imdb']for O00OO00000OOO00OO in OOO00000000OO0O00 .list ]#line:386
        OO00OO00OO00000O0 =[O0O0OOO00OO0O00OO for O0OOO0OOOO000O0OO ,O0O0OOO00OO0O00OO in enumerate (OO00OO00OO00000O0 )if O0O0OOO00OO0O00OO not in OO00OO00OO00000O0 [:O0OOO0OOOO000O0OO ]]#line:387
        if len (OO00OO00OO00000O0 )==1 :#line:388
                OOO00000000OO0O00 .movie_info (0 );OOO00000000OO0O00 .tv_info (0 )#line:389
                if OOO00000000OO0O00 .meta :OOO00OOO0OO0O0000 .insert (OOO00000000OO0O00 .meta )#line:390
        for OO00OO0OO0000OOO0 in range (0 ,OOO0O00000O0O00O0 ):OOO00000000OO0O00 .list [OO00OO0OO0000OOO0 ].update ({'metacache':False })#line:392
        OOO00000000OO0O00 .list =OOO00OOO0OO0O0000 .fetch (OOO00000000OO0O00 .list ,OOO00000000OO0O00 .lang )#line:393
        for OO0000O00OO0000OO in range (0 ,OOO0O00000O0O00O0 ,50 ):#line:395
            OO000OOOO00OOOO0O =[]#line:396
            for OO00OO0OO0000OOO0 in range (OO0000O00OO0000OO ,OO0000O00OO0000OO +50 ):#line:397
                if OO00OO0OO0000OOO0 <=OOO0O00000O0O00O0 :OO000OOOO00OOOO0O .append (O0OO0OOO0OO00O0O0 .Thread (OOO00000000OO0O00 .movie_info ,OO00OO0OO0000OOO0 ))#line:398
                if OO00OO0OO0000OOO0 <=OOO0O00000O0O00O0 :OO000OOOO00OOOO0O .append (O0OO0OOO0OO00O0O0 .Thread (OOO00000000OO0O00 .tv_info ,OO00OO0OO0000OOO0 ))#line:399
            [OOOO000O00OOOOO00 .start ()for OOOO000O00OOOOO00 in OO000OOOO00OOOO0O ]#line:400
            [O000O00O0000O0OO0 .join ()for O000O00O0000O0OO0 in OO000OOOO00OOOO0O ]#line:401
        if OOO00000000OO0O00 .meta :OOO00OOO0OO0O0000 .insert (OOO00000000OO0O00 .meta )#line:403
    def movie_info (OOOO0000OOO000OO0 ,O000O00O0OO00O00O ):#line:406
        try :#line:407
            if OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ]['metacache']==True :raise Exception ()#line:408
            if not OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ]['content']=='movies':raise Exception ()#line:410
            O0O0000O0000OO000 =OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ]['imdb']#line:412
            if O0O0000O0000OO000 =='0':raise Exception ()#line:413
            O0OO0OO00OO0000OO =OOOO0000OOO000OO0 .imdb_info_link %O0O0000O0000OO000 #line:415
            OOOO0O0000O00000O =O0OOOOO0O0OOO0OO0 .request (O0OO0OO00OO0000OO ,timeout ='10')#line:417
            OOOO0O0000O00000O =OOO0O0OO0O00O0OO0 .loads (OOOO0O0000O00000O )#line:418
            if 'Error'in OOOO0O0000O00000O and 'incorrect imdb'in OOOO0O0000O00000O ['Error'].lower ():#line:420
                return OOOO0000OOO000OO0 .meta .append ({'imdb':O0O0000O0000OO000 ,'tmdb':'0','tvdb':'0','lang':OOOO0000OOO000OO0 .lang ,'item':{'code':'0'}})#line:421
            OOOOO000O00O000O0 =OOOO0O0000O00000O ['Title']#line:423
            OOOOO000O00O000O0 =OOOOO000O00O000O0 .encode ('utf-8')#line:424
            if not OOOOO000O00O000O0 =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'title':OOOOO000O00O000O0 })#line:425
            OO000OO000O00000O =OOOO0O0000O00000O ['Year']#line:427
            OO000OO000O00000O =OO000OO000O00000O .encode ('utf-8')#line:428
            if not OO000OO000O00000O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'year':OO000OO000O00000O })#line:429
            O0O0000O0000OO000 =OOOO0O0000O00000O ['imdbID']#line:431
            if O0O0000O0000OO000 ==None or O0O0000O0000OO000 ==''or O0O0000O0000OO000 =='N/A':O0O0000O0000OO000 ='0'#line:432
            O0O0000O0000OO000 =O0O0000O0000OO000 .encode ('utf-8')#line:433
            if not O0O0000O0000OO000 =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'imdb':O0O0000O0000OO000 ,'code':O0O0000O0000OO000 })#line:434
            OO0OOOOO0OOO0OOOO =OOOO0O0000O00000O ['Released']#line:436
            if OO0OOOOO0OOO0OOOO ==None or OO0OOOOO0OOO0OOOO ==''or OO0OOOOO0OOO0OOOO =='N/A':OO0OOOOO0OOO0OOOO ='0'#line:437
            OO0OOOOO0OOO0OOOO =OOO0O0000OOOO0O0O .findall ('(\d*) (.+?) (\d*)',OO0OOOOO0OOO0OOOO )#line:438
            try :OO0OOOOO0OOO0OOOO ='%s-%s-%s'%(OO0OOOOO0OOO0OOOO [0 ][2 ],{'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}[OO0OOOOO0OOO0OOOO [0 ][1 ]],OO0OOOOO0OOO0OOOO [0 ][0 ])#line:439
            except :OO0OOOOO0OOO0OOOO ='0'#line:440
            OO0OOOOO0OOO0OOOO =OO0OOOOO0OOO0OOOO .encode ('utf-8')#line:441
            if not OO0OOOOO0OOO0OOOO =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'premiered':OO0OOOOO0OOO0OOOO })#line:442
            O000OO00O0OOOOOOO =OOOO0O0000O00000O ['Genre']#line:444
            if O000OO00O0OOOOOOO ==None or O000OO00O0OOOOOOO ==''or O000OO00O0OOOOOOO =='N/A':O000OO00O0OOOOOOO ='0'#line:445
            O000OO00O0OOOOOOO =O000OO00O0OOOOOOO .replace (', ',' / ')#line:446
            O000OO00O0OOOOOOO =O000OO00O0OOOOOOO .encode ('utf-8')#line:447
            if not O000OO00O0OOOOOOO =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'genre':O000OO00O0OOOOOOO })#line:448
            O000OO000OO0OOO0O =OOOO0O0000O00000O ['Runtime']#line:450
            if O000OO000OO0OOO0O ==None or O000OO000OO0OOO0O ==''or O000OO000OO0OOO0O =='N/A':O000OO000OO0OOO0O ='0'#line:451
            O000OO000OO0OOO0O =OOO0O0000OOOO0O0O .sub ('[^0-9]','',str (O000OO000OO0OOO0O ))#line:452
            try :O000OO000OO0OOO0O =str (int (O000OO000OO0OOO0O )*60 )#line:453
            except :pass #line:454
            O000OO000OO0OOO0O =O000OO000OO0OOO0O .encode ('utf-8')#line:455
            if not O000OO000OO0OOO0O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'duration':O000OO000OO0OOO0O })#line:456
            OO000OO00OO0O000O =OOOO0O0000O00000O ['imdbRating']#line:458
            if OO000OO00OO0O000O ==None or OO000OO00OO0O000O ==''or OO000OO00OO0O000O =='N/A'or OO000OO00OO0O000O =='0.0':OO000OO00OO0O000O ='0'#line:459
            OO000OO00OO0O000O =OO000OO00OO0O000O .encode ('utf-8')#line:460
            if not OO000OO00OO0O000O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'rating':OO000OO00OO0O000O })#line:461
            O0O00000O0O0000OO =OOOO0O0000O00000O ['imdbVotes']#line:463
            try :O0O00000O0O0000OO =str (format (int (O0O00000O0O0000OO ),',d'))#line:464
            except :pass #line:465
            if O0O00000O0O0000OO ==None or O0O00000O0O0000OO ==''or O0O00000O0O0000OO =='N/A':O0O00000O0O0000OO ='0'#line:466
            O0O00000O0O0000OO =O0O00000O0O0000OO .encode ('utf-8')#line:467
            if not O0O00000O0O0000OO =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'votes':O0O00000O0O0000OO })#line:468
            OO00OO0OO0O00OOO0 =OOOO0O0000O00000O ['Rated']#line:470
            if OO00OO0OO0O00OOO0 ==None or OO00OO0OO0O00OOO0 ==''or OO00OO0OO0O00OOO0 =='N/A':OO00OO0OO0O00OOO0 ='0'#line:471
            OO00OO0OO0O00OOO0 =OO00OO0OO0O00OOO0 .encode ('utf-8')#line:472
            if not OO00OO0OO0O00OOO0 =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'mpaa':OO00OO0OO0O00OOO0 })#line:473
            OOOOO00000OO0000O =OOOO0O0000O00000O ['Director']#line:475
            if OOOOO00000OO0000O ==None or OOOOO00000OO0000O ==''or OOOOO00000OO0000O =='N/A':OOOOO00000OO0000O ='0'#line:476
            OOOOO00000OO0000O =OOOOO00000OO0000O .replace (', ',' / ')#line:477
            OOOOO00000OO0000O =OOO0O0000OOOO0O0O .sub (r'\(.*?\)','',OOOOO00000OO0000O )#line:478
            OOOOO00000OO0000O =' '.join (OOOOO00000OO0000O .split ())#line:479
            OOOOO00000OO0000O =OOOOO00000OO0000O .encode ('utf-8')#line:480
            if not OOOOO00000OO0000O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'director':OOOOO00000OO0000O })#line:481
            OOOOOOOO00O0OO00O =OOOO0O0000O00000O ['Writer']#line:483
            if OOOOOOOO00O0OO00O ==None or OOOOOOOO00O0OO00O ==''or OOOOOOOO00O0OO00O =='N/A':OOOOOOOO00O0OO00O ='0'#line:484
            OOOOOOOO00O0OO00O =OOOOOOOO00O0OO00O .replace (', ',' / ')#line:485
            OOOOOOOO00O0OO00O =OOO0O0000OOOO0O0O .sub (r'\(.*?\)','',OOOOOOOO00O0OO00O )#line:486
            OOOOOOOO00O0OO00O =' '.join (OOOOOOOO00O0OO00O .split ())#line:487
            OOOOOOOO00O0OO00O =OOOOOOOO00O0OO00O .encode ('utf-8')#line:488
            if not OOOOOOOO00O0OO00O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'writer':OOOOOOOO00O0OO00O })#line:489
            O0OO00000OO0O00OO =OOOO0O0000O00000O ['Actors']#line:491
            if O0OO00000OO0O00OO ==None or O0OO00000OO0O00OO ==''or O0OO00000OO0O00OO =='N/A':O0OO00000OO0O00OO ='0'#line:492
            O0OO00000OO0O00OO =[O0000OOO00O00OO00 .strip ()for O0000OOO00O00OO00 in O0OO00000OO0O00OO .split (',')if not O0000OOO00O00OO00 =='']#line:493
            try :O0OO00000OO0O00OO =[(O0O0O000OO0O00O00 .encode ('utf-8'),'')for O0O0O000OO0O00O00 in O0OO00000OO0O00OO ]#line:494
            except :O0OO00000OO0O00OO =[]#line:495
            if O0OO00000OO0O00OO ==[]:O0OO00000OO0O00OO ='0'#line:496
            if not O0OO00000OO0O00OO =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'cast':O0OO00000OO0O00OO })#line:497
            OOOO00O0O0000OO0O =OOOO0O0000O00000O ['Plot']#line:499
            if OOOO00O0O0000OO0O ==None or OOOO00O0O0000OO0O ==''or OOOO00O0O0000OO0O =='N/A':OOOO00O0O0000OO0O ='0'#line:500
            OOOO00O0O0000OO0O =O0OOOOO0O0OOO0OO0 .replaceHTMLCodes (OOOO00O0O0000OO0O )#line:501
            OOOO00O0O0000OO0O =OOOO00O0O0000OO0O .encode ('utf-8')#line:502
            if not OOOO00O0O0000OO0O =='0':OOOO0000OOO000OO0 .list [O000O00O0OO00O00O ].update ({'plot':OOOO00O0O0000OO0O })#line:503
            OOOO0000OOO000OO0 .meta .append ({'imdb':O0O0000O0000OO000 ,'tmdb':'0','tvdb':'0','lang':OOOO0000OOO000OO0 .lang ,'item':{'title':OOOOO000O00O000O0 ,'year':OO000OO000O00000O ,'code':O0O0000O0000OO000 ,'imdb':O0O0000O0000OO000 ,'premiered':OO0OOOOO0OOO0OOOO ,'genre':O000OO00O0OOOOOOO ,'duration':O000OO000OO0OOO0O ,'rating':OO000OO00OO0O000O ,'votes':O0O00000O0O0000OO ,'mpaa':OO00OO0OO0O00OOO0 ,'director':OOOOO00000OO0000O ,'writer':OOOOOOOO00O0OO00O ,'cast':O0OO00000OO0O00OO ,'plot':OOOO00O0O0000OO0O }})#line:505
        except :#line:506
            pass #line:507
    def tv_info (OOO0OO0OOOO00OO00 ,O00OOO00O0000OO00 ):#line:510
        try :#line:511
            if OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ]['metacache']==True :raise Exception ()#line:512
            if not OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ]['content']in ['tvshows','seasons','episodes']:raise Exception ()#line:514
            OOO000000O00OOOOO =OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ]['tvdb']#line:516
            if OOO000000O00OOOOO =='0':raise Exception ()#line:517
            OO0OOOO00O0O000OO =OOO0OO0OOOO00OO00 .tvmaze_info_link %OOO000000O00OOOOO #line:519
            O000OOO0O0OO00OOO =O0OOOOO0O0OOO0OO0 .request (OO0OOOO00O0O000OO ,output ='extended',error =True ,timeout ='10')#line:521
            if O000OOO0O0OO00OOO [1 ]=='404':#line:523
                return OOO0OO0OOOO00OO00 .meta .append ({'imdb':'0','tmdb':'0','tvdb':OOO000000O00OOOOO ,'lang':OOO0OO0OOOO00OO00 .lang ,'item':{'code':'0'}})#line:524
            O000OOO0O0OO00OOO =OOO0O0OO0O00O0OO0 .loads (O000OOO0O0OO00OOO [0 ])#line:526
            OO0O0O0O00O0OO0OO =O000OOO0O0OO00OOO ['name']#line:528
            OO0O0O0O00O0OO0OO =OO0O0O0O00O0OO0OO .encode ('utf-8')#line:529
            if not OO0O0O0O00O0OO0OO =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'tvshowtitle':OO0O0O0O00O0OO0OO })#line:530
            O0OO000O0OOO000OO =O000OOO0O0OO00OOO ['premiered']#line:532
            O0OO000O0OOO000OO =OOO0O0000OOOO0O0O .findall ('(\d{4})',O0OO000O0OOO000OO )[0 ]#line:533
            O0OO000O0OOO000OO =O0OO000O0OOO000OO .encode ('utf-8')#line:534
            if not O0OO000O0OOO000OO =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'year':O0OO000O0OOO000OO })#line:535
            try :O00OO00OOOO000O0O =O000OOO0O0OO00OOO ['externals']['imdb']#line:537
            except :O00OO00OOOO000O0O ='0'#line:538
            if O00OO00OOOO000O0O ==''or O00OO00OOOO000O0O ==None :O00OO00OOOO000O0O ='0'#line:539
            O00OO00OOOO000O0O =O00OO00OOOO000O0O .encode ('utf-8')#line:540
            if OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ]['imdb']=='0'and not O00OO00OOOO000O0O =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'imdb':O00OO00OOOO000O0O })#line:541
            try :OOO000000OO00OOO0 =O000OOO0O0OO00OOO ['network']['name']#line:543
            except :OOO000000OO00OOO0 ='0'#line:544
            if OOO000000OO00OOO0 ==''or OOO000000OO00OOO0 ==None :OOO000000OO00OOO0 ='0'#line:545
            OOO000000OO00OOO0 =OOO000000OO00OOO0 .encode ('utf-8')#line:546
            if not OOO000000OO00OOO0 =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'studio':OOO000000OO00OOO0 })#line:547
            OO0OOO0000000OO00 =O000OOO0O0OO00OOO ['genres']#line:549
            if OO0OOO0000000OO00 ==''or OO0OOO0000000OO00 ==None or OO0OOO0000000OO00 ==[]:OO0OOO0000000OO00 ='0'#line:550
            OO0OOO0000000OO00 =' / '.join (OO0OOO0000000OO00 )#line:551
            OO0OOO0000000OO00 =OO0OOO0000000OO00 .encode ('utf-8')#line:552
            if not OO0OOO0000000OO00 =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'genre':OO0OOO0000000OO00 })#line:553
            try :OOOOOOO0O0O000OOO =str (O000OOO0O0OO00OOO ['runtime'])#line:555
            except :OOOOOOO0O0O000OOO ='0'#line:556
            if OOOOOOO0O0O000OOO ==''or OOOOOOO0O0O000OOO ==None :OOOOOOO0O0O000OOO ='0'#line:557
            try :OOOOOOO0O0O000OOO =str (int (OOOOOOO0O0O000OOO )*60 )#line:558
            except :pass #line:559
            OOOOOOO0O0O000OOO =OOOOOOO0O0O000OOO .encode ('utf-8')#line:560
            if not OOOOOOO0O0O000OOO =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'duration':OOOOOOO0O0O000OOO })#line:561
            O000OO0OO0O00000O =str (O000OOO0O0OO00OOO ['rating']['average'])#line:563
            if O000OO0OO0O00000O ==''or O000OO0OO0O00000O ==None :O000OO0OO0O00000O ='0'#line:564
            O000OO0OO0O00000O =O000OO0OO0O00000O .encode ('utf-8')#line:565
            if not O000OO0OO0O00000O =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'rating':O000OO0OO0O00000O })#line:566
            OOO0000O0000O00O0 =O000OOO0O0OO00OOO ['summary']#line:568
            if OOO0000O0000O00O0 ==''or OOO0000O0000O00O0 ==None :OOO0000O0000O00O0 ='0'#line:569
            OOO0000O0000O00O0 =OOO0O0000OOOO0O0O .sub ('\n|<.+?>|</.+?>|.+?#\d*:','',OOO0000O0000O00O0 )#line:570
            OOO0000O0000O00O0 =OOO0000O0000O00O0 .encode ('utf-8')#line:571
            if not OOO0000O0000O00O0 =='0':OOO0OO0OOOO00OO00 .list [O00OOO00O0000OO00 ].update ({'plot':OOO0000O0000O00O0 })#line:572
            OOO0OO0OOOO00OO00 .meta .append ({'imdb':O00OO00OOOO000O0O ,'tmdb':'0','tvdb':OOO000000O00OOOOO ,'lang':OOO0OO0OOOO00OO00 .lang ,'item':{'tvshowtitle':OO0O0O0O00O0OO0OO ,'year':O0OO000O0OOO000OO ,'code':O00OO00OOOO000O0O ,'imdb':O00OO00OOOO000O0O ,'tvdb':OOO000000O00OOOOO ,'studio':OOO000000OO00OOO0 ,'genre':OO0OOO0000000OO00 ,'duration':OOOOOOO0O0O000OOO ,'rating':O000OO0OO0O00000O ,'plot':OOO0000O0000O00O0 }})#line:574
        except :#line:575
            pass #line:576
    def addDirectory (O00O00O0OOOOOO00O ,OO00OOOO0OO00O00O ,queue =False ):#line:579
        if OO00OOOO0OO00O00O ==None or len (OO00OOOO0OO00O00O )==0 :return #line:580
        O0OOOO0O0O0O000OO =O0OOO0000OO0O00O0 .argv [0 ]#line:582
        O000O00O00OOOOOOO =O0O00O0OO00OO0OO0 =O000OO0O0OOO00O0O .addonInfo ('icon')#line:583
        OOO00OO00000OOO0O =O000OO0O0OOO00O0O .addonInfo ('fanart')#line:584
        OO00OOOOOO0OOO0OO =O000OO0O0OOO00O0O .playlist #line:586
        if not queue ==False :OO00OOOOOO0OOO0OO .clear ()#line:587
        try :OOO0OO0O00O0OOOOO =True if 'testings.xml'in O000OO0O0OOO00O0O .listDir (O000OO0O0OOO00O0O .dataPath )[1 ]else False #line:589
        except :OOO0OO0O00O0OOOOO =False #line:590
        OO0OO0O0O0OOO0OO0 =[OOOO0O000O00O0O00 ['content']for OOOO0O000O00O0O00 in OO00OOOO0OO00O00O if 'content'in OOOO0O000O00O0O00 ]#line:592
        if 'movies'in OO0OO0O0O0OOO0OO0 :OO0OO0O0O0OOO0OO0 ='movies'#line:593
        elif 'tvshows'in OO0OO0O0O0OOO0OO0 :OO0OO0O0O0OOO0OO0 ='tvshows'#line:594
        elif 'seasons'in OO0OO0O0O0OOO0OO0 :OO0OO0O0O0OOO0OO0 ='seasons'#line:595
        elif 'episodes'in OO0OO0O0O0OOO0OO0 :OO0OO0O0O0OOO0OO0 ='episodes'#line:596
        elif 'addons'in OO0OO0O0O0OOO0OO0 :OO0OO0O0O0OOO0OO0 ='addons'#line:597
        else :OO0OO0O0O0OOO0OO0 ='videos'#line:598
        for OOOO00O00OOO0O000 in OO00OOOO0OO00O00O :#line:600
            try :#line:601
                try :OO0O0OO0O00000O00 =O000OO0O0OOO00O0O .lang (int (OOOO00O00OOO0O000 ['name'])).encode ('utf-8')#line:602
                except :OO0O0OO0O00000O00 =OOOO00O00OOO0O000 ['name']#line:603
                O00000O00O00OOOOO ='%s?action=%s'%(O0OOOO0O0O0O000OO ,OOOO00O00OOO0O000 ['action'])#line:605
                try :O00000O00O00OOOOO +='&url=%s'%OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['url'])#line:606
                except :pass #line:607
                try :O00000O00O00OOOOO +='&content=%s'%OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['content'])#line:608
                except :pass #line:609
                if OOOO00O00OOO0O000 ['action']=='plugin'and 'url'in OOOO00O00OOO0O000 :O00000O00O00OOOOO =OOOO00O00OOO0O000 ['url']#line:611
                try :O0OO0OO0O0OOO0OOO =dict (OOOOOO00O000OOOOO .parse_qsl (OOOOOO00O000OOOOO .urlparse (O00000O00O00OOOOO ).query ))['action']#line:613
                except :O0OO0OO0O0OOO0OOO =None #line:614
                if O0OO0OO0O0OOO0OOO =='developer'and not OOO0OO0O00O0OOOOO ==True :raise Exception ()#line:615
                O000000OO00OO0000 =OOOO00O00OOO0O000 ['poster']if 'poster'in OOOO00O00OOO0O000 else '0'#line:617
                OO0O0OOO00OOOOO00 =OOOO00O00OOO0O000 ['banner']if 'banner'in OOOO00O00OOO0O000 else '0'#line:618
                O0O0O00O00000O000 =OOOO00O00OOO0O000 ['fanart']if 'fanart'in OOOO00O00OOO0O000 else '0'#line:619
                if O000000OO00OO0000 =='0':O000000OO00OO0000 =O000O00O00OOOOOOO #line:620
                if OO0O0OOO00OOOOO00 =='0'and O000000OO00OO0000 =='0':OO0O0OOO00OOOOO00 =O0O00O0OO00OO0OO0 #line:621
                elif OO0O0OOO00OOOOO00 =='0':OO0O0OOO00OOOOO00 =O000000OO00OO0000 #line:622
                OO0O0O00O0000OOO0 =OOOO00O00OOO0O000 ['content']if 'content'in OOOO00O00OOO0O000 else '0'#line:624
                OO000O0OO0OO0OOO0 =OOOO00O00OOO0O000 ['folder']if 'folder'in OOOO00O00OOO0O000 else True #line:626
                OOOO0O0000O00O00O =dict ((OO00OOOO0O0OOOOOO ,OO0OO0OO000O00O00 )for OO00OOOO0O0OOOOOO ,OO0OO0OO000O00O00 in OOOO00O00OOO0O000 .iteritems ()if not OO0OO0OO000O00O00 =='0')#line:628
                OOOO0O00O0000O0OO =[]#line:630
                if OO0O0O00O0000OOO0 in ['movies','tvshows']:#line:632
                    OOOO0O0000O00O00O .update ({'trailer':'%s?action=trailer&name=%s'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (OO0O0OO0O00000O00 ))})#line:633
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30707 ).encode ('utf-8'),'RunPlugin(%s?action=trailer&name=%s)'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (OO0O0OO0O00000O00 ))))#line:634
                if OO0O0O00O0000OOO0 in ['movies','tvshows','seasons','episodes']:#line:636
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30708 ).encode ('utf-8'),'XBMC.Action(Info)'))#line:637
                if (OO000O0OO0OO0OOO0 ==False and not '|regex='in str (OOOO00O00OOO0O000 .get ('url')))or (OO000O0OO0OO0OOO0 ==True and OO0O0O00O0000OOO0 in ['tvshows','seasons']):#line:639
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30723 ).encode ('utf-8'),'RunPlugin(%s?action=queueItem)'%O0OOOO0O0O0O000OO ))#line:640
                if OO0O0O00O0000OOO0 =='movies':#line:642
                    try :O0OOOOO0O0OOO0000 ='%s (%s)'%(OOOO00O00OOO0O000 ['title'],OOOO00O00OOO0O000 ['year'])#line:643
                    except :O0OOOOO0O0OOO0000 =OO0O0OO0O00000O00 #line:644
                    try :OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (O0OOOOO0O0OOO0000 ),OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['url']),OO0O0OOOOOOOOOOO0 .quote_plus (O000000OO00OO0000 ))))#line:645
                    except :pass #line:646
                elif OO0O0O00O0000OOO0 =='episodes':#line:647
                    try :O0OOOOO0O0OOO0000 ='%s S%02dE%02d'%(OOOO00O00OOO0O000 ['tvshowtitle'],int (OOOO00O00OOO0O000 ['season']),int (OOOO00O00OOO0O000 ['episode']))#line:648
                    except :O0OOOOO0O0OOO0000 =OO0O0OO0O00000O00 #line:649
                    try :OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (O0OOOOO0O0OOO0000 ),OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['url']),OO0O0OOOOOOOOOOO0 .quote_plus (O000000OO00OO0000 ))))#line:650
                    except :pass #line:651
                elif OO0O0O00O0000OOO0 =='songs':#line:652
                    try :OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (OO0O0OO0O00000O00 ),OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['url']),OO0O0OOOOOOOOOOO0 .quote_plus (O000000OO00OO0000 ))))#line:653
                    except :pass #line:654
                if OO0OO0O0O0OOO0OO0 =='movies':#line:656
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30711 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=movies)'%O0OOOO0O0O0O000OO ))#line:657
                elif OO0OO0O0O0OOO0OO0 =='tvshows':#line:658
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30712 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=tvshows)'%O0OOOO0O0O0O000OO ))#line:659
                elif OO0OO0O0O0OOO0OO0 =='seasons':#line:660
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30713 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=seasons)'%O0OOOO0O0O0O000OO ))#line:661
                elif OO0OO0O0O0OOO0OO0 =='episodes':#line:662
                    OOOO0O00O0000O0OO .append ((O000OO0O0OOO00O0O .lang (30714 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=episodes)'%O0OOOO0O0O0O000OO ))#line:663
                if OOO0OO0O00O0OOOOO ==True :#line:665
                    try :OOOO0O00O0000O0OO .append (('Open in browser','RunPlugin(%s?action=browser&url=%s)'%(O0OOOO0O0O0O000OO ,OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['url']))))#line:666
                    except :pass #line:667
                O0000000O0OOO0O0O =O000OO0O0OOO00O0O .item (label =OO0O0OO0O00000O00 ,iconImage =O000000OO00OO0000 ,thumbnailImage =O000000OO00OO0000 )#line:670
                try :O0000000O0OOO0O0O .setArt ({'poster':O000000OO00OO0000 ,'tvshow.poster':O000000OO00OO0000 ,'season.poster':O000000OO00OO0000 ,'banner':OO0O0OOO00OOOOO00 ,'tvshow.banner':OO0O0OOO00OOOOO00 ,'season.banner':OO0O0OOO00OOOOO00 })#line:672
                except :pass #line:673
                if not O0O0O00O00000O000 =='0':#line:675
                    O0000000O0OOO0O0O .setProperty ('Fanart_Image',O0O0O00O00000O000 )#line:676
                elif not OOO00OO00000OOO0O ==None :#line:677
                    O0000000O0OOO0O0O .setProperty ('Fanart_Image',OOO00OO00000OOO0O )#line:678
                if queue ==False :#line:680
                    O0000000O0OOO0O0O .setInfo (type ='Video',infoLabels =OOOO0O0000O00O00O )#line:681
                    O0000000O0OOO0O0O .addContextMenuItems (OOOO0O00O0000O0OO )#line:682
                    O000OO0O0OOO00O0O .addItem (handle =int (O0OOO0000OO0O00O0 .argv [1 ]),url =O00000O00O00OOOOO ,listitem =O0000000O0OOO0O0O ,isFolder =OO000O0OO0OO0OOO0 )#line:683
                else :#line:684
                    O0000000O0OOO0O0O .setInfo (type ='Video',infoLabels =OOOO0O0000O00O00O )#line:685
                    OO00OOOOOO0OOO0OO .add (url =O00000O00O00OOOOO ,listitem =O0000000O0OOO0O0O )#line:686
            except :#line:687
                pass #line:688
        if not queue ==False :#line:690
            return O000OO0O0OOO00O0O .player .play (OO00OOOOOO0OOO0OO )#line:691
        try :#line:693
            OOOO00O00OOO0O000 =OO00OOOO0OO00O00O [0 ]#line:694
            if OOOO00O00OOO0O000 ['next']=='':raise Exception ()#line:695
            O00000O00O00OOOOO ='%s?action=%s&url=%s'%(O0OOOO0O0O0O000OO ,OOOO00O00OOO0O000 ['nextaction'],OO0O0OOOOOOOOOOO0 .quote_plus (OOOO00O00OOO0O000 ['next']))#line:696
            O0000000O0OOO0O0O =O000OO0O0OOO00O0O .item (label =O000OO0O0OOO00O0O .lang (30500 ).encode ('utf-8'))#line:697
            O0000000O0OOO0O0O .setArt ({'addonPoster':O000O00O00OOOOOOO ,'thumb':O000O00O00OOOOOOO ,'poster':O000O00O00OOOOOOO ,'tvshow.poster':O000O00O00OOOOOOO ,'season.poster':O000O00O00OOOOOOO ,'banner':O000O00O00OOOOOOO ,'tvshow.banner':O000O00O00OOOOOOO ,'season.banner':O000O00O00OOOOOOO })#line:698
            O0000000O0OOO0O0O .setProperty ('addonFanart_Image',OOO00OO00000OOO0O )#line:699
            O000OO0O0OOO00O0O .addItem (handle =int (O0OOO0000OO0O00O0 .argv [1 ]),url =O00000O00O00OOOOO ,listitem =O0000000O0OOO0O0O ,isFolder =True )#line:700
        except :#line:701
            pass #line:702
        if not OO0OO0O0O0OOO0OO0 ==None :O000OO0O0OOO00O0O .content (int (O0OOO0000OO0O00O0 .argv [1 ]),OO0OO0O0O0OOO0OO0 )#line:704
        O000OO0O0OOO00O0O .directory (int (O0OOO0000OO0O00O0 .argv [1 ]),cacheToDisc =True )#line:705
        if OO0OO0O0O0OOO0OO0 in ['movies','tvshows','seasons','episodes']:#line:706
            O00O0OO0OOOOOO0O0 .setView (OO0OO0O0O0OOO0OO0 ,{'skin.estuary':55 })#line:707
class resolver :#line:711
    def browser (O00OOO00000OOO0O0 ,OO0O0OO0O0OO0OO0O ):#line:712
        try :#line:713
            OO0O0OO0O0OO0OO0O =O00OOO00000OOO0O0 .get (OO0O0OO0O0OO0OO0O )#line:714
            if OO0O0OO0O0OO0OO0O ==False :return #line:715
            O000OO0O0OOO00O0O .execute ('RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)'%OO0O0OOOOOOOOOOO0 .quote_plus (OO0O0OO0O0OO0OO0O ))#line:716
        except :#line:717
            pass #line:718
    def link (OOO0OO0O0OO0O00O0 ,O00OOOO00O0000O00 ):#line:721
        try :#line:722
            O00OOOO00O0000O00 =OOO0OO0O0OO0O00O0 .get (O00OOOO00O0000O00 )#line:723
            if O00OOOO00O0000O00 ==False :return #line:724
            O000OO0O0OOO00O0O .execute ('ActivateWindow(busydialog)')#line:726
            O00OOOO00O0000O00 =OOO0OO0O0OO0O00O0 .process (O00OOOO00O0000O00 )#line:727
            O000OO0O0OOO00O0O .execute ('Dialog.Close(busydialog)')#line:728
            if O00OOOO00O0000O00 ==None :return O000OO0O0OOO00O0O .infoDialog (O000OO0O0OOO00O0O .lang (30705 ).encode ('utf-8'))#line:730
            return O00OOOO00O0000O00 #line:731
        except :#line:732
            pass #line:733
    def get (O0O00OOO0O000O00O ,OOOO0000OO000O00O ):#line:736
        try :#line:737
            OOO000O0000OO0O00 =OOO0O0000OOOO0O0O .compile ('<sublink(?:\s+name=|)(?:\'|\"|)(.*?)(?:\'|\"|)>(.+?)</sublink>').findall (OOOO0000OO000O00O )#line:738
            if len (OOO000O0000OO0O00 )==0 :return OOOO0000OO000O00O #line:740
            if len (OOO000O0000OO0O00 )==1 :return OOO000O0000OO0O00 [0 ][1 ]#line:741
            OOO000O0000OO0O00 =[('Link %s'%(int (OOO000O0000OO0O00 .index (OOO0O00O00OO00000 ))+1 )if OOO0O00O00OO00000 [0 ]==''else OOO0O00O00OO00000 [0 ],OOO0O00O00OO00000 [1 ])for OOO0O00O00OO00000 in OOO000O0000OO0O00 ]#line:743
            O0O000000000O0OOO =O000OO0O0OOO00O0O .selectDialog ([OO0OO0OOO0O0OO000 [0 ]for OO0OO0OOO0O0OO000 in OOO000O0000OO0O00 ],O000OO0O0OOO00O0O .infoLabel ('listitem.label'))#line:745
            if O0O000000000O0OOO ==-1 :return False #line:747
            else :return OOO000O0000OO0O00 [O0O000000000O0OOO ][1 ]#line:748
        except :#line:749
            pass #line:750
    def f4m (OO0000000OOO0O0OO ,O00O0000OOOO0O0O0 ,O00O0OOOOO0OO0OOO ):#line:753
            try :#line:754
                if not any (O00OOO000000O0000 in O00O0000OOOO0O0O0 for O00OOO000000O0000 in ['.f4m','.ts']):raise Exception ()#line:755
                OOO0OOO00000OOOO0 =O00O0000OOOO0O0O0 .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:756
                if not OOO0OOO00000OOOO0 in ['f4m','ts']:raise Exception ()#line:757
                OO0O000O00O0O0O0O =OOOOOO00O000OOOOO .parse_qs (O00O0000OOOO0O0O0 )#line:759
                try :O0OO00O0O0OOO0000 =OO0O000O00O0O0O0O ['proxy'][0 ]#line:761
                except :O0OO00O0O0OOO0000 =None #line:762
                try :O000OOO00OOOOO00O =OOO0O0OO0O00O0OO0 .loads (OO0O000O00O0O0O0O ['proxy_for_chunks'][0 ])#line:764
                except :O000OOO00OOOOO00O =True #line:765
                try :O0000O0O000OO0OO0 =int (OO0O000O00O0O0O0O ['maxbitrate'][0 ])#line:767
                except :O0000O0O000OO0OO0 =0 #line:768
                try :OOO0O0OOOOO0O0OOO =OOO0O0OO0O00O0OO0 .loads (OO0O000O00O0O0O0O ['simpledownloader'][0 ])#line:770
                except :OOO0O0OOOOO0O0OOO =False #line:771
                try :OOO00OO0O000O0000 =OO0O000O00O0O0O0O ['auth'][0 ]#line:773
                except :OOO00OO0O000O0000 =''#line:774
                try :O000O0O0OOO0O00OO =OO0O000O00O0O0O0O ['streamtype'][0 ]#line:776
                except :O000O0O0OOO0O00OO ='TSDOWNLOADER'if OOO0OOO00000OOOO0 =='ts'else 'HDS'#line:777
                try :OOOOO0O00O0O0OO0O =OO0O000O00O0O0O0O ['swf'][0 ]#line:779
                except :OOOOO0O00O0O0OO0O =None #line:780
                from F4mProxy import f4mProxyHelper as OO00000O000O0OOO0 #line:782
                return OO00000O000O0OOO0 ().playF4mLink (O00O0000OOOO0O0O0 ,O00O0OOOOO0OO0OOO ,O0OO00O0O0OOO0000 ,O000OOO00OOOOO00O ,O0000O0O000OO0OO0 ,OOO0O0OOOOO0O0OOO ,OOO00OO0O000O0000 ,O000O0O0OOO0O00OO ,False ,OOOOO0O00O0O0OO0O )#line:783
            except :#line:784
                pass #line:785
    def process (OO0O0O00O0OOO00O0 ,O0OOOOOOO0000OO0O ,direct =True ):#line:788
        try :#line:789
            if not any (O0000O0000OOO00O0 in O0OOOOOOO0000OO0O for O0000O0000OOO00O0 in ['.jpg','.png','.gif']):raise Exception ()#line:790
            O00O00OO000000O0O =O0OOOOOOO0000OO0O .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:791
            if not O00O00OO000000O0O in ['jpg','png','gif']:raise Exception ()#line:792
            try :#line:793
                O0OO0OO00O0OOO000 =O000OO0OO000OOO00 .path .join (O000OO0O0OOO00O0O .dataPath ,'img')#line:794
                O000OO0O0OOO00O0O .deleteFile (O0OO0OO00O0OOO000 )#line:795
                O0OOO0O00OO0O000O =O000OO0O0OOO00O0O .openFile (O0OO0OO00O0OOO000 ,'w')#line:796
                O0OOO0O00OO0O000O .write (O0OOOOO0O0OOO0OO0 .request (O0OOOOOOO0000OO0O ))#line:797
                O0OOO0O00OO0O000O .close ()#line:798
                O000OO0O0OOO00O0O .execute ('ShowPicture("%s")'%O0OO0OO00O0OOO000 )#line:799
                return False #line:800
            except :#line:801
                return #line:802
        except :#line:803
            pass #line:804
        try :#line:806
            O00OO0O0OOOOO00O0 ,OO0OOO0O000O000OO =OOO0O0000OOOO0O0O .findall ('(.+?)\|regex=(.+?)$',O0OOOOOOO0000OO0O )[0 ]#line:807
            OO0OOO0O000O000OO =O0O0000OOO0OO0OO0 .fetch (OO0OOO0O000O000OO )#line:808
            O00OO0O0OOOOO00O0 +=OO0O0OOOOOOOOOOO0 .unquote_plus (OO0OOO0O000O000OO )#line:809
            if not '</regex>'in O00OO0O0OOOOO00O0 :raise Exception ()#line:810
            O0O00000O00OO000O =O0O0000OOO0OO0OO0 .resolve (O00OO0O0OOOOO00O0 )#line:811
            if not O0O00000O00OO000O ==None :O0OOOOOOO0000OO0O =O0O00000O00OO000O #line:812
        except :#line:813
            pass #line:814
        try :#line:816
            if not O0OOOOOOO0000OO0O .startswith ('rtmp'):raise Exception ()#line:817
            if len (OOO0O0000OOOO0O0O .compile ('\s*timeout=(\d*)').findall (O0OOOOOOO0000OO0O ))==0 :O0OOOOOOO0000OO0O +=' timeout=10'#line:818
            return O0OOOOOOO0000OO0O #line:819
        except :#line:820
            pass #line:821
        try :#line:823
            if not any (O0O000OOOO0OOOO0O in O0OOOOOOO0000OO0O for O0O000OOOO0OOOO0O in ['.m3u8','.f4m','.ts']):raise Exception ()#line:824
            O00O00OO000000O0O =O0OOOOOOO0000OO0O .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:825
            if not O00O00OO000000O0O in ['m3u8','f4m','ts']:raise Exception ()#line:826
            return O0OOOOOOO0000OO0O #line:827
        except :#line:828
            pass #line:829
        try :#line:831
            O00OOO000O0OOOOO0 =OOO0O0000OOOO0O0O .findall ('<preset>(.+?)</preset>',O0OOOOOOO0000OO0O )[0 ]#line:832
            if not 'search'in O00OOO000O0OOOOO0 :raise Exception ()#line:834
            OO000O0O0OOO0O000 ,OO0OOOO00OO00O0O0 ,OO0OO00O0O0OOO000 =OOO0O0000OOOO0O0O .findall ('<title>(.+?)</title>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<year>(.+?)</year>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<imdb>(.+?)</imdb>',O0OOOOOOO0000OO0O )[0 ]#line:836
            try :OOOO0OOOOOO0000O0 ,O00OOO0O0OO0OOO00 ,OO0OO00O00OO00OOO ,OO00OOOOOO000000O ,O0OOO0O00OOO0OOOO =OOO0O0000OOOO0O0O .findall ('<tvdb>(.+?)</tvdb>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<premiered>(.+?)</premiered>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<season>(.+?)</season>',O0OOOOOOO0000OO0O )[0 ],OOO0O0000OOOO0O0O .findall ('<episode>(.+?)</episode>',O0OOOOOOO0000OO0O )[0 ]#line:838
            except :OOOO0OOOOOO0000O0 =O00OOO0O0OO0OOO00 =OO0OO00O00OO00OOO =OO00OOOOOO000000O =O0OOO0O00OOO0OOOO =None #line:839
            direct =False #line:841
            OO0000OO0O0O0OOOO ='HD'if not O00OOO000O0OOOOO0 =='searchsd'else 'SD'#line:843
            from resources .lib .sources import sources as OO000O00O0OOOOO0O #line:845
            O0O00000O00OO000O =OO000O00O0OOOOO0O ().getSources (OO000O0O0OOO0O000 ,OO0OOOO00OO00O0O0 ,OO0OO00O0O0OOO000 ,OOOO0OOOOOO0000O0 ,OO00OOOOOO000000O ,O0OOO0O00OOO0OOOO ,O00OOO0O0OO0OOO00 ,OO0OO00O00OO00OOO ,OO0000OO0O0O0OOOO )#line:847
            if not O0O00000O00OO000O ==None :return O0O00000O00OO000O #line:849
        except :#line:850
            pass #line:851
        try :#line:853
            from resources .lib .sources import sources as OO000O00O0OOOOO0O #line:854
            O0O00000O00OO000O =OO000O00O0OOOOO0O ().getURISource (O0OOOOOOO0000OO0O )#line:856
            if not O0O00000O00OO000O ==False :direct =False #line:858
            if O0O00000O00OO000O ==None or O0O00000O00OO000O ==False :raise Exception ()#line:859
            return O0O00000O00OO000O #line:861
        except :#line:862
            pass #line:863
        try :#line:865
            if not '.google.com'in O0OOOOOOO0000OO0O :raise Exception ()#line:866
            from resources .lib .modules import directstream as OOO0OO0O0O00O000O #line:867
            O0O00000O00OO000O =OOO0OO0O0O00O000O .google (O0OOOOOOO0000OO0O )[0 ]['url']#line:868
            return O0O00000O00OO000O #line:869
        except :#line:870
            pass #line:871
        try :#line:873
            if not 'filmon.com/'in O0OOOOOOO0000OO0O :raise Exception ()#line:874
            from resources .lib .modules import filmon as O0000OOOO00O0O0OO #line:875
            O0O00000O00OO000O =O0000OOOO00O0O0OO .resolve (O0OOOOOOO0000OO0O )#line:876
            return O0O00000O00OO000O #line:877
        except :#line:878
            pass #line:879
        try :#line:881
            import urlresolver as O0O0OO000OO0OOOO0 #line:882
            O0O0O0OOO00OO00OO =O0O0OO000OO0OOOO0 .HostedMediaFile (url =O0OOOOOOO0000OO0O )#line:884
            if O0O0O0OOO00OO00OO .valid_url ()==False :raise Exception ()#line:886
            direct =False ;O0O00000O00OO000O =O0O0O0OOO00OO00OO .resolve ()#line:888
            if not O0O00000O00OO000O ==False :return O0O00000O00OO000O #line:890
        except :#line:891
            pass #line:892
        if direct ==True :return O0OOOOOOO0000OO0O #line:894
class player (OOO00O000OOOO00OO .Player ):#line:897
    def __init__ (O00OOO000OOOO000O ):#line:898
        OOO00O000OOOO00OO .Player .__init__ (O00OOO000OOOO000O )#line:899
    def play (O0O00OOO0000O00OO ,O0O0OOOOOOO00O000 ,content =None ):#line:902
        try :#line:903
            O0OO00O0OOOO00OO0 =O0O0OOOOOOO00O000 #line:904
            O0O0OOOOOOO00O000 =resolver ().get (O0O0OOOOOOO00O000 )#line:906
            if O0O0OOOOOOO00O000 ==False :return #line:907
            O000OO0O0OOO00O0O .execute ('ActivateWindow(busydialog)')#line:909
            O0O0OOOOOOO00O000 =resolver ().process (O0O0OOOOOOO00O000 )#line:910
            O000OO0O0OOO00O0O .execute ('Dialog.Close(busydialog)')#line:911
            if O0O0OOOOOOO00O000 ==None :return O000OO0O0OOO00O0O .infoDialog (O000OO0O0OOO00O0O .lang (30705 ).encode ('utf-8'))#line:913
            if O0O0OOOOOOO00O000 ==False :return #line:914
            O000OO0000OOO0O00 ={}#line:916
            for O0OO000000OOO0OO0 in ['title','originaltitle','tvshowtitle','year','season','episode','genre','rating','votes','director','writer','plot','tagline']:#line:917
                try :O000OO0000OOO0O00 [O0OO000000OOO0OO0 ]=O000OO0O0OOO00O0O .infoLabel ('listitem.%s'%O0OO000000OOO0OO0 )#line:918
                except :pass #line:919
            O000OO0000OOO0O00 =dict ((O0O0000OOOO00OO0O ,O00O0OO000OO00O0O )for O0O0000OOOO00OO0O ,O00O0OO000OO00O0O in O000OO0000OOO0O00 .iteritems ()if not O00O0OO000OO00O0O =='')#line:920
            if not 'title'in O000OO0000OOO0O00 :O000OO0000OOO0O00 ['title']=O000OO0O0OOO00O0O .infoLabel ('listitem.label')#line:921
            O00OOO0O00O000OOO =O000OO0O0OOO00O0O .infoLabel ('listitem.icon')#line:922
            O0O00OOO0000O00OO .name =O000OO0000OOO0O00 ['title'];O0O00OOO0000O00OO .year =O000OO0000OOO0O00 ['year']if 'year'in O000OO0000OOO0O00 else '0'#line:925
            O0O00OOO0000O00OO .getbookmark =True if (content =='movies'or content =='episodes')else False #line:927
            O0O00OOO0000O00OO .offset =bookmarks ().get (O0O00OOO0000O00OO .name ,O0O00OOO0000O00OO .year )#line:929
            OO00O00O00O0OO00O =resolver ().f4m (O0O0OOOOOOO00O000 ,O0O00OOO0000O00OO .name )#line:931
            if not OO00O00O00O0OO00O ==None :return #line:932
            O0000000O000OO00O =O000OO0O0OOO00O0O .item (path =O0O0OOOOOOO00O000 ,iconImage =O00OOO0O00O000OOO ,thumbnailImage =O00OOO0O00O000OOO )#line:935
            try :O0000000O000OO00O .setArt ({'icon':O00OOO0O00O000OOO })#line:936
            except :pass #line:937
            O0000000O000OO00O .setInfo (type ='Video',infoLabels =O000OO0000OOO0O00 )#line:938
            O000OO0O0OOO00O0O .player .play (O0O0OOOOOOO00O000 ,O0000000O000OO00O )#line:939
            O000OO0O0OOO00O0O .resolve (int (O0OOO0000OO0O00O0 .argv [1 ]),True ,O0000000O000OO00O )#line:940
            O0O00OOO0000O00OO .totalTime =0 ;O0O00OOO0000O00OO .currentTime =0 #line:942
            for O0OO000000OOO0OO0 in range (0 ,240 ):#line:944
                if O0O00OOO0000O00OO .isPlayingVideo ():break #line:945
                O000OO0O0OOO00O0O .sleep (1000 )#line:946
            while O0O00OOO0000O00OO .isPlayingVideo ():#line:947
                try :#line:948
                    O0O00OOO0000O00OO .totalTime =O0O00OOO0000O00OO .getTotalTime ()#line:949
                    O0O00OOO0000O00OO .currentTime =O0O00OOO0000O00OO .getTime ()#line:950
                except :#line:951
                    pass #line:952
                O000OO0O0OOO00O0O .sleep (2000 )#line:953
            O000OO0O0OOO00O0O .sleep (5000 )#line:954
        except :#line:955
            pass #line:956
    def onPlayBackStarted (O0000O000OO000O00 ):#line:959
        O000OO0O0OOO00O0O .execute ('Dialog.Close(all,true)')#line:960
        if O0000O000OO000O00 .getbookmark ==True and not O0000O000OO000O00 .offset =='0':#line:961
            O0000O000OO000O00 .seekTime (float (O0000O000OO000O00 .offset ))#line:962
    def onPlayBackStopped (OOO00OO0OOO0O00O0 ):#line:965
        if OOO00OO0OOO0O00O0 .getbookmark ==True :#line:966
            bookmarks ().reset (OOO00OO0OOO0O00O0 .currentTime ,OOO00OO0OOO0O00O0 .totalTime ,OOO00OO0OOO0O00O0 .name ,OOO00OO0OOO0O00O0 .year )#line:967
    def onPlayBackEnded (OO0OOOO0O00OO0O0O ):#line:970
        OO0OOOO0O00OO0O0O .onPlayBackStopped ()#line:971
class bookmarks :#line:975
    def get (OO0OOOO0OO0OOO0OO ,O0O00OO0OOOOOOO0O ,year ='0'):#line:976
        try :#line:977
            OOOOO000O0OO0O0OO ='0'#line:978
            OOO0OOO00OOO0O0OO =O0000O0O00O0OOO0O .md5 ()#line:982
            for O0O0O0O0OO0OOOOOO in O0O00OO0OOOOOOO0O :OOO0OOO00OOO0O0OO .update (str (O0O0O0O0OO0OOOOOO ))#line:983
            for O0O0O0O0OO0OOOOOO in year :OOO0OOO00OOO0O0OO .update (str (O0O0O0O0OO0OOOOOO ))#line:984
            OOO0OOO00OOO0O0OO =str (OOO0OOO00OOO0O0OO .hexdigest ())#line:985
            O0O0O00OO000OOO00 =OO000OO0000OO000O .connect (O000OO0O0OOO00O0O .bookmarksFile )#line:987
            OOO00000O0OOO00OO =O0O0O00OO000OOO00 .cursor ()#line:988
            OOO00000O0OOO00OO .execute ("SELECT * FROM bookmark WHERE idFile = '%s'"%OOO0OOO00OOO0O0OO )#line:989
            OO0OO00O00O000OOO =OOO00000O0OOO00OO .fetchone ()#line:990
            OO0OOOO0OO0OOO0OO .offset =str (OO0OO00O00O000OOO [1 ])#line:991
            O0O0O00OO000OOO00 .commit ()#line:992
            if OO0OOOO0OO0OOO0OO .offset =='0':raise Exception ()#line:994
            OO00OOOOOOO000O00 ,O0OOO000O0O0OOO00 =divmod (float (OO0OOOO0OO0OOO0OO .offset ),60 );O00O00OOO00OO00O0 ,OO00OOOOOOO000O00 =divmod (OO00OOOOOOO000O00 ,60 )#line:996
            OO00O0O0OOOOO000O ='%02d:%02d:%02d'%(O00O00OOO00OO00O0 ,OO00OOOOOOO000O00 ,O0OOO000O0O0OOO00 )#line:997
            OO00O0O0OOOOO000O =(O000OO0O0OOO00O0O .lang (32502 )%OO00O0O0OOOOO000O ).encode ('utf-8')#line:998
            try :OO00O0O0000O00OO0 =O000OO0O0OOO00O0O .dialog .contextmenu ([OO00O0O0OOOOO000O ,O000OO0O0OOO00O0O .lang (32501 ).encode ('utf-8'),])#line:1000
            except :OO00O0O0000O00OO0 =O000OO0O0OOO00O0O .yesnoDialog (OO00O0O0OOOOO000O ,'','',str (O0O00OO0OOOOOOO0O ),O000OO0O0OOO00O0O .lang (32503 ).encode ('utf-8'),O000OO0O0OOO00O0O .lang (32501 ).encode ('utf-8'))#line:1001
            if OO00O0O0000O00OO0 :OO0OOOO0OO0OOO0OO .offset ='0'#line:1003
            return OO0OOOO0OO0OOO0OO .offset #line:1005
        except :#line:1006
            return OOOOO000O0OO0O0OO #line:1007
    def reset (O0000O00O000000O0 ,O00OOO0OO0000OO0O ,O0O0O00OO0OO00000 ,OOO00OOOO0O0OOOOO ,year ='0'):#line:1010
        try :#line:1011
            OO000O0O00O0O0OO0 =str (O00OOO0OO0000OO0O )#line:1014
            OOOOO0O000000OO0O =int (O00OOO0OO0000OO0O )>180 and (O00OOO0OO0000OO0O /O0O0O00OO0OO00000 )<=.92 #line:1015
            O0O00OOO000000O0O =O0000O0O00O0OOO0O .md5 ()#line:1017
            for O0O00O0O000OOO000 in OOO00OOOO0O0OOOOO :O0O00OOO000000O0O .update (str (O0O00O0O000OOO000 ))#line:1018
            for O0O00O0O000OOO000 in year :O0O00OOO000000O0O .update (str (O0O00O0O000OOO000 ))#line:1019
            O0O00OOO000000O0O =str (O0O00OOO000000O0O .hexdigest ())#line:1020
            O000OO0O0OOO00O0O .makeFile (O000OO0O0OOO00O0O .dataPath )#line:1022
            O0O0OO00O0O00OOOO =OO000OO0000OO000O .connect (O000OO0O0OOO00O0O .bookmarksFile )#line:1023
            O0OO000O0OO0OOO0O =O0O0OO00O0O00OOOO .cursor ()#line:1024
            O0OO000O0OO0OOO0O .execute ("CREATE TABLE IF NOT EXISTS bookmark (" "idFile TEXT, " "timeInSeconds TEXT, " "UNIQUE(idFile)" ");")#line:1025
            O0OO000O0OO0OOO0O .execute ("DELETE FROM bookmark WHERE idFile = '%s'"%O0O00OOO000000O0O )#line:1026
            if OOOOO0O000000OO0O :O0OO000O0OO0OOO0O .execute ("INSERT INTO bookmark Values (?, ?)",(O0O00OOO000000O0O ,OO000O0O00O0O0OO0 ))#line:1027
            O0O0OO00O0O00OOOO .commit ()#line:1028
        except :#line:1029
            pass 
#e9015584e6a44b14988f13e2298bcbf9
