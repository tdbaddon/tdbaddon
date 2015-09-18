#!/usr/bin/env python
# cleaners

# NB. htmlcleaner (to clean unicode entities) is run in the addDir function
# in default.py
# it is only called in cleaners.py when cleaning something for a metadata lookup.

import re
import htmlcleaner

def CLEANUP_FOR_META(name):
    #cleaner for when using a name for a metadata lookup

    # left these legacy functions in even thought they are not really needed
    # thanks to htmlcleaner. might help with some meta lookups
    name=re.sub('&#39;',"'",name)
    name=re.sub('&amp;','&',name)
    name=re.sub('&#xC6;','AE',name)
    name=re.sub('&#x27;',"'",name)
    name=re.sub('&#xED;','i',name)
    name=re.sub('&frac12;',' 1/2',name)
    name=re.sub('&#xBD;',' 1/2',name)
    name=re.sub('&#x26;','&',name)
    name=re.sub('&#x22;','',name)
    name=re.sub('&#xF4;','o',name)
    name=re.sub('&#xE9;',"e",name)
    name=re.sub('&#xEB;',"e",name)
    name=re.sub('&#248;',"o",name)
    name=re.sub('&#xE2;',"a",name)
    name=re.sub('&#xFB;',"u",name)
    name=re.sub('&apos;',"'",name)
    name=re.sub('&#xE1;',"a",name)
    name=re.sub('&#xFC;',"u",name)

    #run the unicode cleaner, but strip unicode to ASCII
    name = htmlcleaner.clean(name,strip=True)

    return name

def CLEANSEARCH(name):        
        name=re.sub('<em>','',name)
        name=re.sub('</em>','',name)
        name=re.sub('DivX - icefilms.info','',name)
        name=re.sub('</a>','',name)
        name=re.sub('<b>...</b>','',name)
        name=re.sub('- icefilms.info','',name)
        name=re.sub('.info','',name)
        name=re.sub('- icefilms','',name)
        name=re.sub(' -icefilms','',name)
        name=re.sub('-icefilms','',name)
        name=re.sub('icefilms','',name)
        name=re.sub('- DivX','',name)
        name=re.sub('- divx','',name)
        name=re.sub('- xvid','',name)
        name=re.sub('DivX','',name)
        name=re.sub('divx','',name)
        name=re.sub('xvid','',name)
        name=re.sub('-  Episode  List','- Episode List',name)
        name=re.sub('-Episode  List','- Episode List',name)
        
        return name

def CLEANUP(name):
    # clean names of annoying garbled text
    
    name=re.sub('</a>','',name)
    name=re.sub('<b>HD</b>',' [COLOR red]*HD*[/COLOR]',name)
    
    name=re.sub('"',"'",name)
    
    #print 'name after cleanup =' + name
    return name
