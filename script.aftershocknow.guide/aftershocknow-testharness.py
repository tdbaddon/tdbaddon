import sys, re, base64

sys.argv = ['script.aftershocknow.guide', '1']


from resources.lib import gui

try:
    w = gui.TVGuide()
    w.doModal()
    del w

except:
    import sys
    import traceback as tb
    (etype, value, traceback) = sys.exc_info()
    tb.print_exception(etype, value, traceback)