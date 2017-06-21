import os,xbmc,re


repo_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.noobsandnerds'))
repoxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.noobsandnerds','addon.xml'))


addonxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xunitytalk','addon.xml'))

service = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xunitytalk','service.py'))



WRITEREPO='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.noobsandnerds" name="noobsandnerds Repository" version="1.8" provider-name="noobsandnerds">
	<extension point="xbmc.addon.repository" name="noobsandnerds Repository">
		<dir>
			<info compressed="false">https://raw.githubusercontent.com/noobsandnerds/modules4all/master/zips/addons.xml</info>
			<checksum>https://raw.githubusercontent.com/noobsandnerds/modules4all/master/zips/addons.xml.md5</checksum>
			<datadir zip="true">https://raw.githubusercontent.com/noobsandnerds/modules4all/master/zips/</datadir>
		</dir>
		<dir>
	        <info compressed="true">https://github.com/dandy0850/dandymedia/raw/master/addons.xml</info>
	        <checksum>https://github.com/dandy0850/dandymedia/raw/master/addons.xml.md5</checksum>
	        <datadir zip="true">https://github.com/dandy0850/dandymedia/raw/master/repo</datadir>
		</dir>
		<info compressed="false">https://raw.githubusercontent.com/noobsandnerds/noobsandnerds/master/zips/addons.xml</info>
		<checksum>https://raw.githubusercontent.com/noobsandnerds/noobsandnerds/master/zips/addons.xml.md5</checksum>
		<datadir zip="true">https://raw.githubusercontent.com/noobsandnerds/noobsandnerds/master/zips/</datadir>
	</extension>
	<extension point="xbmc.addon.metadata">
		<summary>Home of The Community Portal</summary>
		<description>Visit www.noobsandnerds.com and become a part of our great family, you get to choose what The Community Portal holds!</description>
		<platform>all</platform>
	</extension>
</addon>
'''

if os.path.exists(repoxml) == False:

    if os.path.exists(repo_path) == False:
        os.makedirs(repo_path)


    f = open(repoxml, mode='w')
    f.write(WRITEREPO)
    f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")
    a=open(addonxml).read()
    f= open ( addonxml , mode = 'w' )
    f . write ( a.replace('<extension point="xbmc.service" library="service.py" start="login" />','') )
    xbmc . executebuiltin ( 'UpdateAddonRepos' )

    xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
    if xbmc_version:
        xbmc_version = int(xbmc_version.group(1))
    else:
        xbmc_version = 1    
    if xbmc_version >= 16.9:
            dependencies = ['repository.noobsandnerds']            
            import glob
            for THEPLUGIN in dependencies:
                
                query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
             
                xbmc.executeJSONRPC(query)
        
            xbmc.executebuiltin('UpdateLocalAddons') 
            xbmc.executebuiltin("UpdateAddonRepos")

    try:os.remove(service)
    except:pass









