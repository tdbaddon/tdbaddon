# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Special thanks to original authors of the code
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: SkymashiTV
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.skymashitvkids'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UC5Ti4_DVp7LW34PjEwB13Xg" #MorphleTV
YOUTUBE_CHANNEL_ID_2 = "UCAOtE1V7Ots4DjM8JLlrYgg" #PeppaPig
YOUTUBE_CHANNEL_ID_3 = "UCmoqVDc7DZWKxXm7Mi7JhkQ" #Kids Zoo Barney
YOUTUBE_CHANNEL_ID_4 = "UCbt63GNsB5wet6NO3dmhssA" #BusyBeavers
YOUTUBE_CHANNEL_ID_5 = "UCmJ6eP-7_6gqm8moQukzd4A" #BabyFirstTV
YOUTUBE_CHANNEL_ID_6 = "UCbCmjCuTUZos6Inko4u57UQ" #ABCkidTV
YOUTUBE_CHANNEL_ID_7 = "UCMU_RNU6KR49ZE8KmOcpdnA" #HopplaKidz
YOUTUBE_CHANNEL_ID_8 = "UCBnZ16ahKA2DZ_T5W0FPUXg" #ChuChuTV
YOUTUBE_CHANNEL_ID_9 = "UC56cowXhoqRWHeqfSJkIQaA" #BouncePatrolKids
YOUTUBE_CHANNEL_ID_10 = "UCzrLO1XxHbOHfwNM9QUe5fA" #DuckDuckKidsTV
YOUTUBE_CHANNEL_ID_11 = "UCbYUa_MhIQFoS1i0xaNDjTQ" #Organic Learning
YOUTUBE_CHANNEL_ID_12 = "UCmC3QKv-6qDKiBSSYMOtmOw" #Barney by VideoStationBRNY
YOUTUBE_CHANNEL_ID_13 = "UC6zPzUJo8hu-5TzUk8IEC2Q" #MotherGoose Club Playhouse
YOUTUBE_CHANNEL_ID_14 = "UCKAqou7V9FAWXpZd9xtOg3Q" #LittleBabyBum
YOUTUBE_CHANNEL_ID_15 = "UCSWRu9m-HZANpMBBQuEf14g" #Toddler World TV
YOUTUBE_CHANNEL_ID_16 = "PLDt4VQajKv8xKH1YB4kzGMMcnVRwtrk8F" # Kids TV Nursery Rhymes
YOUTUBE_CHANNEL_ID_17 = "UC-exISJxZ6hYgRSJVKshpeA" #Hippo on Wheels
YOUTUBE_CHANNEL_ID_18 = "UCpq1tEJYbykozES2oqwdwlw" #Kids play doh
YOUTUBE_CHANNEL_ID_19 = "UC3KknIJZXRygH2pZ6MDtGbg" #Kids Channel
YOUTUBE_CHANNEL_ID_20 = "UCyXWYhbJomJcTUg98MR5PFA" #Kids Playtime
YOUTUBE_CHANNEL_ID_21 = "UC4iRwR3TPWhz1Gstf0sGZhg" #Kids Baby Club
YOUTUBE_CHANNEL_ID_22 = "UCUbu9zPKclGL4quBu1IUelA" #Finger Family
YOUTUBE_CHANNEL_ID_23 = "UCLsooMJoIpl_7ux2jvdPB-Q" #Super Simple Songs
YOUTUBE_CHANNEL_ID_24 = "UCIX0Z-09kLkf-96-StW3hAw" #Tiny School TV
YOUTUBE_CHANNEL_ID_25 = "UCn--vKxbXBYt_b0lKJ0JEnw" #Shopkins World
YOUTUBE_CHANNEL_ID_26 = "UCc-2P5tCezbxegb7gxp6EXg" #Hobby Kids TV
YOUTUBE_CHANNEL_ID_27 = "UC1sb-8607_3Qc_JLeIssPzA" #Hobby Kids Vids
YOUTUBE_CHANNEL_ID_28 = "UCej8z9NGaA9Hdd8k5hueXKw" #Mega Kids TV
YOUTUBE_CHANNEL_ID_29 = "UCbg1xn1JhBqKpL2M6xi5-0A" #Vids4kids
YOUTUBE_CHANNEL_ID_30 = "UC_1FUFB6TlGeGOyDI4ikkzg" #Best Games 4 Kids
YOUTUBE_CHANNEL_ID_31 = "UC8k_I-jEQWwlMFLbBUau68A" #Raggs TV
YOUTUBE_CHANNEL_ID_32 = "UCyUPl-XOlhCufY6WCGdz_FQ" #Emi TV Lyrics
YOUTUBE_CHANNEL_ID_33 = "UC7Pq3Ko42YpkCB_Q4E981jw" #Kids TV English
YOUTUBE_CHANNEL_ID_34 = "UCfeljpDR__qqp-lLBJdiQkw" #Kids TV Russia
YOUTUBE_CHANNEL_ID_35 = "UC_CE5uL8tsIPsWCt4D8wc8A" #Kids TV Francaise
YOUTUBE_CHANNEL_ID_36 = "UCmMFR_377vB6LLkMFpB8QkA" #Kids TV Deutschland
YOUTUBE_CHANNEL_ID_37 = "UCDz5RUlZ7rstZcJvOeN4IBA" #Kids TV Espanol Latino
YOUTUBE_CHANNEL_ID_38 = "UCv2quJy0NKOIA3MOdtarxig" #Kids TV Italiano
YOUTUBE_CHANNEL_ID_39 = "UCL7jOlb_fr5jNr_YLycovPA" #Kids TV Portugues
YOUTUBE_CHANNEL_ID_40 = "UCZbTuDplLcBb4bTHa_-5_UA" #Kids TV India
YOUTUBE_CHANNEL_ID_41 = "UC9ya8rlHpqsS3yIAqs55PeA" #Kids TV Arabic
YOUTUBE_CHANNEL_ID_42 = "UCeVTeLnKQ17H1hoT3kVd1iQ" #Kids TV Vietnam
YOUTUBE_CHANNEL_ID_43 = "UC1JZiF288_cx-TyT8ll2XzQ" #Kids TV Thailand
YOUTUBE_CHANNEL_ID_44 = "UCMlwYHjsYtGLSe4lKlZv2Ww" #Kids TV China
YOUTUBE_CHANNEL_ID_45 = "UCTc15uvrhUmW044MfJG4HHw" #Kids TV Korea
YOUTUBE_CHANNEL_ID_46 = "UCZloN3sRZuT6RVz8ktLdd2Q" #Kids TV Japanese

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
        title="Morphle TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-VBqDCWsdb9Q/AAAAAAAAAAI/AAAAAAAAAAA/o57M8TV6Kjo/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Peppa Pig",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-oSAbz46-1qw/AAAAAAAAAAI/AAAAAAAAAAA/UzFF1NAQRSo/s500-c-k-no/photo.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Barney by Kids Zoo",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-HBHiPGhi2yI/AAAAAAAAAAI/AAAAAAAAAAA/FR-a8o-7B5I/s500-c-k-no/photo.jpg",
        folder=True )
				
    plugintools.add_item( 
        #action="", 
        title="Busy Beavers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-gB_SFlcGzDc/AAAAAAAAAAI/AAAAAAAAAAA/KwtbUnJTQTQ/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BabyFirst TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-jy2mm7NMW5o/AAAAAAAAAAI/AAAAAAAAAAA/SQnxxQNjgAY/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ABCkidTV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51V8MrZu5TL._SY300_.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="HooplaKidz Shows",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-R4Yt7fFk6A4/AAAAAAAAAAI/AAAAAAAAAAA/2tqwFduNGjw/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ChuChu TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-QHPC9emY_8c/AAAAAAAAAAI/AAAAAAAAAAA/03fPGkHcBbk/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bounce Patrol Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-P3GrO-qDn8c/AAAAAAAAAAI/AAAAAAAAAAA/WGyon47JL38/s500-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="DuckDuck KidsTV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-AVz1gWBdaIA/AAAAAAAAAAI/AAAAAAAAAAA/rhC1aZhd2Ns/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Organic Learning",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-OX_6KLsHGQY/AAAAAAAAAAI/AAAAAAAAAAA/TO2Q16jvlpc/s500-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Barney by VideoStationBRNY",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-EJjQW__M0E0/AAAAAAAAAAI/AAAAAAAAAAA/4wROo1SSKnU/s500-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Mothergoose Club Playhouse",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-7EZ4R90FGWk/AAAAAAAAAAI/AAAAAAAAAAA/EGvKs_ccXVc/s500-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="LittleBabyBum",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-KLfbkE3zovQ/AAAAAAAAAAI/AAAAAAAAAAA/gMZ_6qxvEXw/s500-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Toddler World TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-qMAZNNmYbo0/AAAAAAAAAAI/AAAAAAAAAAA/UNMnnj2SuAI/s500-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Kids TV Nursery Rhymes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-Vas4UzOl0KE/AAAAAAAAAAI/AAAAAAAAAAA/_fWZBwq0qnA/s500-c-k-no-mo/photo.jpg",
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="Hippo on Wheels",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-HaiJISRArdc/AAAAAAAAAAI/AAAAAAAAAAA/m77-kxw9FKI/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Play Doh",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-lem-4FgoESY/AAAAAAAAAAI/AAAAAAAAAAA/jkJYoBcC4XM/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-08bC4ULIwPQ/AAAAAAAAAAI/AAAAAAAAAAA/71B5YHtofOw/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Play Time",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-E7hAbAy0J7k/AAAAAAAAAAI/AAAAAAAAAAA/8x2tzmPluTI/s500-c-k-no/photo.jpg",
        folder=True )
 
    plugintools.add_item( 
        #action="", 
        title="Kids Baby Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-hzuxfRs1E4Q/AAAAAAAAAAI/AAAAAAAAAAA/jZhq1P1Ed_c/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )
 
    plugintools.add_item( 
        #action="", 
        title="Finger Family",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-1d8pxVPaYuw/AAAAAAAAAAI/AAAAAAAAAAA/XIitiKcyy4s/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Super Simple Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-nHzSx4QKfsY/AAAAAAAAAAI/AAAAAAAAAAA/o_0k7TejOiI/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="TinySchool TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-GKF9gp5kPTA/AAAAAAAAAAI/AAAAAAAAAAA/RTTvkaJ4UyE/s500-c-k-no/photo.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="ShopkinsWorld",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-jPfU68yA4yo/AAAAAAAAAAI/AAAAAAAAAAA/BKo01shIosI/s500-c-k-no/photo.jpg",
        folder=True )
 		
    plugintools.add_item( 
        #action="", 
        title="Hobby Kids TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-N5ri7XcyLH0/AAAAAAAAAAI/AAAAAAAAAAA/R4KMAYzcC88/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )
 		
    plugintools.add_item( 
        #action="", 
        title="Hobby Kids Vids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-Li0dUsouuVs/AAAAAAAAAAI/AAAAAAAAAAA/h1lsJwA9Fh8/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Mega Kids TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-O9vmJF_kcrU/AAAAAAAAAAI/AAAAAAAAAAA/Ksnfb2EbSSQ/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Vids4Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-UpkOWyWbtzM/AAAAAAAAAAI/AAAAAAAAAAA/p4YawW4dIL8/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Best Games 4 Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-5pUwQKkReE8/AAAAAAAAAAI/AAAAAAAAAAA/gUKqWhH7yNU/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Raggs TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-ooolvkNZNCQ/AAAAAAAAAAI/AAAAAAAAAAA/Z_RucnORKMw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Emi TV Lyrics",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-lFo05B3R4eU/AAAAAAAAAAI/AAAAAAAAAAA/3jIIb2Cx7Fg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV English",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-Vas4UzOl0KE/AAAAAAAAAAI/AAAAAAAAAAA/_fWZBwq0qnA/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Russia",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-DZioWCcwZs4/AAAAAAAAAAI/AAAAAAAAAAA/O56d-t4-zuk/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Francaise",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-w3R3MJLL72k/AAAAAAAAAAI/AAAAAAAAAAA/Zole3vG6Zf4/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Deutschland",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-EL1XysTmSDg/AAAAAAAAAAI/AAAAAAAAAAA/ciGM9qpGcFg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Espanol Latino",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-xFRltqFElVI/AAAAAAAAAAI/AAAAAAAAAAA/spG9gUMZzH0/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Italiano",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-OrrVKKirLc4/AAAAAAAAAAI/AAAAAAAAAAA/4GAz9dJSUMg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Português",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-1n4XQxhAbow/AAAAAAAAAAI/AAAAAAAAAAA/nwg-xuNUgKE/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV India",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-XnmU0oEj2Vs/AAAAAAAAAAI/AAAAAAAAAAA/dEKIniE1N2A/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Arabic",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-eFyWF_fpJu0/AAAAAAAAAAI/AAAAAAAAAAA/-WCHnIVT6TI/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Vietnam",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-d0knAjNyjPE/AAAAAAAAAAI/AAAAAAAAAAA/jg1rh8tNwBw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Thailand",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-PRTNTXczIdw/AAAAAAAAAAI/AAAAAAAAAAA/dh17MejobCw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV China",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-KaEUrOjPkbA/AAAAAAAAAAI/AAAAAAAAAAA/qmjvxoVj-B4/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Korea",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-ikCWBrPWCFQ/AAAAAAAAAAI/AAAAAAAAAAA/1Qvrj5URemw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
 		
    plugintools.add_item( 
        #action="", 
        title="Kids TV Japanese",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-QCzGrzmMXeU/AAAAAAAAAAI/AAAAAAAAAAA/qjm8MgH3AJc/s500-c-k-no-rj-c0xffffff/photo.jpg",
        folder=True )       
				
run()		
