
KODI Popcorn Time
===========

What it is
----------
With KODI Popcorn Time you can search for movies that you can see immediately in KODI.

Download
--------
Check out the [Releases](https://github.com/Diblo/KODI-Popcorn-Time/releases) tab to download the ZIP file.

Supported Platforms
-------------------
* Windows x32 x64
* OS X x32 and x64
* Linux x32 and x64
* Raspberry Pi
* Android 4.0+


How it works
------------
KODI Popcorn Time is actually two parts:
* _KODI Popcorn Time_: the addon written in Python.
* `torrent2http`: a custom torrent client written in Go and leveraging libtorrent-rasterbar, that turns magnet links into HTTP endpoints, using sequential download.

Issues
-----------
Please, file an issue :) - [issues](https://github.com/Diblo/KODI-Popcorn-Time/issues)

Credits
-----------
* KODI Popcorn Time is a rewrite of [xbmctorrent](https://github.com/steeve/xbmctorrent).
* https://github.com/steeve/libtorrent-go
* https://github.com/steeve/torrent2http


FAQ
---
#### I can't code. How can I help?
Spread the word. Talk about it with your friends, show them, make videos, tutorials. Talk about it on social networks, blogs etc...

#### The plugin doesn't work at all, what can I do?
Post your issue on the [issues](https://github.com/Diblo/KODI-Popcorn-Time/issues) page with your kodi.log.

#### Can it stream HD?
Of course! 720p, 1080p and 3D work fine, provided you have enough bandwidth, and there are enough people on the torrent.

#### Does it supports subtitles?
Of course! It will always download the proper subtitle of the film, if there is one. It is also possible to use KODI to search for the subtitle in the absence of a subtitle.

#### Does it downloads the whole file? Do I need the space? Is it ever deleted?
Yes and yes. KODI Popcorn Time will pre-allocate the whole file before download. So if you want to watch a 4GB video, you'll need the 4GB. The file is deleted once you stop watching it.

#### Where is the file located? Can I change it?
Currently the file is download in the same directory as the torrent2http executable (in resources/bin/<OS>/ in the addon directory). Yes of course.

#### Can I keep the file after playback?
Yes, just enable this option in the addon settings.

#### Can I set it to download directly to my NAS and keep it after playback?
Yes of course. Just set the download directly to your NAS location, and make sure you have enabled "Keep files after playback" option.

#### What about seeding?
KODI Popcorn Time will seed the file you're watching until it's finished playing. For instance, if the download of a 2 hours long movie is finished in 10 minutes, you'll continue seeding it until you finish watching the movie. This is by design, to make up for the fact that we are using sequential download.

#### The movie are suddenly paused and then interrupted/stopped. What can I do ?
Probably your network is too slow and you are hitting a timeout used for HTTP on KODI.
You can increase the timeout as documented [here](http://kodi.wiki/view/Advancedsettings.xml#playlisttimeout). Please
note that increasing the timeout won't make your network faster, you just will wait more time before the torrent is interrupted.

Changelog
---------
Check out the [Releases](https://github.com/Diblo/KODI-Popcorn-Time/releases) tab.
