import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import shutil, glob
import os,fnmatch
import shutil, time
from common import regex_get_all, regex_from_to, create_directory, write_to_file, read_from_file

ADDON = xbmcaddon.Addon(id='plugin.video.gachecker')
check_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
settings_path = os.path.join(xbmc.translatePath('special://home/userdata'), 'addon_data')
packages_path = os.path.join(xbmc.translatePath('special://home/addons'), 'packages')


                  												  
def CATEGORIES():
    af = "test"
    list = []
    encr = ""
    py_list = []
    directories = os.listdir(check_path)
    for d in directories:
        if d == "script.module.xbmc.ads":
            addonpath = os.path.join(check_path, d)
            list.append(d)
            addDir('[COLOR cyan]'+ d + '[/COLOR]' + " (ADVERTS!)",d,2,'','list addons', d)
        if d != "plugin.video.gachecker":
            addonpath = os.path.join(check_path, d)
            for py_file in glob.glob(os.path.join(addonpath, "*.py")):
                text = read_from_file(py_file)
                if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0 or text.find('ADDON_ADVERTISE')>0 or text.find('OOo') > 0:
                    if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                        gf = ' GA references found, '
                    else:
                        gf = ' No GA references found '
                    if text.find('OOo') > 0:
                        af = 'HIDDEN CODE'
                    else:
                        af = "."
                    if text.count('GA(') == 0:
                        cnt = '0 events '
                    else:
                        cnt = "%s %s" % (text.count('GA('), "events ")
                    list.append(d)
                    addDir('[COLOR cyan]'+ d + '[/COLOR]' + gf + cnt + af,d,2,'','list addons', py_file)
            if os.path.isdir(addonpath):
                directories = os.listdir(addonpath)
                for sd in directories:
                    subd = os.path.join(check_path, d, sd)
                    for py_file in glob.glob(os.path.join(subd, "*.py")):
                        text = read_from_file(py_file)
                        if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0 or text.find('ADDON_ADVERTISE')>0 or text.find('OOo') > 0:
                            if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                                gf = ' GA references found, '
                            else:
                                gf = ' No GA references found '
                            if text.find('OOo') > 0:
                                af = 'HIDDEN CODE'
                            else:
                                af = "."
                            if text.count('GA(') == 0:
                                cnt = '0 events '
                            else:
                                cnt = "%s %s" % (text.count('GA('), "events ")
                            list.append(d)
                            addDir('[COLOR cyan]'+ d + '[/COLOR]' + gf + cnt + af,d,2,'','list addons', py_file)
                    if os.path.isdir(subd):
                        directories = os.listdir(subd)
                        for sd2 in directories:
                            subd2 = os.path.join(check_path, d, sd, sd2)
                            for py_file in glob.glob(os.path.join(subd2, "*.py")):
                                text = read_from_file(py_file)
                                if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0 or text.find('ADDON_ADVERTISE')>0 or text.find('OOo') > 0:
                                    if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                                        gf = ' GA references found, '
                                    else:
                                        gf = ' No GA references found '
                                    if text.find('OOo') > 0:
                                        af = 'HIDDEN CODE'
                                    else:
                                        af = "."
                                    if text.count('GA(') == 0:
                                        cnt = '0 events '
                                    else:
                                        cnt = "%s %s" % (text.count('GA('), "events ")
                                    list.append(d)
                                    addDir('[COLOR cyan]'+ d + '[/COLOR]' + gf + cnt + af,d,2,'','list addons', py_file)
                            if os.path.isdir(subd2):
                                directories = os.listdir(subd2)
                                for sd3 in directories:
                                    subd3 = os.path.join(check_path, d, sd, sd2, sd3)
                                    for py_file in glob.glob(os.path.join(subd3, "*.py")):
                                        text = read_from_file(py_file)
                                        if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0 or text.find('ADDON_ADVERTISE')>0 or text.find('OOo') > 0:
                                            if text.find('google-analytics') > 0 or text.find('GA(') > 0 or text.find('UA-') > 0:
                                                gf = ' GA references found, '
                                            else:
                                                gf = ' No GA references found '
                                            if text.find('OOo') > 0:
                                                af = 'HIDDEN CODE'
                                            else:
                                                af = "."
                                            if text.count('GA(') == 0:
                                                cnt = '0 events '
                                            else:
                                                cnt = "%s %s" % (text.count('GA('), "events ")
                                            list.append(d)
                                            addDir('[COLOR cyan]'+ d + '[/COLOR]' + gf + cnt + af,d,2,'','list addons', py_file)

        						
    if len(list) == 0:
        addDir("No Google Analytics, ads or hidden code found","",1,'','list addons','')


