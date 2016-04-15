# -*- coding: utf-8 -*-
from lib.modules.webutils import *
import json


trakt_api='684e0c03f9b8439a4ce05f957f9afab3c7a97e7890e74a25997d773b54e0f77d'
trakt_header= {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '%s'%trakt_api,
      
      
    }

def convert_linksx(links):
    # try:
    #     html=read_url(links)
    #     html=get_string(html)
    #     link=re.compile('<(?:iframe|IFRAME).*?(?:src|SRC)="(.+?)"').findall(html)[1]
    #     return link
    # except:
    #     pass
    # new=[]
    # for link in links:
    # 	print(link)
    #     html=read_url(link)
    #     html=get_string(html)
    #     link=re.compile('<(?:iframe|IFRAME).*?(?:src|SRC)="(.+?)"').findall(html)[1]
    #     new+=[link]
    return links
def get_string(text):
        string=text.replace('-','\\u00')
        #numbers
        string=string.replace('\\u0030','0').replace('\\u0031','1').replace('\\u0032','2').replace('\\u0033','3').replace('\\u0034','4').replace('\\u0035','5').replace('\\u0036','6').replace('\\u0037','7').replace('\\u0038','8').replace('\\u0039','9')
        #special chars
        string=string.replace('\\u0020',' ').replace('\\u0021','!').replace('\\u0022','"').replace('\\u0023','#').replace('\\u0024','$').replace('\\u0025','%').replace('\\u0026','&')  
        string=string.replace('\\u0027',"'").replace('\\u0028','(').replace('\\u0029',')').replace('\\u002a','*').replace('\\u002b','+').replace('\\u002c',',').replace('\\u002d','-').replace('\\u002e','.').replace('\\u002f','/')    
        string=string.replace('\\u003a',':').replace('\\u003b',';').replace('\\u003c','<').replace('\\u003d','=').replace('\\u003e','>').replace('\\u003f','?').replace('\\u0040','@')  
        string=string.replace('\\u005b','[').replace('\\u005c','\\').replace('\\u005d',']').replace('\\u005e','^').replace('\\u005f','_').replace('\\u0060','`')
        string=string.replace('\\u007b','{').replace('\\u007c','|').replace('\\u007d','}').replace('\\u007e','~')
        #eng alpha
        string=string.replace('\\u0041','A').replace('\\u0042','B').replace('\\u0043','C').replace('\\u0044','D').replace('\\u0045','E').replace('\\u0046','F').replace('\\u0047','G').replace('\\u0048','H').replace('\\u0049','I').replace('\\u004a','J').replace('\\u004b','K').replace('\\u004c','L').replace('\\u004d','M').replace('\\u004e','N').replace('\\u004f','O')
        string=string.replace('\\u0050','P').replace('\\u0051','Q').replace('\\u0052','R').replace('\\u0053','S').replace('\\u0054','T').replace('\\u0055','U').replace('\\u0056','V').replace('\\u0057','W').replace('\\u0058','X').replace('\\u0059','Y').replace('\\u005a','Z')
        
        string=string.replace('\\u0061','a').replace('\\u0062','b').replace('\\u0063','c').replace('\\u0064','d').replace('\\u0065','e').replace('\\u0066','f').replace('\\u0067','g').replace('\\u0068','h').replace('\\u0069','i').replace('\\u006a','j').replace('\\u006b','k').replace('\\u006c','l').replace('\\u006d','m').replace('\\u006e','n').replace('\\u006f','o')
        string=string.replace('\\u0070','p').replace('\\u0071','q').replace('\\u0072','r').replace('\\u0073','s').replace('\\u0074','t').replace('\\u0075','u').replace('\\u0076','v').replace('\\u0077','w').replace('\\u0078','x').replace('\\u0079','y').replace('\\u007a','z')

        #hrv abc
        string=string.replace('\\u00d0','D').replace('\\u0106','C').replace('\\u0107','c').replace('\\u010c','C').replace('\\u010d','c').replace('\\u0160','S').replace('\\u0161','s').replace('\\u017d','Z').replace('\\u017e','z')
        string=string.replace('\\u000a','\n')
        return string
