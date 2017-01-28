import urllib,urllib2,urlparse,re,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs
import json
import random
import sys
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'audio')

url = 'http://goo.gl/KLlY6m'
li = xbmcgui.ListItem('00s Club Hits', iconImage='http://api.audioaddict.com/v1/assets/image/1f2189badb0bb9ccba20e54163afff69.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/1f2189badb0bb9ccba20e54163afff69.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/KYZEXC'
li = xbmcgui.ListItem('Ambient', iconImage='http://api.audioaddict.com/v1/assets/image/9760862fcf5601c05c3581d6c0984128.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/9760862fcf5601c05c3581d6c0984128.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/pnw00c'
li = xbmcgui.ListItem('Bass & Jackin-House', iconImage='http://api.audioaddict.com/v1/assets/image/89b0dfb93cb7eba4d345d116f7fc00e7.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/89b0dfb93cb7eba4d345d116f7fc00e7.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/85abPX'
li = xbmcgui.ListItem('Bassline', iconImage='http://api.audioaddict.com/v1/assets/image/98bbdb73486e5c0431a44117af617576.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/98bbdb73486e5c0431a44117af617576.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/nM9KJO'
li = xbmcgui.ListItem('Big Room House', iconImage='http://api.audioaddict.com/v1/assets/image/5b7f5db07bd3bc6e8097ea33bbea7552.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5b7f5db07bd3bc6e8097ea33bbea7552.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/yj8z7Y'
li = xbmcgui.ListItem('Breaks', iconImage='http://api.audioaddict.com/v1/assets/image/5fe8da68c08afeba771f1c0a5ba6bc2f.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5fe8da68c08afeba771f1c0a5ba6bc2f.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/pTM8kz'
li = xbmcgui.ListItem('ChillHop', iconImage='http://api.audioaddict.com/v1/assets/image/2bca153955723e44b5ef9ab9e9fcba8d.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/2bca153955723e44b5ef9ab9e9fcba8d.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/pWBXPp'
li = xbmcgui.ListItem('Chillout Dreams', iconImage='http://api.audioaddict.com/v1/assets/image/7a0a070cca01976ea62c9e1c5a19e9b1.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/7a0a070cca01976ea62c9e1c5a19e9b1.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/3DbFWl'
li = xbmcgui.ListItem('Chillout', iconImage='http://api.audioaddict.com/v1/assets/image/8f7ce44aa749a97563c98dc5b69053aa.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/8f7ce44aa749a97563c98dc5b69053aa.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/25gJhg'
li = xbmcgui.ListItem('Chillstep', iconImage='http://api.audioaddict.com/v1/assets/image/7251688497a15b6a27a8e6952a3318fc.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/7251688497a15b6a27a8e6952a3318fc.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/DeKh27'
li = xbmcgui.ListItem('Classic EuroDance', iconImage='http://api.audioaddict.com/v1/assets/image/a272766a55dc1d3c5b63e688d7a3d0de.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a272766a55dc1d3c5b63e688d7a3d0de.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/UxM6Yb'
li = xbmcgui.ListItem('Classic EuroDisco', iconImage='http://api.audioaddict.com/v1/assets/image/f9c6cdb880da74aa74ec581dc3f09dbd.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/f9c6cdb880da74aa74ec581dc3f09dbd.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/i9aMBc'
li = xbmcgui.ListItem('Classic Trance', iconImage='http://api.audioaddict.com/v1/assets/image/53906dc786e7f3d55536defca56a4b5f.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/53906dc786e7f3d55536defca56a4b5f.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/oRGdGC'
li = xbmcgui.ListItem('Classic Vocal Trance', iconImage='http://api.audioaddict.com/v1/assets/image/6c59bb5709a2e2ecae99765d64ce57e6.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/6c59bb5709a2e2ecae99765d64ce57e6.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/aAfDRG'
li = xbmcgui.ListItem('Club Dubstep', iconImage='http://api.audioaddict.com/v1/assets/image/29b1b727e81f9dc1c6ca40926ac8ae34.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/29b1b727e81f9dc1c6ca40926ac8ae34.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/I77zsS'
li = xbmcgui.ListItem('Club Sounds', iconImage='http://api.audioaddict.com/v1/assets/image/6620a82bb6a6d0bc281260645b996b0a.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/6620a82bb6a6d0bc281260645b996b0a.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/azQjDe'
li = xbmcgui.ListItem('Dark Dnb', iconImage='http://api.audioaddict.com/v1/assets/image/1561ba009eb79c68b9de141f8685c927.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/1561ba009eb79c68b9de141f8685c927.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/eOdJwq'
li = xbmcgui.ListItem('Deep House', iconImage='http://api.audioaddict.com/v1/assets/image/8dd90c88b4ee5399e6182204a2ede8ed.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/8dd90c88b4ee5399e6182204a2ede8ed.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/kzXHzG'
li = xbmcgui.ListItem('Deep Nu-Disco', iconImage='http://api.audioaddict.com/v1/assets/image/3896ecff86795302304c64386ff2c5db.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/3896ecff86795302304c64386ff2c5db.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/rlVpld'
li = xbmcgui.ListItem('Deep Tech', iconImage='http://api.audioaddict.com/v1/assets/image/87d3b2ee913e6ac75882329971d58be4.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/87d3b2ee913e6ac75882329971d58be4.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/lg4So9'
li = xbmcgui.ListItem('Disco House', iconImage='http://api.audioaddict.com/v1/assets/image/0ea9396414430256ffb76cd6148bf88a.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/0ea9396414430256ffb76cd6148bf88a.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/NaLOZo'
li = xbmcgui.ListItem('Downtempo Lounge', iconImage='http://api.audioaddict.com/v1/assets/image/6da83f72080cb225acf608e54f992cf2.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/6da83f72080cb225acf608e54f992cf2.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/X53iEH'
li = xbmcgui.ListItem('DJ Mixes', iconImage='http://api.audioaddict.com/v1/assets/image/5a0a6603d9a3f151b9eced1629e77d66.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5a0a6603d9a3f151b9eced1629e77d66.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/7G6L6V'
li = xbmcgui.ListItem('Drum and Bass', iconImage='http://api.audioaddict.com/v1/assets/image/f2ed26a932bdb5cd0a0eac576aebfa3f.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/f2ed26a932bdb5cd0a0eac576aebfa3f.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/4axAH2'
li = xbmcgui.ListItem('Dubstep', iconImage='http://api.audioaddict.com/v1/assets/image/e0614d304c8fd5879a1278dd626d8769.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/e0614d304c8fd5879a1278dd626d8769.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/lcitbb'
li = xbmcgui.ListItem('EcLectronica', iconImage='http://api.audioaddict.com/v1/assets/image/25f559a97855d8107e7cdc63f2acb345.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/25f559a97855d8107e7cdc63f2acb345.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/IhRGd0'
li = xbmcgui.ListItem('Electro House', iconImage='http://api.audioaddict.com/v1/assets/image/387bfe3c7d50b4edd1408135596a03df.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/387bfe3c7d50b4edd1408135596a03df.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/s4aCi9'
li = xbmcgui.ListItem('Electropop', iconImage='http://api.audioaddict.com/v1/assets/image/72852e54a50b903aa0a726f87c0050c2.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/72852e54a50b903aa0a726f87c0050c2.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/FHIWp2'
li = xbmcgui.ListItem('Epic Trance', iconImage='http://api.audioaddict.com/v1/assets/image/5a76739725cd2106a3e2f30a1461a9bd.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5a76739725cd2106a3e2f30a1461a9bd.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/ueUBHy'
li = xbmcgui.ListItem('EuroDance', iconImage='http://api.audioaddict.com/v1/assets/image/a42ae2b9810acb81c6003915113c7d9d.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a42ae2b9810acb81c6003915113c7d9d.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/fpm2GG'
li = xbmcgui.ListItem('Funky House', iconImage='http://api.audioaddict.com/v1/assets/image/45d5aa9e246fd59fe03e601171059581.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/45d5aa9e246fd59fe03e601171059581.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/4YvOGo'
li = xbmcgui.ListItem('Future Garage', iconImage='http://api.audioaddict.com/v1/assets/image/d6aa1e9b4c48141fa573d498eba41a2a.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/d6aa1e9b4c48141fa573d498eba41a2a.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/P5vuQV'
li = xbmcgui.ListItem('Future Synthpop', iconImage='http://api.audioaddict.com/v1/assets/image/f4b0f3c30b34cf76de0955652ae5664a.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/f4b0f3c30b34cf76de0955652ae5664a.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/ec6aYi'
li = xbmcgui.ListItem('Gabber', iconImage='http://api.audioaddict.com/v1/assets/image/83b92cbe5cdc692fb0c8871135e98c55.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/83b92cbe5cdc692fb0c8871135e98c55.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/ddexWK'
li = xbmcgui.ListItem('Goa & Psychedelic Trance', iconImage='http://api.audioaddict.com/v1/assets/image/b5b22bf5232f246bf63b25914bd369e3.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/b5b22bf5232f246bf63b25914bd369e3.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/dpZkzN'
li = xbmcgui.ListItem('Hands Up', iconImage='http://api.audioaddict.com/v1/assets/image/9d04d9b20de5378994fa8653a1dc69f3.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/9d04d9b20de5378994fa8653a1dc69f3.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/A92JIT'
li = xbmcgui.ListItem('Hard Dance', iconImage='http://api.audioaddict.com/v1/assets/image/a67b19cab6cdb97ec77f8264f9c4c562.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a67b19cab6cdb97ec77f8264f9c4c562.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/N6iXwj'
li = xbmcgui.ListItem('Hard Techno', iconImage='http://api.audioaddict.com/v1/assets/image/64249abcb7fcfb5b790953632dc6c779.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/64249abcb7fcfb5b790953632dc6c779.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/I7OU5k'
li = xbmcgui.ListItem('Hardcore', iconImage='http://api.audioaddict.com/v1/assets/image/14f1a4484dc88e0df006e9cd71407bcb.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/14f1a4484dc88e0df006e9cd71407bcb.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/NUYmUL'
li = xbmcgui.ListItem('Hardstyle', iconImage='http://api.audioaddict.com/v1/assets/image/b27a7b020806ce4428307b30b44734ec.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/b27a7b020806ce4428307b30b44734ec.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/yRVD3a'
li = xbmcgui.ListItem('House', iconImage='http://api.audioaddict.com/v1/assets/image/6f8a0b3279c24b1c5fa1c6c1397b9b56.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/6f8a0b3279c24b1c5fa1c6c1397b9b56.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/pCfHuS'
li = xbmcgui.ListItem('Jungle', iconImage='http://api.audioaddict.com/v1/assets/image/1501288819231087619e6e659f122830.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/1501288819231087619e6e659f122830.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/KyPgyu'
li = xbmcgui.ListItem('Latin House', iconImage='http://api.audioaddict.com/v1/assets/image/fb8908953ab95d2f01402660e2cc0883.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/fb8908953ab95d2f01402660e2cc0883.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/jRo2SK'
li = xbmcgui.ListItem('Liquid DnB', iconImage='http://api.audioaddict.com/v1/assets/image/75b2b5e697e7948f5fcd64a1c54f3f72.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/75b2b5e697e7948f5fcd64a1c54f3f72.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/anLo9d'
li = xbmcgui.ListItem('Liquid Dubstep', iconImage='http://api.audioaddict.com/v1/assets/image/df258a92e9d5152cb182b439f1d0eb2b.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/df258a92e9d5152cb182b439f1d0eb2b.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/4qBh16'
li = xbmcgui.ListItem('Lounge', iconImage='http://api.audioaddict.com/v1/assets/image/58f7afca5a6883c063f8642bfd2cef80.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/58f7afca5a6883c063f8642bfd2cef80.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/OB3tA8'
li = xbmcgui.ListItem('Mainstage', iconImage='http://api.audioaddict.com/v1/assets/image/5bafe3802484d479d77b21aa34f537fe.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5bafe3802484d479d77b21aa34f537fe.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/cE3bOu'
li = xbmcgui.ListItem('Minimal', iconImage='http://api.audioaddict.com/v1/assets/image/5c29e3063f748d156260fb874634b602.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5c29e3063f748d156260fb874634b602.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/scbPIu'
li = xbmcgui.ListItem('Nightcore', iconImage='http://api.audioaddict.com/v1/assets/image/2200134b0c655a3cd40e0fbf7380c9a0.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/2200134b0c655a3cd40e0fbf7380c9a0.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/RBmvSw'
li = xbmcgui.ListItem('Nu Disco', iconImage='http://api.audioaddict.com/v1/assets/image/4ba0684daed5c3c422b8ad3aa59c7eaf.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/4ba0684daed5c3c422b8ad3aa59c7eaf.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/FHGBfH'
li = xbmcgui.ListItem('Oldschool Acid', iconImage='http://api.audioaddict.com/v1/assets/image/7edf76e784f740c1a20904309bbc7080.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/7edf76e784f740c1a20904309bbc7080.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/kIRcKG'
li = xbmcgui.ListItem('Oldschool Rave', iconImage='http://api.audioaddict.com/v1/assets/image/8c4ec9353361ef5fd6c9cbc4999e2fd1.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/8c4ec9353361ef5fd6c9cbc4999e2fd1.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/MWeysQ'
li = xbmcgui.ListItem('Oldschool Techno & Trance', iconImage='http://api.audioaddict.com/v1/assets/image/ad112b71e9682c79343a4df45d419297.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/ad112b71e9682c79343a4df45d419297.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/Zabv14'
li = xbmcgui.ListItem('Progressive Psy', iconImage='http://api.audioaddict.com/v1/assets/image/4aeae25360c3792e8e9fd6f2e5cdf39e.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/4aeae25360c3792e8e9fd6f2e5cdf39e.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/JpO8XX'
li = xbmcgui.ListItem('Progressive', iconImage='http://api.audioaddict.com/v1/assets/image/fcea7c9d9a16314103a41f66bd6dfd15.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/fcea7c9d9a16314103a41f66bd6dfd15.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/RKuUMG'
li = xbmcgui.ListItem('Psybient', iconImage='http://api.audioaddict.com/v1/assets/image/178802e0d43b3d42f2476a183541d652.jpg', thumbnailImage='http://api.audioaddict.com/v1/assets/image/178802e0d43b3d42f2476a183541d652.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/R9bhl3'
li = xbmcgui.ListItem('PsyChill', iconImage='http://api.audioaddict.com/v1/assets/image/f301e3e597472b3edbf50a770a52c087.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/f301e3e597472b3edbf50a770a52c087.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/YvvXGc'
li = xbmcgui.ListItem('Russian Club Hits', iconImage='http://api.audioaddict.com/v1/assets/image/3b2e1348eb2ded04b1b97e1791001bf8.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/3b2e1348eb2ded04b1b97e1791001bf8.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/kNnFCq'
li = xbmcgui.ListItem('Soulful House', iconImage='http://api.audioaddict.com/v1/assets/image/950ff823b9989f18f19ba65fb149fcad.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/950ff823b9989f18f19ba65fb149fcad.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/AjnKj8'
li = xbmcgui.ListItem('Space Dreams', iconImage='http://api.audioaddict.com/v1/assets/image/4531d1656bc302d4f1898f779a988c17.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/4531d1656bc302d4f1898f779a988c17.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/2BkS6G'
li = xbmcgui.ListItem('Tech House', iconImage='http://api.audioaddict.com/v1/assets/image/a1cb226c2170a74ed0fdb4839dafe869.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a1cb226c2170a74ed0fdb4839dafe869.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/wfHVU7'
li = xbmcgui.ListItem('Techno', iconImage='http://api.audioaddict.com/v1/assets/image/cedaa3b495a451bdd6ee4b21311e155c.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/cedaa3b495a451bdd6ee4b21311e155c.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/YLTTGa'
li = xbmcgui.ListItem('Trance', iconImage='http://api.audioaddict.com/v1/assets/image/befc1043f0a216128f8570d3664856f7.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/befc1043f0a216128f8570d3664856f7.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/yvHGfr'
li = xbmcgui.ListItem('Trap', iconImage='http://api.audioaddict.com/v1/assets/image/a79fc1acd04100c12f7b55c17c72a23e.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a79fc1acd04100c12f7b55c17c72a23e.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/vGWUrW'
li = xbmcgui.ListItem('UMF Radio', iconImage='http://api.audioaddict.com/v1/assets/image/2c91e9bbb77821106c9905653a5ade9e.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/2c91e9bbb77821106c9905653a5ade9e.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/FpzkBK'
li = xbmcgui.ListItem('Underground Techno', iconImage='http://api.audioaddict.com/v1/assets/image/cfaee945340928dd2250e731efda8e6c.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/cfaee945340928dd2250e731efda8e6c.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/qLs0Oj'
li = xbmcgui.ListItem('Vocal Chillout', iconImage='http://api.audioaddict.com/v1/assets/image/a5b0bd27de43d04e1da9acf5b8883e85.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/a5b0bd27de43d04e1da9acf5b8883e85.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/Xsh9a1'
li = xbmcgui.ListItem('Vocal Lounge', iconImage='http://api.audioaddict.com/v1/assets/image/5381371e7ebab35aaa3b8f3f290f31ca.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/5381371e7ebab35aaa3b8f3f290f31ca.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

url = 'http://goo.gl/nvbDmd'
li = xbmcgui.ListItem('Vocal Trance', iconImage='http://api.audioaddict.com/v1/assets/image/009b4fcdb032cceee6f3da5efd4a86e9.png', thumbnailImage='http://api.audioaddict.com/v1/assets/image/009b4fcdb032cceee6f3da5efd4a86e9.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

li.setProperty('fanart_image', 'fanart.jpg')

xbmcplugin.endOfDirectory(addon_handle)