def remove_single(url):
    dialog = xbmcgui.Dialog()
    if dialog.yesno(url, "Do you want to remove this addon?"):
        urld = os.path.join(check_path, url)
        shutil.rmtree(urld)
		
        if dialog.yesno(url + " settings", "Do you want to remove this addon's settings?"):
            urld = os.path.join(settings_path, url)
            if os.path.exists(urld):
                shutil.rmtree(urld)
            else:
                dialog.ok(url + " settings", "", "No settings directories found")
		
        if dialog.yesno(url + " zip files", "Do you want to remove this addon's zip files?"):
            for package in glob.glob(os.path.join(packages_path, url + "*")):
                os.remove(package)
        if dialog.yesno(url + " - related repository", "Do you want to remove the repository?"):
            try:
                repositories(url)
            except:
                dialog.ok(url + " related repository", "Unable to remove - remove manually if required", "You might have already removed it.")
				
        dialog = xbmcgui.Dialog()
        if dialog.yesno("GA Checker", "Restart XBMC to finish removal", "", '', "Reboot Later", "Reboot Now"):
            if xbmc.getCondVisibility('system.platform.windows'):
                xbmc.executebuiltin('RestartApp')
            else:
                xbmc.executebuiltin('Reboot')

        xbmc.executebuiltin("Container.Refresh")
		
def py_list(py_list):
    addDir('[COLOR cyan]'+ py_list + '[/COLOR]',"url",4,'','list addons',"")
	
def repositories(addon_name):
    dialog = xbmcgui.Dialog()
    list = []
    repo_list = []
    dp = xbmcgui.DialogProgress()
    dp.create('Repository')
    directories = os.listdir(check_path)
    count = 0
    for d in directories:
        if d.startswith('repository'):
            addonpath = os.path.join(check_path, d)
            percent = 25
            dp.update(percent, "Scanning installed repositories")
            for file in glob.glob(os.path.join(addonpath, "addon.xml")):
                text = read_from_file(file)
                repo_url = regex_from_to(text, '<datadir zip="true">', '</datadir>')
                req = urllib2.Request(repo_url)
                percent = 50
                dp.update(percent, "Fetching repository addon information")
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                try:
                    response = urllib2.urlopen(req)
                    link=response.read()
                    response.close()
                    if repo_url.find('bitbucket') > 0:
                        match = re.compile('class="pjax-trigger execute"><span class="aui-icon aui-icon-small aui-iconfont-devtools-folder-closed"></span>(.+?)</a>').findall(link)
                    else:
                        match = re.compile('<a href="(.+?)/">').findall(link)
	                nItem = len(match)
                    for addons in match:
                        if addons.startswith('plugin') or addons.startswith('script') or addons.startswith('skin') or addons.startswith('metadata'):
                            percent = 75
                            dp.update(percent, "Matching addon to repository")
                            repo_list.append("<<%s/%s>>" % (addons, d))
                except:
                    pass
    
    if str(repo_list).find(addon_name) > 0:
        repo_name = regex_from_to(str(repo_list), addon_name + "/", ">>")
        repo_path = os.path.join(check_path, repo_name)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            percent = 100
            dp.update(percent, "Repository removed")
            time.sleep(1)
        else:
            dialog.ok(repo_name, "", "No repository found")
    else:
            dialog.ok(repo_name, "", "No repository found")
	
def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None


   
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

       
def addDir(name,url,mode,iconimage,description,py_list):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        contextMenuItems.append(('View related file name', "XBMC.Container.Update(%s?mode=5&url=%s)" % (sys.argv[0], py_list )))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

		

def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
        
               
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
		
elif mode==2:
        print ""+url
        remove_single(url)
		
elif mode==3:
        print ""+url
        remove_all(url)
		
elif mode==5:
        print ""+url
        py_list(url)
        

       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
