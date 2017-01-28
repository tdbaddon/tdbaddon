"""
    urlresolver XBMC Addon
    Copyright (C) 2013 Bstrdsmkr
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Adapted for use in xbmc from:
    https://github.com/einars/js-beautify/blob/master/python/jsbeautifier/unpackers/packer.py
    
    usage:
    if detect(some_string):
        unpacked = unpack(some_string)
Unpacker for Dean Edward's p.a.c.k.e.r
"""

import re

def detect(source):
    """Detects whether `source` is P.A.C.K.E.R. coded."""
    source = source.replace(' ', '')
    if re.search('eval\(function\(p,a,c,k,e,(?:r|d)', source): return True
    else: return False

def unpack(source):
    """Unpacks P.A.C.K.E.R. packed js code."""
    payload, symtab, radix, count = _filterargs(source)

    if count != len(symtab):
        raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

    try:
        unbase = Unbaser(radix)
    except TypeError:
        raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

    def lookup(match):
        """Look up symbols in the synthetic symtab."""
        word = match.group(0)
        return symtab[unbase(word)] or word

    source = re.sub(r'\b\w+\b', lookup, payload)
    source = source.replace("\\'", "'")

    return _replacestrings(source)

def _filterargs(source):
    """Juice from a source file the four args needed by decoder."""
    argsregex = (r"}\('(.*)', *(\d+), *(\d+), *'(.*?)'\.split\('\|'\)")
    args = re.search(argsregex, source, re.DOTALL).groups()

    try:
        return args[0], args[3].split('|'), int(args[1]), int(args[2])
    except ValueError:
        raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

def _replacestrings(source):
    """Strip string lookup table (list) and replace values in source."""
    match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

    if match:
        varname, strings = match.groups()
        startpoint = len(match.group(0))
        lookup = strings.split('","')
        variable = '%s[%%d]' % varname
        for index, value in enumerate(lookup):
            source = source.replace(variable % index, '"%s"' % value)
        return source[startpoint:]
    return source


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }
    
    def __init__(self, base):
        self.base = base

        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret

class UnpackingError(Exception):
    """Badly packed source or general error. Argument is a
    meaningful description."""
    pass


