import os as OOOOOOO00OOO0O0O0 ,re as OO0O000OOO00O0OOO ,sys as OO00000OO00000000 ,hashlib as O0OOOO00O0OO0O000 ,urllib as OOOOOO000O000OOOO ,urlparse as OOO0OO0000OO0OOOO ,json as OO00000O0OOOOOOOO ,base64 as OOOO0O0O0OO0O0000 ,random as OOOOOO00OOO0OO0O0 ,datetime as OOO00O0O000OO0O00 #line:1
import xbmc as O0OOO00O000OO00OO #line:2
try :from sqlite3 import dbapi2 as OOO0OO00OO0OO0O00 #line:4
except :from pysqlite2 import dbapi2 as OOO0OO00OO0OO0O00 #line:5
from resources .lib .modules import cache as O0OOOOO0OO0O0O00O #line:7
from resources .lib .modules import metacache as OOO0OO0OO0O0000O0 #line:8
from resources .lib .modules import client as O00O00O0OO00OOO00 #line:9
from resources .lib .modules import control as O000OOO0OOO0000O0 #line:10
from resources .lib .modules import regex as OO00O0OO0OO000000 #line:11
from resources .lib .modules import trailer as OOO0O0OOO000O0OOO #line:12
from resources .lib .modules import workers as O0O0OOO000O000O0O #line:13
from resources .lib .modules import youtube as O000OOOO00OOOOO0O #line:14
from resources .lib .modules import views as O0OO0OOOOO0OOOO0O #line:15
version =102 #line:18
class indexer :#line:20
    def __init__ (O0OO0O00000O000OO ):#line:21
        O0OO0O00000O000OO .list =[];O0OO0O00000O000OO .hash =[]#line:22
    def root (O00O0OOOO00O00OO0 ):#line:25
        try :#line:26
            OO00O0OO0OO000000 .clear ()#line:27
            O0O000O0OOO0OOO0O ='http://beaub.srve.io/specialist/addon/specialist%20index.xml'#line:28
            O00O0OOOO00O00OO0 .list =O00O0OOOO00O00OO0 .specialist_list (O0O000O0OOO0OOO0O )#line:29
            for O00OO0O0O00O000OO in O00O0OOOO00O00OO0 .list :O00OO0O0O00O000OO .update ({'content':'addons'})#line:30
            O00O0OOOO00O00OO0 .addDirectory (O00O0OOOO00O00OO0 .list )#line:31
            return O00O0OOOO00O00OO0 .list #line:32
        except :#line:33
            pass #line:34
    def get (OO000000O00O0OO00 ,O0OOO000OOOOO0O0O ):#line:37
        try :#line:38
            OO000000O00O0OO00 .list =OO000000O00O0OO00 .specialist_list (O0OOO000OOOOO0O0O )#line:39
            OO000000O00O0OO00 .worker ()#line:40
            OO000000O00O0OO00 .addDirectory (OO000000O00O0OO00 .list )#line:41
            return OO000000O00O0OO00 .list #line:42
        except :#line:43
            pass #line:44
    def getq (OOOO0000OOO000O0O ,O0O000O0O0OO00O00 ):#line:47
        try :#line:48
            OOOO0000OOO000O0O .list =OOOO0000OOO000O0O .specialist_list (O0O000O0O0OO00O00 )#line:49
            OOOO0000OOO000O0O .worker ()#line:50
            OOOO0000OOO000O0O .addDirectory (OOOO0000OOO000O0O .list ,queue =True )#line:51
            return OOOO0000OOO000O0O .list #line:52
        except :#line:53
            pass #line:54
    def getx (O0OOO0000O000OOO0 ,OOOO0OOO00O0O0000 ,worker =False ):#line:57
        try :#line:58
            OO000OO0000O000O0 ,OO0OO000O0O0O0OO0 =OO0O000OOO00O0OOO .findall ('(.+?)\|regex=(.+?)$',OOOO0OOO00O0O0000 )[0 ]#line:59
            OO0OO000O0O0O0OO0 =OO00O0OO0OO000000 .fetch (OO0OO000O0O0O0OO0 )#line:60
            OO000OO0000O000O0 +=OOOOOO000O000OOOO .unquote_plus (OO0OO000O0O0O0OO0 )#line:61
            OOOO0OOO00O0O0000 =OO00O0OO0OO000000 .resolve (OO000OO0000O000O0 )#line:62
            O0OOO0000O000OOO0 .list =O0OOO0000O000OOO0 .specialist_list ('',result =OOOO0OOO00O0O0000 )#line:63
            O0OOO0000O000OOO0 .addDirectory (O0OOO0000O000OOO0 .list )#line:64
            return O0OOO0000O000OOO0 .list #line:65
        except :#line:66
            pass #line:67
    def developer (OO00O0OO0O00OO00O ):#line:70
        try :#line:71
            O0000000O0OOO000O =OOOOOOO00OOO0O0O0 .path .join (O000OOO0OOO0000O0 .dataPath ,'testings.xml')#line:72
            O00OOOO00OO0OO0OO =O000OOO0OOO0000O0 .openFile (O0000000O0OOO000O );O0O0O0OOOO0OO0OOO =O00OOOO00OO0OO0OO .read ();O00OOOO00OO0OO0OO .close ()#line:73
            OO00O0OO0O00OO00O .list =OO00O0OO0O00OO00O .specialist_list ('',result =O0O0O0OOOO0OO0OOO )#line:74
            for O0OOO0OO0000OOO00 in OO00O0OO0O00OO00O .list :O0OOO0OO0000OOO00 .update ({'content':'videos'})#line:75
            OO00O0OO0O00OO00O .addDirectory (OO00O0OO0O00OO00O .list )#line:76
            return OO00O0OO0O00OO00O .list #line:77
        except :#line:78
            pass #line:79
    def youtube (O00O0O00OOOOO00OO ,OO0O0O0OOOO00O000 ,O0O0OOO000OOO0OO0 ):#line:82
        try :#line:83
            O0OOOOOOO000OO0O0 =OOO0O0OOO000O0OOO .trailer ().key_link .split ('=',1 )[-1 ]#line:84
            if 'PlaylistTuner'in O0O0OOO000OOO0OO0 :#line:86
                O00O0O00OOOOO00OO .list =O0OOOOO0OO0O0O00O .get (O000OOOO00OOOOO0O .youtube (key =O0OOOOOOO000OO0O0 ).playlist ,1 ,OO0O0O0OOOO00O000 )#line:87
            elif 'Playlist'in O0O0OOO000OOO0OO0 :#line:88
                O00O0O00OOOOO00OO .list =O0OOOOO0OO0O0O00O .get (O000OOOO00OOOOO0O .youtube (key =O0OOOOOOO000OO0O0 ).playlist ,1 ,OO0O0O0OOOO00O000 ,True )#line:89
            elif 'ChannelTuner'in O0O0OOO000OOO0OO0 :#line:90
                O00O0O00OOOOO00OO .list =O0OOOOO0OO0O0O00O .get (O000OOOO00OOOOO0O .youtube (key =O0OOOOOOO000OO0O0 ).videos ,1 ,OO0O0O0OOOO00O000 )#line:91
            elif 'Channel'in O0O0OOO000OOO0OO0 :#line:92
                O00O0O00OOOOO00OO .list =O0OOOOO0OO0O0O00O .get (O000OOOO00OOOOO0O .youtube (key =O0OOOOOOO000OO0O0 ).videos ,1 ,OO0O0O0OOOO00O000 ,True )#line:93
            if 'Tuner'in O0O0OOO000OOO0OO0 :#line:95
                for O00O00O00OOO00O00 in O00O0O00OOOOO00OO .list :O00O00O00OOO00O00 .update ({'name':O00O00O00OOO00O00 ['title'],'poster':O00O00O00OOO00O00 ['image'],'action':'plugin','folder':False })#line:96
                if 'Tuner2'in O0O0OOO000OOO0OO0 :O00O0O00OOOOO00OO .list =sorted (O00O0O00OOOOO00OO .list ,key =lambda OO0OO0OOO00OO0OO0 :OOOOOO00OOO0OO0O0 .random ())#line:97
                O00O0O00OOOOO00OO .addDirectory (O00O0O00OOOOO00OO .list ,queue =True )#line:98
            else :#line:99
                for O00O00O00OOO00O00 in O00O0O00OOOOO00OO .list :O00O00O00OOO00O00 .update ({'name':O00O00O00OOO00O00 ['title'],'poster':O00O00O00OOO00O00 ['image'],'nextaction':O0O0OOO000OOO0OO0 ,'action':'play','folder':False })#line:100
                O00O0O00OOOOO00OO .addDirectory (O00O0O00OOOOO00OO .list )#line:101
            return O00O0O00OOOOO00OO .list #line:103
        except :#line:104
            pass #line:105
    def tvtuner (OO000000OO0O00000 ,O0OOO0O00O00OO0OO ):#line:108
        try :#line:109
            OOOOOOOOO00OOOOOO =OO0O000OOO00O0OOO .findall ('<preset>(.+?)</preset>',O0OOO0O00O00OO0OO )[0 ]#line:110
            OOO00000OO0O0O0O0 =((OOO00O0O000OO0O00 .datetime .utcnow ()-OOO00O0O000OO0O00 .timedelta (hours =5 ))).strftime ('%Y-%m-%d')#line:112
            OOO00000OO0O0O0O0 =int (OO0O000OOO00O0OOO .sub ('[^0-9]','',str (OOO00000OO0O0O0O0 )))#line:113
            O0OOO0O00O00OO0OO ,OO000OOOOOO00OOOO ,O00O00OO00OO00OOO ,OO00OO0O0OO0OO0O0 ,OO00O00O00OOOO0OO ,O00OOOOOO000O0000 ,OOOO0O0O00000000O =OO0O000OOO00O0OOO .findall ('<url>(.+?)</url>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<imdb>(.+?)</imdb>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<tvdb>(.+?)</tvdb>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<year>(.+?)</year>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<thumbnail>(.+?)</thumbnail>',O0OOO0O00O00OO0OO )[0 ],OO0O000OOO00O0OOO .findall ('<fanart>(.+?)</fanart>',O0OOO0O00O00OO0OO )[0 ]#line:115
            OO0O00O000OOO0OO0 =O00O00O0OO00OOO00 .request ('http://api.tvmaze.com/lookup/shows?thetvdb=%s'%O00O00OO00OO00OOO )#line:117
            if OO0O00O000OOO0OO0 ==None :OO0O00O000OOO0OO0 =O00O00O0OO00OOO00 .request ('http://api.tvmaze.com/lookup/shows?imdb=%s'%OO000OOOOOO00OOOO )#line:118
            OO0O00O000OOO0OO0 ='http://api.tvmaze.com/shows/%s/episodes'%str (OO00000O0OOOOOOOO .loads (OO0O00O000OOO0OO0 ).get ('id'))#line:119
            O0O000000O0000O0O =OO00000O0OOOOOOOO .loads (O00O00O0OO00OOO00 .request (OO0O00O000OOO0OO0 ))#line:120
            O0O000000O0000O0O =[(str (O0000OO0OO00O0OO0 .get ('season')),str (O0000OO0OO00O0OO0 .get ('number')),O0000OO0OO00O0OO0 .get ('name').strip (),O0000OO0OO00O0OO0 .get ('airdate'))for O0000OO0OO00O0OO0 in O0O000000O0000O0O ]#line:121
            if OOOOOOOOO00OOOOOO =='tvtuner':#line:123
                O000OO00OO0OOO000 =OOOOOO00OOO0OO0O0 .choice (O0O000000O0000O0O )#line:124
                O0O000000O0000O0O =O0O000000O0000O0O [O0O000000O0000O0O .index (O000OO00OO0OOO000 ):]+O0O000000O0000O0O [:O0O000000O0000O0O .index (O000OO00OO0OOO000 )]#line:125
                O0O000000O0000O0O =O0O000000O0000O0O [:100 ]#line:126
            O00OOO0000OOOOOOO =''#line:128
            for O000O00OO00OOOO0O in O0O000000O0000O0O :#line:130
                try :#line:131
                    if int (OO0O000OOO00O0OOO .sub ('[^0-9]','',str (O000O00OO00OOOO0O [3 ])))>OOO00000OO0O0O0O0 :raise Exception ()#line:132
                    O00OOO0000OOOOOOO +='<item><title> %01dx%02d . %s</title><meta><content>episode</content><imdb>%s</imdb><tvdb>%s</tvdb><tvshowtitle>%s</tvshowtitle><year>%s</year><title>%s</title><premiered>%s</premiered><season>%01d</season><episode>%01d</episode></meta><link><sublink>search</sublink><sublink>searchsd</sublink></link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(int (O000O00OO00OOOO0O [0 ]),int (O000O00OO00OOOO0O [1 ]),O000O00OO00OOOO0O [2 ],OO000OOOOOO00OOOO ,O00O00OO00OO00OOO ,OO00OO0O0OO0OO0O0 ,OO00O00O00OOOO0OO ,O000O00OO00OOOO0O [2 ],O000O00OO00OOOO0O [3 ],int (O000O00OO00OOOO0O [0 ]),int (O000O00OO00OOOO0O [1 ]),O00OOOOOO000O0000 ,OOOO0O0O00000000O )#line:133
                except :#line:134
                    pass #line:135
            O00OOO0000OOOOOOO =OO0O000OOO00O0OOO .sub (r'[^\x00-\x7F]+',' ',O00OOO0000OOOOOOO )#line:137
            if OOOOOOOOO00OOOOOO =='tvtuner':#line:139
                O00OOO0000OOOOOOO =O00OOO0000OOOOOOO .replace ('<sublink>searchsd</sublink>','')#line:140
            OO000000OO0O00000 .list =OO000000OO0O00000 .specialist_list ('',result =O00OOO0000OOOOOOO )#line:142
            if OOOOOOOOO00OOOOOO =='tvtuner':#line:144
                OO000000OO0O00000 .addDirectory (OO000000OO0O00000 .list ,queue =True )#line:145
            else :#line:146
                OO000000OO0O00000 .worker ()#line:147
                OO000000OO0O00000 .addDirectory (OO000000OO0O00000 .list )#line:148
        except :#line:149
            pass #line:150
    def search (OO0OO0O00OOOOO00O ):#line:153
        try :#line:154
            OO0OO0O00OOOOO00O .list =[{'name':30702 ,'action':'addSearch'}]#line:155
            OO0OO0O00OOOOO00O .list +=[{'name':30703 ,'action':'delSearch'}]#line:156
            try :#line:158
                def O0OO0000O0O0OOO0O ():return #line:159
                O0OOO000O0O0000O0 =O0OOOOO0OO0O0O00O .get (O0OO0000O0O0OOO0O ,600000000 ,table ='rel_srch')#line:160
                for O0OOO000OO000OOOO in O0OOO000O0O0000O0 :#line:162
                    try :OO0OO0O00OOOOO00O .list +=[{'name':'%s...'%O0OOO000OO000OOOO ,'url':O0OOO000OO000OOOO ,'action':'addSearch'}]#line:163
                    except :pass #line:164
            except :#line:165
                pass #line:166
            OO0OO0O00OOOOO00O .addDirectory (OO0OO0O00OOOOO00O .list )#line:168
            return OO0OO0O00OOOOO00O .list #line:169
        except :#line:170
            pass #line:171
    def delSearch (OO0OOOOO00OOOOOO0 ):#line:174
        try :#line:175
            O0OOOOO0OO0O0O00O .clear ('rel_srch')#line:176
            O000OOO0OOO0000O0 .refresh ()#line:177
        except :#line:178
            pass #line:179
    def addSearch (OO00O00000OO000O0 ,url =None ):#line:182
        try :#line:183
            O00OOOO000O0000OO ='http://beaub.srve.io/specialist/addon/search.xml'#line:184
            if (url ==None or url ==''):#line:186
                OOO0OOOO00OO00O0O =O000OOO0OOO0000O0 .keyboard ('',O000OOO0OOO0000O0 .lang (30702 ).encode ('utf-8'))#line:187
                OOO0OOOO00OO00O0O .doModal ()#line:188
                if not (OOO0OOOO00OO00O0O .isConfirmed ()):return #line:189
                url =OOO0OOOO00OO00O0O .getText ()#line:190
            if (url ==None or url ==''):return #line:192
            def OOOOO000OO0O0000O ():return [url ]#line:194
            O0O0O0O00000OOOO0 =O0OOOOO0OO0O0O00O .get (OOOOO000OO0O0000O ,600000000 ,table ='rel_srch')#line:195
            def OOOOO000OO0O0000O ():return [OOO00000O00OO0OO0 for OO0OOO0O00O0OO0O0 ,OOO00000O00OO0OO0 in enumerate ((O0O0O0O00000OOOO0 +[url ]))if OOO00000O00OO0OO0 not in (O0O0O0O00000OOOO0 +[url ])[:OO0OOO0O00O0OO0O0 ]]#line:196
            O0OOOOO0OO0O0O00O .get (OOOOO000OO0O0000O ,0 ,table ='rel_srch')#line:197
            OOOO0OO0OO0000OOO =O00O00O0OO00OOO00 .request (O00OOOO000O0000OO )#line:199
            OOOO0OO0OO0000OOO =OO0O000OOO00O0OOO .findall ('<link>(.+?)</link>',OOOO0OO0OO0000OOO )#line:200
            OOOO0OO0OO0000OOO =[OOOO0OOO00OO000O0 for OOOO0OOO00OO000O0 in OOOO0OO0OO0000OOO if str (OOOO0OOO00OO000O0 ).startswith ('http')]#line:201
            OO00O00000OO000O0 .list =[];O0OO00O0O0OO0OOOO =[]#line:203
            for O00OOOO000O0000OO in OOOO0OO0OO0000OOO :O0OO00O0O0OO0OOOO .append (O0O0OOO000O000O0O .Thread (OO00O00000OO000O0 .specialist_list ,O00OOOO000O0000OO ))#line:204
            [OO0OO000O0O000O0O .start ()for OO0OO000O0O000O0O in O0OO00O0O0OO0OOOO ];[OO0O0OOOOO00OO0OO .join ()for OO0O0OOOOO00OO0OO in O0OO00O0O0OO0OOOO ]#line:205
            OO00O00000OO000O0 .list =[OOO0000O0OOO0OO00 for OOO0000O0OOO0OO00 in OO00O00000OO000O0 .list if url .lower ()in OOO0000O0OOO0OO00 ['name'].lower ()]#line:207
            for OOOOOOOOOOO0OOO0O in OO00O00000OO000O0 .list :#line:209
                try :#line:210
                    OO00O000000OOOOOO =''#line:211
                    if not OOOOOOOOOOO0OOO0O ['vip']in ['specialist TV']:OO00O000000OOOOOO +='[B]%s[/B] | '%OOOOOOOOOOO0OOO0O ['vip'].upper ()#line:212
                    OO00O000000OOOOOO +=OOOOOOOOOOO0OOO0O ['name']#line:213
                    OOOOOOOOOOO0OOO0O .update ({'name':OO00O000000OOOOOO })#line:214
                except :#line:215
                    pass #line:216
            for OOOOOOOOOOO0OOO0O in OO00O00000OO000O0 .list :OOOOOOOOOOO0OOO0O .update ({'content':'videos'})#line:218
            OO00O00000OO000O0 .addDirectory (OO00O00000OO000O0 .list )#line:219
        except :#line:220
            pass #line:221
    def specialist_list (OOOO00O0O000O00O0 ,OOO000OO00O00O00O ,result =None ):#line:224
        try :#line:225
            if result ==None :result =O0OOOOO0OO0O0O00O .get (O00O00O0OO00OOO00 .request ,0 ,OOO000OO00O00O00O )#line:226
            if result .strip ().startswith ('#EXTM3U')and '#EXTINF'in result :#line:228
                result =OO0O000OOO00O0OOO .compile ('#EXTINF:.+?\,(.+?)\n(.+?)\n',OO0O000OOO00O0OOO .MULTILINE |OO0O000OOO00O0OOO .DOTALL ).findall (result )#line:229
                result =['<item><title>%s</title><link>%s</link></item>'%(OOO0OOO00O0OOO0O0 [0 ],OOO0OOO00O0OOO0O0 [1 ])for OOO0OOO00O0OOO0O0 in result ]#line:230
                result =''.join (result )#line:231
            try :OO0O0OO000000O000 =OOOO0O0O0OO0O0000 .b64decode (result )#line:233
            except :OO0O0OO000000O000 =''#line:234
            if '</link>'in OO0O0OO000000O000 :result =OO0O0OO000000O000 #line:235
            result =str (result )#line:237
            result =OOOO00O0O000O00O0 .account_filter (result )#line:239
            O0O0O0OO0O0O0OOOO =result .split ('<item>')[0 ].split ('<dir>')[0 ]#line:241
            try :OOOO000O0OOOO0O0O =OO0O000OOO00O0OOO .findall ('<poster>(.+?)</poster>',O0O0O0OO0O0O0OOOO )[0 ]#line:243
            except :OOOO000O0OOOO0O0O ='0'#line:244
            try :OOO0OO00OOO00OO0O =OO0O000OOO00O0OOO .findall ('<thumbnail>(.+?)</thumbnail>',O0O0O0OO0O0O0OOOO )[0 ]#line:246
            except :OOO0OO00OOO00OO0O ='0'#line:247
            try :O0O000OO0000OO0OO =OO0O000OOO00O0OOO .findall ('<fanart>(.+?)</fanart>',O0O0O0OO0O0O0OOOO )[0 ]#line:249
            except :O0O000OO0000OO0OO ='0'#line:250
            OOO00O0O0OO000OOO =OO0O000OOO00O0OOO .compile ('((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',OO0O000OOO00O0OOO .MULTILINE |OO0O000OOO00O0OOO .DOTALL ).findall (result )#line:252
        except :#line:253
            return #line:254
        for OO0O0O0000O000OOO in OOO00O0O0OO000OOO :#line:256
            try :#line:257
                O0O000O000OO000O0 =OO0O000OOO00O0OOO .compile ('(<regex>.+?</regex>)',OO0O000OOO00O0OOO .MULTILINE |OO0O000OOO00O0OOO .DOTALL ).findall (OO0O0O0000O000OOO )#line:258
                O0O000O000OO000O0 =''.join (O0O000O000OO000O0 )#line:259
                OO0O0O0OO00OO0OO0 =OO0O000OOO00O0OOO .compile ('(<listrepeat>.+?</listrepeat>)',OO0O000OOO00O0OOO .MULTILINE |OO0O000OOO00O0OOO .DOTALL ).findall (O0O000O000OO000O0 )#line:260
                O0O000O000OO000O0 =OOOOOO000O000OOOO .quote_plus (O0O000O000OO000O0 )#line:261
                O0O00O00000OO0OOO =O0OOOO00O0OO0O000 .md5 ()#line:263
                for O00OOOO0O0OOOOO0O in O0O000O000OO000O0 :O0O00O00000OO0OOO .update (str (O00OOOO0O0OOOOO0O ))#line:264
                O0O00O00000OO0OOO =str (O0O00O00000OO0OOO .hexdigest ())#line:265
                OO0O0O0000O000OOO =OO0O0O0000O000OOO .replace ('\r','').replace ('\n','').replace ('\t','').replace ('&nbsp;','')#line:267
                OO0O0O0000O000OOO =OO0O000OOO00O0OOO .sub ('<regex>.+?</regex>','',OO0O0O0000O000OOO )#line:268
                OO0O0O0000O000OOO =OO0O000OOO00O0OOO .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OO0O0O0000O000OOO )#line:269
                OO0O0O0000O000OOO =OO0O000OOO00O0OOO .sub ('<link></link>','',OO0O0O0000O000OOO )#line:270
                O0OO0O00OO000OOO0 =OO0O000OOO00O0OOO .sub ('<meta>.+?</meta>','',OO0O0O0000O000OOO )#line:272
                try :O0OO0O00OO000OOO0 =OO0O000OOO00O0OOO .findall ('<title>(.+?)</title>',O0OO0O00OO000OOO0 )[0 ]#line:273
                except :O0OO0O00OO000OOO0 =OO0O000OOO00O0OOO .findall ('<name>(.+?)</name>',O0OO0O00OO000OOO0 )[0 ]#line:274
                try :O0000OO0O0O000O0O =OO0O000OOO00O0OOO .findall ('<date>(.+?)</date>',OO0O0O0000O000OOO )[0 ]#line:276
                except :O0000OO0O0O000O0O =''#line:277
                if OO0O000OOO00O0OOO .search (r'\d+',O0000OO0O0O000O0O ):O0OO0O00OO000OOO0 +=' [COLOR red] Updated %s[/COLOR]'%O0000OO0O0O000O0O #line:278
                try :OOOO000OO0OOO00OO =OO0O000OOO00O0OOO .findall ('<thumbnail>(.+?)</thumbnail>',OO0O0O0000O000OOO )[0 ]#line:280
                except :OOOO000OO0OOO00OO =OOO0OO00OOO00OO0O #line:281
                try :O0O00OOO0O000OO0O =OO0O000OOO00O0OOO .findall ('<fanart>(.+?)</fanart>',OO0O0O0000O000OOO )[0 ]#line:283
                except :O0O00OOO0O000OO0O =O0O000OO0000OO0OO #line:284
                try :O0000000O00OO0000 =OO0O000OOO00O0OOO .findall ('<meta>(.+?)</meta>',OO0O0O0000O000OOO )[0 ]#line:286
                except :O0000000O00OO0000 ='0'#line:287
                try :OOO000OO00O00O00O =OO0O000OOO00O0OOO .findall ('<link>(.+?)</link>',OO0O0O0000O000OOO )[0 ]#line:289
                except :OOO000OO00O00O00O ='0'#line:290
                OOO000OO00O00O00O =OOO000OO00O00O00O .replace ('>search<','><preset>search</preset>%s<'%O0000000O00OO0000 )#line:291
                OOO000OO00O00O00O ='<preset>search</preset>%s'%O0000000O00OO0000 if OOO000OO00O00O00O =='search'else OOO000OO00O00O00O #line:292
                OOO000OO00O00O00O =OOO000OO00O00O00O .replace ('>searchsd<','><preset>searchsd</preset>%s<'%O0000000O00OO0000 )#line:293
                OOO000OO00O00O00O ='<preset>searchsd</preset>%s'%O0000000O00OO0000 if OOO000OO00O00O00O =='searchsd'else OOO000OO00O00O00O #line:294
                OOO000OO00O00O00O =OO0O000OOO00O0OOO .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OOO000OO00O00O00O )#line:295
                if OO0O0O0000O000OOO .startswith ('<item>'):OOOOOOOOO0OOO00O0 ='play'#line:297
                elif OO0O0O0000O000OOO .startswith ('<plugin>'):OOOOOOOOO0OOO00O0 ='plugin'#line:298
                elif OO0O0O0000O000OOO .startswith ('<info>')or OOO000OO00O00O00O =='0':OOOOOOOOO0OOO00O0 ='0'#line:299
                else :OOOOOOOOO0OOO00O0 ='directory'#line:300
                if OOOOOOOOO0OOO00O0 =='play'and OO0O0O0OO00OO0OO0 :OOOOOOOOO0OOO00O0 ='xdirectory'#line:301
                if not O0O000O000OO000O0 =='':#line:303
                    OOOO00O0O000O00O0 .hash .append ({'regex':O0O00O00000OO0OOO ,'response':O0O000O000OO000O0 })#line:304
                    OOO000OO00O00O00O +='|regex=%s'%O0O00O00000OO0OOO #line:305
                if OOOOOOOOO0OOO00O0 in ['directory','xdirectory','plugin']:#line:307
                    O00OO0000OO000OO0 =True #line:308
                else :#line:309
                    O00OO0000OO000OO0 =False #line:310
                try :O00O0OO00OO0OOOO0 =OO0O000OOO00O0OOO .findall ('<content>(.+?)</content>',O0000000O00OO0000 )[0 ]#line:312
                except :O00O0OO00OO0OOOO0 ='0'#line:313
                if O00O0OO00OO0OOOO0 =='0':#line:314
                    try :O00O0OO00OO0OOOO0 =OO0O000OOO00O0OOO .findall ('<content>(.+?)</content>',OO0O0O0000O000OOO )[0 ]#line:315
                    except :O00O0OO00OO0OOOO0 ='0'#line:316
                if not O00O0OO00OO0OOOO0 =='0':O00O0OO00OO0OOOO0 +='s'#line:317
                if 'tvshow'in O00O0OO00OO0OOOO0 and not OOO000OO00O00O00O .strip ().endswith ('.xml'):#line:319
                    OOO000OO00O00O00O ='<preset>tvindexer</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OOO000OO00O00O00O ,OOOO000OO0OOO00OO ,O0O00OOO0O000OO0O ,O0000000O00OO0000 )#line:320
                    OOOOOOOOO0OOO00O0 ='tvtuner'#line:321
                if 'tvtuner'in O00O0OO00OO0OOOO0 and not OOO000OO00O00O00O .strip ().endswith ('.xml'):#line:323
                    OOO000OO00O00O00O ='<preset>tvtuner</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(OOO000OO00O00O00O ,OOOO000OO0OOO00OO ,O0O00OOO0O000OO0O ,O0000000O00OO0000 )#line:324
                    OOOOOOOOO0OOO00O0 ='tvtuner'#line:325
                try :OOO0O0O00O0OOOO0O =OO0O000OOO00O0OOO .findall ('<imdb>(.+?)</imdb>',O0000000O00OO0000 )[0 ]#line:327
                except :OOO0O0O00O0OOOO0O ='0'#line:328
                try :OOOOOOOOOOO00O0OO =OO0O000OOO00O0OOO .findall ('<tvdb>(.+?)</tvdb>',O0000000O00OO0000 )[0 ]#line:330
                except :OOOOOOOOOOO00O0OO ='0'#line:331
                try :OO000O0O0OO0O000O =OO0O000OOO00O0OOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O0000000O00OO0000 )[0 ]#line:333
                except :OO000O0O0OO0O000O ='0'#line:334
                try :O00OO0OO00O00OOO0 =OO0O000OOO00O0OOO .findall ('<title>(.+?)</title>',O0000000O00OO0000 )[0 ]#line:336
                except :O00OO0OO00O00OOO0 ='0'#line:337
                if O00OO0OO00O00OOO0 =='0'and not OO000O0O0OO0O000O =='0':O00OO0OO00O00OOO0 =OO000O0O0OO0O000O #line:339
                try :OOO0OO0000O00O00O =OO0O000OOO00O0OOO .findall ('<year>(.+?)</year>',O0000000O00OO0000 )[0 ]#line:341
                except :OOO0OO0000O00O00O ='0'#line:342
                try :O0O0OO000OO0OOO00 =OO0O000OOO00O0OOO .findall ('<premiered>(.+?)</premiered>',O0000000O00OO0000 )[0 ]#line:344
                except :O0O0OO000OO0OOO00 ='0'#line:345
                try :O0O000OO00000O000 =OO0O000OOO00O0OOO .findall ('<season>(.+?)</season>',O0000000O00OO0000 )[0 ]#line:347
                except :O0O000OO00000O000 ='0'#line:348
                try :OOOO0OO00OOO0O000 =OO0O000OOO00O0OOO .findall ('<episode>(.+?)</episode>',O0000000O00OO0000 )[0 ]#line:350
                except :OOOO0OO00OOO0O000 ='0'#line:351
                OOOO00O0O000O00O0 .list .append ({'name':O0OO0O00OO000OOO0 ,'vip':OOOO000O0OOOO0O0O ,'url':OOO000OO00O00O00O ,'action':OOOOOOOOO0OOO00O0 ,'folder':O00OO0000OO000OO0 ,'poster':OOOO000OO0OOO00OO ,'banner':'0','fanart':O0O00OOO0O000OO0O ,'content':O00O0OO00OO0OOOO0 ,'imdb':OOO0O0O00O0OOOO0O ,'tvdb':OOOOOOOOOOO00O0OO ,'tmdb':'0','title':O00OO0OO00O00OOO0 ,'originaltitle':O00OO0OO00O00OOO0 ,'tvshowtitle':OO000O0O0OO0O000O ,'year':OOO0OO0000O00O00O ,'premiered':O0O0OO000OO0OOO00 ,'season':O0O000OO00000O000 ,'episode':OOOO0OO00OOO0O000 })#line:353
            except :#line:354
                pass #line:355
        OO00O0OO0OO000000 .insert (OOOO00O0O000O00O0 .hash )#line:357
        return OOOO00O0O000O00O0 .list #line:359
    def account_filter (O0O0OOOOO00O0OO0O ,OOO0OOO0OOO00OOOO ):#line:362
        if (O000OOO0OOO0000O0 .setting ('ustvnow_email')==''or O000OOO0OOO0000O0 .setting ('ustvnow_pass')==''):#line:363
            OOO0OOO0OOO00OOOO =OO0O000OOO00O0OOO .sub ('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<','<',OOO0OOO0OOO00OOOO )#line:364
        if (O000OOO0OOO0000O0 .setting ('streamlive_user')==''or O000OOO0OOO0000O0 .setting ('streamlive_pass')==''):#line:366
            OOO0OOO0OOO00OOOO =OO0O000OOO00O0OOO .sub ('http(?:s|)://(?:www\.|)streamlive\.to/.+?<','<',OOO0OOO0OOO00OOOO )#line:367
        return OOO0OOO0OOO00OOOO #line:369
    def worker (O00O0OO0O0OOO0000 ):#line:372
        if not O000OOO0OOO0000O0 .setting ('metadata')=='true':return #line:373
        O00O0OO0O0OOO0000 .imdb_info_link ='http://www.omdbapi.com/?i=%s&plot=full&r=json'#line:375
        O00O0OO0O0OOO0000 .tvmaze_info_link ='http://api.tvmaze.com/lookup/shows?thetvdb=%s'#line:376
        O00O0OO0O0OOO0000 .lang ='en'#line:377
        O00O0OO0O0OOO0000 .meta =[]#line:379
        O0OO000OO0OOOO000 =len (O00O0OO0O0OOO0000 .list )#line:380
        if O0OO000OO0OOOO000 ==0 :return #line:381
        for OO0OOOOO0O000O0O0 in range (0 ,O0OO000OO0OOOO000 ):O00O0OO0O0OOO0000 .list [OO0OOOOO0O000O0O0 ].update ({'metacache':False })#line:383
        O00O0OO0O0OOO0000 .list =OOO0OO0OO0O0000O0 .fetch (O00O0OO0O0OOO0000 .list ,O00O0OO0O0OOO0000 .lang )#line:384
        OOO0O00OO0O000OO0 =[OOOO0O0O0OOO0O000 ['imdb']for OOOO0O0O0OOO0O000 in O00O0OO0O0OOO0000 .list ]#line:386
        OOO0O00OO0O000OO0 =[OO000O0O000O00OO0 for OO0000O0OO0000000 ,OO000O0O000O00OO0 in enumerate (OOO0O00OO0O000OO0 )if OO000O0O000O00OO0 not in OOO0O00OO0O000OO0 [:OO0000O0OO0000000 ]]#line:387
        if len (OOO0O00OO0O000OO0 )==1 :#line:388
                O00O0OO0O0OOO0000 .movie_info (0 );O00O0OO0O0OOO0000 .tv_info (0 )#line:389
                if O00O0OO0O0OOO0000 .meta :OOO0OO0OO0O0000O0 .insert (O00O0OO0O0OOO0000 .meta )#line:390
        for OO0OOOOO0O000O0O0 in range (0 ,O0OO000OO0OOOO000 ):O00O0OO0O0OOO0000 .list [OO0OOOOO0O000O0O0 ].update ({'metacache':False })#line:392
        O00O0OO0O0OOO0000 .list =OOO0OO0OO0O0000O0 .fetch (O00O0OO0O0OOO0000 .list ,O00O0OO0O0OOO0000 .lang )#line:393
        for O0OOOO000OOOO000O in range (0 ,O0OO000OO0OOOO000 ,50 ):#line:395
            O000O0O0OOOO0O0O0 =[]#line:396
            for OO0OOOOO0O000O0O0 in range (O0OOOO000OOOO000O ,O0OOOO000OOOO000O +50 ):#line:397
                if OO0OOOOO0O000O0O0 <=O0OO000OO0OOOO000 :O000O0O0OOOO0O0O0 .append (O0O0OOO000O000O0O .Thread (O00O0OO0O0OOO0000 .movie_info ,OO0OOOOO0O000O0O0 ))#line:398
                if OO0OOOOO0O000O0O0 <=O0OO000OO0OOOO000 :O000O0O0OOOO0O0O0 .append (O0O0OOO000O000O0O .Thread (O00O0OO0O0OOO0000 .tv_info ,OO0OOOOO0O000O0O0 ))#line:399
            [O0OO0OO0O00OO000O .start ()for O0OO0OO0O00OO000O in O000O0O0OOOO0O0O0 ]#line:400
            [OO00O0OO0OOO0OO00 .join ()for OO00O0OO0OOO0OO00 in O000O0O0OOOO0O0O0 ]#line:401
        if O00O0OO0O0OOO0000 .meta :OOO0OO0OO0O0000O0 .insert (O00O0OO0O0OOO0000 .meta )#line:403
    def movie_info (OO0O0OOOO0OOOO00O ,O00OO0O00O0OOOO0O ):#line:406
        try :#line:407
            if OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ]['metacache']==True :raise Exception ()#line:408
            if not OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ]['content']=='movies':raise Exception ()#line:410
            OO00O000O0OOO0O00 =OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ]['imdb']#line:412
            if OO00O000O0OOO0O00 =='0':raise Exception ()#line:413
            O000O000OO0OOO0O0 =OO0O0OOOO0OOOO00O .imdb_info_link %OO00O000O0OOO0O00 #line:415
            O0O00OO00O00OOOO0 =O00O00O0OO00OOO00 .request (O000O000OO0OOO0O0 ,timeout ='10')#line:417
            O0O00OO00O00OOOO0 =OO00000O0OOOOOOOO .loads (O0O00OO00O00OOOO0 )#line:418
            if 'Error'in O0O00OO00O00OOOO0 and 'incorrect imdb'in O0O00OO00O00OOOO0 ['Error'].lower ():#line:420
                return OO0O0OOOO0OOOO00O .meta .append ({'imdb':OO00O000O0OOO0O00 ,'tmdb':'0','tvdb':'0','lang':OO0O0OOOO0OOOO00O .lang ,'item':{'code':'0'}})#line:421
            O0OO0O00OOOOOOOOO =O0O00OO00O00OOOO0 ['Title']#line:423
            O0OO0O00OOOOOOOOO =O0OO0O00OOOOOOOOO .encode ('utf-8')#line:424
            if not O0OO0O00OOOOOOOOO =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'title':O0OO0O00OOOOOOOOO })#line:425
            OOO0O00O0OOOO000O =O0O00OO00O00OOOO0 ['Year']#line:427
            OOO0O00O0OOOO000O =OOO0O00O0OOOO000O .encode ('utf-8')#line:428
            if not OOO0O00O0OOOO000O =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'year':OOO0O00O0OOOO000O })#line:429
            OO00O000O0OOO0O00 =O0O00OO00O00OOOO0 ['imdbID']#line:431
            if OO00O000O0OOO0O00 ==None or OO00O000O0OOO0O00 ==''or OO00O000O0OOO0O00 =='N/A':OO00O000O0OOO0O00 ='0'#line:432
            OO00O000O0OOO0O00 =OO00O000O0OOO0O00 .encode ('utf-8')#line:433
            if not OO00O000O0OOO0O00 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'imdb':OO00O000O0OOO0O00 ,'code':OO00O000O0OOO0O00 })#line:434
            OO0OO00OO000O0OO0 =O0O00OO00O00OOOO0 ['Released']#line:436
            if OO0OO00OO000O0OO0 ==None or OO0OO00OO000O0OO0 ==''or OO0OO00OO000O0OO0 =='N/A':OO0OO00OO000O0OO0 ='0'#line:437
            OO0OO00OO000O0OO0 =OO0O000OOO00O0OOO .findall ('(\d*) (.+?) (\d*)',OO0OO00OO000O0OO0 )#line:438
            try :OO0OO00OO000O0OO0 ='%s-%s-%s'%(OO0OO00OO000O0OO0 [0 ][2 ],{'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}[OO0OO00OO000O0OO0 [0 ][1 ]],OO0OO00OO000O0OO0 [0 ][0 ])#line:439
            except :OO0OO00OO000O0OO0 ='0'#line:440
            OO0OO00OO000O0OO0 =OO0OO00OO000O0OO0 .encode ('utf-8')#line:441
            if not OO0OO00OO000O0OO0 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'premiered':OO0OO00OO000O0OO0 })#line:442
            OOOO00O000000OO00 =O0O00OO00O00OOOO0 ['Genre']#line:444
            if OOOO00O000000OO00 ==None or OOOO00O000000OO00 ==''or OOOO00O000000OO00 =='N/A':OOOO00O000000OO00 ='0'#line:445
            OOOO00O000000OO00 =OOOO00O000000OO00 .replace (', ',' / ')#line:446
            OOOO00O000000OO00 =OOOO00O000000OO00 .encode ('utf-8')#line:447
            if not OOOO00O000000OO00 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'genre':OOOO00O000000OO00 })#line:448
            OOOO0OOO0O000OOO0 =O0O00OO00O00OOOO0 ['Runtime']#line:450
            if OOOO0OOO0O000OOO0 ==None or OOOO0OOO0O000OOO0 ==''or OOOO0OOO0O000OOO0 =='N/A':OOOO0OOO0O000OOO0 ='0'#line:451
            OOOO0OOO0O000OOO0 =OO0O000OOO00O0OOO .sub ('[^0-9]','',str (OOOO0OOO0O000OOO0 ))#line:452
            try :OOOO0OOO0O000OOO0 =str (int (OOOO0OOO0O000OOO0 )*60 )#line:453
            except :pass #line:454
            OOOO0OOO0O000OOO0 =OOOO0OOO0O000OOO0 .encode ('utf-8')#line:455
            if not OOOO0OOO0O000OOO0 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'duration':OOOO0OOO0O000OOO0 })#line:456
            OOOOOOO0O0000000O =O0O00OO00O00OOOO0 ['imdbRating']#line:458
            if OOOOOOO0O0000000O ==None or OOOOOOO0O0000000O ==''or OOOOOOO0O0000000O =='N/A'or OOOOOOO0O0000000O =='0.0':OOOOOOO0O0000000O ='0'#line:459
            OOOOOOO0O0000000O =OOOOOOO0O0000000O .encode ('utf-8')#line:460
            if not OOOOOOO0O0000000O =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'rating':OOOOOOO0O0000000O })#line:461
            OO0O0O00O0OO0OOOO =O0O00OO00O00OOOO0 ['imdbVotes']#line:463
            try :OO0O0O00O0OO0OOOO =str (format (int (OO0O0O00O0OO0OOOO ),',d'))#line:464
            except :pass #line:465
            if OO0O0O00O0OO0OOOO ==None or OO0O0O00O0OO0OOOO ==''or OO0O0O00O0OO0OOOO =='N/A':OO0O0O00O0OO0OOOO ='0'#line:466
            OO0O0O00O0OO0OOOO =OO0O0O00O0OO0OOOO .encode ('utf-8')#line:467
            if not OO0O0O00O0OO0OOOO =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'votes':OO0O0O00O0OO0OOOO })#line:468
            OO0OOOOO00OOOO0OO =O0O00OO00O00OOOO0 ['Rated']#line:470
            if OO0OOOOO00OOOO0OO ==None or OO0OOOOO00OOOO0OO ==''or OO0OOOOO00OOOO0OO =='N/A':OO0OOOOO00OOOO0OO ='0'#line:471
            OO0OOOOO00OOOO0OO =OO0OOOOO00OOOO0OO .encode ('utf-8')#line:472
            if not OO0OOOOO00OOOO0OO =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'mpaa':OO0OOOOO00OOOO0OO })#line:473
            OO0OOOOO0O0OO0000 =O0O00OO00O00OOOO0 ['Director']#line:475
            if OO0OOOOO0O0OO0000 ==None or OO0OOOOO0O0OO0000 ==''or OO0OOOOO0O0OO0000 =='N/A':OO0OOOOO0O0OO0000 ='0'#line:476
            OO0OOOOO0O0OO0000 =OO0OOOOO0O0OO0000 .replace (', ',' / ')#line:477
            OO0OOOOO0O0OO0000 =OO0O000OOO00O0OOO .sub (r'\(.*?\)','',OO0OOOOO0O0OO0000 )#line:478
            OO0OOOOO0O0OO0000 =' '.join (OO0OOOOO0O0OO0000 .split ())#line:479
            OO0OOOOO0O0OO0000 =OO0OOOOO0O0OO0000 .encode ('utf-8')#line:480
            if not OO0OOOOO0O0OO0000 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'director':OO0OOOOO0O0OO0000 })#line:481
            O0OOO000O0OOO000O =O0O00OO00O00OOOO0 ['Writer']#line:483
            if O0OOO000O0OOO000O ==None or O0OOO000O0OOO000O ==''or O0OOO000O0OOO000O =='N/A':O0OOO000O0OOO000O ='0'#line:484
            O0OOO000O0OOO000O =O0OOO000O0OOO000O .replace (', ',' / ')#line:485
            O0OOO000O0OOO000O =OO0O000OOO00O0OOO .sub (r'\(.*?\)','',O0OOO000O0OOO000O )#line:486
            O0OOO000O0OOO000O =' '.join (O0OOO000O0OOO000O .split ())#line:487
            O0OOO000O0OOO000O =O0OOO000O0OOO000O .encode ('utf-8')#line:488
            if not O0OOO000O0OOO000O =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'writer':O0OOO000O0OOO000O })#line:489
            O0O0000O0OOO00O00 =O0O00OO00O00OOOO0 ['Actors']#line:491
            if O0O0000O0OOO00O00 ==None or O0O0000O0OOO00O00 ==''or O0O0000O0OOO00O00 =='N/A':O0O0000O0OOO00O00 ='0'#line:492
            O0O0000O0OOO00O00 =[O00OO0OO00000O00O .strip ()for O00OO0OO00000O00O in O0O0000O0OOO00O00 .split (',')if not O00OO0OO00000O00O =='']#line:493
            try :O0O0000O0OOO00O00 =[(O0OO0OOOO0OOOOO0O .encode ('utf-8'),'')for O0OO0OOOO0OOOOO0O in O0O0000O0OOO00O00 ]#line:494
            except :O0O0000O0OOO00O00 =[]#line:495
            if O0O0000O0OOO00O00 ==[]:O0O0000O0OOO00O00 ='0'#line:496
            if not O0O0000O0OOO00O00 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'cast':O0O0000O0OOO00O00 })#line:497
            O00O000000O00O000 =O0O00OO00O00OOOO0 ['Plot']#line:499
            if O00O000000O00O000 ==None or O00O000000O00O000 ==''or O00O000000O00O000 =='N/A':O00O000000O00O000 ='0'#line:500
            O00O000000O00O000 =O00O00O0OO00OOO00 .replaceHTMLCodes (O00O000000O00O000 )#line:501
            O00O000000O00O000 =O00O000000O00O000 .encode ('utf-8')#line:502
            if not O00O000000O00O000 =='0':OO0O0OOOO0OOOO00O .list [O00OO0O00O0OOOO0O ].update ({'plot':O00O000000O00O000 })#line:503
            OO0O0OOOO0OOOO00O .meta .append ({'imdb':OO00O000O0OOO0O00 ,'tmdb':'0','tvdb':'0','lang':OO0O0OOOO0OOOO00O .lang ,'item':{'title':O0OO0O00OOOOOOOOO ,'year':OOO0O00O0OOOO000O ,'code':OO00O000O0OOO0O00 ,'imdb':OO00O000O0OOO0O00 ,'premiered':OO0OO00OO000O0OO0 ,'genre':OOOO00O000000OO00 ,'duration':OOOO0OOO0O000OOO0 ,'rating':OOOOOOO0O0000000O ,'votes':OO0O0O00O0OO0OOOO ,'mpaa':OO0OOOOO00OOOO0OO ,'director':OO0OOOOO0O0OO0000 ,'writer':O0OOO000O0OOO000O ,'cast':O0O0000O0OOO00O00 ,'plot':O00O000000O00O000 }})#line:505
        except :#line:506
            pass #line:507
    def tv_info (OOO00OO0OO00OOO00 ,OOO00OOO00OO00000 ):#line:510
        try :#line:511
            if OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ]['metacache']==True :raise Exception ()#line:512
            if not OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ]['content']in ['tvshows','seasons','episodes']:raise Exception ()#line:514
            O0O00000O0OO0O000 =OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ]['tvdb']#line:516
            if O0O00000O0OO0O000 =='0':raise Exception ()#line:517
            OOOO0O0OO000O0000 =OOO00OO0OO00OOO00 .tvmaze_info_link %O0O00000O0OO0O000 #line:519
            O0OOOOO000O0OOO00 =O00O00O0OO00OOO00 .request (OOOO0O0OO000O0000 ,output ='extended',error =True ,timeout ='10')#line:521
            if O0OOOOO000O0OOO00 [1 ]=='404':#line:523
                return OOO00OO0OO00OOO00 .meta .append ({'imdb':'0','tmdb':'0','tvdb':O0O00000O0OO0O000 ,'lang':OOO00OO0OO00OOO00 .lang ,'item':{'code':'0'}})#line:524
            O0OOOOO000O0OOO00 =OO00000O0OOOOOOOO .loads (O0OOOOO000O0OOO00 [0 ])#line:526
            O0O00000OOO000O0O =O0OOOOO000O0OOO00 ['name']#line:528
            O0O00000OOO000O0O =O0O00000OOO000O0O .encode ('utf-8')#line:529
            if not O0O00000OOO000O0O =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'tvshowtitle':O0O00000OOO000O0O })#line:530
            OOOO0O0OOOOOO00O0 =O0OOOOO000O0OOO00 ['premiered']#line:532
            OOOO0O0OOOOOO00O0 =OO0O000OOO00O0OOO .findall ('(\d{4})',OOOO0O0OOOOOO00O0 )[0 ]#line:533
            OOOO0O0OOOOOO00O0 =OOOO0O0OOOOOO00O0 .encode ('utf-8')#line:534
            if not OOOO0O0OOOOOO00O0 =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'year':OOOO0O0OOOOOO00O0 })#line:535
            try :O00O0OO0OO00O000O =O0OOOOO000O0OOO00 ['externals']['imdb']#line:537
            except :O00O0OO0OO00O000O ='0'#line:538
            if O00O0OO0OO00O000O ==''or O00O0OO0OO00O000O ==None :O00O0OO0OO00O000O ='0'#line:539
            O00O0OO0OO00O000O =O00O0OO0OO00O000O .encode ('utf-8')#line:540
            if OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ]['imdb']=='0'and not O00O0OO0OO00O000O =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'imdb':O00O0OO0OO00O000O })#line:541
            try :O00OO0O0OO0OO0O00 =O0OOOOO000O0OOO00 ['network']['name']#line:543
            except :O00OO0O0OO0OO0O00 ='0'#line:544
            if O00OO0O0OO0OO0O00 ==''or O00OO0O0OO0OO0O00 ==None :O00OO0O0OO0OO0O00 ='0'#line:545
            O00OO0O0OO0OO0O00 =O00OO0O0OO0OO0O00 .encode ('utf-8')#line:546
            if not O00OO0O0OO0OO0O00 =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'studio':O00OO0O0OO0OO0O00 })#line:547
            O0OO0000O0OOOOOOO =O0OOOOO000O0OOO00 ['genres']#line:549
            if O0OO0000O0OOOOOOO ==''or O0OO0000O0OOOOOOO ==None or O0OO0000O0OOOOOOO ==[]:O0OO0000O0OOOOOOO ='0'#line:550
            O0OO0000O0OOOOOOO =' / '.join (O0OO0000O0OOOOOOO )#line:551
            O0OO0000O0OOOOOOO =O0OO0000O0OOOOOOO .encode ('utf-8')#line:552
            if not O0OO0000O0OOOOOOO =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'genre':O0OO0000O0OOOOOOO })#line:553
            try :O00OO0O0OOO0O0OO0 =str (O0OOOOO000O0OOO00 ['runtime'])#line:555
            except :O00OO0O0OOO0O0OO0 ='0'#line:556
            if O00OO0O0OOO0O0OO0 ==''or O00OO0O0OOO0O0OO0 ==None :O00OO0O0OOO0O0OO0 ='0'#line:557
            try :O00OO0O0OOO0O0OO0 =str (int (O00OO0O0OOO0O0OO0 )*60 )#line:558
            except :pass #line:559
            O00OO0O0OOO0O0OO0 =O00OO0O0OOO0O0OO0 .encode ('utf-8')#line:560
            if not O00OO0O0OOO0O0OO0 =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'duration':O00OO0O0OOO0O0OO0 })#line:561
            OOO00OO000O0O0OOO =str (O0OOOOO000O0OOO00 ['rating']['average'])#line:563
            if OOO00OO000O0O0OOO ==''or OOO00OO000O0O0OOO ==None :OOO00OO000O0O0OOO ='0'#line:564
            OOO00OO000O0O0OOO =OOO00OO000O0O0OOO .encode ('utf-8')#line:565
            if not OOO00OO000O0O0OOO =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'rating':OOO00OO000O0O0OOO })#line:566
            OO0OO0OO00OOOOO0O =O0OOOOO000O0OOO00 ['summary']#line:568
            if OO0OO0OO00OOOOO0O ==''or OO0OO0OO00OOOOO0O ==None :OO0OO0OO00OOOOO0O ='0'#line:569
            OO0OO0OO00OOOOO0O =OO0O000OOO00O0OOO .sub ('\n|<.+?>|</.+?>|.+?#\d*:','',OO0OO0OO00OOOOO0O )#line:570
            OO0OO0OO00OOOOO0O =OO0OO0OO00OOOOO0O .encode ('utf-8')#line:571
            if not OO0OO0OO00OOOOO0O =='0':OOO00OO0OO00OOO00 .list [OOO00OOO00OO00000 ].update ({'plot':OO0OO0OO00OOOOO0O })#line:572
            OOO00OO0OO00OOO00 .meta .append ({'imdb':O00O0OO0OO00O000O ,'tmdb':'0','tvdb':O0O00000O0OO0O000 ,'lang':OOO00OO0OO00OOO00 .lang ,'item':{'tvshowtitle':O0O00000OOO000O0O ,'year':OOOO0O0OOOOOO00O0 ,'code':O00O0OO0OO00O000O ,'imdb':O00O0OO0OO00O000O ,'tvdb':O0O00000O0OO0O000 ,'studio':O00OO0O0OO0OO0O00 ,'genre':O0OO0000O0OOOOOOO ,'duration':O00OO0O0OOO0O0OO0 ,'rating':OOO00OO000O0O0OOO ,'plot':OO0OO0OO00OOOOO0O }})#line:574
        except :#line:575
            pass #line:576
    def addDirectory (OOO0000OO00OOOO00 ,O0OOOOOO0OOO0O000 ,queue =False ):#line:579
        if O0OOOOOO0OOO0O000 ==None or len (O0OOOOOO0OOO0O000 )==0 :return #line:580
        OOOOOOO00OOOOO00O =OO00000OO00000000 .argv [0 ]#line:582
        OOOOO000OOOO0OOOO =OO0OOO000O0O0OO00 =O000OOO0OOO0000O0 .addonInfo ('icon')#line:583
        O00O0OO0OOO0000OO =O000OOO0OOO0000O0 .addonInfo ('fanart')#line:584
        OOO00000OO0O0OO00 =O000OOO0OOO0000O0 .playlist #line:586
        if not queue ==False :OOO00000OO0O0OO00 .clear ()#line:587
        try :O0OOOOOOOOO0O000O =True if 'testings.xml'in O000OOO0OOO0000O0 .listDir (O000OOO0OOO0000O0 .dataPath )[1 ]else False #line:589
        except :O0OOOOOOOOO0O000O =False #line:590
        O000O0000OOO0O000 =[O000O000O00000O00 ['content']for O000O000O00000O00 in O0OOOOOO0OOO0O000 if 'content'in O000O000O00000O00 ]#line:592
        if 'movies'in O000O0000OOO0O000 :O000O0000OOO0O000 ='movies'#line:593
        elif 'tvshows'in O000O0000OOO0O000 :O000O0000OOO0O000 ='tvshows'#line:594
        elif 'seasons'in O000O0000OOO0O000 :O000O0000OOO0O000 ='seasons'#line:595
        elif 'episodes'in O000O0000OOO0O000 :O000O0000OOO0O000 ='episodes'#line:596
        elif 'addons'in O000O0000OOO0O000 :O000O0000OOO0O000 ='addons'#line:597
        else :O000O0000OOO0O000 ='videos'#line:598
        for O0OOO0000OOO0O0OO in O0OOOOOO0OOO0O000 :#line:600
            try :#line:601
                try :O0O0OOOO00000O0O0 =O000OOO0OOO0000O0 .lang (int (O0OOO0000OOO0O0OO ['name'])).encode ('utf-8')#line:602
                except :O0O0OOOO00000O0O0 =O0OOO0000OOO0O0OO ['name']#line:603
                OO00O0O000OO0O0OO ='%s?action=%s'%(OOOOOOO00OOOOO00O ,O0OOO0000OOO0O0OO ['action'])#line:605
                try :OO00O0O000OO0O0OO +='&url=%s'%OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['url'])#line:606
                except :pass #line:607
                try :OO00O0O000OO0O0OO +='&content=%s'%OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['content'])#line:608
                except :pass #line:609
                if O0OOO0000OOO0O0OO ['action']=='plugin'and 'url'in O0OOO0000OOO0O0OO :OO00O0O000OO0O0OO =O0OOO0000OOO0O0OO ['url']#line:611
                try :OO0O0OOOO0O000000 =dict (OOO0OO0000OO0OOOO .parse_qsl (OOO0OO0000OO0OOOO .urlparse (OO00O0O000OO0O0OO ).query ))['action']#line:613
                except :OO0O0OOOO0O000000 =None #line:614
                if OO0O0OOOO0O000000 =='developer'and not O0OOOOOOOOO0O000O ==True :raise Exception ()#line:615
                O0OO00O0000OO0O0O =O0OOO0000OOO0O0OO ['poster']if 'poster'in O0OOO0000OOO0O0OO else '0'#line:617
                O0000OO0000000OOO =O0OOO0000OOO0O0OO ['banner']if 'banner'in O0OOO0000OOO0O0OO else '0'#line:618
                OO0OOOOOOO0O0OOO0 =O0OOO0000OOO0O0OO ['fanart']if 'fanart'in O0OOO0000OOO0O0OO else '0'#line:619
                if O0OO00O0000OO0O0O =='0':O0OO00O0000OO0O0O =OOOOO000OOOO0OOOO #line:620
                if O0000OO0000000OOO =='0'and O0OO00O0000OO0O0O =='0':O0000OO0000000OOO =OO0OOO000O0O0OO00 #line:621
                elif O0000OO0000000OOO =='0':O0000OO0000000OOO =O0OO00O0000OO0O0O #line:622
                OOOOOO0O00000OOOO =O0OOO0000OOO0O0OO ['content']if 'content'in O0OOO0000OOO0O0OO else '0'#line:624
                O0OOO000O0O0OO0O0 =O0OOO0000OOO0O0OO ['folder']if 'folder'in O0OOO0000OOO0O0OO else True #line:626
                OOO00000OO0000000 =dict ((OO0O00O00OO0OOO00 ,O0OOO0OO00O00OOO0 )for OO0O00O00OO0OOO00 ,O0OOO0OO00O00OOO0 in O0OOO0000OOO0O0OO .iteritems ()if not O0OOO0OO00O00OOO0 =='0')#line:628
                O0O00000OOOOO00O0 =[]#line:630
                if OOOOOO0O00000OOOO in ['movies','tvshows']:#line:632
                    OOO00000OO0000000 .update ({'trailer':'%s?action=trailer&name=%s'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (O0O0OOOO00000O0O0 ))})#line:633
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30707 ).encode ('utf-8'),'RunPlugin(%s?action=trailer&name=%s)'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (O0O0OOOO00000O0O0 ))))#line:634
                if OOOOOO0O00000OOOO in ['movies','tvshows','seasons','episodes']:#line:636
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30708 ).encode ('utf-8'),'XBMC.Action(Info)'))#line:637
                if (O0OOO000O0O0OO0O0 ==False and not '|regex='in str (O0OOO0000OOO0O0OO .get ('url')))or (O0OOO000O0O0OO0O0 ==True and OOOOOO0O00000OOOO in ['tvshows','seasons']):#line:639
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30723 ).encode ('utf-8'),'RunPlugin(%s?action=queueItem)'%OOOOOOO00OOOOO00O ))#line:640
                if OOOOOO0O00000OOOO =='movies':#line:642
                    try :OOO0O0OOO0O0OOOOO ='%s (%s)'%(O0OOO0000OOO0O0OO ['title'],O0OOO0000OOO0O0OO ['year'])#line:643
                    except :OOO0O0OOO0O0OOOOO =O0O0OOOO00000O0O0 #line:644
                    try :O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (OOO0O0OOO0O0OOOOO ),OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['url']),OOOOOO000O000OOOO .quote_plus (O0OO00O0000OO0O0O ))))#line:645
                    except :pass #line:646
                elif OOOOOO0O00000OOOO =='episodes':#line:647
                    try :OOO0O0OOO0O0OOOOO ='%s S%02dE%02d'%(O0OOO0000OOO0O0OO ['tvshowtitle'],int (O0OOO0000OOO0O0OO ['season']),int (O0OOO0000OOO0O0OO ['episode']))#line:648
                    except :OOO0O0OOO0O0OOOOO =O0O0OOOO00000O0O0 #line:649
                    try :O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (OOO0O0OOO0O0OOOOO ),OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['url']),OOOOOO000O000OOOO .quote_plus (O0OO00O0000OO0O0O ))))#line:650
                    except :pass #line:651
                elif OOOOOO0O00000OOOO =='songs':#line:652
                    try :O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (O0O0OOOO00000O0O0 ),OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['url']),OOOOOO000O000OOOO .quote_plus (O0OO00O0000OO0O0O ))))#line:653
                    except :pass #line:654
                if O000O0000OOO0O000 =='movies':#line:656
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30711 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=movies)'%OOOOOOO00OOOOO00O ))#line:657
                elif O000O0000OOO0O000 =='tvshows':#line:658
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30712 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=tvshows)'%OOOOOOO00OOOOO00O ))#line:659
                elif O000O0000OOO0O000 =='seasons':#line:660
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30713 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=seasons)'%OOOOOOO00OOOOO00O ))#line:661
                elif O000O0000OOO0O000 =='episodes':#line:662
                    O0O00000OOOOO00O0 .append ((O000OOO0OOO0000O0 .lang (30714 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=episodes)'%OOOOOOO00OOOOO00O ))#line:663
                if O0OOOOOOOOO0O000O ==True :#line:665
                    try :O0O00000OOOOO00O0 .append (('Open in browser','RunPlugin(%s?action=browser&url=%s)'%(OOOOOOO00OOOOO00O ,OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['url']))))#line:666
                    except :pass #line:667
                O0OOO0000OOOOO000 =O000OOO0OOO0000O0 .item (label =O0O0OOOO00000O0O0 ,iconImage =O0OO00O0000OO0O0O ,thumbnailImage =O0OO00O0000OO0O0O )#line:670
                try :O0OOO0000OOOOO000 .setArt ({'poster':O0OO00O0000OO0O0O ,'tvshow.poster':O0OO00O0000OO0O0O ,'season.poster':O0OO00O0000OO0O0O ,'banner':O0000OO0000000OOO ,'tvshow.banner':O0000OO0000000OOO ,'season.banner':O0000OO0000000OOO })#line:672
                except :pass #line:673
                if not OO0OOOOOOO0O0OOO0 =='0':#line:675
                    O0OOO0000OOOOO000 .setProperty ('Fanart_Image',OO0OOOOOOO0O0OOO0 )#line:676
                elif not O00O0OO0OOO0000OO ==None :#line:677
                    O0OOO0000OOOOO000 .setProperty ('Fanart_Image',O00O0OO0OOO0000OO )#line:678
                if queue ==False :#line:680
                    O0OOO0000OOOOO000 .setInfo (type ='Video',infoLabels =OOO00000OO0000000 )#line:681
                    O0OOO0000OOOOO000 .addContextMenuItems (O0O00000OOOOO00O0 )#line:682
                    O000OOO0OOO0000O0 .addItem (handle =int (OO00000OO00000000 .argv [1 ]),url =OO00O0O000OO0O0OO ,listitem =O0OOO0000OOOOO000 ,isFolder =O0OOO000O0O0OO0O0 )#line:683
                else :#line:684
                    O0OOO0000OOOOO000 .setInfo (type ='Video',infoLabels =OOO00000OO0000000 )#line:685
                    OOO00000OO0O0OO00 .add (url =OO00O0O000OO0O0OO ,listitem =O0OOO0000OOOOO000 )#line:686
            except :#line:687
                pass #line:688
        if not queue ==False :#line:690
            return O000OOO0OOO0000O0 .player .play (OOO00000OO0O0OO00 )#line:691
        try :#line:693
            O0OOO0000OOO0O0OO =O0OOOOOO0OOO0O000 [0 ]#line:694
            if O0OOO0000OOO0O0OO ['next']=='':raise Exception ()#line:695
            OO00O0O000OO0O0OO ='%s?action=%s&url=%s'%(OOOOOOO00OOOOO00O ,O0OOO0000OOO0O0OO ['nextaction'],OOOOOO000O000OOOO .quote_plus (O0OOO0000OOO0O0OO ['next']))#line:696
            O0OOO0000OOOOO000 =O000OOO0OOO0000O0 .item (label =O000OOO0OOO0000O0 .lang (30500 ).encode ('utf-8'))#line:697
            O0OOO0000OOOOO000 .setArt ({'addonPoster':OOOOO000OOOO0OOOO ,'thumb':OOOOO000OOOO0OOOO ,'poster':OOOOO000OOOO0OOOO ,'tvshow.poster':OOOOO000OOOO0OOOO ,'season.poster':OOOOO000OOOO0OOOO ,'banner':OOOOO000OOOO0OOOO ,'tvshow.banner':OOOOO000OOOO0OOOO ,'season.banner':OOOOO000OOOO0OOOO })#line:698
            O0OOO0000OOOOO000 .setProperty ('addonFanart_Image',O00O0OO0OOO0000OO )#line:699
            O000OOO0OOO0000O0 .addItem (handle =int (OO00000OO00000000 .argv [1 ]),url =OO00O0O000OO0O0OO ,listitem =O0OOO0000OOOOO000 ,isFolder =True )#line:700
        except :#line:701
            pass #line:702
        if not O000O0000OOO0O000 ==None :O000OOO0OOO0000O0 .content (int (OO00000OO00000000 .argv [1 ]),O000O0000OOO0O000 )#line:704
        O000OOO0OOO0000O0 .directory (int (OO00000OO00000000 .argv [1 ]),cacheToDisc =True )#line:705
        if O000O0000OOO0O000 in ['movies','tvshows','seasons','episodes']:#line:706
            O0OO0OOOOO0OOOO0O .setView (O000O0000OOO0O000 ,{'skin.estuary':55 })#line:707
class resolver :#line:711
    def browser (OO00O00OOOO00OOO0 ,OOO0OOOO000000O00 ):#line:712
        try :#line:713
            OOO0OOOO000000O00 =OO00O00OOOO00OOO0 .get (OOO0OOOO000000O00 )#line:714
            if OOO0OOOO000000O00 ==False :return #line:715
            O000OOO0OOO0000O0 .execute ('RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)'%OOOOOO000O000OOOO .quote_plus (OOO0OOOO000000O00 ))#line:716
        except :#line:717
            pass #line:718
    def link (OO00O0O00O0O0O00O ,O0OO0OO00OOOOOO00 ):#line:721
        try :#line:722
            O0OO0OO00OOOOOO00 =OO00O0O00O0O0O00O .get (O0OO0OO00OOOOOO00 )#line:723
            if O0OO0OO00OOOOOO00 ==False :return #line:724
            O000OOO0OOO0000O0 .execute ('ActivateWindow(busydialog)')#line:726
            O0OO0OO00OOOOOO00 =OO00O0O00O0O0O00O .process (O0OO0OO00OOOOOO00 )#line:727
            O000OOO0OOO0000O0 .execute ('Dialog.Close(busydialog)')#line:728
            if O0OO0OO00OOOOOO00 ==None :return O000OOO0OOO0000O0 .infoDialog (O000OOO0OOO0000O0 .lang (30705 ).encode ('utf-8'))#line:730
            return O0OO0OO00OOOOOO00 #line:731
        except :#line:732
            pass #line:733
    def get (O000OO00OO0OO0OOO ,OOO00O0O0O000OO0O ):#line:736
        try :#line:737
            OOO0OO00O000OO000 =OO0O000OOO00O0OOO .compile ('<sublink(?:\s+name=|)(?:\'|\"|)(.*?)(?:\'|\"|)>(.+?)</sublink>').findall (OOO00O0O0O000OO0O )#line:738
            if len (OOO0OO00O000OO000 )==0 :return OOO00O0O0O000OO0O #line:740
            if len (OOO0OO00O000OO000 )==1 :return OOO0OO00O000OO000 [0 ][1 ]#line:741
            OOO0OO00O000OO000 =[('Link %s'%(int (OOO0OO00O000OO000 .index (OOOO000OO0OOOOOOO ))+1 )if OOOO000OO0OOOOOOO [0 ]==''else OOOO000OO0OOOOOOO [0 ],OOOO000OO0OOOOOOO [1 ])for OOOO000OO0OOOOOOO in OOO0OO00O000OO000 ]#line:743
            OOO0OOO0OO0000O00 =O000OOO0OOO0000O0 .selectDialog ([O0O0OO0OOO0000000 [0 ]for O0O0OO0OOO0000000 in OOO0OO00O000OO000 ],O000OOO0OOO0000O0 .infoLabel ('listitem.label'))#line:745
            if OOO0OOO0OO0000O00 ==-1 :return False #line:747
            else :return OOO0OO00O000OO000 [OOO0OOO0OO0000O00 ][1 ]#line:748
        except :#line:749
            pass #line:750
    def f4m (OO0O000O00O00OOO0 ,O0OO000000000OO00 ,O0O000OOO0OOOO0OO ):#line:753
            try :#line:754
                if not any (O00O00OO0O0O0O0OO in O0OO000000000OO00 for O00O00OO0O0O0O0OO in ['.f4m','.ts']):raise Exception ()#line:755
                OO0OO0O00O000OO0O =O0OO000000000OO00 .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:756
                if not OO0OO0O00O000OO0O in ['f4m','ts']:raise Exception ()#line:757
                O000O000OOOO0OO0O =OOO0OO0000OO0OOOO .parse_qs (O0OO000000000OO00 )#line:759
                try :OOO0OOOO0O00O00O0 =O000O000OOOO0OO0O ['proxy'][0 ]#line:761
                except :OOO0OOOO0O00O00O0 =None #line:762
                try :O00OOOOO00OO0OOOO =OO00000O0OOOOOOOO .loads (O000O000OOOO0OO0O ['proxy_for_chunks'][0 ])#line:764
                except :O00OOOOO00OO0OOOO =True #line:765
                try :O0O00OO0OO0O00000 =int (O000O000OOOO0OO0O ['maxbitrate'][0 ])#line:767
                except :O0O00OO0OO0O00000 =0 #line:768
                try :OOOOOO00O00O000O0 =OO00000O0OOOOOOOO .loads (O000O000OOOO0OO0O ['simpledownloader'][0 ])#line:770
                except :OOOOOO00O00O000O0 =False #line:771
                try :OOOOOOOO00O0O0OOO =O000O000OOOO0OO0O ['auth'][0 ]#line:773
                except :OOOOOOOO00O0O0OOO =''#line:774
                try :OOO0OOO000O0O0O0O =O000O000OOOO0OO0O ['streamtype'][0 ]#line:776
                except :OOO0OOO000O0O0O0O ='TSDOWNLOADER'if OO0OO0O00O000OO0O =='ts'else 'HDS'#line:777
                try :O0OOO0O00O0O0OOOO =O000O000OOOO0OO0O ['swf'][0 ]#line:779
                except :O0OOO0O00O0O0OOOO =None #line:780
                from F4mProxy import f4mProxyHelper as OOO0OOO00O0O000O0 #line:782
                return OOO0OOO00O0O000O0 ().playF4mLink (O0OO000000000OO00 ,O0O000OOO0OOOO0OO ,OOO0OOOO0O00O00O0 ,O00OOOOO00OO0OOOO ,O0O00OO0OO0O00000 ,OOOOOO00O00O000O0 ,OOOOOOOO00O0O0OOO ,OOO0OOO000O0O0O0O ,False ,O0OOO0O00O0O0OOOO )#line:783
            except :#line:784
                pass #line:785
    def process (OOO00OO0O000O00OO ,O000000O0OOOOOOO0 ,direct =True ):#line:788
        try :#line:789
            if not any (O0OO00OOO0OOO00O0 in O000000O0OOOOOOO0 for O0OO00OOO0OOO00O0 in ['.jpg','.png','.gif']):raise Exception ()#line:790
            OO0O00OOO00000O00 =O000000O0OOOOOOO0 .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:791
            if not OO0O00OOO00000O00 in ['jpg','png','gif']:raise Exception ()#line:792
            try :#line:793
                OOOOO0OOOO0O00000 =OOOOOOO00OOO0O0O0 .path .join (O000OOO0OOO0000O0 .dataPath ,'img')#line:794
                O000OOO0OOO0000O0 .deleteFile (OOOOO0OOOO0O00000 )#line:795
                OOOO0OOOOOOO0OO00 =O000OOO0OOO0000O0 .openFile (OOOOO0OOOO0O00000 ,'w')#line:796
                OOOO0OOOOOOO0OO00 .write (O00O00O0OO00OOO00 .request (O000000O0OOOOOOO0 ))#line:797
                OOOO0OOOOOOO0OO00 .close ()#line:798
                O000OOO0OOO0000O0 .execute ('ShowPicture("%s")'%OOOOO0OOOO0O00000 )#line:799
                return False #line:800
            except :#line:801
                return #line:802
        except :#line:803
            pass #line:804
        try :#line:806
            OOO0000OOOOO00O0O ,OOOO00000000O0OO0 =OO0O000OOO00O0OOO .findall ('(.+?)\|regex=(.+?)$',O000000O0OOOOOOO0 )[0 ]#line:807
            OOOO00000000O0OO0 =OO00O0OO0OO000000 .fetch (OOOO00000000O0OO0 )#line:808
            OOO0000OOOOO00O0O +=OOOOOO000O000OOOO .unquote_plus (OOOO00000000O0OO0 )#line:809
            if not '</regex>'in OOO0000OOOOO00O0O :raise Exception ()#line:810
            OO000O00O00O0O00O =OO00O0OO0OO000000 .resolve (OOO0000OOOOO00O0O )#line:811
            if not OO000O00O00O0O00O ==None :O000000O0OOOOOOO0 =OO000O00O00O0O00O #line:812
        except :#line:813
            pass #line:814
        try :#line:816
            if not O000000O0OOOOOOO0 .startswith ('rtmp'):raise Exception ()#line:817
            if len (OO0O000OOO00O0OOO .compile ('\s*timeout=(\d*)').findall (O000000O0OOOOOOO0 ))==0 :O000000O0OOOOOOO0 +=' timeout=10'#line:818
            return O000000O0OOOOOOO0 #line:819
        except :#line:820
            pass #line:821
        try :#line:823
            if not any (OOO000O00OOOOO000 in O000000O0OOOOOOO0 for OOO000O00OOOOO000 in ['.m3u8','.f4m','.ts']):raise Exception ()#line:824
            OO0O00OOO00000O00 =O000000O0OOOOOOO0 .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:825
            if not OO0O00OOO00000O00 in ['m3u8','f4m','ts']:raise Exception ()#line:826
            return O000000O0OOOOOOO0 #line:827
        except :#line:828
            pass #line:829
        try :#line:831
            OO00O000O0O0O0OOO =OO0O000OOO00O0OOO .findall ('<preset>(.+?)</preset>',O000000O0OOOOOOO0 )[0 ]#line:832
            if not 'search'in OO00O000O0O0O0OOO :raise Exception ()#line:834
            OO00O00O000O000O0 ,OO000O000O0O0000O ,O000O0000O0OOOOO0 =OO0O000OOO00O0OOO .findall ('<title>(.+?)</title>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<year>(.+?)</year>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<imdb>(.+?)</imdb>',O000000O0OOOOOOO0 )[0 ]#line:836
            try :OOO0OO0O0OO000O00 ,OO000O0O00O0O00OO ,O00O00O00OOO000O0 ,O0OO00000OO0OOOO0 ,O000O0OOOOO0O0O0O =OO0O000OOO00O0OOO .findall ('<tvdb>(.+?)</tvdb>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<premiered>(.+?)</premiered>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<season>(.+?)</season>',O000000O0OOOOOOO0 )[0 ],OO0O000OOO00O0OOO .findall ('<episode>(.+?)</episode>',O000000O0OOOOOOO0 )[0 ]#line:838
            except :OOO0OO0O0OO000O00 =OO000O0O00O0O00OO =O00O00O00OOO000O0 =O0OO00000OO0OOOO0 =O000O0OOOOO0O0O0O =None #line:839
            direct =False #line:841
            OO0OO0O0O00O00OOO ='HD'if not OO00O000O0O0O0OOO =='searchsd'else 'SD'#line:843
            from resources .lib .sources import sources as O0OOOOOOOOOOOOOO0 #line:845
            OO000O00O00O0O00O =O0OOOOOOOOOOOOOO0 ().getSources (OO00O00O000O000O0 ,OO000O000O0O0000O ,O000O0000O0OOOOO0 ,OOO0OO0O0OO000O00 ,O0OO00000OO0OOOO0 ,O000O0OOOOO0O0O0O ,OO000O0O00O0O00OO ,O00O00O00OOO000O0 ,OO0OO0O0O00O00OOO )#line:847
            if not OO000O00O00O0O00O ==None :return OO000O00O00O0O00O #line:849
        except :#line:850
            pass #line:851
        try :#line:853
            from resources .lib .sources import sources as O0OOOOOOOOOOOOOO0 #line:854
            OO000O00O00O0O00O =O0OOOOOOOOOOOOOO0 ().getURISource (O000000O0OOOOOOO0 )#line:856
            if not OO000O00O00O0O00O ==False :direct =False #line:858
            if OO000O00O00O0O00O ==None or OO000O00O00O0O00O ==False :raise Exception ()#line:859
            return OO000O00O00O0O00O #line:861
        except :#line:862
            pass #line:863
        try :#line:865
            if not '.google.com'in O000000O0OOOOOOO0 :raise Exception ()#line:866
            from resources .lib .modules import directstream as O0O000OOO0OO000OO #line:867
            OO000O00O00O0O00O =O0O000OOO0OO000OO .google (O000000O0OOOOOOO0 )[0 ]['url']#line:868
            return OO000O00O00O0O00O #line:869
        except :#line:870
            pass #line:871
        try :#line:873
            if not 'filmon.com/'in O000000O0OOOOOOO0 :raise Exception ()#line:874
            from resources .lib .modules import filmon as OOO0OO00OOOOO0OO0 #line:875
            OO000O00O00O0O00O =OOO0OO00OOOOO0OO0 .resolve (O000000O0OOOOOOO0 )#line:876
            return OO000O00O00O0O00O #line:877
        except :#line:878
            pass #line:879
        try :#line:881
            import urlresolver as O0000O0OOOO0000O0 #line:882
            OOOOOOOO00O0OO00O =O0000O0OOOO0000O0 .HostedMediaFile (url =O000000O0OOOOOOO0 )#line:884
            if OOOOOOOO00O0OO00O .valid_url ()==False :raise Exception ()#line:886
            direct =False ;OO000O00O00O0O00O =OOOOOOOO00O0OO00O .resolve ()#line:888
            if not OO000O00O00O0O00O ==False :return OO000O00O00O0O00O #line:890
        except :#line:891
            pass #line:892
        if direct ==True :return O000000O0OOOOOOO0 #line:894
class player (O0OOO00O000OO00OO .Player ):#line:897
    def __init__ (OOOOO0O0OO0O00OOO ):#line:898
        O0OOO00O000OO00OO .Player .__init__ (OOOOO0O0OO0O00OOO )#line:899
    def play (OOO0O000O00O00O00 ,OOOO0O00OO00OO00O ,content =None ):#line:902
        try :#line:903
            O0O00O0O000O0O0OO =OOOO0O00OO00OO00O #line:904
            OOOO0O00OO00OO00O =resolver ().get (OOOO0O00OO00OO00O )#line:906
            if OOOO0O00OO00OO00O ==False :return #line:907
            O000OOO0OOO0000O0 .execute ('ActivateWindow(busydialog)')#line:909
            OOOO0O00OO00OO00O =resolver ().process (OOOO0O00OO00OO00O )#line:910
            O000OOO0OOO0000O0 .execute ('Dialog.Close(busydialog)')#line:911
            if OOOO0O00OO00OO00O ==None :return O000OOO0OOO0000O0 .infoDialog (O000OOO0OOO0000O0 .lang (30705 ).encode ('utf-8'))#line:913
            if OOOO0O00OO00OO00O ==False :return #line:914
            OO00O0OOO000OOO0O ={}#line:916
            for O0OO0OO0000OO00O0 in ['title','originaltitle','tvshowtitle','year','season','episode','genre','rating','votes','director','writer','plot','tagline']:#line:917
                try :OO00O0OOO000OOO0O [O0OO0OO0000OO00O0 ]=O000OOO0OOO0000O0 .infoLabel ('listitem.%s'%O0OO0OO0000OO00O0 )#line:918
                except :pass #line:919
            OO00O0OOO000OOO0O =dict ((O0O0O000O0O00OOOO ,O0O0OO0O0O0OO00O0 )for O0O0O000O0O00OOOO ,O0O0OO0O0O0OO00O0 in OO00O0OOO000OOO0O .iteritems ()if not O0O0OO0O0O0OO00O0 =='')#line:920
            if not 'title'in OO00O0OOO000OOO0O :OO00O0OOO000OOO0O ['title']=O000OOO0OOO0000O0 .infoLabel ('listitem.label')#line:921
            O00OOO0OOO0000000 =O000OOO0OOO0000O0 .infoLabel ('listitem.icon')#line:922
            OOO0O000O00O00O00 .name =OO00O0OOO000OOO0O ['title'];OOO0O000O00O00O00 .year =OO00O0OOO000OOO0O ['year']if 'year'in OO00O0OOO000OOO0O else '0'#line:925
            OOO0O000O00O00O00 .getbookmark =True if (content =='movies'or content =='episodes')else False #line:927
            OOO0O000O00O00O00 .offset =bookmarks ().get (OOO0O000O00O00O00 .name ,OOO0O000O00O00O00 .year )#line:929
            OOO0O0O0000O00000 =resolver ().f4m (OOOO0O00OO00OO00O ,OOO0O000O00O00O00 .name )#line:931
            if not OOO0O0O0000O00000 ==None :return #line:932
            O00000O0O0000O0OO =O000OOO0OOO0000O0 .item (path =OOOO0O00OO00OO00O ,iconImage =O00OOO0OOO0000000 ,thumbnailImage =O00OOO0OOO0000000 )#line:935
            try :O00000O0O0000O0OO .setArt ({'icon':O00OOO0OOO0000000 })#line:936
            except :pass #line:937
            O00000O0O0000O0OO .setInfo (type ='Video',infoLabels =OO00O0OOO000OOO0O )#line:938
            O000OOO0OOO0000O0 .player .play (OOOO0O00OO00OO00O ,O00000O0O0000O0OO )#line:939
            O000OOO0OOO0000O0 .resolve (int (OO00000OO00000000 .argv [1 ]),True ,O00000O0O0000O0OO )#line:940
            OOO0O000O00O00O00 .totalTime =0 ;OOO0O000O00O00O00 .currentTime =0 #line:942
            for O0OO0OO0000OO00O0 in range (0 ,240 ):#line:944
                if OOO0O000O00O00O00 .isPlayingVideo ():break #line:945
                O000OOO0OOO0000O0 .sleep (1000 )#line:946
            while OOO0O000O00O00O00 .isPlayingVideo ():#line:947
                try :#line:948
                    OOO0O000O00O00O00 .totalTime =OOO0O000O00O00O00 .getTotalTime ()#line:949
                    OOO0O000O00O00O00 .currentTime =OOO0O000O00O00O00 .getTime ()#line:950
                except :#line:951
                    pass #line:952
                O000OOO0OOO0000O0 .sleep (2000 )#line:953
            O000OOO0OOO0000O0 .sleep (5000 )#line:954
        except :#line:955
            pass #line:956
    def onPlayBackStarted (O0OOOO0OO00O0O00O ):#line:959
        O000OOO0OOO0000O0 .execute ('Dialog.Close(all,true)')#line:960
        if O0OOOO0OO00O0O00O .getbookmark ==True and not O0OOOO0OO00O0O00O .offset =='0':#line:961
            O0OOOO0OO00O0O00O .seekTime (float (O0OOOO0OO00O0O00O .offset ))#line:962
    def onPlayBackStopped (O0OOO00O0O0OO000O ):#line:965
        if O0OOO00O0O0OO000O .getbookmark ==True :#line:966
            bookmarks ().reset (O0OOO00O0O0OO000O .currentTime ,O0OOO00O0O0OO000O .totalTime ,O0OOO00O0O0OO000O .name ,O0OOO00O0O0OO000O .year )#line:967
    def onPlayBackEnded (OOO0O0O0O00OO0OO0 ):#line:970
        OOO0O0O0O00OO0OO0 .onPlayBackStopped ()#line:971
class bookmarks :#line:975
    def get (OO000OO00O00OOO00 ,O00OO000O00000000 ,year ='0'):#line:976
        try :#line:977
            O0O00OOO0OO000O00 ='0'#line:978
            O0O0OO000O0OOO0OO =O0OOOO00O0OO0O000 .md5 ()#line:982
            for O00O0OO00OO0O00O0 in O00OO000O00000000 :O0O0OO000O0OOO0OO .update (str (O00O0OO00OO0O00O0 ))#line:983
            for O00O0OO00OO0O00O0 in year :O0O0OO000O0OOO0OO .update (str (O00O0OO00OO0O00O0 ))#line:984
            O0O0OO000O0OOO0OO =str (O0O0OO000O0OOO0OO .hexdigest ())#line:985
            O00000000OO0O0O0O =OOO0OO00OO0OO0O00 .connect (O000OOO0OOO0000O0 .bookmarksFile )#line:987
            O0O00OO0OOO000OO0 =O00000000OO0O0O0O .cursor ()#line:988
            O0O00OO0OOO000OO0 .execute ("SELECT * FROM bookmark WHERE idFile = '%s'"%O0O0OO000O0OOO0OO )#line:989
            OO0000OOO000O0OO0 =O0O00OO0OOO000OO0 .fetchone ()#line:990
            OO000OO00O00OOO00 .offset =str (OO0000OOO000O0OO0 [1 ])#line:991
            O00000000OO0O0O0O .commit ()#line:992
            if OO000OO00O00OOO00 .offset =='0':raise Exception ()#line:994
            O0000OOO0000O0000 ,OOO00O0OOO00OOO0O =divmod (float (OO000OO00O00OOO00 .offset ),60 );OO0OO0OO000O000OO ,O0000OOO0000O0000 =divmod (O0000OOO0000O0000 ,60 )#line:996
            OOO0O0OO0OO00000O ='%02d:%02d:%02d'%(OO0OO0OO000O000OO ,O0000OOO0000O0000 ,OOO00O0OOO00OOO0O )#line:997
            OOO0O0OO0OO00000O =(O000OOO0OOO0000O0 .lang (32502 )%OOO0O0OO0OO00000O ).encode ('utf-8')#line:998
            try :O0O0O0OOOOO0OOOO0 =O000OOO0OOO0000O0 .dialog .contextmenu ([OOO0O0OO0OO00000O ,O000OOO0OOO0000O0 .lang (32501 ).encode ('utf-8'),])#line:1000
            except :O0O0O0OOOOO0OOOO0 =O000OOO0OOO0000O0 .yesnoDialog (OOO0O0OO0OO00000O ,'','',str (O00OO000O00000000 ),O000OOO0OOO0000O0 .lang (32503 ).encode ('utf-8'),O000OOO0OOO0000O0 .lang (32501 ).encode ('utf-8'))#line:1001
            if O0O0O0OOOOO0OOOO0 :OO000OO00O00OOO00 .offset ='0'#line:1003
            return OO000OO00O00OOO00 .offset #line:1005
        except :#line:1006
            return O0O00OOO0OO000O00 #line:1007
    def reset (O00000OO0OOOO00O0 ,OOOOOO0O0000O000O ,O00O000O0O0O00000 ,OO0O0O00OO00O0OO0 ,year ='0'):#line:1010
        try :#line:1011
            O0O000O0O00OO0O0O =str (OOOOOO0O0000O000O )#line:1014
            OO0000OO0OOO000O0 =int (OOOOOO0O0000O000O )>180 and (OOOOOO0O0000O000O /O00O000O0O0O00000 )<=.92 #line:1015
            O0O0000OO0O0O00OO =O0OOOO00O0OO0O000 .md5 ()#line:1017
            for OO00OOO00O00OOOOO in OO0O0O00OO00O0OO0 :O0O0000OO0O0O00OO .update (str (OO00OOO00O00OOOOO ))#line:1018
            for OO00OOO00O00OOOOO in year :O0O0000OO0O0O00OO .update (str (OO00OOO00O00OOOOO ))#line:1019
            O0O0000OO0O0O00OO =str (O0O0000OO0O0O00OO .hexdigest ())#line:1020
            O000OOO0OOO0000O0 .makeFile (O000OOO0OOO0000O0 .dataPath )#line:1022
            O0000O0O0OO000O00 =OOO0OO00OO0OO0O00 .connect (O000OOO0OOO0000O0 .bookmarksFile )#line:1023
            OOO000O0000000OOO =O0000O0O0OO000O00 .cursor ()#line:1024
            OOO000O0000000OOO .execute ("CREATE TABLE IF NOT EXISTS bookmark (" "idFile TEXT, " "timeInSeconds TEXT, " "UNIQUE(idFile)" ");")#line:1025
            OOO000O0000000OOO .execute ("DELETE FROM bookmark WHERE idFile = '%s'"%O0O0000OO0O0O00OO )#line:1026
            if OO0000OO0OOO000O0 :OOO000O0000000OOO .execute ("INSERT INTO bookmark Values (?, ?)",(O0O0000OO0O0O00OO ,O0O000O0O00OO0O0O ))#line:1027
            O0000O0O0OO000O00 .commit ()#line:1028
        except :#line:1029
            pass 
#e9015584e6a44b14988f13e2298bcbf9
