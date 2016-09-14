import util, search as db
import threading, time, json
import xbmc, xbmcplugin

client_id="HQWCL2WKYEAM4" #realdebrid clientid

def auth():
    xbmc.executebuiltin('ActivateWindow(10138)')
    authData=util.getURL("https://api.real-debrid.com/oauth/v2/device/code?client_id="+client_id+"&new_credentials=yes")
    authThread=threading.Thread(target=verifyThread, args=(authData,))
    
    authThread.start()
    
def verifyThread(authData):
    xbmc.executebuiltin('Dialog.Close(10138)') 
    # convert string to JSON
    authJSON=json.loads(authData)
    
    # create dialog with progress to show information
    authMsg="To authorise your RealDebrid account, use a browser to browse to [B]"+authJSON['verification_url']+"[/B] and enter the verification code [B]"+authJSON['user_code']+"[/B]"
    authDialog=util.progressStart("RealDebrid Authentication", authMsg)
    
    authorised=False
    timer=0
    credJSON=""
    while authorised==False:
        time.sleep(5)
        timer=timer+5
        
        util.progressUpdate(authDialog, timer, authMsg)
        # check if we need to exit
        if util.progressCancelled(authDialog)==True:
            util.progressStop(authDialog)
            break
        if timer==100:
            util.progressStop(authDialog)
            util.alert("RealDebrid aithentication has timed out. Please try again.")
            break
            
        # all good to carry on lets check auth
        util.logError("https://api.real-debrid.com/oauth/v2/device/credentials?client_id="+client_id+"&code="+authJSON['device_code'])
        credentials=util.getURL("https://api.real-debrid.com/oauth/v2/device/credentials?client_id="+client_id+"&code="+authJSON['device_code'])
        try:
            if "error" in credentials:
                #may need to jazz up a bit, but for now its ok
                pass
            else:
                credJSON=json.loads(credentials)
                #store credentials in the database
                db.storeDebrid(credJSON['client_id'], credJSON['client_secret'], authJSON['device_code'])
                authorised=True
        except:
            pass
            
    # check how we exited loop
    if authorised==True:
        util.progrssStop(authDialog)
        util.alert("RealDebrid authenticated")
        