if __name__ == "__main__":
    # test = '''eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('4(\'30\').2z({2y:\'5://a.8.7/i/z/y/w.2x\',2w:{b:\'2v\',19:\'<p><u><2 d="20" c="#17">2u 19.</2></u><16/><u><2 d="18" c="#15">2t 2s 2r 2q.</2></u></p>\',2p:\'<p><u><2 d="20" c="#17">2o 2n b.</2></u><16/><u><2 d="18" c="#15">2m 2l 2k 2j.</2></u></p>\',},2i:\'2h\',2g:[{14:"11",b:"5://a.8.7/2f/13.12"},{14:"2e",b:"5://a.8.7/2d/13.12"},],2c:"11",2b:[{10:\'2a\',29:\'5://v.8.7/t-m/m.28\'},{10:\'27\'}],26:{\'25-3\':{\'24\':{\'23\':22,\'21\':\'5://a.8.7/i/z/y/\',\'1z\':\'w\',\'1y\':\'1x\'}}},s:\'5://v.8.7/t-m/s/1w.1v\',1u:"1t",1s:"1r",1q:\'1p\',1o:"1n",1m:"1l",1k:\'5\',1j:\'o\',});l e;l k=0;l 6=0;4().1i(9(x){f(6>0)k+=x.r-6;6=x.r;f(q!=0&&k>=q){6=-1;4().1h();4().1g(o);$(\'#1f\').j();$(\'h.g\').j()}});4().1e(9(x){6=-1});4().1d(9(x){n(x)});4().1c(9(){$(\'h.g\').j()});9 n(x){$(\'h.g\').1b();f(e)1a;e=1;}',36,109,'||font||jwplayer|http|p0102895|me|vidto|function|edge3|file|color|size|vvplay|if|video_ad|div||show|tt102895|var|player|doPlay|false||21600|position|skin|test||static|1y7okrqkv4ji||00020|01|type|360p|mp4|video|label|FFFFFF|br|FF0000||deleted|return|hide|onComplete|onPlay|onSeek|play_limit_box|setFullscreen|stop|onTime|dock|provider|391|height|650|width|over|controlbar|5110|duration|uniform|stretching|zip|stormtrooper|213|frequency|prefix||path|true|enabled|preview|timeslidertooltipplugin|plugins|html5|swf|src|flash|modes|hd_default|3bjhohfxpiqwws4phvqtsnolxocychumk274dsnkblz6sfgq6uz6zt77gxia|240p|3bjhohfxpiqwws4phvqtsnolxocychumk274dsnkba36sfgq6uzy3tv2oidq|hd|original|ratio|broken|is|link|Your|such|No|nofile|more|any|availabe|Not|File|OK|previw|jpg|image|setup|flvplayer'.split('|')))'''
    # test = '''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('y.x(A(\'%0%f%b%9%1%d%8%8%o%e%B%c%0%e%d%0%f%w%1%7%3%2%p%d%1%n%2%1%c%0%t%0%f%7%8%8%d%5%6%1%7%e%b%l%7%1%2%e%9%q%c%0%6%1%z%2%0%f%b%1%9%c%0%s%6%6%l%G%4%4%5%5%5%k%b%7%5%8%o%i%2%k%6%i%4%2%3%p%2%n%4%5%7%6%9%s%4%j%q%a%h%a%3%a%E%a%3%D%H%9%K%C%I%m%r%g%h%L%v%g%u%F%r%g%3%J%3%j%3%m%h%4\'));',48,48,'22|72|65|6d|2f|77|74|61|6c|63|4e|73|3d|6f|6e|20|4d|32|76|59|2e|70|51|64|69|62|79|31|68|30|7a|34|66|write|document|75|unescape|67|4f|5a|57|55|3a|44|47|4a|78|49'.split('|'),0,{}))'''
    # test = '''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('x.w(z(\'%1%f%9%b%0%d%7%7%m%e%A%c%1%e%d%1%f%v%0%3%i%2%o%d%0%s%2%0%c%1%q%1%f%3%7%7%d%6%5%0%3%e%9%l%3%0%2%e%b%g%c%1%5%0%y%2%1%f%9%0%b%c%1%r%5%5%l%E%4%4%6%6%6%n%9%3%6%7%m%k%2%n%5%k%4%2%i%o%2%s%4%6%3%5%b%r%4%8%D%h%C%a%F%8%H%B%I%h%i%a%g%8%u%a%q%j%t%j%g%8%t%h%p%j%p%a%G%4\'));',45,45,'72|22|65|61|2f|74|77|6c|5a|73|55|63|3d|6f|6e|20|79|59|6d|4d|76|70|69|2e|62|7a|30|68|64|44|54|66|write|document|75|unescape|67|51|32|6a|3a|35|5f|47|34'.split('|'),0,{}))'''
    #test = '''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('q.r(s(\'%h%t%a%p%u%6%c%n%0%5%l%4%2%4%7%j%0%8%1%o%b%3%7%m%1%8%a%7%b%3%d%6%1%f%0%v%1%5%D%9%0%5%c%g%0%4%A%9%0%f%k%z%2%8%1%C%2%i%d%6%2%3%k%j%2%3%y%e%x%w%g%B%E%F%i%h%e\'));',42,42,'5a|4d|4f|54|6a|44|33|6b|57|7a|56|4e|68|55|3e|47|69|65|6d|32|45|46|31|6f|30|75|document|write|unescape|6e|62|6c|2f|3c|22|79|63|66|78|59|72|61'.split('|'),0,{}))'''
    #test='''eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('8("39").38({37:[{p:"4://1.3.2/36/v.35",34:"33"}],32:"4://1.3.2/i/31/30/2z.2y",2x:"2w",2v:"q%",2u:"q%",2t:"16:9",2s:"2r",2q:"2p",2o:[{p:"4://3.2/j?h=2n&g=7",2m:"2l"}],2k:{2j:\'#2i\',2h:14,2g:"2f",2e:0},"2d":{2c:"%2b 2a%o%29%28%27%26.2%25-7.a%22 24%e 23%e 21%e 20%1z 1y%o%1x%22 1w%1v 1u%1t%n%1s%1r%n",1q:"4://3.2/7.a"},1p:"1o",1n:"1m.1l | 1k 1j 1i 1h 1g ",1f:"4://3.2"});1e b,d;8().1d(6(x){k(5>0&&x.1c>=5&&d!=1){d=1;$(\'c.1b\').1a(\'19\')}});8().18(6(x){m(x)});8().17(6(){$(\'c.l\').15()});6 m(x){$(\'c.l\').13();k(b)12;b=1;$.11(\'4://3.2/j?h=10&g=7&z=y-w-u-t-s\',6(f){$(\'#r\').a(f)})}',36,118,'||tv|putload|https||function|3t1tlhv83pqr|jwplayer||html|vvplay|div|vvad|3D0|data|file_code|op||dl|if|video_ad|doPlay|3E|3D|file|100|fviews|2b320c6ae13efa71a060a7076ca296c2|1485454645|106||81||32755|hash|view|get|return|hide||show||onComplete|onPlay|slow|fadeIn|video_ad_fadein|position|onTime|var|aboutlink|Home|Sharing|And|Uploading|Video|TV|PUTLOAD|abouttext|vapor|skin|link|2FIFRAME|3C|3D500|HEIGHT|3D900|WIDTH|22true|allowfullscreen|3DNO|SCROLLING|MARGINHEIGHT||MARGINWIDTH|FRAMEBORDER|2Fembed|2Fputload|2F|3A|22http|SRC|3CIFRAME|code|sharing|backgroundOpacity|Verdana|fontFamily|fontSize|FFFFFF|color|captions|thumbnails|kind|get_slides|tracks|start|startparam|true|androidhls|aspectratio|height|width|4548|duration|jpg|3t1tlhv83pqr_xt|00006|01|image|480|label|mp4|ykgip2nkk62birmpnhxgrirvpya7wwl2t74yvewln767vcte7devr4is3yta|sources|setup|vplayer'.split('|')))'''
    #test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('w.C(a(){m(d(\'u\')==e){}},B);a p(4,h,f,6,7){2 3=q r();3.t(3.s()+(f*g*g*o));2 8="; 8="+3.D();k.l=4+"="+h+8+";7="+7+"; 6="+6}a d(4){2 b=4+"=";2 9=k.l.z(\';\');y(2 i=0;i<9.5;i++){2 c=9[i];x(c.A(0)==\' \')c=c.j(1,c.5);m(c.v(b)==0)n c.j(b.5,c.5)}n e}',40,40,'||var|date|name|length|path|domain|expires|ca|function|nameEQ||getcookie|null|hours|60|value||substring|document|cookie|if|return|1000|setcookie|new|Date|getTime|setTime|09ffa5fd853pbe2faac20a3e74138ea72a4807d21f2b|indexOf|window|while|for|split|charAt|5000|setTimeout|toGMTString'.split('|'),0,{}))'''
    #test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('j.G=j.w(3(){2(7.c("B-C").k>0){2(7.c("B-C")[0].Y=="X"){j.Z(G);9=7.c("B-C")[0];o=7.c("4").k;n=7.c("v").k;2(o>0){4=7.c("4")[0];4.H=3(){h(4,"e")};4.I=3(){d(4,"e")};9.J(7.F(\'4\'))}7.11.12=3(){2(n>0){d(b,"g")}2(o>0){d(4,"g")}};2(n>0){b=7.c("v")[0];b.H=3(){h(b,"e")};b.I=3(){d(b,"e")};9.J(7.F(\'v\'))}j.w(3(){2(n>0){2(8(9,"f-p")==m){d(b,"g")}l 2(8(9,"f-p")==i&&8(9,"f-E-M")==m&&8(b,"e")==i){h(b,"g")}}2(o>0){j.w(3(){2(8(9,"f-p")==m){d(4,"g")}l 2(8(9,"f-p")==i&&8(9,"f-E-M")==m&&8(4,"e")==i){h(4,"g")}},A)}},A)}}},A);3 8(S,T){y(\' \'+S.5+\' \').Q(\' \'+T+\' \')>-1}3 h(6,5){2(6.q){6.q.14(5)}l 2(!O(6,5)){6.5+=" "+5}}3 d(6,5){2(6.q){6.q.N(5)}l 2(O(6,5)){z P=D V(\'(\\s|^)\'+5+\'(\\s|$)\');6.5=6.5.U(P,\' \')}}W.10.N=3(){z x,a=16,L=a.k,u;R(L&&t.k){x=a[--L];R((u=t.Q(x))!==-1){t.17(u,1)}}y t};3 18(K){z r=D 19();r.1a("1c",K,i);r.1b(13);y r.15}',62,75,'||if|function|infobar|className|el|document|hasThisClass|videodiv||changerdiv|getElementsByClassName|removeClass|hover|vjs|hide|addClass|false|window|length|else|true|ischangerhere|isinfohere|paused|classList|xmlHttp||this|ax|changer|setInterval|what|return|var|500|video|js|new|user|getElementById|checkforvideo|onmouseenter|onmouseleave|appendChild|theUrl||inactive|remove|hasClass|reg|indexOf|while|element|cls|replace|RegExp|Array|DIV|tagName|clearInterval|prototype|body|onmousemove|null|add|responseText|arguments|splice|httpGet|XMLHttpRequest|open|send|GET'.split('|'),0,{}))'''
    #test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('z.A(9(){p(t(\'q\')==l){7(\'B\',\'a\',6,\'/\',\'.f.g\');7(\'q\',\'a\',1,\'/\',\'.f.g\');7(\'C\',\'a\',2,\'/\',\'.f.g\')}},v);9 7(4,k,m,b,h){3 5=D J();5.K(5.I()+(m*r*r*G));3 d="; d="+5.F();u.s=4+"="+k+d+";h="+h+"; b="+b}9 t(4){3 j=4+"=";3 e=u.s.x(\';\');w(3 i=0;i<e.8;i++){3 c=e[i];y(c.E(0)==\' \')c=c.n(1,c.8);p(c.H(j)==0)o c.n(j.8,c.8)}o l}',47,47,'|||var|name|date||setcookie|length|function|OK|path||expires|ca|vkpass|com|domain||nameEQ|value|null|hours|substring|return|if|09ffa5fd853pbe2faac20a3e74138ea72a4807d21f2b|60|cookie|getcookie|document|5000|for|split|while|window|setTimeout|09ffa5fd853bbe2faac20a3e74138ea72a4807d21f2b|09ffa5fd853rbe2faac20a3e74138ea72a4807d21f2b|new|charAt|toGMTString|1000|indexOf|getTime|Date|setTime'.split('|'),0,{}))'''
    #test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('8(2.C.B<A){8(2.9("h").e>0){2.9("h")[0].a.b=\'c\'}}H i(j,6){4 1=G F();4 5="";4 7=[];4 3;z(3 y 6){7.r(l(3)+\'=\'+l(6[3]))}5=7.w(\'&\').v(/%u/g,\'+\');1.J(\'I\',j);1.k(\'m-Y\',\'11/x-X-Z-10\');1.k(\'m-W\',5.e);1.M(5)}2.K(\'O\').a.b=\'c\';i(\'t://Q.R.n/S\',{P:\'L//N/U+V/12|T=\',s:\'q://o.p.n/E/d//D\',f:2.f});',62,65,'|XHR|document|name|var|urlEncodedData|data|urlEncodedDataPairs|if|getElementsByClassName|style|display|block||length|referrer||close_min|sendPost|link|setRequestHeader|encodeURIComponent|Content|com|drive|google|https|push|video_link|http|20|replace|join||in|for|400|scrollHeight|body|view|file|XMLHttpRequest|new|function|POST|open|getElementById|VVf0YnFvAZTWk1Yyq8kDH7o95L2Ywk8On80uA8aLu8FO0p42wWghKPQiym3BBhGDfBIyrfBRgdg613iNJucCNgamYPGyfh|send|vQItcR|ntfound|id|cdn25|vkpass|broken|hfPNqJY8djW1iNqYEMRb8064DovKJXBiunE26FSt3eI|wUZ||Length|www|Type|form|urlencoded|application|pdyfE0GfU9E6XxutQi2'.split('|'),0,{}))'''
    test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('f.w(\'<0 v u="" t="0" x="0-y b-B-A" s C="p" l="k:i%;n:i%;"><7 8="1://9.2.3/a/r" c="0/6" 5="q" 4="o" /><7 8="1://9.2.3/a/m" c="0/6" 5="z" 4="R" /><7 8="1://9.2.3/a/Q" c="0/6" 5="D" 4="P" /><7 8="1://9.2.3/a/U" c="0/6" 5="M" 4="F" /></0>\');d j="",h="1://2.3/";E.b=H(\'0\');b.I();b.K({J:j,L:h});d g=f.G("0");g.N(\'V\',S(e){e.O()},T);',58,58,'video|http|vkpass|com|res|label|mp4|source|src|cdn25|hop|vjs|type|var||document|myVideo|vlolink|100|vlofile|width|style|40d5a90cb487138ecd4711cf7fffe448|height|360|auto|360p|bec4ddbc646483156b9f434221520d8f|controls|id|poster|crossdomain|write|class|js|720p|skin|default|preload|1080p|window|480|getElementById|videojs|videoJsResolutionSwitcher|image|logobrand|destination|480p|addEventListener|preventDefault|1080|cb9eed6a123ac3856f87d4a88b89d939|720|function|false|7f553afd1a8ddd486d40a15a4b9c12c0|contextmenu'.split('|'),0,{}))'''
    print unpack(test)
