# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Out of this World Documentaries Addon by coldkeys
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.outofthisworld'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UFOTVstudios"
YOUTUBE_CHANNEL_ID_2 = "thirdphaseofmoon"
YOUTUBE_CHANNEL_ID_3 = "ProjectUFOs"
YOUTUBE_CHANNEL_ID_4 = "UCtwAqRfw901jAo9JbX3KEHQ"
YOUTUBE_CHANNEL_ID_5 = "DiscloseTruthTV"
YOUTUBE_CHANNEL_ID_6 = "DisclosureDiscovery"
YOUTUBE_CHANNEL_ID_7 = "davidicke"
YOUTUBE_CHANNEL_ID_8 = "MrTechinnovations"
YOUTUBE_CHANNEL_ID_9 = "UC4Q36FUg_NOHCpxoBv2wQ1g"
YOUTUBE_CHANNEL_ID_10 = "DisclosureNation"
YOUTUBE_CHANNEL_ID_11 = "NonHumanEntities"
YOUTUBE_CHANNEL_ID_12 = "UCqLr8VyFA9qYPuGSLedT2RQ"
YOUTUBE_CHANNEL_ID_13 = "thetruthrevealed777"
YOUTUBE_CHANNEL_ID_14 = "iufoc"
YOUTUBE_CHANNEL_ID_15 = "ParanormalMoviesful"
YOUTUBE_CHANNEL_ID_16 = "DeepakChopraFan1"
YOUTUBE_CHANNEL_ID_17 = "DiscoveryDisclosure"
YOUTUBE_CHANNEL_ID_18 = "UCoawEOkPOrEYKnQs72RnQGw"
YOUTUBE_CHANNEL_ID_19 = "HubbleSiteChannel"
YOUTUBE_CHANNEL_ID_20 = "stevequaylefan"
YOUTUBE_CHANNEL_ID_21 = "TheUFODocumentaries"
YOUTUBE_CHANNEL_ID_22 = "UFOvni2012"
YOUTUBE_CHANNEL_ID_23 = "FindingUFO"
YOUTUBE_CHANNEL_ID_24 = "UCTKuGHAEZsc1Jb1oD2gaW6Q"
YOUTUBE_CHANNEL_ID_25 = "UC_Fb75M4HSsNEwdxZwEXIJQ"
YOUTUBE_CHANNEL_ID_26 = "PLmkjUS2UqPAOQn25fI5g9dCaQ0N-Vz758"
YOUTUBE_CHANNEL_ID_27 = "TheAlexJonesChannel"
YOUTUBE_CHANNEL_ID_28 = "UCSLd3-nGt1fzcYhdh_0Nr0g"
YOUTUBE_CHANNEL_ID_29 = "UCeRIjtKGM0XJugGWDvctxuA"
YOUTUBE_CHANNEL_ID_30 = "AncientAliensRadio"
YOUTUBE_CHANNEL_ID_31 = "PL152bjytsMC4vJUB8Jsnvb8qV-iM5ltp-"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC7SbTJwZMofEBw9goAuyEBk"
YOUTUBE_CHANNEL_ID_33 = "PL152bjytsMC7PfoHBRo-O88IuSJEbwu_Y"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC7nsw4GXHtBHnhEmXhP5pBU"
YOUTUBE_CHANNEL_ID_35 = "PL152bjytsMC4fYj4kF4Xy7EcdX-QouNlC"
YOUTUBE_CHANNEL_ID_36 = "PL152bjytsMC6HJab4OHiCy1sZMnY3nQHJ"
YOUTUBE_CHANNEL_ID_37 = "PL152bjytsMC6KxWlUEqZCAzMZK21TNYL4"
YOUTUBE_CHANNEL_ID_38 = "PL152bjytsMC4QPzz-4aMoenXjziVZVsa3"
YOUTUBE_CHANNEL_ID_39 = "UCGhbRSOWRoYVlPXX1haANKg"
YOUTUBE_CHANNEL_ID_40 = "PLHjrRqyg8ug-ts0AjzUZGpwh9V08uN0i_"
YOUTUBE_CHANNEL_ID_41 = "alienufodisclose"
YOUTUBE_CHANNEL_ID_42 = "PLAA6438176C65375F"
YOUTUBE_CHANNEL_ID_43 = "insearchoftv"
YOUTUBE_CHANNEL_ID_44 = "PLYS2UP0Xbu_bzvxQe3XC5RqL-gVkRMmXt"
YOUTUBE_CHANNEL_ID_45 = "PLlXFGABj3pT6tpo3XrJim2wlNWGjFmAfM"
YOUTUBE_CHANNEL_ID_46 = "AnnunakiRadio"
YOUTUBE_CHANNEL_ID_47 = "PL152bjytsMC70EjJ86WiIvxfb-b4iR7Gn"
YOUTUBE_CHANNEL_ID_48 = "PL152bjytsMC4bORPmQTpsfKTdDSA9Y_pr"
YOUTUBE_CHANNEL_ID_49 = "PL152bjytsMC7tXBplCwvAS-aqL-uw72RF"
YOUTUBE_CHANNEL_ID_50 = "PL152bjytsMC4ApPkn7YIMxZk0sveC8qkl"

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title=" UFOTV® The Disclosure Movie Network ",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-LzxbTMc5jx8/AAAAAAAAAAI/AAAAAAAAAAA/oJYbn_2y4ec/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="thirdphaseofmoon",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-VngAwXZ40Ac/AAAAAAAAAAI/AAAAAAAAAAA/csSGfPEeepg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Project UFOs",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-aANPcaWzCL8/AAAAAAAAAAI/AAAAAAAAAAA/-yp4POfzcYk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The WTF Files™",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-e2m0BS8apsg/AAAAAAAAAAI/AAAAAAAAAAA/v1DHpMIVayE/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title=" Disclose Truth TV ",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-8QbaDb5gcG4/AAAAAAAAAAI/AAAAAAAAAAA/GLM9wpNMMkI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title=" Disclosure Discovery ",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-kvrUGWS4uBU/AAAAAAAAAAI/AAAAAAAAAAA/E4pMp5mZUWA/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="David Icke",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-6eMfz62QtOM/AAAAAAAAAAI/AAAAAAAAAAA/MZlIr7cR7V4/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title=" Ancient Innovations ",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-UTV1LvTy3EA/AAAAAAAAAAI/AAAAAAAAAAA/nJgVyoAoqS8/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="  E.B.E Extraterrestrial Biological Entity ",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-xPwa4vxuwCs/AAAAAAAAAAI/AAAAAAAAAAA/KluzIqc3VQg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Disclosure Nation",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-lfNeciUCA0o/AAAAAAAAAAI/AAAAAAAAAAA/BExVzsACKL0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Non Human Entities",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-WWM0lj8yQl0/AAAAAAAAAAI/AAAAAAAAAAA/pqSvMzo4nvY/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Beyond UFOs 2016",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-L0HHPpel3pY/AAAAAAAAAAI/AAAAAAAAAAA/0Pz6bshbTho/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="The Truth Revealed777",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-5Hgv70lbKH4/AAAAAAAAAAI/AAAAAAAAAAA/vdSzmY69pR4/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Mothership Productions",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-qGSWZ81b36k/AAAAAAAAAAI/AAAAAAAAAAA/soPfYiUHP50/s100-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Paranormal Alien Movies",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/--LRjv3f2MTI/AAAAAAAAAAI/AAAAAAAAAAA/FPk6N7Ky2Ew/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nibiru is Planet X 2015",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-_VhIRKkteeM/AAAAAAAAAAI/AAAAAAAAAAA/aCfehLao6K4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Discovery Disclosure",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-5X-GguFNPto/AAAAAAAAAAI/AAAAAAAAAAA/DuUMGHSu2gM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nova",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-OgfbGny2RiI/AAAAAAAAAAI/AAAAAAAAAAA/7qWMPC7zRMA/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Hubble Space Telescope",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-Y09EJ1SfRDw/AAAAAAAAAAI/AAAAAAAAAAA/Q5cTt7J-bk4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Red Star Kachina",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-WKXVsqHWLwE/AAAAAAAAAAI/AAAAAAAAAAA/jBse_B2BRns/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="The UFO Documentaries",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-xfFNxVaHChM/AAAAAAAAAAI/AAAAAAAAAAA/NBIV0VQZgWA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFOvni2012",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-_7UcjcoUUcc/AAAAAAAAAAI/AAAAAAAAAAA/mPOtxNCw3ek/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Finding UFO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-80fACT-fyZk/AAAAAAAAAAI/AAAAAAAAAAA/6emQESOEoWM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The UFO Agenda 2015",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-HvuNl630RhA/AAAAAAAAAAI/AAAAAAAAAAA/CEbX6j53s-E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO and Aliens Collected",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-1d1CMPx2-aM/AAAAAAAAAAI/AAAAAAAAAAA/nre84MVTm0k/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Files",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://i.ytimg.com/i/3FHcND9fX0E7eleSQP4nFQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Alex Jones Channel",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-DbNegouDvyU/AAAAAAAAAAI/AAAAAAAAAAA/QyDM_-5eUFc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Zachary Crooks",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-NW0ur4r9V7k/AAAAAAAAAAI/AAAAAAAAAAA/vrj4_uJGwgY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Aliens",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-DWiMy45hYI0/AAAAAAAAAAI/AAAAAAAAAAA/YskcZsaSeMA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Radio",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-ss6dyrKvhM8/AAAAAAAAAAI/AAAAAAAAAAA/10DZvKMWqO8/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 3",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 4",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 5",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 6",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 7",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Season 8",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The UFO Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-u25OrL0u2po/AAAAAAAAAAI/AAAAAAAAAAA/dUnqmskNMq8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alien Abduction",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://i.ytimg.com/i/uDRV1Wy1eSEy9NAvVudm3Q/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Aliens Moon Truth Exposed",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-fY_zbuo3qWI/AAAAAAAAAAI/AAAAAAAAAAA/BH9Z3TiwQs8/s100-c-k-no-mo/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-uOOpUsuxHfw/AAAAAAAAAAI/AAAAAAAAAAA/TSblknGKCpg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="(Leonard Nimoy)In Search Of ",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-hsZUv5hqBNY/AAAAAAAAAAI/AAAAAAAAAAA/R0wsx3RntNI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forbidden History Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-e3b6DQRi3Eg/AAAAAAAAAAI/AAAAAAAAAAA/ZHyDt6TAj48/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alien UFO Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-pqSJ6ix3Oww/AAAAAAAAAAI/AAAAAAAAAAA/yGvJyvJBVw4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Annunaki Radio",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-k0YKCFnbkbA/AAAAAAAAAAI/AAAAAAAAAAA/LOg2nkS5B8k/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Hunters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forbidden Knowledge",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Discoveries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Aliens, History and Mystery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail=icon,
        folder=True )
run()
