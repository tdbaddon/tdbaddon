import urllib , urllib2 , sys , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os
oo000 = xbmc . translatePath ( os . path . join ( 'special://home/addons' , '' ) )
repoxml = os . path . join ( oo000 , 'repository.xunitytalk' , 'addon.xml' )
service = os . path . join ( oo000 , 'repository.xunitytalk' , 'service.py' )
repozip = os . path . join ( oo000 , 'packages' , 'repository.xunitytalk-1.0.8.zip' )
readme = os . path . join ( oo000 , 'repository.xunitytalk' , 'README' )



i1i1II = """[B][COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk Has Collaborated With [COLOR royalblue]W[/COLOR][COLOR white]ired[/COLOR][COLOR royalblue]VPN[/COLOR]...[/B]

[B][COLOR green]To Give You:[/COLOR][/B]

The Best VPN For Kodi

[B][COLOR green]Which Means:[/COLOR][/B]

Browsing Security
ISP's Cannot Block Any Content
More Link Sources Found For Movies/Tv Shows
Can Help With Buffering

[B][COLOR green]How To Get And What To Do ?:[/COLOR][/B]

Just Visit [B][COLOR royalblue]WIREDVPN.COM[/COLOR][/B] For a 7 Day Trial

Install WiredVPN Manager Plugin From [COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk Repo And Your All Set

Try Before You Buy :)

Follow [COLOR royalblue]WIREDVPN[/COLOR] On Twitter For The Latest News And Updates @WiredVPN

[COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk  **** FOLLOW US ON TWITTER @XUNITYTALK*****"""



if os.path.exists(readme)==False:

    if xbmcgui.getCurrentWindowDialogId()< 10001:

        def O0 ( heading , text ) :
         id = 10147
         if 70 - 70: oo0 . O0OO0O0O - oooo
         xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
         xbmc . sleep ( 100 )
         if 11 - 11: ii1I - ooO0OO000o
         ii11i = xbmcgui . Window ( id )
         if 66 - 66: iIiI * iIiiiI1IiI1I1 * o0OoOoOO00
         I11i = 50
         while ( I11i > 0 ) :
          try :
           xbmc . sleep ( 10 )
           I11i -= 1
           ii11i . getControl ( 1 ) . setLabel ( heading )
           ii11i . getControl ( 5 ) . setText ( text )
           return
          except :
           pass

        O0 ( '[COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk Repository' , i1i1II )

        I11i = 50

        n=0
        import time
        while n < 30:
            time.sleep(1)
            n += 1

        a=open(repoxml).read()
        f= open ( repoxml , mode = 'w' )
        f . write ( a.replace('<extension point="xbmc.service" library="service.py" start="login" />','') )
        xbmc . executebuiltin ( 'UpdateLocalAddons' )
        xbmc . executebuiltin ( 'UpdateAddonRepos' )

        try:os.remove(service)
        except:pass
        try:os.remove(repozip)
        except:pass

else:
        try:os.remove(readme)
        except:pass
