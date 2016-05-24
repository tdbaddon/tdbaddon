# coding: utf-8

import sys
import updater
import xbmcgui

update_status = updater.check_update()

if update_status == '':
    import generator
else:
    xbmcgui.Dialog().ok("[COLOR yellowgreen]B[/COLOR][COLOR dodgerblue]B[/COLOR][COLOR white]T[/COLOR][COLOR orangered]S[/COLOR]", update_status)
    sys.exit(-1)

# xbmcgui.Dialog().ok("DEBUG", "[" + sys.argv[2] + "]")

generator.go()