def get_links_sx(url):
    

    def check(lista):
        lista=lista
        for i in range(len(lista)):
            if 'klipovito' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'filmovita' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'facebook' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'twitter' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'tvprofil' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'narod.hr' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif lista[i]=='t':
            	lista.pop(i)
            	check(lista)
            	break
        return lista

    def get_sites_linkovi(link):
        hosts=['streamin','played','vodlocker','neodrive','openload','filehoot','videowood','thevideo']
        read=read_url(link)
        sites=[]
        for i in range (len(hosts)):
            try:    
                reg='http://www.filmovita.com/(.+?)-%s/'%hosts[i]
                site='http://www.filmovita.com/' + re.findall(re.compile(reg),read)[0] +'-%s/'%hosts[i]
                sites+=[site]
            except: pass
        return sites

    def get_links_from_sites(sites):
        links=[]
        for i in range(len(sites)):
            html=read_url(sites[i])
            reg="id='engimadiv(.+?)'"
            enigma="engimadiv" + re.findall(re.compile(reg),html)[0] 
            soup=bs(html)
            text=soup.find('span',{'id':'%s'%enigma})['data-enigmav']
            text=get_string(text)#.lower()
            text=str(text)

            reg='(?:src|SRC)="(.+?)"'
            try:
                link=re.findall(re.compile(reg),text)[0]
                links+=[link]
            except:
                pass
        return links
    def get_links_str2(link):
        text=read_url(link)
        reg='href="(.+?)"'
        links=re.findall(re.compile(reg),text)
        return links


    def get_links_enigma(url):
        html=read_url(url)
        reg="id='engimadiv(.+?)'"
        enigma="engimadiv" + re.findall(re.compile(reg),html)[0] 
        soup=bs(html)
        text=soup.find('span',{'id':'%s'%enigma})['data-enigmav']
        text=get_string(text).lower()

        reg='href="(.+?)"'
        links=re.findall(re.compile(reg),text)
        return check(links)
    def get_links_verzija(url):
        html=read_url(url).lower()

        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
    
        reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]

        

        reg='href="(.+?)" (.+?)>gledaj na'
        listy=re.findall(re.compile(reg),html)

        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[0]
            items+=[item]
        
        return items

        
    html=read_url(url)
    
    if 'http://filmovita.com/links/' in html:
        reg='http://filmovita.com/links/(.+?)"'
        link='http://filmovita.com/links/' + re.findall(re.compile(reg),html)[0]
        sites=get_sites_linkovi(link)
        links=get_links_from_sites(sites)
        
        
        reg='http://filmovita.com/links/(.+?)"'
        link='http://filmovita.com/links/' + re.findall(re.compile(reg),html)[0]
            
        linko=get_links_str2(link)
        for i in range(len(linko)):
            links+=[linko[i]]
        
    elif 'enigmadiv' in html or 'enigmav' in html:
        links=get_links_enigma(url)
        
    elif 'Verzija' in html:
        links=get_links_verzija(url)
        
    elif 'youtube.com/embed/' in html:
        return ['Film je u vise djelova na youtube-u.','Posjetite filmovita.com']
    else:
        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]
    if links==[]:
        html=read_url(url).lower()

        reg='<iframe src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]
        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]


    return check(links)





def get_episode_link_sx(show_slug,season,number,show_year):
        slugs=['game-of-thrones','walking-dead','vampire-diaries','breaking-bad','tudors','da-vincis-demons',
            'vikings','better-call-saul','true-detective','originals','gotham','sherlock','blacklist','rome']
        slugy=['game-of-thrones','the-walking-dead','the-vampire-diaries','breaking-bad','the-tudors','da-vinci-s-demons',
            'vikings','better-call-saul','true-detective','the-originals','gotham','sherlock','the-blacklist','rome']

        for i in range(len(slugy)):
            if slugy[i]==show_slug:
                index=i
                break

        slug=slugs[index]
        sea=int(season)
        if season=='6': season='sesta'
        if season=='5': season='peta'
        if season=='4': season='cetvrta'
        if season=='3': season='treca'
        if season=='2': season='druga'
        if season=='1': season='prva'

        
        url='http://www.serijex.com/%s-%s-sezona-epizoda-%s/'%(slug,season,number)
        if slug=='the-blacklist' or slug=='blacklist':
        	print('okay')
        	if sea >1 and int(number)>7:
        		url='http://www.serijex.com/the-blacklist-%s-sezona-epizoda-%s/'%(season,number)

        return url
def get_tvshows_sx():

    slugs=['game-of-thrones','the-walking-dead','the-vampire-diaries','breaking-bad','the-tudors','da-vinci-s-demons',
            'vikings','better-call-saul','true-detective','the-originals','gotham','sherlock','the-blacklist','rome']


    results=[]
    for slug in slugs:
        request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s?extended=images'%slug, headers=trakt_header)
        response_body = urllib2.urlopen(request).read().decode('utf-8')
        decoded_data=json.loads(response_body)

        title=decoded_data['title']
        year=decoded_data['year']
        thumb=decoded_data['images']['poster']['thumb']
        slug=decoded_data['ids']['slug']
        imdb=decoded_data['ids']['imdb']
        trakt=decoded_data['ids']['trakt']
        
        results.append([title,year,slug,imdb,trakt,thumb])
    return results
def get_seasons_sx(slug):
    request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s/seasons?extended=images'%slug, headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title='Season %s'%decoded_data[i]['number']
        number=decoded_data[i]['number']
        id=decoded_data[i]['ids']['trakt']
        thumb=decoded_data[i]['images']['poster']['thumb']
        results+=[[title,id,thumb,number]]

    return results

def get_episodes_sx(slug,season):
    request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s/seasons/%s/?extended=images'%(slug,season), headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title=decoded_data[i]['title']
        season=decoded_data[i]['season']
        number=decoded_data[i]['number']
        id=decoded_data[i]['ids']['trakt']

        thumb=decoded_data[i]['images']['screenshot']['medium']
        results+=[[title,season,number,id,thumb]]

    return results



def get_host_names(urls):
    names=[]
    
    for i in range(len(urls)):
        url=urls[i]
        if 'www'in url:
            reg='http://www.(.+?)/'
        elif 'https' in url:
            reg='https://(.+?)/'
        else:
            reg='http://(.+?)/'
        try:
            name=re.findall(re.compile(reg),url)[0]
            names+=['%d. %s'%(i+1,name)]
        except:
            names+=[url]
    return names


