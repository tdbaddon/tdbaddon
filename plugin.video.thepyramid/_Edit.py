import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cHM6Ly9hcmNoaXZlLm9yZy9kb3dubG9hZC90b21iZWJiaW5ndG9uNF92aXJnaW5tZWRpYV9Ib21lL2hvbWUudHh0'))
addon = xbmcaddon.Addon('plugin.video.thepyramid')