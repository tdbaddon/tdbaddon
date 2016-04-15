# more info on the M3U file format available here:
# http://n4k3d.com/the-m3u-file-format/

#modified by natko1412 to work with online sources

import sys,os
from webutils import read_url
import xbmc,xbmcaddon

my_addon = xbmcaddon.Addon()
addon_path = my_addon.getAddonInfo('path')
addon_id= my_addon.getAddonInfo('id')
m3u_path = xbmc.translatePath("special://profile/addon_data/"+addon_id)
m3uTemp = os.path.join(m3u_path,'playlist.m3u')
class track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path


# # # song info lines are formatted like:
#EXTINF:419,Alice In Chains - Rotten Apple
# length (seconds)
# Song title
# # # file name - relative or absolute path of file
# ..\Minus The Bear - Planet of Ice\Minus The Bear_Planet of Ice_01_Burying Luck.mp3
def parseM3U(infile):
    text = read_url(infile).lstrip()
    inf = open(m3uTemp,'w')
    inf.write(text)
    inf.close()
    inf = open(m3uTemp,'r')

    # # # all m3u files should start with this line:
        #EXTM3U
    # this is not a valid M3U and we should stop..
    line = inf.readline()
    if not line.startswith('#EXTM3U'):
       return

    # initialize playlist variables before reading file
    playlist=[]
    song=track(None,None,None)

    for line in inf:
        banana='y'
        line=line.strip()
        if line.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            try:
                length,title=line.split('#EXTINF:')[1].split(',',1)
                song=track(length,title,None)
            except: banana = 'x'
        elif (len(line) != 0):
            if banana!='x':
                # pull song path from all other, non-blank lines
                song.path=line
                playlist.append(song)

                # reset the song variable so it doesn't use the same EXTINF more than once
                song=track(None,None,None)
            else:
                banana='x'

    inf.close()

    return playlist

# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    m3ufile=sys.argv[1]
    playlist = parseM3U(m3ufile)
    for track in playlist:
        print (track.title, track.length, track.path)

if __name__ == '__main__':
    main()

